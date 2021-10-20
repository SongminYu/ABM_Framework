# -*- coding:utf-8 -*-
# @Time: 2021/10/19 19:11
# @Author: Zhanyi Hou
# @Email: 1295752786@qq.com
# @File: ast_parse.py

import ast
import logging

import sys
from typing import List, Any, Dict, TypeVar

import astunparse
from pprintast import pprintast

from Melodie import Agent, AgentManager
from Melodie.management.ast_parse import find_class_defs, find_class_methods
import numpy as np

logging.basicConfig(level=logging.WARNING, stream=sys.stderr)
logger = logging.getLogger(__name__)


class RewriteName(ast.NodeTransformer):
    def __init__(self, root_name: str, initial_types: Dict[str, TypeVar]):
        super().__init__()
        self.root_name = root_name

        self.types_inferred: Dict[str, TypeVar] = initial_types.copy()

    def visit_Name(self, node: ast.Name):
        if node.id == 'self':
            node.id = self.root_name
        return node


class TypeInferr(ast.NodeVisitor):
    def __init__(self, initial_types: Dict[str, TypeVar]):
        self.types_inferred: Dict[str, TypeVar] = initial_types.copy()

    def visit_AnnAssign(self, node: ast.AnnAssign) -> Any:
        target = node.target
        assert isinstance(target, ast.Name), "Assert could only be to a single variable"
        if isinstance(node.value, ast.Constant):
            if node.value.value is None:
                assert isinstance(node.annotation, ast.Constant)
                self.types_inferred[target.id] = eval(node.annotation.value)
                # raise NotImplementedError
            else:
                self.types_inferred[target.id] = type(node.value.value)
        else:
            logger.warning(f"skipping annassign {ast.dump(node)}")
            assert isinstance(node.annotation, ast.Constant)
            annotated_type = eval(node.annotation.value)
            if target.id in self.types_inferred:
                inferred_type = self.types_inferred[target.id]
                assert issubclass(annotated_type, inferred_type)
            else:
                self.types_inferred[target.id] = annotated_type

    def visit_Assign(self, node: ast.Assign) -> Any:
        assert len(node.targets) == 1
        target = node.targets[0]
        if isinstance(target, ast.Name):
            if isinstance(node.value, ast.Constant):
                if node.value is None:
                    raise NotImplementedError
                    pass
                else:
                    self.types_inferred[target.id] = type(node.value.value)
            elif isinstance(node.value, ast.Name):
                assert node.value.id in self.types_inferred, node.value.id
                self.types_inferred[target.id] = self.types_inferred[node.value.id]
            elif isinstance(node.value, ast.Call):
                func = node.value.func
                if isinstance(func, ast.Name):
                    func_name = func.id
                    if func_name in {'len', 'sum'}:
                        self.types_inferred[target.id] = int
                    else:
                        raise NotImplementedError(func_name)
                elif isinstance(func, ast.Attribute):
                    logger.warning('found assignment in a special way')
                    return
                else:
                    raise NotImplementedError(ast.dump(node.value))
            elif isinstance(node.value, ast.BinOp):
                self.types_inferred[target.id] = np.float
                logger.warning(f'Found binop at {ast.dump(node.value)}. Assigning the left value to np.float')
                return
            else:
                self.types_inferred[target.id] = int
                logger.warning(f'ignored {ast.dump(node.value)}')
        elif isinstance(target, ast.Tuple):
            names = target.elts
            for name in names:
                if name.id not in self.types_inferred:
                    raise TypeError(f'Vars in Tuple assigning should be annotated declared '
                                    f'before.')
            return
        elif isinstance(target, ast.Attribute):
            logger.warning(f'Skipping the assigning to attribute {ast.dump(target)}')
            return
        elif isinstance(target, ast.Subscript):
            logger.warning(f'Skipping the assigning to subscript {ast.dump(target)}')
            return
        else:

            raise NotImplementedError(ast.dump(target))

    def visit_For(self, node: ast.For) -> Any:
        self._visit_For(node)
        # self.visit(node.iter)
        for child in node.body:
            self.visit(child)

    def _visit_For(self, node: ast.For) -> Any:

        assert isinstance(node.target, ast.Name), "当前只支持ast.Name型作为for循环的迭代变量"
        if isinstance(node.iter, ast.Name):  # "当前只支持ast.Name型作为for循环的迭代变量"
            if node.iter.id in self.types_inferred:
                if issubclass(self.types_inferred[node.iter.id], AgentManager):
                    self.types_inferred[node.target.id] = Agent
                    return
                elif issubclass(self.types_inferred[node.iter.id], np.ndarray):
                    self.types_inferred[node.target.id] = np.ndarray
                    return
                else:
                    raise NotImplementedError
            else:
                raise TypeError(f"node.iter was {ast.dump(node.iter)}, which has not been type-inferred.")
        elif isinstance(node.iter, ast.Call):
            func_name = node.iter.func.id
            if func_name == 'range':
                self.types_inferred[node.target.id] = int
                return
            else:

                raise NotImplementedError(ast.dump(node))
        else:
            raise ValueError(ast.dump(node))
        # pprintast(node)/
        raise NotImplementedError(ast.dump(node))
        # return node


