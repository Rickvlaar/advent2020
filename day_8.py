import util
game_file = 'input_files/day_8.txt'


class GameBoy:
    def __init__(self, file):
        self.accumulator = 0
        self.program_index = 0
        self.instruction_dict = {'nop': self.nop, 'jmp': self.jmp, 'acc': self.acc}
        self.instructions = self.read_instructions(file) if file else None

    def nop(self, value):
        self.program_index += 1

    def jmp(self, value):
        self.program_index += value

    def acc(self, value):
        self.accumulator += value
        self.program_index += 1

    def read_instructions(self, file):
        return [self.Instruction(operation=instruction.split(' ')[0], value=instruction.split(' ')[1]) for instruction in util.parse_file_as_list(file)]

    def run(self):
        while True:
            if self.program_index == len(self.instructions):
                print('program finished! Accumulator at: ' + str(self.accumulator))
                return True

            current_instruction = self.instructions[self.program_index]
            if current_instruction.run_times == 1:
                print('oopsie, infinite loop, better stop! Accumulator at: ' + str(self.accumulator))
                return False

            self.instruction_dict.get(current_instruction.operation)(current_instruction.value)
            current_instruction.run_times += 1

    def fix_my_code(self):
        nop_jmp_indexes = [index for index, instruction in enumerate(self.instructions) if instruction.operation == 'nop' or instruction.operation == 'jmp']
        for instruction_index in nop_jmp_indexes:
            self.instructions[instruction_index].operation = 'nop' if self.instructions[instruction_index].operation == 'jmp' else 'jmp'
            ran_program_succesfully = self.run()
            if ran_program_succesfully:
                return
            else:
                self.reset()

    def reset(self):
        self.instructions = self.read_instructions(game_file)
        self.program_index = 0
        self.accumulator = 0

    class Instruction:
        def __init__(self, operation, value):
            self.operation = operation
            self.value = int(value)
            self.run_times = 0


def run_gameboy():
    gameboy = GameBoy(game_file)
    gameboy.fix_my_code()
