import {Dict, List, Optional} from './types';
import {Element} from './agent';
class Environment extends Element {
    constructor() {
        super();
        this.model = null;
        this.scenario = null;
    }
    setup() {
        /*
        The setup method of the environment.
        Use `self.scenario` to get the parameters from the scenario.
        :return:
        */
    }
    to_dict(properties) {
        /*
        Dump Environment to a plain dict.
        :param properties:
        :return:
        */
        var d;
        if ((properties === null)) {
            properties = this.__dict__.keys();
        }
        d = {};
        for (var property, _pj_c = 0, _pj_a = properties, _pj_b = _pj_a.length; (_pj_c < _pj_b); _pj_c += 1) {
            property = _pj_a[_pj_c];
            d[property] = this.__dict__[property];
        }
        return d;
    }
}
export {Environment};

//# sourceMappingURL=environment.js.map
