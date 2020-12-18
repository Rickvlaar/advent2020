import util
import math

validation_rules = '''departure location: 41-598 or 605-974
departure station: 30-617 or 625-957
departure platform: 29-914 or 931-960
departure track: 39-734 or 756-972
departure date: 37-894 or 915-956
departure time: 48-54 or 70-955
arrival location: 39-469 or 491-955
arrival station: 47-269 or 282-949
arrival platform: 26-500 or 521-960
arrival track: 26-681 or 703-953
class: 49-293 or 318-956
duration: 25-861 or 873-973
price: 30-446 or 465-958
route: 50-525 or 551-973
row: 39-129 or 141-972
seat: 37-566 or 573-953
train: 43-330 or 356-969
type: 32-770 or 792-955
wagon: 47-435 or 446-961
zone: 30-155 or 179-957
'''

nearby_tickets = util.parse_file_as_list('input_files/day_16.txt')
your_ticket = ['71', '127', '181', '179', '113', '109', '79', '151', '97', '107', '53', '193', '73', '83', '191', '101', '89', '149', '103', '197']


def get_rules():
    validation_dict = {}
    for rule in validation_rules.splitlines():
        rule_name, values = rule.split(':')
        range_values = [number.strip() for value in values.split(' or ') for number in value.split('-')]
        validation_code_string = 'x in range({0}, {1} + 1) or x in range({2}, {3} + 1)'.format(*range_values)
        validation_dict[rule_name] = validation_code_string
    return validation_dict


def is_valid_for_1_rule(ticket_value, the_rules):
    return any([True for name, rule in the_rules.items() if eval(rule.replace('x', ticket_value))])


def get_nearby_tickets_error_rate():
    the_rules = get_rules()
    return sum([int(value) for ticket in nearby_tickets for value in ticket.split(',') if not is_valid_for_1_rule(value, the_rules)])


def what_my_ticket_say():
    the_rules = get_rules()

    clean_ticketlist = [ticket.split(',') for ticket in nearby_tickets if all([is_valid_for_1_rule(value, the_rules) for value in ticket.split(',')])]

    index_meaning_dict = {index: set(value for value in the_rules.keys()) for index, value in enumerate(the_rules.keys())}
    for ticket in clean_ticketlist:
        for index, value in enumerate(ticket):
            for rule_name, rule in the_rules.items():
                if not eval(rule.replace('x', value)):
                    index_meaning_dict[index].discard(rule_name)

    set_values = set()
    for meaning_set in sorted(index_meaning_dict.values()):
        meaning_set.difference_update(set_values)
        for index, meaning in index_meaning_dict.items():
            if len(meaning) > 1:
                index_meaning_dict[index].difference_update(meaning_set)
        set_values.update(meaning_set)

    return math.prod([int(your_ticket[index]) for index, meaning in index_meaning_dict.items() if 'departure' in list(meaning)[0]])
