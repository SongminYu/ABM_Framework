# -*- coding:utf-8 -*-
# @Time: {{cookiecutter.created_at}}
# @Author: {{cookiecutter.author}}
# @Email: {{cookiecutter.email}}
import random

from Melodie import Environment
from Melodie import get_agent_manager


class _ALIAS_Environment(Environment):
    def setup(self):
        pass

    def step(self):
        for agent in get_agent_manager():
            agent.a += random.randint(0, 100)