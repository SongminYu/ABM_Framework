# import random

from .types import TYPE_CHECKING, ClassVar, List, Dict, Union, Set, Optional, TypeVar, Type, Generic

from .agent import Agent



class SeqIter:
    """
    The iterator to deal with for-loops in AgentList or other agent containers
    """

    def __init__(self, seq):
        self._seq = seq
        self._i = 0

    def __next__(self):
        if self._i >= len(self._seq):
            raise StopIteration
        next_item = self._seq[self._i]
        self._i += 1
        return next_item

class BaseAgentContainer:
    """
    The base class that contains agents
    """

    def __init__(self):
        self._id_offset = -1
        self.scenario: Union['Scenario', None] = None
        self.agents: Union[List['AgentGeneric'],
                           Set['AgentGeneric'], None] = None

    def new_id(self):
        """
        Create a new auto-increment ID
        :return:
        """
        self._id_offset += 1
        return self._id_offset

    def all_agent_ids(self) -> List[int]:
        """
        Get id of all agents.
        :return:
        """
        return [agent.id for agent in self.agents]

    def to_list(self, column_names: List[str] = None) -> List[Dict]:
        """
        Convert all agent properties to a list of dict.
        :param column_names:  property names
        :return:
        """

    def get_agent(self, agent_id: int):
        index = binary_search(self.agents, agent_id,
                              key=lambda agent: agent.id)
        if index == -1:
            return None
        else:
            return self.agents[index]


class AgentList(BaseAgentContainer):

    def __init__(self, agent_class: "ClassVar[AgentGeneric]", length: int, model: 'Model') -> None:
        super().__init__()
        self._iter_index = 0
        self.scenario = model.scenario
        self.agent_class: "ClassVar[AgentGeneric]" = agent_class
        self.initial_agent_num: int = length
        self.model = model
        self.agents: List[AgentGeneric] = []

    def __repr__(self):
        return f"<AgentList {self.agents}>"

    def __len__(self):
        return len(self.agents)

    def __getitem__(self, item) -> AgentGeneric:
        return self.agents.__getitem__(item)

    def __iter__(self):
        self._iter_index = 0
        return SeqIter(self.agents)

    def init_agents(self) -> List[AgentGeneric]:
        """
        Initialize all agents in the container, and call the `setup()` method
        :return:
        """
        agents: List['AgentGeneric'] = [self.agent_class(self.new_id()) for i in
                                        range(self.initial_agent_num)]
        scenario = self.model.scenario
        for agent in agents:
            agent.scenario = scenario
            agent.model = self.model
            agent.setup()
        return agents

    def random_sample(self, sample_num: int) -> List['AgentGeneric']:
        """
        Randomly sample `sample_num` agents from the container
        :param sample_num:
        :return:
        """
        return random.sample(self.agents, sample_num)

    def remove(self, agent: 'AgentGeneric'):
        """
        Remove the agent
        :param agent:
        :return:
        """
        for i in range(len(self.agents)):
            a = self.agents[i]
            if a is agent:
                self.agents.pop(i)
                break

    def add(self, agent: 'AgentGeneric' = None, params: Dict = None):
        """
        Add an agent
        :param agent:
        :param params:
        :return:
        """
        new_id = self.new_id()
        if agent is not None:
            assert isinstance(agent, Agent)
        else:
            agent = new(self.agent_class(new_id))

        agent.scenario = self.model.scenario
        agent.model = self.model
        agent.setup()
        if params is not None:
            assert isinstance(params, dict)
            if params.get('id') is not None:
                logger.warning(
                    "Warning, agent 'id' passed together with 'params' will be overridden by a new id "
                    "generated automatically")
            agent.set_params(params)
        agent.id = new_id
        self.agents.append(agent)

    def set_properties(self, props_df: pd.DataFrame):
        """
        Extract properties from a dataframe, and Each row in the dataframe represents the property of an agent.
        :param props_df:
        :return:
        """
        super().set_properties(props_df)
        self.agents.sort(key=lambda agent: agent.id)


__all__ = ['AgentList']
