import numpy as np
import sqlalchemy

from Melodie import DataFrameLoader
from .scenario import CovidScenario

class CovidDataFrameLoader(DataFrameLoader):

    def register_scenario_dataframe(self):
        scenarios_dict = {
            "periods": sqlalchemy.Integer(),
            "agent_num": sqlalchemy.Integer(),
            "grid_x_size": sqlalchemy.Integer(),
            "grid_y_size": sqlalchemy.Integer(),
            "initial_infected_percentage": sqlalchemy.Float(),
            "infection_probability": sqlalchemy.Integer(),
            "number_of_path": sqlalchemy.Integer(),
            "number_of_generation": sqlalchemy.Integer(),
            "population": sqlalchemy.Integer(),
            "mutation_prob": sqlalchemy.Float(),
            "param_code_length": sqlalchemy.Integer(),
            "infection_probability_min": sqlalchemy.Float(),
            "infection_probability_max": sqlalchemy.Float()
        }
        self.load_dataframe('simulator_scenarios', 'simulator_scenarios.xlsx', scenarios_dict)
        self.load_dataframe('calibrator_scenarios', 'calibrator_scenarios.xlsx', scenarios_dict)
        self.load_dataframe('calibrator_params_scenarios', 'calibrator_params_scenarios.xlsx', scenarios_dict)

    def register_generated_dataframes(self):

        def init_condition(initial_infected_percentage: float):
            condition = 0
            rand = np.random.uniform(0, 1)
            if rand <= initial_infected_percentage:
                condition = 1
            else:
                pass
            return condition

        with self.new_table_generator('agent_params', lambda scenario: scenario.agent_num) as g:
            def generator_func(scenario: 'CovidScenario'):
                return {'id': g.increment(),
                        'x_pos': np.random.randint(0, scenario.grid_x_size),
                        'y_pos': np.random.randint(0, scenario.grid_y_size),
                        'condition': init_condition(scenario.initial_infected_percentage)}

            g.set_row_generator(generator_func)
            g.set_column_data_types({'id': sqlalchemy.Integer(),
                                     'x_pos': sqlalchemy.Integer(),
                                     'y_pos': sqlalchemy.Integer(),
                                     'condition': sqlalchemy.Integer()})