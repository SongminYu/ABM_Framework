from .types import ClassVar, Set, Dict, List, Tuple

from .agent import Agent


class GridItem(Agent):
    def __init__(self, agent_id: int, grid, x: int = 0, y: int = 0):
        super().__init__(agent_id)
        self.grid = grid
        self.x = x
        self.y = y

    # def set_params(self, params):
    #     """

    #     :param params:
    #     :return:
    #     """
    #     for paramName, paramValue in params.items():
    #         assert hasattr(
    #             self, paramName), f"property named {paramName} not in {self.__class__.__name__}"
    #         setattr(self, paramName, paramValue)

    def __repr__(self):
        return f"<{self.__class__.__name__} 'x': {self.x}, 'y': {self.y}>"


class GridAgent(GridItem):
    def __init__(self, agent_id: int, x: int = 0, y: int = 0, grid=None):
        super().__init__(agent_id, grid, x, y)
        self.category = -1
        self.set_category()
        assert self.category >= 0, "Category should be larger or "

    def set_category(self) -> int:
        """
        Set the category of GridAgent.

        As there may be more than one types of agent wandering around the grid, `category` is used to tell the type of
        `GridAgent`. So be sure to inherit this method in custom GridAgent implementation.

        :return: int
        """
        raise NotImplementedError("Category should be set for GridAgent")

    def rand_move_agent(self, x_range, y_range):
        """
        Randomly move to a new position within x and y range.

        :return: None
        """
        if self.grid is None:
            raise ValueError(
                "Grid Agent has not been registered onto the grid!")
        self.x, self.y = self.grid.rand_move_agent(
            self, self.category, x_range, y_range)


class Spot(GridItem):
    def __init__(self, spot_id: int, grid: Grid, x: int = 0, y: int = 0):
        super().__init__(spot_id, grid, x, y)
        self.grid = grid
        self.colormap = 0

    def get_spot_agents(self):
        """
        Get all agents on the spot.

        :return: a list of grid agent.
        """
        return self.grid.get_spot_agents(self)

    def __repr__(self):
        return f"<{self.__class__.__name__} 'x': {self.x}, 'y': {self.y}, 'colormap': {self.colormap}, 'payload' : {self.__dict__}>"

    def get_style(self):
        return {
            "backgroundColor": "#ffffff"
        }


