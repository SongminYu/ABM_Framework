var SIZE, data, model, t0, t1;
class MyScenario extends Scenario {
    setup() {
        this.agent_num = 10000;
    }
}
class MyModel extends Model {
    setup() {
        this.a = 123;
        this.grid = new Grid();
        this.agents = null;
    }
    count(spots) {
        var alive_count;
        alive_count = 0;
        for (var spot of spots) {
            if (spot.alive) {
                alive_count += 1;
            }
        }
        if ((alive_count < 3)) {
            spot.alive_next = true;
        } else {
            if ((alive_count === 3)) {
                spot.alive_next = spot.alive;
            } else {
                spot.alive_next = false;
            }
        }
    }
    step() {
        var neighborhood, spot;
        for (var i = 0, _pj_a = this.grid.width; (i < _pj_a); i += 1) {
            for (var j = 0, _pj_b = this.grid.height; (j < _pj_b); j += 1) {
                spot = this.grid.get_spot(i, j);
                neighborhood = this.grid.get_spot_neighborhood(spot);
                this.count(neighborhood);
            }
        }
        for (var i = 0, _pj_a = this.grid.width; (i < _pj_a); i += 1) {
            for (var j = 0, _pj_b = this.grid.height; (j < _pj_b); j += 1) {
                spot = this.grid.get_spot(i, j);
                spot.alive = spot.alive_next;
            }
        }
    }
    run() {
        this.step();
    }
}
class MyAgent extends GridAgent {
    setup() {
        this.a = 123123123;
    }
    set_category() {
        this.category = 1;
    }
    test() {
        var s;
        s = 0;
        for (var i = 0, _pj_a = 1000; (i < _pj_a); i += 1) {
            if ((random.normalvariate() < 0.5)) {
                s += 1;
            } else {
                s -= 1;
            }
        }
        return s;
    }
}
class MyEnv extends Environment {
    setup() {
        this.tmp = 123;
    }
}
SIZE = 300;
data = {"model_cls": "MyModel", "scenario": {"cls": "MyScenario", "data": {"agent_num": 10000}}, "components": [{"type": "environment", "cls": "MyEnv"}, {"prop_name": "agents", "type": "agent_list", "cls": "AgentList", "agent_cls": "MyAgent", "agents": [{"a": 123, "id": 0}]}, {"prop_name": "grid", "type": "grid", "cls": "Grid", "spot_cls": "Spot", "width": SIZE, "height": SIZE, "spots": []}]};
for (var i = 0, _pj_a = 10000; (i < _pj_a); i += 1) {
    data["components"][1]["agents"].push({"a": 123, "id": (i + 1), "x": random.randint(0, 9), "y": random.randint(0, 9), "category": 1});
}
for (var x = 0, _pj_a = SIZE; (x < _pj_a); x += 1) {
    for (var y = 0, _pj_b = SIZE; (y < _pj_b); y += 1) {
        data["components"][2]["spots"].push({"x": x, "y": y, "id": (i + 1), "alive": false, "alive_nexttick": false});
    }
}
model = unmarshallModel(data);
t0 = time.time();
model.run();
t1 = time.time();
console.log("took time", (t1 - t0));

//# sourceMappingURL=run.js.map
