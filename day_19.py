test_rules = ['0: 4 1 5',
              '1: 2 3 | 3 2',
              '2: 4 4 | 5 5',
              '3: 4 5 | 5 4',
              '4: "a"',
              '5: "b"']

test_messages = ['ababbb',
                 'bababa',
                 'abbbab',
                 'aaabbb',
                 'aaaabbb']


def build_rules(start_rule_no=0):
    rules_dict = {rule.split(':')[0]: rule.split(':')[1].strip().split(' ') for rule in test_rules}

    rule = rules_dict.get(start_rule_no)
    return rules_dict