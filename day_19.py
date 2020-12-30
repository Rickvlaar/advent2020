import util
import itertools

test_rules = ['0: 4 1 5',
              '1: 2 3 | 3 2',
              '2: 4 4 | 5 5',
              '3: 4 5 | 5 4',
              '4: "a"',
              '5: "b"',
              '',
              'ababbb',
              'bababa',
              'abbbab',
              'aaabbb',
              'aaaabbb']

the_rules = util.parse_file_as_list('input_files/day_19.txt')


class Node:
    def __init__(self, left=None, right=None):
        self.left = left
        self.right = right
        self.value = None
        self.parent = None
        self.str_list = []
        self.end_nodes = []

    def __repr__(self):
        return 'Node value: ' + str(self.value)

    def add_child(self, value=None, go_right=False):
        child = Node()
        child.parent = self
        child.value = value

        if go_right:
            if self.right is None:
                self.right = child
            else:
                child = self.right.add_child(value)
        else:
            if self.left is None:
                self.left = child
            else:
                child = self.left.add_child(value)
        return child

    def traverse_tree(self, node=None):
        self.end_nodes.clear()
        if not node:
            node = self

        if self.value:
            if self.parent:
                self.str_list = self.parent.str_list.copy()
            if self.value.isalpha():
                self.str_list.append(self.value)

        if self.left:
            self.left.traverse_tree(node)
        else:
            node.end_nodes.append(self)

        if self.right:
            self.right.traverse_tree(node)


def build_rules(start_rule_no='0', part_2=False):
    rules_dict = {rule.split(':')[0]: rule.split(':')[1][1:].replace('"', '').split(' ') for rule in the_rules if
                  ':' in rule}
    values_set = set([rule for rule in the_rules if ':' not in rule])

    if part_2:
        rules_dict['8'] = ['42', '|', '42', '8']
        rules_dict['11'] = ['42', '31', '|', '42', '11', '31']

    root = Node()
    rule_check(start_rule_no, rules_dict, root)
    root.end_nodes.clear()
    root.traverse_tree()
    allcombos = set()
    print(len(root.end_nodes))
    for node in root.end_nodes:
        allcombos.add(''.join(node.str_list))
    allcombos.intersection_update(values_set)
    return allcombos


def rule_check(rule_no, rules_dict, node):
    rule_list = rules_dict.get(rule_no)

    if rule_list[0] in ('a', 'b'):
        node.add_child(value=rule_list[0])
    else:
        split_index = len(rule_list)
        if '|' in rule_list:
            split_index = rule_list.index('|')

        sister_node = None
        for index, rule in enumerate(rule_list[:split_index]):
            if index > 0:
                sister_node.traverse_tree()
                for end_node in sister_node.end_nodes:
                    rule_check(rule, rules_dict, end_node.add_child(value=rule))
            else:
                rule_check(rule, rules_dict, node.add_child(value=rule))
                sister_node = node.left

        if '|' in rule_list:
            for index, rule in enumerate(rule_list[split_index + 1:]):
                if index > 0:
                    sister_node.traverse_tree()
                    for end_node in sister_node.end_nodes:
                        rule_check(rule, rules_dict, end_node.add_child(value=rule))
                else:
                    rule_check(rule, rules_dict, node.add_child(value=rule, go_right=True))
                    sister_node = node.right
