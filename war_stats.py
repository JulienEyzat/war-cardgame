from collections import Counter
import matplotlib.pyplot as plt
import numpy as np
import os

def get_cycle_size_multiples(all_cycle_sizes, nb_cards):
    return [ cycle_size/nb_cards for cycle_size in sorted(list(set(all_cycle_sizes))) ]

def print_stats():
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
        nb_cards = nb_colors * nb_values
        print("%s (%s) : %.2f%%" %(key, int(key)/nb_cards, proportion_cycle_size))

    # plt.hist(all_cycle_sizes, bins=1000)
    # plt.show()

def cycles_to_csv(all_cycle_sizes, nb_colors, nb_values, max_nb_values, max_nb_colors):
    nb_cards = nb_colors * nb_values
    cycle_size_multiples = get_cycle_size_multiples(all_cycle_sizes, nb_cards)

    data_dir = "data"
    file_path = os.path.join(data_dir, "save_cycles_%s_%s.csv" %(max_nb_colors, max_nb_values))
    if not os.path.isdir(data_dir):
        os.mkdir(data_dir)
    if os.path.isfile(file_path):
        my_data = np.loadtxt(file_path, delimiter=';', dtype="object")
    else:
        my_data = np.zeros((max_nb_colors, max_nb_values), dtype='object')
    if cycle_size_multiples:
        cycle_size_multiples = map(int, cycle_size_multiples)
        cycle_size_multiples = map(str, cycle_size_multiples)
        my_data[nb_colors-1, nb_values-1] = ",".join(cycle_size_multiples)
    else:
        my_data[nb_colors-1, nb_values-1] = "NONE"
    np.savetxt(file_path, my_data, delimiter=";", fmt='%s')
