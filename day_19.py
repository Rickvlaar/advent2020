import util
import re

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

twest_rules = util.parse_file_as_list('input_files/day_19_part_2.txt')

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


def build_rules(start_rule_no='0'):
    rules_dict = {rule.split(':')[0]: rule.split(':')[1][1:].replace('"', '').split(' ') for rule in the_rules if
                  ':' in rule}
    values_set = set([rule for rule in the_rules if ':' not in rule])

    root = Node()
    rule_check(start_rule_no, rules_dict, root)
    root.traverse_tree()
    allcombos = set()

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


def build_rules_2(start_rule_no='0', part_2=False):

    rules_dict = {rule.split(':')[0]: rule.split(':')[1][1:].replace('"', '') for rule in the_rules if
                  ':' in rule}
    values_set = set([rule for rule in the_rules if ':' not in rule])

    if part_2:
        rules_dict['8'] = '42 | 42 8'
        rules_dict['11'] = '42 31 | 42 11 31'
        # 8 = 42 42 42 42 infinite
        # 11 = 42 31 or 42 42 42 31 31 31 infinite expanding outwards
        # start rule = 8 AND 11
        # minimaal 2* 42, geen max, minimaal 1*31 en minimaal x*31 en x+1*42
        fodytwo = (regexp_solution('42', rules_dict)).replace(' ', '')
        dirtyone = (regexp_solution('31', rules_dict)).replace(' ', '')

        matching_rules = set()
        regexp = '\\b' + fodytwo + fodytwo + dirtyone + '\\b'
        for value in values_set:
            if re.search(regexp, value):
                matching_rules.add(value)
            else:
                for x in range(1, 10):
                    regexp = '\\b' + x * fodytwo + fodytwo + dirtyone + '\\b'
                    if re.search(regexp, value):
                        matching_rules.add(value)
                        break
                    for y in range(1, 10):
                        regexp = '\\b' + y * fodytwo + x * fodytwo + x * dirtyone + '\\b'
                        if re.search(regexp, value):
                            matching_rules.add(value)
                            break
        return matching_rules, regexp
    else:
        regexp = '\\b' + (regexp_solution(start_rule_no, rules_dict)).replace(' ', '') + '\\b'

        matching_rules = set()
        for value in values_set:
            if re.search(regexp, value):
                matching_rules.add(value)
        return matching_rules, regexp


def regexp_solution(rule_no, rules_dict):
    rule = rules_dict.get(rule_no)
    rule = rule.split(' ')

    new_rule = ''
    for index, char in enumerate(rule):
        if char.isdigit():
            new_rule += regexp_solution(char, rules_dict)
        else:
            new_rule += char
        if index != len(rule) - 1:
            new_rule += ' '
    if '|' in rule:
        new_rule = '(' + new_rule + ')'
    return new_rule

