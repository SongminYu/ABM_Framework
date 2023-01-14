var data, model, t0, t1;
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
    run() {
        var spot, sum;
        spot = this.grid.get_spot(5, 5);
        console.log("spot", spot);
        console.log(this.grid.get_spot_neighborhood(spot));
        sum = 0;
        this.agents.add();
        for (var agent of this.agents) {
            sum += agent.test();
        }
        console.log(sum);
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
data = {"model_cls": "MyModel", "scenario": {"cls": "MyScenario", "data": {"agent_num": 10000}}, "components": [{"type": "environment", "cls": "MyEnv"}, {"prop_name": "agents", "type": "agent_list", "cls": "AgentList", "agent_cls": "MyAgent", "agents": [{"a": 123, "id": 0}]}, {"prop_name": "grid", "type": "grid", "cls": "Grid", "spot_cls": "Spot", "width": 10, "height": 10, "spots": []}]};
for (var i = 0, _pj_a = 10000; (i < _pj_a); i += 1) {
    data["components"][1]["agents"].push({"a": 123, "id": (i + 1), "x": random.randint(0, 9), "y": random.randint(0, 9), "category": 1});
}
for (var x = 0, _pj_a = 10; (x < _pj_a); x += 1) {
    for (var y = 0, _pj_b = 10; (y < _pj_b); y += 1) {
        data["components"][2]["spots"].push({"x": x, "y": y, "id": (i + 1)});
    }
}
model = unmarshallModel(data);
t0 = time.time();
model.run();
t1 = time.time();
console.log("took time", (t1 - t0));

//# sourceMappingURL=run.js.map
