import tqdm

import war
import war_stats

def play_multiple_games(nb_values, nb_colors):

    battle_cards_get_algo_type = "nothing"

    all_endings = []
    all_nb_tours = []
    all_cycle_sizes = []
    all_before_cycle_size = []
    is_playing = True
    while is_playing:
        ending_type, nb_tours, cycle_size, before_cycle_size = war.play_game(nb_colors, nb_values, battle_cards_get_algo_type, print_ending=False)
        all_endings.append(ending_type)
        if cycle_size == 0:
            all_nb_tours.append(nb_tours)
        else:
            all_cycle_sizes.append(cycle_size)
            all_before_cycle_size.append(before_cycle_size)

        # Stop playing
        if len(all_cycle_sizes) >= 70:
            is_playing = False
        elif len(all_nb_tours) >= 200:
            is_playing = False

    return all_endings, all_nb_tours, all_cycle_sizes, all_before_cycle_size

def play_ensemble_games():
    range_nb_values = range(1, 8)
    max_nb_values = max(range_nb_values)
    range_nb_colors = range(1, 8)
    max_nb_colors = max(range_nb_colors)
    for nb_values in range_nb_values:
        for nb_colors in range_nb_colors:
            all_endings, all_nb_tours, all_cycle_sizes, all_before_cycle_size = play_multiple_games(nb_values, nb_colors)
            war_stats.cycles_to_csv(all_cycle_sizes, nb_colors, nb_values, max_nb_values, max_nb_colors)


# Play
play_ensemble_games()

