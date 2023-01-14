import {Any, Dict, Optional, TYPE_CHECKING} from './types';
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
    function in_es6(left, right) {
        if (((right instanceof Array) || ((typeof right) === "string"))) {
            return (right.indexOf(left) > (- 1));
        } else {
            if (((right instanceof Map) || (right instanceof Set) || (right instanceof WeakMap) || (right instanceof WeakSet))) {
                return right.has(left);
            } else {
                return (left in right);
            }
        }
    }
    container["_assert"] = _assert;
    container["in_es6"] = in_es6;
    return container;
}
_pj = {};
_pj_snippets(_pj);
class Element {
    set_params(params) {
        /*
        :param params:
        :return:
        */
        var paramName, paramValue;
        for (var item, _pj_c = 0, _pj_a = params.items(), _pj_b = _pj_a.length; (_pj_c < _pj_b); _pj_c += 1) {
            item = _pj_a[_pj_c];
            [paramName, paramValue] = item;
            _pj._assert(_pj.in_es6(paramName, this.__dict__.keys()), `param named ${paramName}, value ${paramValue} not in Agent.params:${this.__dict__.keys()}`);
            this[paramName] = paramValue;
        }
    }
}
class Agent extends Element {
    constructor(agent_id) {
        super();
        this.id = agent_id;
        this.scenario = null;
        this.model = null;
    }
    setup() {
        /*
        This is the initialization method, declare properties here.
        Here, "Declare" is to define properties with zero as initial value, such as:
        ```python
        class NewAgent(Agent)
        def setup(self):
        self.int_property = 0
        self.float_property = 0.0
        self.str_property = ""
        ```
        It is also fine to define properties with complex data structure such as dict/list/set, but the values in the
        complex data structure is hard to be recorded by the `DataCollector`
        This method is executed at the end of the `__init__` method of the corresponding agent container.
        :return:
        */
    }
    __repr__() {
        var d, k, v;
        d = {};
        for (var item, _pj_c = 0, _pj_a = this.__dict__.items(), _pj_b = _pj_a.length; (_pj_c < _pj_b); _pj_c += 1) {
            item = _pj_a[_pj_c];
            [k, v] = item;
            if ((! k.startswith("_"))) {
                d[k] = v;
            }
        }
        return ("<%s %s>" % [this.__class__.__name__, d]);
    }
}
export {Element, Agent};

//# sourceMappingURL=agent.js.map
