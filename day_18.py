import util
import re

homework = util.parse_file_as_list('input_files/day_18.txt')


def alternate_math():
    prepped_homework = [line.replace('))', ') )') for line in homework]
    return sum([walk_the_line(line.split(' '), 0)[0] for line in prepped_homework])


def walk_the_line(operator_list, total_value, index=0):
    operator = ''
    while index < len(operator_list):
        value = operator_list[index]
        if value.isdigit() and total_value == 0:
            total_value = int(value)
        elif value.isdigit():
            total_value = eval(str(total_value) + operator + value)
        elif value in ('+', '*'):
            operator = value
        elif value.startswith('('):
            operator_list[index] = value[1:]
            sub_total, end_index = walk_the_line(operator_list, 0, index=index)
            operator_list[index + 1: end_index] = [str(sub_total)]
        elif value.endswith(')'):
            if value != ')':
                total_value = eval(str(total_value) + operator + value.strip(')'))
            return total_value, index + 1
        index += 1
    return total_value, index + 1


def forbidden_methods():
    clean_homework = [line.replace(' ', '') for line in homework]
    calculated_homework = []
    for line in clean_homework:
        do_subcalcs = True
        while do_subcalcs:
            found_parenth = re.search('([(][^()][0-9+*]*?[)])', line)
            if found_parenth:
                calculated_parenths = line_calculator(line[found_parenth.start() + 1: found_parenth.end() - 1])
                line = line[:found_parenth.start()] + calculated_parenths + line[found_parenth.end():]
            else:
                do_subcalcs = False
                calculated_homework.append(int(line_calculator(line)))
    return sum(calculated_homework)


def line_calculator(line):
    do_addition = True
    while do_addition:
        plus_sum = re.search('([0-9]+[+][0-9]+)', line)
        if plus_sum:
            line = line[:plus_sum.start()] + str(eval(plus_sum.group(0))) + line[plus_sum.end():]
        else:
            do_addition = False

    do_multiply = True
    while do_multiply:
        prod = re.search('([0-9]+[*][0-9]+)', line)
        if prod:
            line = line[:prod.start()] + str(eval(prod.group(0))) + line[prod.end():]
        else:
            do_multiply = False
    return line
