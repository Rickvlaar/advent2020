import math


CARD_PUB_KEY = 8458505
DOOR_PUB_KEY = 16050997
TEST_CARD_PUB_KEY = 5764801
TEST_DOOR_PUB_KEY = 17807724


class Cracker:
    def __init__(self, public_key):
        self.subject_number = 7
        self.init_value = 1
        self.loop_size = 0
        self.divider = 20201227
        self.public_key = public_key
        self.encryption_key = 1
        self.cracked_loop_size = None

    def transform(self):
        self.init_value = self.init_value * self.subject_number
        self.init_value = self.init_value % self.divider

    def reset(self):
        self.init_value = 1

    def crack_it(self):
        while True:
            self.loop_size += 1
            self.transform()
            if self.public_key == self.init_value:
                self.cracked_loop_size = self.loop_size
                print('Cracked: ' + str(self.init_value))
                break

    def get_encryption_key(self, cracker):
        self.loop_size = cracker.cracked_loop_size
        for x in range(self.loop_size):
            self.encryption_key = self.encryption_key * self.public_key
            self.encryption_key = self.encryption_key % self.divider


def crack_ware():

    card_cracker = Cracker(CARD_PUB_KEY)
    card_cracker.crack_it()

    door_cracker = Cracker(DOOR_PUB_KEY)
    door_cracker.crack_it()

    card_cracker.get_encryption_key(door_cracker)
    door_cracker.get_encryption_key(card_cracker)

    if card_cracker.encryption_key == door_cracker.encryption_key:
        print('Bingo: ' + str(card_cracker.encryption_key))


crack_ware()