class Grid:
    """
    Grid is a widely-used discrete space for ABM.
    Grid contains many `Spot`s, each `Spot` could contain several agents.
    """

    def __init__(self, spot_cls: ClassVar[Spot], width: int, height: int, wrap=True, caching=True):
        """
        :param spot_cls: The class of Spot
        :param width: The width of Grid
        :param height: The height of Grid
        :param wrap: If true, the coordinate overflow will be mapped to another end.
        :param caching: If true, the neighbors and bound check results will be cached to avoid re-computing.
        """
        self.width = width
        self.height = height
        self.wrap = wrap
        self._spot_cls = spot_cls
        self._existed_agents: Dict[str, Dict[int, Tuple[int, int]]] = {}
        self._agent_ids: Dict[str, List[Set[int]]] = {}
        self._spots = []
        self.caching = caching
        self._agent_containers = {}

    def init_grid(self):
        self._spots = [[new(self._spot_cls(self._convert_to_1d(x, y), x, y))
                        for x in range(self.width)] for y in range(self.height)]
        for x in range(self.width):
            for y in range(self.height):
                self._spots[y][x].setup()
        # [set() for i in range(width * height)]

        # if caching:
        #     self.get_neighbors = functools.lru_cache(
        #         self.width * self.height)(self.get_neighbors)
        #     self._bound_check = functools.lru_cache(
        #         self.width * self.height)(self._bound_check)

    def add_category(self, category_name: str):
        """
        Add agent category
        :param category_name:
        :return:
        """
        self._agent_ids[category_name] = [set()
                                          for i in range(self.width * self.height)]
        self._existed_agents[category_name] = {}

    def get_spot(self, x, y) -> "Spot":
        """
        Get a ``Spot`` at position ``(x, y)``

        :param x:
        :param y:
        :return: The ``Spot`` at position (x, y)
        """
        x, y = self._bound_check(x, y)
        return self._spots[y][x]

    def get_agent_ids(self, category: str, x: int, y: int) -> Set[int]:
        """
        Get all agent of a specific category from the spot at (x, y)
        :param category:
        :param x:
        :param y:
        :return: A set of int, the agent ids.
        """
        agent_ids = self._agent_ids[category][self._convert_to_1d(x, y)]
        if agent_ids is None:
            raise KeyError(f'Category {category} not registered!')
        return agent_ids

    def _convert_to_1d(self, x, y):
        return x * self.height + y

    def _in_bounds(self, x, y):
        return (0 <= x < self.width) and (0 <= y <= self.height)

    def _get_category_of_agents(self, category_name: str):
        category = self._existed_agents.get(category_name)
        if category is None:
            raise ValueError(f"Category {category_name} is not registered!")
        return category

    def _bound_check(self, x, y):
        if self.wrap:
            return self.coords_wrap(x, y)
        if not (0 <= x < self.width):
            raise IndexError("grid index x was out of range")
        elif not (0 <= y <= self.height):
            raise IndexError("grid index y was out of range")
        else:
            return x, y

    def coords_wrap(self, x, y):
        """
        Wrap the coordination
        :param x:
        :param y:
        :return:
        """
        x_wrapped, y_wrapped = x % self.width, y % self.height
        x_wrapped = x_wrapped if x_wrapped >= 0 else self.width + x_wrapped
        y_wrapped = y_wrapped if y_wrapped >= 0 else self.height + y_wrapped
        return x_wrapped, y_wrapped

    def _get_neighbor_positions(self, x, y, radius: int = 1, moore=True, except_self=True) -> List[Tuple[int, int]]:
        """
        Get the neighbors of some spot.

        :param x:
        :param y:
        :param radius:
        :param moore:
        :param except_self:
        :return:
        """
        x, y = self._bound_check(x, y)
        neighbors = []
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                if not moore and abs(dx) + abs(dy) > radius:
                    continue
                if not self.wrap and not self._in_bounds(x + dx, y + dy):
                    continue
                if dx == 0 and dy == 0 and except_self:
                    continue
                neighbors.append(self._bound_check(x + dx, y + dy))
        return neighbors

    def _get_neighborhood(self, x, y, radius=1, moore=True, except_self=True):
        """
        Get all spots around (x, y)

        """
        neighbor_positions = self._get_neighbor_positions(
            x, y, radius, moore, except_self)
        spots = []
        for pos in neighbor_positions:
            x, y = pos
            spots.append(self.get_spot(x, y))
        return spots

    def get_agent_neighborhood(self, agent, radius=1, moore=True, except_self=True):
        return self._get_neighborhood(agent.x, agent.y, radius, moore, except_self)

    def get_spot_neighborhood(self, spot, radius=1, moore=True, except_self=True):
        return self._get_neighborhood(spot.x, spot.y, radius, moore, except_self)

    def add_agent(self, agent_id: int, category: str, x: int, y: int):
        """
        Add agent onto the grid
        :param agent_id:
        :param category:
        :param x:
        :param y:
        :return:
        """
        x, y = self._bound_check(x, y)

        category_of_agents = self._get_category_of_agents(category)

        if agent_id in category_of_agents.keys():
            raise ValueError(
                f"Agent with id: {agent_id} already exists on grid!")

        if agent_id in self._agent_ids[category][self._convert_to_1d(x, y)]:
            raise ValueError(
                f"Agent with id: {agent_id} already exists at position {(x, y)}!")
        else:
            self._agent_ids[category][self._convert_to_1d(x, y)].add(agent_id)
            self._existed_agents[category][agent_id] = (x, y)

    def _remove_agent(self, agent_id: int, category: str, x: int, y: int):
        x, y = self._bound_check(x, y)

        category_of_agents = self._get_category_of_agents(category)

        if agent_id not in category_of_agents.keys():
            raise ValueError(
                f"Agent with id: {agent_id} does not exist on grid!")

        if agent_id not in self._existed_agents[category]:
            raise ValueError("Agent does not exist on the grid!")
        if agent_id not in self._agent_ids[category][self._convert_to_1d(x, y)]:
            print("Melodie-boost error occured. agent_id:", agent_id, "x:", x, "y:",
                  y)
            raise IndexError("agent_id does not exist on such coordinate.")
        else:
            self._agent_ids[category][self._convert_to_1d(
                x, y)].remove(agent_id)
            self._existed_agents[category].pop(agent_id)

    def remove_agent(self, agent_id: int, category: str):
        """
        Remove agent from the grid
        :param agent_id:
        :param category:
        :return:
        """
        source_x, source_y = self.get_agent_pos(agent_id, category)
        self._remove_agent(agent_id, category, source_x, source_y)

    def move_agent(self, agent_id, category: str, target_x, target_y):
        """
        Move agent to target position.
        :param agent_id:
        :param category:
        :param target_x:
        :param target_y:
        :return:
        """
        source_x, source_y = self.get_agent_pos(agent_id, category)
        self._remove_agent(agent_id, category, source_x, source_y)
        self.add_agent(agent_id, category, target_x, target_y)

    def get_agent_pos(self, agent_id: int, category: str) -> Tuple[int, int]:
        """
        Get the agent position at the grid.
        :param agent_id:
        :param category:
        :return:
        """
        return self._existed_agents[category][agent_id]

    def to_2d_array(self, attr_name: str) -> np.ndarray:
        """
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
        """
        return vectorize_2d(self._spots, attr_name)

    def get_roles(self):
        grid_roles = np.zeros((self.height * self.width, 4))
        for x in range(self.width):
            for y in range(self.height):
                spot = self.get_spot(x, y)
                # role = spot.role
                pos_1d = self._convert_to_1d(x, y)
                grid_roles[pos_1d, 0] = x
                grid_roles[pos_1d, 1] = y
                grid_roles[pos_1d, 2] = 0
                grid_roles[pos_1d, 3] = spot.role
        return grid_roles

    def setup_agent_locations(self, category, initial_placement="direct") -> None:
        """
        Add an agent category.

        For example, if there are two classes of agents: `Wolf(GridAgent)` and `Sheep(GridAgent)`,
        and there are 100 agents with id 0~99 for each class. It is obvious in such a circumstance that
        we cannot identify an agent only with agent *id*.So it is essential to use *category_name* to distinguish two types of agents.

        :param category_id: The id of new category.
        :param category: An AgentList object
        :param initial_placement: A str object stand for initial placement.
        :return: None
        """
        initial_placement = initial_placement.lower()
        self._add_agent_container(category, initial_placement)

    def _add_agent_container(self, category, initial_placement):

        assert category is not None, f"Agent Container was None"
        agent = category[0]
        category_id = agent.category
        assert 0 <= category_id < 100, f"Category ID {category_id} should be a int between [0, 100)"
        assert self._agent_containers[category_id] is None, f"Category ID {category_id} already existed!"
        self._agent_containers[category_id] = category
        assert initial_placement in {"random_single", "direct"}, f"Invalid initial placement '{initial_placement}' "
        if initial_placement == "random_single":
            for agent in category:
                pos = self.find_empty_spot()
                agent.x = pos[0]
                agent.y = pos[1]
                self.add_agent(agent)
        elif initial_placement == "direct":
            for agent in category:
                self.add_agent(agent)


__all__ = ['GridAgent', 'GridItem', 'Spot', 'Grid']
