from Melodie import Model, Agent, Environment
import random
import time
class MyModel(Model):
    def setup(self):
        self.a = 123
        # self.agents =
        self.agents = self.create_agent_list(MyAgent)
        for i in range(10000):
            self.agents.add(params={'a': 123})

    def run(self):
        sum = 0
        for agent in self.agents:
            sum += agent.test()
        print(sum)


class MyAgent(Agent):
    def setup(self):
        self.a = 123123123

    def test(self):
        s = 0
        for i in range(1000):
            if random.normalvariate(0, 0) < 0.5:
                s += 1
            else:
                s -= 1
        return s


class MyEnv(Environment):
    def setup(self):
        self.tmp = 123


model = MyModel(config=None, scenario=None)
model.setup()
print(model)

t0 = time.time()
model.run()
t1 = time.time()
print('took time', t1-t0)
