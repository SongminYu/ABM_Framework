import {ClassVar, Dict, Generic, List, Optional, Set, TYPE_CHECKING, Type, TypeVar, Union} from './types';
import {Agent} from './agent';
var _pj;
function _pj_snippets(container) {
    function _assert(comp, msg) {
        function PJAssertionError(message) {
            this.name = "PJAssertionError";
            this.message = (message || "Custom error PJAssertionError");
            if (((typeof Error.captureStackTrace) === "function")) {
                Error.captureStackTrace(this, this.constructor);
            } else {
                this.stack = new Error(message).stack;
            }
        }
        PJAssertionError.prototype = Object.create(Error.prototype);
        PJAssertionError.prototype.constructor = PJAssertionError;
        msg = (msg || "Assertion failed.");
        if ((! comp)) {
            throw new PJAssertionError(msg);
        }
    }
    container["_assert"] = _assert;
    return container;
}
_pj = {};
_pj_snippets(_pj);
class SeqIter {
    /*
    The iterator to deal with for-loops in AgentList or other agent containers
    */
    constructor(seq) {
        this._seq = seq;
        this._i = 0;
    }
    __next__() {
        var next_item;
        if ((this._i >= this._seq.length)) {
            throw StopIteration;
        }
        next_item = this._seq[this._i];
        this._i += 1;
        return next_item;
    }
}
class BaseAgentContainer {
    /*
    The base class that contains agents
    */
    constructor() {
        this._id_offset = (- 1);
        this.scenario = null;
        this.agents = null;
    }
    new_id() {
        /*
        Create a new auto-increment ID
        :return:
        */
        this._id_offset += 1;
        return this._id_offset;
    }
    all_agent_ids() {
        /*
        Get id of all agents.
        :return:
        */
        return function () {
    var _pj_a = [], _pj_b = this.agents;
    for (var _pj_c = 0, _pj_d = _pj_b.length; (_pj_c < _pj_d); _pj_c += 1) {
        var agent = _pj_b[_pj_c];
        _pj_a.push(agent.id);
    }
    return _pj_a;
}
.call(this);
    }
    to_list(column_names = null) {
        /*
        Convert all agent properties to a list of dict.
        :param column_names:  property names
        :return:
        */
    }
    get_agent(agent_id) {
        var index;
        index = binary_search(this.agents, agent_id, {"key": (agent) => {
    return agent.id;
}});
        if ((index === (- 1))) {
            return null;
        } else {
            return this.agents[index];
        }
    }
}
class AgentList extends BaseAgentContainer {
    constructor(agent_class, length, model) {
        super();
        this._iter_index = 0;
        this.scenario = model.scenario;
        this.agent_class = agent_class;
        this.initial_agent_num = length;
        this.model = model;
        this.agents = [];
    }
    __repr__() {
        return `<AgentList ${this.agents}>`;
    }
    get length() {
        return this.agents.length;
    }
    __getitem__(item) {
        return this.agents.__getitem__(item);
    }
    __iter__() {
        this._iter_index = 0;
        return new SeqIter(this.agents);
    }
    init_agents() {
        /*
        Initialize all agents in the container, and call the `setup()` method
        :return:
        */
        var agents, scenario;
        agents = function () {
    var _pj_a = [], _pj_b = range(this.initial_agent_num);
    for (var _pj_c = 0, _pj_d = _pj_b.length; (_pj_c < _pj_d); _pj_c += 1) {
        var i = _pj_b[_pj_c];
        _pj_a.push(this.agent_class(this.new_id()));
    }
    return _pj_a;
}
.call(this);
        scenario = this.model.scenario;
        for (var agent, _pj_c = 0, _pj_a = agents, _pj_b = _pj_a.length; (_pj_c < _pj_b); _pj_c += 1) {
            agent = _pj_a[_pj_c];
            agent.scenario = scenario;
            agent.model = this.model;
            agent.setup();
        }
        return agents;
    }
    random_sample(sample_num) {
        /*
        Randomly sample `sample_num` agents from the container
        :param sample_num:
        :return:
        */
        return random.sample(this.agents, sample_num);
    }
    remove(agent) {
        /*
        Remove the agent
        :param agent:
        :return:
        */
        var a;
        for (var i = 0, _pj_a = this.agents.length; (i < _pj_a); i += 1) {
            a = this.agents[i];
            if ((a === agent)) {
                this.agents.pop(i);
                break;
            }
        }
    }
    add(agent = null, params = null) {
        /*
        Add an agent
        :param agent:
        :param params:
        :return:
        */
        var new_id;
        new_id = this.new_id();
        if ((agent !== null)) {
            _pj._assert((agent instanceof Agent), null);
        } else {
            agent = new this.agent_class(new_id);
        }
        agent.scenario = this.model.scenario;
        agent.model = this.model;
        agent.setup();
        if ((params !== null)) {
            _pj._assert((params instanceof dict), null);
            if ((params.get("id") !== null)) {
                logger.warning("Warning, agent 'id' passed together with 'params' will be overridden by a new id generated automatically");
            }
            agent.set_params(params);
        }
        agent.id = new_id;
        this.agents.append(agent);
    }
    set_properties(props_df) {
        /*
        Extract properties from a dataframe, and Each row in the dataframe represents the property of an agent.
        :param props_df:
        :return:
        */
        super.set_properties(props_df);
        this.agents.sort({"key": (agent) => {
    return agent.id;
}});
    }
}
export {AgentList};

//# sourceMappingURL=agent_list.js.map