class RewriteCallEnv(ast.NodeTransformer):
    def __init__(self, root_name: str, initial_types: Dict[str, TypeVar]):
        super().__init__()
        self.root_name = root_name

        self.types_inferred: Dict[str, TypeVar] = initial_types.copy()

    # def visit_For(self, node: ast.For) -> Any:
    #
    #     self.visit(node.iter)
    #     return node

    def visit_Attribute(self, node: ast.Attribute) -> ast.Name:
        print(ast.dump(node))
        attribute_name = node.attr
        if isinstance(node.value, ast.Name):
            if node.value.id.startswith('___'):
                subs = ast.Subscript(value=node.value,
                                     slice=ast.Index(value=ast.Constant(value=attribute_name, kind=None)))
                return subs
            elif node.value.id in self.types_inferred:
                subs = ast.Subscript(value=node.value,
                                     slice=ast.Index(value=ast.Constant(value=attribute_name, kind=None)))
                return subs
            else:
                logger.warning(f"{ast.dump(node)}")
                return node
        return node

    def visit_Call(self, node: ast.Call) -> Any:
        if isinstance(node.func, ast.Attribute):
            attr: ast.Attribute = node.func
            while isinstance(attr.value, ast.Attribute):
                attr = attr.value
            assert isinstance(attr.value, ast.Name)
            if attr.value.id == self.root_name:
                name = ast.Name(id=self.root_name + "___" + attr.attr)
                node.func = name
                node.args.insert(0, ast.Name(id=self.root_name))
                return node
            elif attr.value.id in self.types_inferred:  # 如果调用的是agent的方法，则传入的第一个参数为agent
                type_var = self.types_inferred[attr.value.id]
                if issubclass(type_var, Agent):
                    node.func = ast.Name(id='___agent___' + attr.attr, )
                    node.args.insert(0, ast.Name(id=attr.value.id))
                    return node
                elif issubclass(type_var, AgentManager):
                    node.func = ast.Name(id='___agent___manager___' + attr.attr)
                    node.args.insert(0, ast.Name(id=attr.value.id))
                    return node
                else:
                    raise TypeError(ast.dump(node.func))
            else:
                logger.warning(f"Skipping the unrecognized function:{ast.dump(attr)}")
                return node
        logger.warning(f"Skipping unexpected function:{node}")
        return node


class RewriteCallModel(ast.NodeTransformer):
    def __init__(self, root_name: str, initial_types: Dict[str, TypeVar]):
        super().__init__()
        self.root_name = root_name

        self.types_inferred: Dict[str, TypeVar] = initial_types.copy()
        self.sub_components = {'environment', 'agent_manager'}

    # def visit_For(self, node: ast.For) -> Any:
    #
    #     for expr in node.body:
    #         self.visit(expr)
    #     return node

    def visit_Attribute(self, node: ast.Attribute) -> ast.Name:
        print(ast.dump(node))
        attr: ast.Attribute = node
        attr_name_chain = [attr.attr]  # 名称链。意思是从右向左搜索方法的名称
        while isinstance(attr.value, ast.Attribute):
            attr = attr.value
            attr_name_chain.append(attr.attr)
        # print(attr_name_chain)
        assert isinstance(attr.value, ast.Name)
        if attr.value.id.startswith(self.root_name):
            # print(attr.value.id)
            pass
            # raise NotImplementedError
        node.value = self.visit(node.value)
        return node
        # print(ast.dump(node))
        # attribute_name = node.attr
        # if isinstance(node.value, ast.Name):
        #     if node.value.id.startswith('___'):
        #         subs = ast.Subscript(value=node.value,
        #                              slice=ast.Index(value=ast.Constant(value=attribute_name, kind=None)))
        #         return subs
        #     elif node.value.id in self.types_inferred:
        #         subs = ast.Subscript(value=node.value,
        #                              slice=ast.Index(value=ast.Constant(value=attribute_name, kind=None)))
        #         return subs
        #     else:
        #         logger.warning(f"{ast.dump(node)}")
        #         return node
        # else:
        #     raise NotImplementedError
        # return node

    def visit_Call(self, node: ast.Call) -> Any:
        # print(ast.dump(node))
        if isinstance(node.func, ast.Attribute):
            attr: ast.Attribute = node.func
            attr_name_chain = [attr.attr]  # 名称链。意思是从右向左搜索方法的名称
            while isinstance(attr.value, ast.Attribute):
                attr = attr.value
                attr_name_chain.append(attr.attr)
            print(attr_name_chain)
            assert isinstance(attr.value, ast.Name)
            if attr.value.id == self.root_name:
                if attr_name_chain[-1] in self.sub_components:  # 调用了agent_manager或者environment等
                    name = ast.Name(id=f"___{attr_name_chain[-1]}___" + attr_name_chain[0])
                    node.func = name
                    # return node
                    node.args.insert(0, ast.Name(id="___model." + attr_name_chain[-1]))
                    # raise NotImplementedError
                else:
                    raise NotImplementedError
            else:
                raise NotImplementedError
            # if attr.value.id == self.root_name:
            #     name = ast.Name(id=self.root_name + "___" + attr.attr)
            #     node.func = name
            #     node.args.insert(0, ast.Name(id=self.root_name))
            #     return node
            # elif attr.value.id in self.types_inferred:  # 如果调用的是agent的方法，则传入的第一个参数为agent
            #     type_var = self.types_inferred[attr.value.id]
            #     if issubclass(type_var, Agent):
            #         node.func = ast.Name(id='___agent___' + attr.attr, )
            #         node.args.insert(0, ast.Name(id=attr.value.id))
            #         return node
            #     elif issubclass(type_var, AgentManager):
            #         node.func = ast.Name(id='___agent___manager___' + attr.attr)
            #         node.args.insert(0, ast.Name(id=attr.value.id))
            #         return node
            #     else:
            #         raise TypeError(ast.dump(node.func))
            # else:
            #     logger.warning(f"Skipping the unrecognized function:{ast.dump(attr)}")
            #     return node
        logger.warning(f"Skipping unexpected function:{ast.dump(node)}")

        node.func = self.visit(node.func)
        args = node.args
        new_args = []
        for i, arg in enumerate(args):
            new_args.append(self.visit(arg))
        node.args = new_args
        return node


