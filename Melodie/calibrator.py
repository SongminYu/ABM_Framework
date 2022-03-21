import abc
import time
from typing import Type, Callable, List, Optional, ClassVar, Iterator, Union, Tuple, Dict
import copy
import numpy as np
import pandas as pd
import logging
from Melodie import Model, Scenario, Config, create_db_conn, GACalibratorParams, DataFrameLoader
from Melodie.algorithms import GeneticAlgorithmCalibrator, SearchingAlgorithm
from Melodie.basic import MelodieExceptions
from .simulator import BaseModellingManager

logger = logging.getLogger(__name__)


class Calibrator(BaseModellingManager):
    """
    Calibrator
    """

    def __init__(self, config: 'Config',
                 scenario_cls: 'Optional[ClassVar[Scenario]]',
                 model_cls: 'Optional[ClassVar[Model]]',
                 df_loader_cls: ClassVar['DataFrameLoader'], ):
        super().__init__(
            config=config,
            scenario_cls=scenario_cls,
            model_cls=model_cls,
            df_loader_cls=df_loader_cls)
        # self.config = config
        self.training_strategy: 'Optional[Type[SearchingAlgorithm]]' = None
        self.container_name: str = ''

        self.properties: List[str] = []
        self.watched_env_properties: List[str] = []
        self.algorithm: Optional[Type[SearchingAlgorithm]] = None
        self.algorithm_cls: Union[ClassVar[SearchingAlgorithm]] = None
        self.algorithm_instance: Iterator[List[float]] = {}

        self.model: Optional[Model] = None

        self.current_algorithm_meta = {
            "calibrator_scenario_id": 1,
            "path_id": 0,
            "generation_id": 0
        }
        self.df_loader: Optional['DataFrameLoader'] = None
        self.df_loader_cls = df_loader_cls

    def setup(self):
        pass

    def generate_scenarios(self) -> List['Scenario']:
        """
        Generate scenario objects by the parameter from static tables or scenarios_dataframe.
        :return:
        """
        return self.df_loader.generate_scenarios_from_dataframe('calibrator_scenarios')

    def calibrate(self):
        self.setup()
        self.pre_run()
        calibrator_scenarios_table = self.get_registered_dataframe('calibrator_params_scenarios')
        assert isinstance(calibrator_scenarios_table, pd.DataFrame), "No learning scenarios table specified!"
        assert self.algorithm_cls is not None
        scenario_cls = None
        if self.algorithm_cls == GeneticAlgorithmCalibrator:
            scenario_cls = GACalibratorParams
        else:
            raise NotImplementedError
        for scenario in self.scenarios:
            self.current_algorithm_meta['calibrator_scenario_id'] = scenario.id
            calibration_scenarios = calibrator_scenarios_table.to_dict(orient="records")
            for calibrator_scenario in calibration_scenarios:
                calibrator_scenario = scenario_cls.from_dataframe_record(calibrator_scenario)
                self.current_algorithm_meta['calibrator_params_scenario_id'] = calibrator_scenario.id
                for trainer_path_id in range(calibrator_scenario.number_of_path):
                    self.current_algorithm_meta['path_id'] = trainer_path_id

                    self.run_once(scenario, calibrator_scenario)

    def run_once(self, scenario, calibration_scenario: GACalibratorParams):

        scenario.manager = self
        self.model = self.model_cls(self.config, scenario)
        self.model.setup()
        iterations = 0
        if self.algorithm_cls == GeneticAlgorithmCalibrator:
            self.algorithm = GeneticAlgorithmCalibrator(calibration_scenario.calibration_generation,
                                                        calibration_scenario.strategy_population,
                                                        calibration_scenario.mutation_prob,
                                                        calibration_scenario.strategy_param_code_length)
            iterations = calibration_scenario.calibration_generation
        else:
            raise NotImplementedError
        self.algorithm.parameter_names = self.properties
        self.algorithm.parameters_range = [(parameter.min, parameter.max) for parameter in
                                           calibration_scenario.parameters]
        self.algorithm.parameters_num = len(self.algorithm.parameters_range)

        self.algorithm_instance = self.algorithm.optimize(self.fitness, scenario)

        for i in range(iterations):
            self.current_algorithm_meta['generation_id'] = i
            logger.info(f"===================Calibrating step {i + 1}=====================")
            strategy_population, params, fitness, meta = self.algorithm_instance.__next__()

            calibrator_result_cov = copy.deepcopy(meta['env_params_cov'])
            calibrator_result_cov.update(meta['env_params_mean'])
            calibrator_result_cov['distance_mean'] = meta['distance_mean']
            calibrator_result_cov['distance_cov'] = meta['distance_cov']

            calibrator_result_cov.update(self.current_algorithm_meta)
            create_db_conn(self.config).write_dataframe('calibrator_result_cov',
                                                        pd.DataFrame([calibrator_result_cov]))

    def add_environment_calibrating_property(self, prop: str):
        """
        Add a property to be calibrated.
        It should be a property of environment.
        :param prop:
        :return:
        """
        assert prop not in self.properties
        self.properties.append(prop)

    def add_environment_result_property(self, prop: str):
        """

        :param prop:
        :return:
        """
        assert prop not in self.watched_env_properties
        self.watched_env_properties.append(prop)

    def fitness(self, params, scenario: Union[Type[Scenario], Scenario], **kwargs) -> Tuple[float, float]:
        for i, prop_name in enumerate(self.properties):
            assert scenario.__getattribute__(prop_name) is not None
            scenario.__setattr__(prop_name, params[i])
        scenario_properties_dict = {prop_name: scenario.__dict__[prop_name] for prop_name in self.properties}
        self.model = self.model_cls(self.config, scenario)
        self.model.setup()
        meta = kwargs['meta']
        environment_record_dict = {}
        environment_record_dict.update(self.current_algorithm_meta)
        t0 = time.time()
        self.model.run()
        t1 = time.time()
        logger.info(f'Model run, taking {t1 - t0}s')
        env = self.model.environment
        distance = self.distance(env)
        fitness = self.convert_distance_to_fitness(distance)
        MelodieExceptions.Assertions.NotNone('fitness', fitness)
        environment_record_dict.update(scenario_properties_dict)
        environment_record_dict['chromosome_id'] = meta['chromosome_id']
        environment_record_dict.update({
            prop: env.__dict__[prop] for prop in self.watched_env_properties
        })
        environment_record_dict['distance'] = distance

        create_db_conn(self.config). \
            write_dataframe('calibrator_result',
                            pd.DataFrame([environment_record_dict]),
                            if_exists="append")
        return fitness, distance

    @abc.abstractmethod
    def distance(self, environment) -> float:
        return -1.0

    def convert_distance_to_fitness(self, distance: float):
        return - distance
