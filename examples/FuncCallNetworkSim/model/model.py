# -*- coding: utf-8 -*-
__author__ = 'Songmin'

import json
from typing import Dict, List, Tuple

from Melodie import Model, AgentList
from Melodie.network import OldNetwork
from .environment import FuncEnvironment
from examples.FuncCallNetworkSim.model.agent import FuncAgent


class FuncModel(Model):
    def setup(self):
        self.network = OldNetwork()
        self.network.add_category('func')
        with self.define_basic_components():
            self.environment = FuncEnvironment()
        node_names_map: Dict[str, int] = {}
        node_id_to_name_map: Dict[str, int] = {}
        edges_with_num: List[Tuple[int, int]] = []
        with open("./data/json_source/lua_call_graph.json") as f:
            network_json = json.load(f)
            vertices = network_json['series']['data']
            edges = network_json['series']['links']
            node_names = set()
            for link in edges:
                node_names.add(link['source'])
                node_names.add(link['target'])
            for i, node_name in enumerate(node_names):
                node_names_map[node_name] = i
                node_id_to_name_map[i] = node_name
            for edge in edges:
                edges_with_num.append((node_names_map[edge['source']], node_names_map[edge['target']]))
        for e in edges_with_num:
            self.network.add_edge(e[0], e[1])

        with open("./data/json_source/graph-demo-with-layout.json") as f:
            network_json = json.load(f)
            vertices = network_json['series']['data']
            self.visualizer.parse_layout(vertices, lambda vertex: (vertex['id'], (vertex['x'], vertex['y'])))
            self.visualizer.parse_edges(network_json['series']['links'],
                                        lambda edge: ((edge['source'], edge['target']), 1))
        self.agent_list = AgentList(FuncAgent, 652, self)
        for i, agent in enumerate(self.agent_list):
            self.network.add_agent(agent.id, 'func', i)
        self.node_name_map = node_names_map
        self.node_id_to_name_map = node_id_to_name_map

    def run(self):
        agent_manager: 'AgentList' = self.agent_list
        for i, a in enumerate(agent_manager.agents):
            a.id = i

        def f(agent):
            return self.node_id_to_name_map[agent.id], agent.status

        self.visualizer.parse_role(self.agent_list.agents, f)
        v = 0
        self.visualizer.set_plot_data(0, 'chart1', {'series1': v, 'series2': 1 - v})
        self.visualizer.start()

        for t in range(0, self.scenario.periods):
            self.environment.step(agent_manager, self.network)
            v = self.environment.get_agents_statistic(self.agent_list)
            self.visualizer.set_plot_data(t, 'chart1', {'series1': v, 'series2': 1 - v})

            self.visualizer.parse_role(self.agent_list.agents, f)
            self.visualizer.step(t)

        self.visualizer.finish()
        self.environment.get_agents_statistic(agent_manager)