def get_all_self_attrs(method_ast) -> List[str]:
    attr_names = []
    for node in ast.walk(method_ast):
        if isinstance(node, ast.Name):
            if node.id.startswith('___'):
                attr_names.append(node.id)
    return attr_names


class GINIAgent(Agent):
    pass


prefix = """
import random
import numpy as np
from Melodie.boost.compiler.boostlib import ___agent___manager___random_sample
import numba

"""


def modify_ast_environment(method: ast.FunctionDef, root_name: str):
    annotations = {}
    for i, arg in enumerate(method.args.args):

        annotations[arg.arg] = arg.annotation
        if i > 0:
            assert arg.annotation is not None
            annotations[arg.arg] = eval(arg.annotation.value)

    RewriteName(root_name, {}).visit(method)

    ti = TypeInferr(annotations)
    ti.visit(method)

    print('types inferred:', ti.types_inferred)
    pprintast(method)
    rce = RewriteCallEnv(root_name, ti.types_inferred)
    rce.visit(method)
    method.args.args[0].arg = root_name
    method.name = root_name + '___' + method.name

    print('+++++++++++++++++++++++++++++++++')
    # print(pprintast(method))
    r = astunparse.unparse(method)

    r = '@numba.jit\n' + r.lstrip() + "\n\n"
    return r


def modify_ast_model(method, root_name):
    annotations = {}
    for i, arg in enumerate(method.args.args):

        annotations[arg.arg] = arg.annotation
        if i > 0:
            assert arg.annotation is not None
            annotations[arg.arg] = eval(arg.annotation.value)

    RewriteName(root_name, {}).visit(method)

    ti = TypeInferr(annotations)
    ti.visit(method)

    print('types inferred:', ti.types_inferred)
    pprintast(method)
    rce = RewriteCallModel(root_name, ti.types_inferred)
    rce.visit(method)
    method.args.args[0].arg = root_name
    method.name = root_name + '___' + method.name

    # method.args.args = [
    #     ast.arg(arg='___scenario', annotation=None),
    #     ast.arg(arg='___environment', annotation=None),
    #     ast.arg(arg='___agent_manager', annotation=None)
    # ]  # .args.insert(0, ast.Name(id="___" + attr_name_chain[-1]))

    print('+++++++++++++++++++++++++++++++++')
    # print(pprintast(method))
    r = astunparse.unparse(method)

    # r = '@numba.jit\n' + r.lstrip() + "\n\n"
    return r


def conv(input: str, output: str):
    with open(input) as f:
        tree = ast.parse(f.read())
    agent_class, env_class, model_class = find_class_defs(tree)
    f = open(output, 'w')
    f.write(prefix)
    for method in find_class_methods(agent_class):
        if method.name != 'setup':
            code = modify_ast_environment(method, '___agent')
            f.write(code)

    for method in find_class_methods(env_class):
        if method.name != 'setup':  # and method.name == 'go_money_transfer':
            code = modify_ast_environment(method, '___environment')
            print(code)
            f.write(code)

    for method in find_class_methods(model_class):
        if method.name != 'setup':  # and method.name == 'go_money_transfer':
            code = modify_ast_model(method, '___model')
            print(code)
            f.write(code)

    f.close()


conv('src/ast_demo.py', 'out.py')