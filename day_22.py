import util

decks = 'input_files/day_22.txt'


def battle():
    parsed_file = util.parse_file_as_list(decks)

    player_1_deck = [int(value) for value in parsed_file[1:26]]
    player_2_deck = [int(value) for value in parsed_file[28:]]

    winner = play_recursive_game(player_1_deck, player_2_deck)
    score = 0
    if winner == 1:
        score = calculate_score(player_1_deck)
    elif winner == 2:
        score = calculate_score(player_2_deck)
    return score


def play_recursive_game(player_1_deck, player_2_deck):
    played_rounds_log = set()

    while True:
        this_round_log = str(player_1_deck) + str(player_2_deck)
        if this_round_log in played_rounds_log:
            print(this_round_log)
            return 1
        played_rounds_log.add(this_round_log)

        player_1_card = player_1_deck.pop(0)
        player_2_card = player_2_deck.pop(0)

        # Start sub-game if both decks allow
        winner = None
        if player_1_card <= len(player_1_deck) and player_2_card <= len(player_2_deck):
            player_1_sub_deck = [card for card in player_1_deck[:player_1_card]]
            player_2_sub_deck = [card for card in player_2_deck[:player_2_card]]
            winner = play_recursive_game(player_1_sub_deck, player_2_sub_deck)
        # Otherwise determine a winner normally
        else:
            winner = 1 if player_1_card > player_2_card else 2

        # Extend deck of winner
        played_cards = [player_1_card, player_2_card] if winner == 1 else [player_2_card, player_1_card]
        if winner == 1:
            player_1_deck.extend(played_cards)
        elif winner == 2:
            player_2_deck.extend(played_cards)

        # 1 if player one  wins, 2 if player two wins
        if len(player_1_deck) == 0 or len(player_2_deck) == 0:
            return 1 if len(player_1_deck) > len(player_2_deck) else 2


def play_normal_game(player_1_deck, player_2_deck):
    game_round = 0
    while True:
        game_round += 1
        player_1_card = player_1_deck.pop(0)
        player_2_card = player_2_deck.pop(0)

        played_cards = [player_1_card, player_2_card]
        played_cards.sort(reverse=True)
        if player_1_card > player_2_card:
            player_1_deck.extend(played_cards)
        else:
            player_2_deck.extend(played_cards)

        if len(player_1_deck) == 0 or len(player_2_deck) == 0:
            break
    return player_1_deck if len(player_1_deck) > len(player_2_deck) else player_2_deck


def calculate_score(winning_deck):
    print(winning_deck)
    winning_deck.reverse()
    score = 0
    for multiplier, card in enumerate(winning_deck):
        score += (multiplier + 1) * card
    return score


print(battle())
