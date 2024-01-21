# -*- coding:utf-8 -*-

import os

from tests.procedures.simulator_demo import Simulator4Test, DCTestModel, TestScenario
from MelodieInfra import Config

cfg_for_temp2 = Config(
    "temp_db_for_parallel_simulation",
    os.path.dirname(__file__),
    input_folder=os.path.join(os.path.dirname(
        __file__), "resources", "excels"),
    output_folder=os.path.join(os.path.dirname(
        __file__), "resources", "output", "parallel_simulation"),
)
AGENT_NUM_1 = 10
AGENT_NUM_2 = 20


def test_sim_parallel():
    sim = Simulator4Test(
        config=cfg_for_temp2,
        model_cls=DCTestModel,
        scenario_cls=TestScenario,
    )
    sim.new_parallel(2)