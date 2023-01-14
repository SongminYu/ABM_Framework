import {List, Optional, Type, Union} from './types';
import {AgentList} from './agent_list';
import {Agent} from './agent';
import {Environment} from './environment';
class ModelRunRoutine {
    /*
    A simple iterator for model run.


    When calling ``Model.iterator()`` method, a ModelRunRoutine object will be created, yielding an ``int``  value
    reprensenting the current number of step, ranging ``[0, max_step - 1]``.


    */
    constructor(max_step, model) {
        this._current_step = (- 1);
        this._max_step = max_step;
        this.model = model;
    }
    __iter__() {
        return this;
    }
    __next__() {
        if ((this._current_step >= (this._max_step - 1))) {
            throw StopIteration;
        }
        this.model._visualizer_step(this._current_step);
        this._current_step += 1;
        return this._current_step;
    }
    __del__() {
        /*
        Remove circular reference before deletion

        :return:
        */
        this.model = null;
    }
}
class Model {
    constructor(config, scenario, run_id_in_scenario = 0, visualizer = null) {
        this.scenario = scenario;
        this.config = config;
        this.environment = null;
        this.data_collector = null;
        this.table_generator = null;
        this.run_id_in_scenario = run_id_in_scenario;
        this.network = null;
        this.visualizer = visualizer;
        this.initialization_queue = [];
    }
    __del__() {
        /*
        Remove circular reference before deletion

        :return:
        */
        this.visualizer = null;
    }
    create() {
        /*
        An initialization method, which is called immediately right after the ``Model`` object is created.

        :return: None
        */
    }
    setup() {
        /*
        General method for model setup, which is called after ``Model.create()``

        :return: None
        */
    }
    create_db_conn() {
        /*
        Create a database connection with the project configuration.

        :return: DBConn object
        */
        return create_db_conn(this.config);
    }
    create_agent_list(agent_class) {
        /*
        Create an agent list object. A model could contain multiple ``AgentList``s.

        :param agent_class: The class of desired agent type.
        :return: Agentlist object created
        */
        return new AgentList(agent_class, {"model": this});
    }
    create_environment(env_class) {
        /*
        Create the environment of model. Notice that a model has only one environment.

        :param env_class:
        :return: Environment object created
        */
        var env;
        env = env_class();
        env.model = this;
        env.scenario = this.scenario;
        this.initialization_queue.append(env);
        return env;
    }
    create_grid(grid_cls = null, spot_cls = null) {
        /*
        Create a grid.

        :param grid_cls: The class of grid, ``Melodie.Grid`` by default.
        :param spot_cls: The class of spot, ``Melodie.Spot`` by default.
        :return: Grid object.
        */
        var grid;
        grid_cls = ((grid_cls !== null) ? grid_cls : Grid);
        spot_cls = ((spot_cls !== null) ? spot_cls : Spot);
        grid = grid_cls(spot_cls, this.scenario);
        this.initialization_queue.append(grid);
        return grid;
    }
    create_network(network_cls = null, edge_cls = null) {
        /*
        Create the network of model.

        :param network_cls: The type of network object, ``Melodie.Network`` by default.
        :param edge_cls: The type of edge object, ``Melodie.Edge`` by default.
        :return: Network object created
        */
        var network;
        if ((network_cls === null)) {
            network_cls = Network;
        }
        network = network_cls(edge_cls);
        this.initialization_queue.append(network);
        return network;
    }
    create_data_collector(data_collector_cls) {
        /*
        Create the data collector of model.

        :param data_collector_cls: The datacollector class, must be a custom class inheriting ``Melodie.DataCollector``.
        :return: Datacollector object created.
        */
        var data_collector;
        data_collector = data_collector_cls();
        data_collector.model = this;
        data_collector.scenario = this.scenario;
        this.initialization_queue.append(data_collector);
        return data_collector;
    }
    create_agent_container(agent_class, initial_num, params_df = null, container_type = "list") {
        /*
        Create a container for agents.

        :param agent_class:
        :param initial_num: Initial number of agents
        :param params_df:   Pandas DataFrame
        :param container_type: a str, "list" or "dict"
        :return: Agent container created
        */
        var agent_container_class, container;
        agent_container_class = None;
        if ((container_type === "list")) {
            agent_container_class = AgentList;
        } else {
            if ((container_type === "dict")) {
                agent_container_class = AgentDict;
            } else {
                throw new NotImplementedError(`Container type '${container_type}' is not valid!`);
            }
        }
        container = agent_container_class(agent_class, {"model": this});
        if ((params_df !== null)) {
            container.set_properties(params_df);
        } else {
            show_prettified_warning((`No dataframe set for the ${agent_container_class.__name__}.
`
 + show_link()));
        }
        this.initialization_queue.append(container);
        return container;
    }
    run() {
        /*
        Model run. Be sure to inherit this method on your model.

        :return: None
        */
    }
    iterator(period_num) {
        /*
        Return an iterator which iterates from `0` to `period_num-1`. In each iteration, the iterator updates the
        visualizer if it exists.

        :param period_num: How many periods will this model run.
        :return: None
        */
        return new ModelRunRoutine(period_num, this);
    }
    _visualizer_step(current_step) {
        /*
        If visualizer is defined, make it step.

        :param current_step:
        :return:
        */
        if (((this.visualizer !== null) && (current_step > 0))) {
            this.visualizer.step(current_step);
        }
    }
    init_visualize() {
        /*
        Be sure to implement it if you would like to use visualizer.

        :return:
        */
    }
    _setup() {
        /*
        Wrapper of setup()

        :return:
        */
        this.create();
        this.setup();
        for (var component_to_init, _pj_c = 0, _pj_a = this.initialization_queue, _pj_b = _pj_a.length; (_pj_c < _pj_b); _pj_c += 1) {
            component_to_init = _pj_a[_pj_c];
            component_to_init._setup();
        }
    }
}
export {Model};

//# sourceMappingURL=model.js.map
