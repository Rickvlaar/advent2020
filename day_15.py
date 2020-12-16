puzzle_input = [1, 0, 15, 2, 10, 13]


def numbers_game(final_turn=2020):
    times_spoken = {num: 1 for num in puzzle_input}
    last_spoken = {num: turn + 1 for turn, num in enumerate(puzzle_input)}
    last_spoken_number = 0
    for turn in range(len(puzzle_input) + 1, final_turn):
        if last_spoken_number in times_spoken.keys() and times_spoken[last_spoken_number] > 0:
            new_last_spoken = turn - last_spoken.get(last_spoken_number)
            times_spoken[last_spoken_number] += 1
            last_spoken[last_spoken_number] = turn
            last_spoken_number = new_last_spoken
        else:
            times_spoken[last_spoken_number] = 1
            last_spoken[last_spoken_number] = turn
            last_spoken_number = 0
    return last_spoken_number
