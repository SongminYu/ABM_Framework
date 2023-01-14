import {Optional, Union} from './types';
import {Element} from './agent';
var _pj;
function _pj_snippets(container) {
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
    container["in_es6"] = in_es6;
    return container;
}
_pj = {};
_pj_snippets(_pj);
class Scenario extends Element {
    /*
    Scenario contains a set of parameters used in simulation model.
    It is created before the initialization of ``Model``.

    */
    constructor(id_scenario = null) {
        /*
        :param id_scenario: the id of scenario. if None, this will be self-increment from 0 to scenarios_number-1
        */
        super();
        this._parameters = [];
        this.manager = null;
        this.id = id_scenario;
        this.run_num = 1;
        this.period_num = 0;
    }
    copy() {
        /*
        Copy current scenario to a new scenario.

        :return: New scenario object.
        */
        var new_scenario, property;
        new_scenario = this.__class__();
        for (var property_name, _pj_c = 0, _pj_a = this.__dict__.keys(), _pj_b = _pj_a.length; (_pj_c < _pj_b); _pj_c += 1) {
            property_name = _pj_a[_pj_c];
            property = this.__dict__[property_name];
            new_scenario[property_name] = property;
        }
        for (var parameter, _pj_c = 0, _pj_a = this._parameters, _pj_b = _pj_a.length; (_pj_c < _pj_b); _pj_c += 1) {
            parameter = _pj_a[_pj_c];
            parameter.init = this[parameter.name];
        }
        return new_scenario;
    }
    setup() {
        /*
        Setup method, be sure to inherit it on the custom scenario class.
        */
    }
    to_dict() {
        /*
        Convert this scenario object to a dict.

        :return: A ``dict``, ``property_name->property_value``
        */
        var d, v;
        d = {};
        for (var k, _pj_c = 0, _pj_a = this.__dict__.keys(), _pj_b = _pj_a.length; (_pj_c < _pj_b); _pj_c += 1) {
            k = _pj_a[_pj_c];
            v = this.__dict__[k];
            d[k] = v;
        }
        return d;
    }
    to_json() {
        /*
        Convert this scenario to a dict without concerning non-serializable properties.

        :return: a ``dict``, ``property_name->property_value``, without non-serializable properties
        */
        var d;
        d = {};
        for (var k, _pj_c = 0, _pj_a = this.__dict__.keys(), _pj_b = _pj_a.length; (_pj_c < _pj_b); _pj_c += 1) {
            k = _pj_a[_pj_c];
            if ((! _pj.in_es6(k, ["manager"]))) {
                d[k] = this.__dict__[k];
            }
        }
        return d;
    }
    __repr__() {
        return `<${this.__class__.__name__} ${this.__dict__}>`;
    }
}
export {Scenario};

//# sourceMappingURL=scenario.js.map
