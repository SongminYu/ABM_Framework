import time
from Melodie import Model, Spot

def iterable(arg):
    return arg

class MySpot(Spot):
    def setup(self):
        self.alive = True
        self.alive_next = False

class MyModel(Model):
    def setup(self):
        self.a = 123
        self.grid = self.create_grid(spot_cls=MySpot)
        self.grid.setup_params(300,300)
        self.agents = None

    def count(self, spots):
        alive_count = 0
        for spot in iterable(spots):
            if spot.alive:
                alive_count+=1
        if alive_count<3:
            spot.alive_next = True
        elif alive_count==3:
            spot.alive_next = spot.alive
        else:
            spot.alive_next = False

    def step(self):
        for i in range(self.grid.width()):
            for j in range(self.grid.height()):
                spot = self.grid.get_spot(i, j)
                neighborhood = self.grid.get_spot_neighborhood(spot)
                self.count(neighborhood)
        for i in range(self.grid.width()):
            for j in range(self.grid.height()):
                spot = self.grid.get_spot(i, j)
                spot.alive = spot.alive_next
                # print()

    def run(self):
        self.step()
        # for i in range(100):
        #     self.step()
        # sum = 0
        # self.agents.add()
        # for agent in iterable(self.agents):
        #     sum += agent.test()
        # print(sum)

model = MyModel(None, None, )
model.setup()
t0 = time.time()
model.run()
t1 = time.time()
print('took time', t1-t0)
