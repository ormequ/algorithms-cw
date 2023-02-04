import sys

import graphviz
import random


class RBTreeNode:
    def __init__(self, color, key=None, value=None, parent=None):
        self.color = color
        self.key = key
        self.value = value
        self.parent = parent
        self.right_child = None
        self.left_child = None

    def __eq__(self, other):
        if isinstance(other, RBTreeNode):
            return self.key == other.key
        return self.key == other

    def __lt__(self, other):
        if isinstance(other, RBTreeNode):
            return self.key < other.key
        return self.key < other

    def __gt__(self, other):
        if isinstance(other, RBTreeNode):
            return self.key > other.key
        return self.key > other

    def __ge__(self, other):
        if isinstance(other, RBTreeNode):
            return self.key >= other.key
        return self.key >= other

    def __le__(self, other):
        if isinstance(other, RBTreeNode):
            return self.key <= other.key
        return self.key <= other

    def __str__(self):
        return f'[Node {self.color} [{self.key}: {self.value}]]'


class RBTree:
    def __init__(self, repeat_keys=False):
        self.repeats = repeat_keys
        self.nil = RBTreeNode('black')
        self.root = self.nil

    def print(self):
        que = [self.root]
        dot = graphviz.Digraph()
        dot.attr('node', fontsize='20')

        def print_node(node, parent_id=''):
            node_id = id(node)
            shape = 'ellipse'
            label = f"{node.key}"
            if node.value is not None:
                label += f": {node.value}"
            if id(node) == id(self.nil):
                shape = 'rectangle'
                node_id += print_node.nils
                print_node.nils += 1
                label = 'nil'
            dot.node(str(node_id), label=label, color=node.color, fontcolor=node.color, shape=shape)
            if parent_id:
                dot.edge(parent_id, str(node_id))

        print_node.nils = 0
        print_node(self.root)

        dot.format = 'png'
        while que:
            tmp_que = []
            for el in que:
                el_id = str(id(el))
                if el.left_child:
                    print_node(el.left_child, el_id)
                    tmp_que.append(el.left_child)
                if el.right_child:
                    print_node(el.right_child, el_id)
                    tmp_que.append(el.right_child)
            que = tmp_que
        dot.render(directory='../../')

    def create_node(self, parent, color, key, value=None):
        node = RBTreeNode(color, key, value, parent)
        node.left_child = self.nil
        node.right_child = self.nil
        if key < parent.key:
            parent.left_child = node
        else:
            parent.right_child = node
        return node

    def insert(self, key, value=None):
        if key is None:
            return
        if id(self.root) == id(self.nil):
            self.root = RBTreeNode('black', key, value)
            self.root.left_child = self.nil
            self.root.right_child = self.nil
            return
        add_node = self.root
        while True:
            parent_node = add_node
            if add_node == key and not self.repeats:
                add_node.value = value
                return
            elif add_node <= key:
                add_node = add_node.right_child
            else:
                add_node = add_node.left_child
            if id(add_node) == id(self.nil):
                add_node = parent_node
                break
        created = self.create_node(add_node, 'red', key, value)

        def check_colors(node):
            parent = node.parent
            if parent is None or parent.color == 'black':
                return
            # Т.к. отец красный, дед всегда существует
            grandparent = parent.parent
            if id(grandparent) != id(self.root):
                grandparent.color = 'red'
            if id(grandparent.left_child) == id(parent):
                uncle = grandparent.right_child
            else:
                uncle = grandparent.left_child
            if uncle.color == 'red':
                """
                       black             red
                      /     \    ->     /   \ 
                    red     red      black  black
                """
                parent.color = 'black'
                uncle.color = 'black'
                # Нужно еще проверить относительно деда
                check_colors(grandparent)
                return
            if (
                    (id(parent.left_child) == id(node) and id(grandparent.left_child) == id(parent)) or
                    (id(parent.right_child) == id(node) and id(grandparent.right_child) == id(parent))
            ):
                # Если родитель с той же стороны от деда, что и ребенок от родителя, то поворачиваем и меняем цвет деда
                self.rotate(parent)
                parent.color = 'black'
                grandparent.color = 'red'
            else:
                self.rotate(node)
                self.rotate(node)
                node.color = 'black'
                grandparent.color = 'red'

        check_colors(created)

    def rotate(self, node):
        if node is None:
            return
        parent = node.parent
        grandparent = parent.parent
        node.parent = grandparent
        parent.parent = node
        if grandparent is not None:
            if id(grandparent.left_child) == id(parent):
                grandparent.left_child = node
            else:
                grandparent.right_child = node
        else:
            # Если деда нет, значит родитель -- корень
            self.root = node

        if id(parent.left_child) == id(node):
            parent.left_child = node.right_child
            parent.left_child.parent = parent
            node.right_child = parent
            # node.right_child.parent = node
        else:
            parent.right_child = node.left_child
            parent.right_child.parent = parent
            node.left_child = parent

    @staticmethod
    def get_uncle(node, parent=None):
        if parent is None:
            parent = node.parent
        if parent is None:
            return None
        if id(parent.left_child) == id(node):
            return parent.right_child
        return parent.left_child

    def erase_node(self, node_del):
        children = (node_del.left_child, node_del.right_child)
        none_children = [child.key is None for child in children]

        def check_colors(node):
            if node.color == 'red':
                # 1. Node - красный, после него идут листья
                return

            # 2. Node - черный
            if id(self.root) == id(node):
                # 2.1. Node - корень
                return

            parent = node.parent
            uncle = self.get_uncle(node, parent)
            if uncle.color == 'red':
                # 2.2.1. Дядя - красный
                """
                Родитель node и дети дяди всегда будут черными, причем дети дяди не будут
                None, так как иначе бы не сходилось по черной высоте до удаления
                """
                uncle.color = 'black'
                parent.color = 'red'
                self.rotate(uncle)
                # Сразу же переходим к случаю черного дяди
                uncle = self.get_uncle(node)
                parent = node.parent
            if uncle.color == 'black':
                # 2.2.2. Дядя - черный
                if id(parent.left_child) == id(uncle):
                    same_pos_child = uncle.left_child
                    another_pos_child = uncle.right_child
                else:
                    same_pos_child = uncle.right_child
                    another_pos_child = uncle.left_child

                def same_pos_black(bro, same_child):
                    bro.color = parent.color
                    parent.color = 'black'
                    same_child.color = 'black'
                    self.rotate(bro)

                if same_pos_child.color == 'red':
                    # 2.2.2.1. Ребенок дяди с его стороны - красный
                    same_pos_black(uncle, same_pos_child)
                elif another_pos_child.color == 'red':
                    # 2.2.2.2. Ребенок дяди со стороны node - красный
                    another_pos_child.color = 'black'
                    uncle.color = 'red'
                    before_sibling = uncle
                    new_sibling = another_pos_child
                    self.rotate(another_pos_child)
                    uncle = new_sibling
                    # Перешли к 2.2.2.1
                    same_pos_black(uncle, before_sibling)
                else:
                    # 2.2.2.3. Оба ребенка дяди - черные
                    uncle.color = 'red'
                    if parent.color == 'red':
                        parent.color = 'black'
                    else:
                        check_colors(parent)

        if all(none_children):
            check_colors(node_del)
            if id(node_del) == id(self.root):
                self.root = self.nil
            elif id(node_del.parent.left_child) == id(node_del):
                node_del.parent.left_child = self.nil
            else:
                node_del.parent.right_child = self.nil

            del node_del
        elif any(none_children):
            # 3. Node имеет только одного ребенка
            child = children[0] if children[0].key is not None else children[1]
            if id(self.root) == id(node_del):
                del node_del
                self.root = child
                child.color = 'black'
                return
            """
            Node всегда будет черным, а child -- красным
            Доказательство:
                Child -- не лист. В таком случае он обязан быть красным, так как в другом поддереве от node 
                количество черных вершин == 1, следовательно, в текущем поддереве количество черных вершин 
                в любой ветви также == 1. Таким образом, child всегда красный, а node всегда черный,
                так как не может идти две красных вершины подряд  
            """
            if id(node_del.parent.left_child) == id(node_del):
                node_del.parent.left_child = child
            else:
                node_del.parent.right_child = child
            child.parent = node_del.parent
            child.color = node_del.color
            del node_del
        else:
            # 4. Node имеет двух детей. Берем минимум в правом поддереве
            child = node_del.right_child
            while id(child.left_child) != id(self.nil):
                child = child.left_child
            # Теперь child -- лист. Нам нужен его родитель
            node_del.key = child.key  # swap
            node_del.value = child.value
            self.erase_node(child)

    def erase(self, key):
        node = self.find(key)
        if node is None:
            return
        self.erase_node(node)

    def find(self, key):
        if key is None:
            return None
        cur_node = self.root
        while cur_node.key is not None:
            if cur_node == key:
                return cur_node
            if cur_node < key:
                cur_node = cur_node.right_child
            elif cur_node > key:
                cur_node = cur_node.left_child
        return None

    def __getitem__(self, key):
        node = self.find(key)
        if node is None:
            return None
        return node.value

    def __setitem__(self, key, value):
        self.insert(key, value)

    def get_size(self):
        res = sys.getsizeof(self.root) + sys.getsizeof(self.nil)
        que = [self.root]
        while que:
            tmp_que = []
            for el in que:
                if el.left_child and id(el.left_child) != id(self.nil):
                    res += sys.getsizeof(el.left_child)
                    tmp_que.append(el.left_child)
                if el.right_child and id(el.right_child) != id(self.nil):
                    res += sys.getsizeof(el.right_child)
                    tmp_que.append(el.right_child)
            que = tmp_que
        return res
