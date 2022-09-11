from typing import TYPE_CHECKING

from Melodie import Model
from tutorial.CovidContagion.source import data_info
from .agent import CovidAgent
from .data_collector import CovidDataCollector
from .environment import CovidEnvironment
from .grid import CovidGrid, CovidSpot
from .scenario import CovidScenario

if TYPE_CHECKING:
    from Melodie import AgentList


class CovidModel(Model):
    scenario: CovidScenario

    def create(self):
        self.agents: "AgentList[CovidAgent]" = self.create_agent_list(CovidAgent)
        self.environment = self.create_environment(CovidEnvironment)
        self.data_collector = self.create_data_collector(CovidDataCollector)
        self.grid = self.create_grid(CovidGrid, CovidSpot)

    def setup(self):
        self.agents.setup_agents(agents_num=self.scenario.agent_num,
                                 params_df=self.scenario.get_dataframe(data_info.agent_params),)
        self.grid.setup_params(width=self.scenario.grid_x_size,
                               height=self.scenario.grid_y_size)
        self.grid.setup_agent_locations(self.agents)

    def run(self):
        for period in self.iterator(self.scenario.period_num):
            self.environment.agents_move(self.agents)
            self.environment.agents_infection(self.agents)
            self.environment.agents_health_state_transition(self.agents)
            self.environment.calc_population_infection_state(self.agents)
            self.data_collector.collect(period)
        self.data_collector.save()
