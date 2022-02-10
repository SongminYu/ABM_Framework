import random
import numpy as np
from typing import Type

from Melodie import Agent, Grid


class PandoraAgent(Agent):

    def setup(self):
        self.x_pos = 0
        self.y_pos = 0
        self.condition = 0

    def move(self, grid: 'Grid'):
        self.x_pos, self.y_pos = \
            grid.coords_wrap(self.x_pos + random.randint(-1, 1),
                             self.y_pos + random.randint(-1, 1))
        grid.move_agent(self.id, 'agent_list', self.x_pos, self.y_pos)