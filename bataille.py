from collections import Counter
import matplotlib.pyplot as plt
import random
import tqdm

nb_values = 14
nb_colors = 4
nb_games = 100
randomize_pli = False
reverse_pli = False

nb_cards = nb_colors * nb_values

def init_game():
    cards = []

    middle_card = int(nb_cards/2)

    for i in range(nb_colors):
        for j in range(nb_values):
            cards.append((i, j))

    cards = random.sample(cards, nb_cards)

    player1_cards = cards[:middle_card]
    player2_cards = cards[middle_card:]

    return player1_cards, player2_cards

def unpile(player1_cards, player2_cards, pli):
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
    pli.append(player1_card)
    pli.append(player2_card)
    return player1_cards, player2_cards, pli, player1_card, player2_card

def bataille(player1_cards, player2_cards, pli):
    player1_cards, player2_cards, pli, player1_card, player2_card = unpile(player1_cards, player2_cards, pli)
    if player1_card is None:
        return [], []
    elif player1_card[1] != player2_card[1]:
        if randomize_pli:
            pli = random.sample(pli, len(pli))
        elif reverse_pli:
            pli = list(reversed(pli))
        if player1_card[1] > player2_card[1]:
            player1_cards+=pli
        else:
            player2_cards+=pli
        return player1_cards, player2_cards
    else:
        player1_cards, player2_cards, pli, player1_card, player2_card = unpile(player1_cards, player2_cards, pli)
        return bataille(player1_cards, player2_cards, pli)

def end_game(player1_cards, player2_cards, do_print):
    if not player1_cards and not player2_cards:
        if do_print:
            print("Equality")
        return True, "Equality"
    if not player1_cards:
        if do_print:
            print("Player 2 wins")
        return True, "2 wins"
    elif not player2_cards:
        if do_print:
            print("Player 1 wins")
        return True, "1 wins"
    else:
        return False, None


def play_game(do_print=True):
    player1_cards, player2_cards = init_game()
    is_over = False
    nb_tours = 0
    cycle_size = 0
    before_cycle_size = 0
    all_states = []
    # all_true_states = []
    while not is_over:
        # Play
        player1_cards, player2_cards = bataille(player1_cards, player2_cards, [])
        is_over, ending_type = end_game(player1_cards, player2_cards, do_print)

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
    return ending_type, nb_tours, cycle_size, before_cycle_size

def play_multiple_games(nb_games):
    all_endings = []
    all_nb_tours = []
    all_cycle_sizes = []
    all_before_cycle_size = []
    for i in tqdm.tqdm(range(nb_games)):
        ending_type, nb_tours, cycle_size, before_cycle_size = play_game(do_print=False)
        all_endings.append(ending_type)
        if cycle_size == 0:
            all_nb_tours.append(nb_tours)
        else:
            all_cycle_sizes.append(cycle_size)
            all_before_cycle_size.append(before_cycle_size)

    return all_endings, all_nb_tours, all_cycle_sizes, all_before_cycle_size

# Play
all_endings, all_nb_tours, all_cycle_sizes, all_before_cycle_size = play_multiple_games(nb_games)

# Endings
sorted_all_endings = sorted(all_endings)
endings_counter = Counter(sorted_all_endings)
print("=== Endings ===")
for key in endings_counter:
    proportion_endings = endings_counter[key]/len(all_endings)*100
    print("%s : %s%%" %(key, proportion_endings))

# Nb tours
print("=== Number of turns ===")
print("Number of finite games : %s" %(len(all_nb_tours)))
# print("Number of plays in each finite games : %s" %(all_nb_tours))
# plt.hist(all_nb_tours, bins=100)
# plt.show()

# Link between the two
print("=== Finite games ===")
proportion_finite_games = len(all_nb_tours)/nb_games*100
print("Proportion of finite games in all games : %.2f%%" %(proportion_finite_games))

# Cycles
print("=== Cycles ===")
# print("Size of cycles in cycle games : %s" %(all_cycle_sizes))
print("Number of cycle games : %s" %(len(all_cycle_sizes)))
# print("Number of plays before the cycle begins : %s" %(all_before_cycle_size))

sorted_all_cycle_sizes = sorted(all_cycle_sizes)
counter = Counter(sorted_all_cycle_sizes)
print("Proportion of each size of cycle")
for key in counter:
    proportion_cycle_size = counter[key]/len(all_cycle_sizes)*100
    print("%s (%s) : %.2f%%" %(key, int(key)/nb_cards, proportion_cycle_size))

# plt.hist(all_cycle_sizes, bins=1000)
# plt.show()