# 设置收集的数据类型能做到吗 --> 存到数据库之前
# 用户可以选择只记录env的参数；对于env和agent的参数，也可以只记录个别period（比如首尾两个）的结果
from Melodie import DataCollector


class DemoDataCollector(DataCollector):
    def setup(self):
        pass