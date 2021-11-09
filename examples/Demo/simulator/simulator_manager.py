
from typing import List, Optional
import pandas as pd

from Melodie import NewScenario, Simulator




# 似乎无论是simulator还是calibrator，都只写相应的manager就可以了，scenario不用出现在任何文件里？
class DemoScenario(NewScenario):

    # 一个完整的scenario是初始化并运行模型需要的所有外生参数的集合，包括两部分：
    # 1. scenario_series = scenario_id +
    #    1.1 env_params: number_of_run, number_of_period, number_of_agent, rich_win_prob等
    #    1.2 [optional] agent_params: parameters that are used to generate agent_params_dataframe

    # 以上所有一开始都存在excel_source文件夹里，之后导入sqlite数据库。
    # 静态文件由Scenario的统一的共享方法来访问。


    pass





class DemoSimulatorManager(Simulator):

    def register_static_dataframes(self):
        # 这个函数必须写：注册每一张excel_source文件夹里的表，包括：变量名、excel表名、列名、列数据类型。
        # 1. 注册Scenarios.xlsx
        # 2. 注册其他的static_table
        #  - assert以上写对了 --> 虽然麻烦，但可以帮助用户少犯错。
        # 把这些表导入sqlite数据库。
        pass



    def generate_scenarios(self) -> List[DemoScenario]:
        # 对每个Scenario的实例，初始化三部分：
        # 1. attributes --> Scenarios.xlsx里的一行
        # 2. agent_params_table --> 用于model.setup_agent_list
        # 3. Scenarios以外的static_table
        # 之后，在agent和env里面，可以直接用scenario.name访问这些attributes和表。
        pass

