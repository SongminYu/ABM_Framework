# -*- coding:utf-8 -*-
# @Time: 2021/11/12 18:51
# @Author: Zhanyi Hou
# @Email: 1295752786@qq.com
# @File: run_studio.py
import random

# import numba
# import numpy as np
# from numba import typed

from Melodie import Grid
from Melodie.visualizer import GridVisualizer


class GameOfLifeVisualizer(GridVisualizer):
    def setup(self):
        self.add_agent_series('sheep', 'scatter', '#bbff00', )
        self.add_agent_series('agents', 'scatter', '#bb0000', )

    def parse(self, grid):
        self.parse_grid_series(grid)

    def other_series_data(self):
        pass
