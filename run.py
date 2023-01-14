
class MyScenario(Scenario):
    def setup(self):
        self.agent_num = 10000


class MyModel(Model):
    def setup(self):
        self.a = 123
        self.grid = Grid()
        self.agents = None

    def run(self):
        spot = self.grid.get_spot(5, 5)
        print('spot', spot)
        # print(self.grid._get_neighbor_positions(5,5))
        print(self.grid.get_spot_neighborhood(spot))
        sum = 0
        self.agents.add()
        for agent in iterable(self.agents):
            sum += agent.test()
        print(sum)


class MyAgent(GridAgent):
    def setup(self):
        self.a = 123123123

    def set_category(self):
        self.category = 1

    def test(self):
        s = 0
        for i in range(1000):
            if random.normalvariate() < 0.5:
                s += 1
            else:
                s -= 1
        return s


class MyEnv(Environment):
    def setup(self):
        self.tmp = 123


data = {
    "model_cls": "MyModel",
    "scenario": {
        "cls": "MyScenario",
        "data": {"agent_num": 10000}
    },
    "components": [
        {'type': "environment",
         "cls": "MyEnv"},
        {"prop_name": "agents",
         'type': "agent_list",
         "cls": "AgentList",
         "agent_cls": "MyAgent",
         "agents": [
             {"a": 123, "id": 0}
         ]
         },
        {
            "prop_name": "grid",
            'type': 'grid',
            "cls": "Grid",
            'spot_cls': 'Spot',
            "width": 10,
            "height": 10,
            "spots": []
        }
    ]
}
for i in range(10000):
    data['components'][1]['agents'].push(
        {"a": 123, "id": i+1, "x": random.randint(0, 9), "y": random.randint(0, 9), 'category': 1})

for x in range(10):
    for y in range(10):
        data['components'][2]['spots'].push({"x": x, "y": y, "id": i+1})
model = unmarshallModel(data)

t0 = time.time()
model.run()
t1 = time.time()
print('took time', t1-t0)
