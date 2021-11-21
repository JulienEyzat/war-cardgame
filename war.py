import random

def init_game(nb_colors, nb_values):
    cards = []
    nb_cards = nb_colors * nb_values
    middle_card = int(nb_cards/2)

    for i in range(nb_colors):
        for j in range(nb_values):
            cards.append((i, j))

    cards = random.sample(cards, nb_cards)

    player1_cards = cards[:middle_card]
    player2_cards = cards[middle_card:]

    return player1_cards, player2_cards

def battle_cards_get_algo(battle_cards, battle_cards_get_algo_type):
    if battle_cards_get_algo_type == "nothing":
        pass
    if battle_cards_get_algo_type == "random":
        battle_cards = random.sample(battle_cards, len(battle_cards))
    elif battle_cards_get_algo_type == "reverse":
        battle_cards = list(reversed(battle_cards))
    return battle_cards

def unpile(player1_cards, player2_cards, battle_cards):
    if player1_cards and player2_cards:
        player1_card = player1_cards.pop(0)
        player2_card = player2_cards.pop(0)
    elif len(player1_cards) >= 2 and not player2_cards:
        player1_card = player1_cards.pop(0)
        player2_card = player1_cards.pop(0)
    elif not player1_cards and len(player2_cards) >= 2:
        player1_card = player2_cards.pop(0)
        player2_card = player2_cards.pop(0)
    else:
        player1_card = None
        player2_card = None
    battle_cards.append(player1_card)
    battle_cards.append(player2_card)
    return player1_cards, player2_cards, battle_cards, player1_card, player2_card

def battle(player1_cards, player2_cards, battle_cards, battle_cards_get_algo_type):
    player1_cards, player2_cards, battle_cards, player1_card, player2_card = unpile(player1_cards, player2_cards, battle_cards)
    if player1_card is None:
        # Equality case
        return [], []
    elif player1_card[1] != player2_card[1]:
        # End of battle case
        battle_cards = battle_cards_get_algo(battle_cards, battle_cards_get_algo_type)
        if player1_card[1] > player2_card[1]:
            player1_cards+=battle_cards
        else:
            player2_cards+=battle_cards
        return player1_cards, player2_cards
    else:
        # War case
        player1_cards, player2_cards, battle_cards, player1_card, player2_card = unpile(player1_cards, player2_cards, battle_cards)
        return battle(player1_cards, player2_cards, battle_cards, battle_cards_get_algo_type)

def end_game(player1_cards, player2_cards):
    if not player1_cards and not player2_cards:
        return True, "Equality"
    if not player1_cards:
        return True, "2 wins"
    elif not player2_cards:
        return True, "1 wins"
    else:
        return False, None

def play_game(nb_colors, nb_values, battle_cards_get_algo_type, print_ending=True):
    player1_cards, player2_cards = init_game(nb_colors, nb_values)
    is_over = False
    nb_tours = 0
    cycle_size = 0
    before_cycle_size = 0
    all_states = []
    # all_true_states = []
    while not is_over:
        # Play
        player1_cards, player2_cards = battle(player1_cards, player2_cards, [], battle_cards_get_algo_type)
        is_over, ending_type = end_game(player1_cards, player2_cards)

        # Check cycle
        current_state = hash(str(player1_cards + player2_cards) + str(len(player1_cards)))
        if current_state in all_states:
            cycle_size = len(all_states) - all_states.index(current_state)
            before_cycle_size = all_states.index(current_state)
            # print(len(player1_cards), len(player2_cards))
            is_over = True
            ending_type = "Cycle"
        all_states.append(current_state)
        # all_true_states.append((player1_cards.copy(), player2_cards.copy()))
        
        # Number of tours
        nb_tours+=1

    if print_ending:
        print("Ending : %s" %(ending_type))

    return ending_type, nb_tours, cycle_size, before_cycle_size