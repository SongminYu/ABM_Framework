import {ClassVar, Dict, List, Set, Tuple} from './types';
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
class GridItem extends Agent {
    constructor(agent_id, grid, x = 0, y = 0) {
        super(agent_id);
        this.grid = grid;
        this.x = x;
        this.y = y;
    }
    __repr__() {
        return `<${this.__class__.__name__} 'x': ${this.x}, 'y': ${this.y}>`;
    }
}
class GridAgent extends GridItem {
    constructor(agent_id, x = 0, y = 0, grid = null) {
        super(agent_id, grid, x, y);
        this.category = (- 1);
        this.set_category();
        _pj._assert((this.category >= 0), "Category should be larger or ");
    }
    set_category() {
        /*
        Set the category of GridAgent.

        As there may be more than one types of agent wandering around the grid, `category` is used to tell the type of
        `GridAgent`. So be sure to inherit this method in custom GridAgent implementation.

        :return: int
        */
        throw new NotImplementedError("Category should be set for GridAgent");
    }
    rand_move_agent(x_range, y_range) {
        /*
        Randomly move to a new position within x and y range.

        :return: None
        */
        if ((this.grid === null)) {
            throw new ValueError("Grid Agent has not been registered onto the grid!");
        }
        [this.x, this.y] = this.grid.rand_move_agent(this, this.category, x_range, y_range);
    }
}
class Spot extends GridItem {
    constructor(spot_id, grid, x = 0, y = 0) {
        super(spot_id, grid, x, y);
        this.grid = grid;
        this.colormap = 0;
    }
    get_spot_agents() {
        /*
        Get all agents on the spot.

        :return: a list of grid agent.
        */
        return this.grid.get_spot_agents(this);
    }
    __repr__() {
        return `<${this.__class__.__name__} 'x': ${this.x}, 'y': ${this.y}, 'colormap': ${this.colormap}, 'payload' : ${this.__dict__}>`;
    }
    get_style() {
        return {"backgroundColor": "#ffffff"};
    }
}
class Grid {
    /*
    Grid is a widely-used discrete space for ABM.
    Grid contains many `Spot`s, each `Spot` could contain several agents.
    */
    constructor(spot_cls, width, height, wrap = true, caching = true) {
        /*
        :param spot_cls: The class of Spot
        :param width: The width of Grid
        :param height: The height of Grid
        :param wrap: If true, the coordinate overflow will be mapped to another end.
        :param caching: If true, the neighbors and bound check results will be cached to avoid re-computing.
        */
        this.width = width;
        this.height = height;
        this.wrap = wrap;
        this._spot_cls = spot_cls;
        this._existed_agents = {};
        this._agent_ids = {};
        this._spots = [];
        this.caching = caching;
    }
    init_grid() {
        this._spots = function () {
    var _pj_a = [], _pj_b = range(this.height);
    for (var _pj_c = 0, _pj_d = _pj_b.length; (_pj_c < _pj_d); _pj_c += 1) {
        var y = _pj_b[_pj_c];
        _pj_a.push(function () {
    var _pj_e = [], _pj_f = range(this.width);
    for (var _pj_g = 0, _pj_h = _pj_f.length; (_pj_g < _pj_h); _pj_g += 1) {
        var x = _pj_f[_pj_g];
        _pj_e.push(new spot_cls(this._convert_to_1d(x, y), x, y));
    }
    return _pj_e;
}
.call(this));
    }
    return _pj_a;
}
.call(this);
        for (var x = 0, _pj_a = this.width; (x < _pj_a); x += 1) {
            for (var y = 0, _pj_b = this.height; (y < _pj_b); y += 1) {
                this._spots[y][x].setup();
            }
        }
        if (caching) {
            this.get_neighbors = functools.lru_cache((this.width * this.height))(this.get_neighbors);
            this._bound_check = functools.lru_cache((this.width * this.height))(this._bound_check);
        }
    }
    add_category(category_name) {
        /*
        Add agent category
        :param category_name:
        :return:
        */
        this._agent_ids[category_name] = function () {
    var _pj_a = [], _pj_b = range((this.width * this.height));
    for (var _pj_c = 0, _pj_d = _pj_b.length; (_pj_c < _pj_d); _pj_c += 1) {
        var i = _pj_b[_pj_c];
        _pj_a.push(set());
    }
    return _pj_a;
}
.call(this);
        this._existed_agents[category_name] = {};
    }
    get_spot(x, y) {
        /*
        Get a ``Spot`` at position ``(x, y)``

        :param x:
        :param y:
        :return: The ``Spot`` at position (x, y)
        */
        [x, y] = this._bound_check(x, y);
        return this._spots[y][x];
    }
    get_agent_ids(category, x, y) {
        /*
        Get all agent of a specific category from the spot at (x, y)
        :param category:
        :param x:
        :param y:
        :return: A set of int, the agent ids.
        */
        var agent_ids;
        agent_ids = this._agent_ids[category][this._convert_to_1d(x, y)];
        if ((agent_ids === null)) {
            throw new KeyError(`Category ${category} not registered!`);
        }
        return agent_ids;
    }
    _convert_to_1d(x, y) {
        return ((x * this.height) + y);
    }
    _in_bounds(x, y) {
        return (((0 <= x) && (x < this.width)) && ((0 <= y) && (y <= this.height)));
    }
    _get_category_of_agents(category_name) {
        var category;
        category = this._existed_agents.get(category_name);
        if ((category === null)) {
            throw new ValueError(`Category ${category_name} is not registered!`);
        }
        return category;
    }
    _bound_check(x, y) {
        if (this.wrap) {
            return this.coords_wrap(x, y);
        }
        if ((! ((0 <= x) && (x < this.width)))) {
            throw new IndexError("grid index x was out of range");
        } else {
            if ((! ((0 <= y) && (y <= this.height)))) {
                throw new IndexError("grid index y was out of range");
            } else {
                return [x, y];
            }
        }
    }
    coords_wrap(x, y) {
        /*
        Wrap the coordination
        :param x:
        :param y:
        :return:
        */
        var x_wrapped, y_wrapped;
        [x_wrapped, y_wrapped] = [(x % this.width), (y % this.height)];
        x_wrapped = ((x_wrapped >= 0) ? x_wrapped : (this.width + x_wrapped));
        y_wrapped = ((y_wrapped >= 0) ? y_wrapped : (this.height + y_wrapped));
        return [x_wrapped, y_wrapped];
    }
    _get_neighbor_positions(x, y, radius = 1, moore = true, except_self = true) {
        /*
        Get the neighbors of some spot.

        :param x:
        :param y:
        :param radius:
        :param moore:
        :param except_self:
        :return:
        */
        var neighbors;
        [x, y] = this._bound_check(x, y);
        neighbors = [];
        for (var dx = (- radius), _pj_a = (radius + 1); (dx < _pj_a); dx += 1) {
            for (var dy = (- radius), _pj_b = (radius + 1); (dy < _pj_b); dy += 1) {
                if (((! moore) && ((abs(dx) + abs(dy)) > radius))) {
                    continue;
                }
                if (((! this.wrap) && (! this._in_bounds((x + dx), (y + dy))))) {
                    continue;
                }
                if ((((dx === 0) && (dy === 0)) && except_self)) {
                    continue;
                }
                neighbors.append(this._bound_check((x + dx), (y + dy)));
            }
        }
        return neighbors;
    }
    _get_neighborhood(x, y, radius = 1, moore = true, except_self = true) {
        /*
        Get all spots around (x, y)

        */
        var neighbor_positions, spots;
        neighbor_positions = this._get_neighbor_positions(x, y, radius, moore, except_self);
        spots = [];
        for (var pos, _pj_c = 0, _pj_a = neighbor_positions, _pj_b = _pj_a.length; (_pj_c < _pj_b); _pj_c += 1) {
            pos = _pj_a[_pj_c];
            [x, y] = pos;
            spots.append(this.get_spot(x, y));
        }
        return spots;
    }
    get_agent_neighborhood(agent, radius = 1, moore = true, except_self = true) {
        return this._get_neighborhood(agent.x, agent.y, radius, moore, except_self);
    }
    get_spot_neighborhood(spot, radius = 1, moore = true, except_self = true) {
        return this._get_neighborhood(spot.x, spot.y, radius, moore, except_self);
    }
    add_agent(agent_id, category, x, y) {
        /*
        Add agent onto the grid
        :param agent_id:
        :param category:
        :param x:
        :param y:
        :return:
        */
        var category_of_agents;
        [x, y] = this._bound_check(x, y);
        category_of_agents = this._get_category_of_agents(category);
        if (_pj.in_es6(agent_id, category_of_agents.keys())) {
            throw new ValueError(`Agent with id: ${agent_id} already exists on grid!`);
        }
        if (_pj.in_es6(agent_id, this._agent_ids[category][this._convert_to_1d(x, y)])) {
            throw new ValueError(`Agent with id: ${agent_id} already exists at position ${[x, y]}!`);
        } else {
            this._agent_ids[category][this._convert_to_1d(x, y)].add(agent_id);
            this._existed_agents[category][agent_id] = [x, y];
        }
    }
    _remove_agent(agent_id, category, x, y) {
        var category_of_agents;
        [x, y] = this._bound_check(x, y);
        category_of_agents = this._get_category_of_agents(category);
        if ((! _pj.in_es6(agent_id, category_of_agents.keys()))) {
            throw new ValueError(`Agent with id: ${agent_id} does not exist on grid!`);
        }
        if ((! _pj.in_es6(agent_id, this._existed_agents[category]))) {
            throw new ValueError("Agent does not exist on the grid!");
        }
        if ((! _pj.in_es6(agent_id, this._agent_ids[category][this._convert_to_1d(x, y)]))) {
            console.log("Melodie-boost error occured. agent_id:", agent_id, "x:", x, "y:", y);
            throw new IndexError("agent_id does not exist on such coordinate.");
        } else {
            this._agent_ids[category][this._convert_to_1d(x, y)].remove(agent_id);
            this._existed_agents[category].pop(agent_id);
        }
    }
    remove_agent(agent_id, category) {
        /*
        Remove agent from the grid
        :param agent_id:
        :param category:
        :return:
        */
        var source_x, source_y;
        [source_x, source_y] = this.get_agent_pos(agent_id, category);
        this._remove_agent(agent_id, category, source_x, source_y);
    }
    move_agent(agent_id, category, target_x, target_y) {
        /*
        Move agent to target position.
        :param agent_id:
        :param category:
        :param target_x:
        :param target_y:
        :return:
        */
        var source_x, source_y;
        [source_x, source_y] = this.get_agent_pos(agent_id, category);
        this._remove_agent(agent_id, category, source_x, source_y);
        this.add_agent(agent_id, category, target_x, target_y);
    }
    get_agent_pos(agent_id, category) {
        /*
        Get the agent position at the grid.
        :param agent_id:
        :param category:
        :return:
        */
        return this._existed_agents[category][agent_id];
    }
    to_2d_array(attr_name) {
        /*
        Collect attribute of each spot and write the attribute value into an 2d np.array.
        Notice:
        - The attribute to collect should be float/int/bool, not other types such as str.
        - If you would like to get an element from the returned array, please write like this:
        ```python
        arr = self.to_2d_array('some_attr')
        y = 10
        x = 5
        spot_at_x_5_y_10 = arr[y][x] # CORRECT. Get the some_attr value of spot at `x = 5, y = 10`
        spot_at_x_5_y_10 = arr[x][y] # INCORRECT. You will get the value of spot at `x = 10, y = 5`
        ```
        :param attr_name: the attribute name to collect for this model.
        :return:
        */
        return vectorize_2d(this._spots, attr_name);
    }
    get_roles() {
        var grid_roles, pos_1d, spot;
        grid_roles = np.zeros([(this.height * this.width), 4]);
        for (var x = 0, _pj_a = this.width; (x < _pj_a); x += 1) {
            for (var y = 0, _pj_b = this.height; (y < _pj_b); y += 1) {
                spot = this.get_spot(x, y);
                pos_1d = this._convert_to_1d(x, y);
                grid_roles[[pos_1d, 0]] = x;
                grid_roles[[pos_1d, 1]] = y;
                grid_roles[[pos_1d, 2]] = 0;
                grid_roles[[pos_1d, 3]] = spot.role;
            }
        }
        return grid_roles;
    }
}
export {GridAgent, GridItem, Spot, Grid};

//# sourceMappingURL=grid.js.map
