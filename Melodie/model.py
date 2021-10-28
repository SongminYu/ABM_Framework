import sys
from typing import ClassVar, Optional

from . import DB
from .agent import Agent
from .agent_manager import AgentManager
from .config import Config
from .data_collector import DataCollector
from .environment import Environment
from .scenario_manager import Scenario
from .table_generator import TableGenerator
from .db import create_db_conn


class Model:
    def __init__(self,
                 config: 'Config' = None,
                 scenario: 'Scenario' = None,
                 agent_class: ClassVar[Agent] = None,
                 environment_class: ClassVar[Environment] = None,
                 data_collector_class: ClassVar[DataCollector] = None,
                 table_generator_class: ClassVar[TableGenerator] = None,
                 run_id_in_scenario: int = 0
                 ):
        self.scenario = scenario
        self.project_name = config.project_name
        self.config = config
        self.agent_class = agent_class
        self.environment_class = environment_class
        self.agent_manager: AgentManager = None
        self.data_collector_class = data_collector_class
        self.table_generator_class = table_generator_class
        self.data_collector: Optional[DataCollector] = None
        self.table_generator: Optional[TableGenerator] = None
        self.run_id_in_scenario = run_id_in_scenario

        self.network = None
        self.setup()
        # assert self.environment_class is not None
        # self._setup()

    def setup(self):
        pass

    def current_scenario(self) -> 'Scenario':
        assert self.scenario != None
        return self.scenario

    def create_db_conn(self) -> 'DB':
        return create_db_conn(self.config)

    def setup_agent_manager(self):
        """
        Setup the agent manager. The steps included:
        1. Create the self.agent_manager;
        2. Set parameters of all agents generated in current scenario;

        :return:
        """
        scenario = self.scenario
        self.agent_manager = AgentManager(self.agent_class, scenario.agent_num, self)

        # Read agent parameters from data
        # db_conn = create_db_conn(self.config)
        agent_para_data_frame = scenario.get_agent_params_table()  # db_conn.read_dataframe(db_conn.AGENT_PARAM_TABLE)
        assert agent_para_data_frame is not None
        # Create agent manager

        reserved_param_names = ['id']
        param_names = reserved_param_names + [param for param in agent_para_data_frame.columns if param not in
                                              {'scenario_id', 'id'}]

        # Assign parameters to properties for each agent.
        for i, agent in enumerate(self.agent_manager.agents):
            params = {}
            for agent_param_name in param_names:
                # .item() was applied to convert pandas/numpy data into python-builtin types.
                params[agent_param_name] = agent_para_data_frame.loc[i, agent_param_name].item()

            agent.set_params(params)

        return self.agent_manager

    def setup_environment(self):
        self.environment = self.environment_class()
        self.environment.model = self
        self.environment.setup()

    def setup_data_collector(self):
        data_collector_class = self.data_collector_class
        if callable(data_collector_class) and issubclass(data_collector_class, DataCollector):
            data_collector = data_collector_class(self)
            data_collector.setup()
        elif data_collector_class is None:
            data_collector = None
        else:
            raise TypeError(data_collector_class)

        self.data_collector = data_collector

    # def setup_table_generator(self, table_generator_class):
    #     """
    #     TODO table generator should be set up before model creates.
    #     :param table_generator_class:
    #     :return:
    #     """
    #     # raise DeprecationWarning('table generator should be set up before model creates.')
    #     if table_generator_class is not None:
    #         self.table_generator: TableGenerator = table_generator_class(self.scenario)
    #         self.table_generator.setup()
    #         # self.table_generator.run()
    #     # else:

    def get_agent_param(self):
        if self.table_generator is not None:
            self.table_generator.run()
        else:
            table = ''

    def _setup(self):
        self.setup_data_collector()
        self.get_agent_param()
        self.setup_environment()
        self.setup_agent_manager()

    def step(self):
        pass

    def run(self):
        scenario = self.scenario
        for i in range(scenario.periods):
            self.step()
            if self.data_collector is not None:
                self.data_collector.collect(i)
        if self.data_collector is not None:
            self.data_collector.save()
