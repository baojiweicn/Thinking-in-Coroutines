#!/usr/bin/env python
# encoding: utf-8
import ujson
from treelib import Tree, Node

def table_to_dict_list(table):
    keys = table[0]
    return [dict(zip(keys,item)) for item in table[1:]]

def multiple_of_three(data):
    return [item for item in data if item%3==0]

def pick_GlossTerm(data):
    input_json = ujson.loads(data)
    def recursion(input_json):
        if isinstance(input_json,dict):
            for key,value in input_json.items():
                if key != "GlossTerm":
                    res = recursion(value)
                    if res:
                        return res
                else:
                    return value
        else:
            return None
    res = recursion(input_json)
    return res

def sort_and_distinct(data):
    return list(set(data))

def sort_by_amount(data):
    return sorted(data, key=lambda x:x.amount, reverse=True)

def calc(method,x,y):
    dispatch = {
        "multiply": lambda x,y:x*y,
        "divide": lambda x,y:x/y,
        "add": lambda x,y:x+y,
        "subtract": lambda x,y:x-y,
    }
    return dispatch[method](x,y)


def build_tree(data={}, tree=None, parent = None):
    for key, value in data.items():
        child = tree.create_node(key,key,parent = parent.identifier)
        if isinstance(value,dict):
            build_tree(value,tree,child)
    return tree

def find_deepest_child(data):
    tree = Tree()
    root = tree.create_node("root", "root")
    tree = build_tree(data=data, tree=tree, parent=root)
    res = tree.paths_to_leaves()
    depth = tree.depth()
    for path in res:
        if len(path) == depth+1:
            return path[-1]
            break
    # 不严谨, 因为返回有可能是多个child??

def find_nodes_that_contains_more_than_three_children(data):
    res = []
    tree = Tree()
    root = tree.create_node("root", "root")
    tree = build_tree(data=data, tree=tree, parent=root)
    nodes = tree.nodes
    for node in nodes:
        if node != "root" and len(tree.children(node)) >= 3:
            res.append(node)
    return set(res)

def count_of_all_distributions_of_linux(data):
    tree = Tree()
    root = tree.create_node('root','root')
    tree = build_tree(data=data["Linux"], tree=tree, parent=root)
    return tree.size() - 1

class Notice():
    def __init__(self,content):
        self.template = '''<li class="notice">%s</li>'''
        self.content = content

    def render(self):
        return self.template%(self.content)

class Message():
    def __init__(self,userid,content):
        self.template = '''<li class="%s">
    <img class="profile" src="${user_image(%s)}">
    <div class="message-content">%s</div>
</li>'''
        self.content = content
        self.userid = userid
        if userid%2 ==0:
            self.side = "right"
        else:
            self.side = "left"

    def render(self):
        return self.template%(self.side,self.userid,self.content)

def render_messages(messages,current_userid):
    # test polymorphism?? so what's the usage of current_userid??
    res = '\n'.join(map(lambda x:x.render(),messages))

    return res
