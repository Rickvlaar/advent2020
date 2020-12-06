declarations_file = 'input_files/day_6.txt'


def part_1():
    declarations = [line.replace('\n', '') for line in open(file=declarations_file).read().split('\n\n')]
    return sum([len(set(declaration)) for declaration in declarations])


def part_2():
    declarations = [[set(declaration) for declaration in line.split('\n') if declaration] for line in open(file=declarations_file).read().split('\n\n')]
    return sum([len(set.intersection(*declaration)) for declaration in declarations])
