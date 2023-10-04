from termcolor import cprint

from validation.errors import get_path_warning, process_strWarnings

def get_destinations(squares, current_square_id):
    get_destinations(squares=squares, previous_square_id=255, current_square_id=current_square_id)


def get_destinations(squares, previous_square_id, current_square_id):
    destinations = []

    if not (current_square_id < len(squares) or current_square_id == 255):
        return
    if not (previous_square_id < len(squares) or previous_square_id == 255):
        return
    
    square = squares[current_square_id]
    for w in square.waypoints:
        #print(f"W: {w}")
        for d in w.destinations:
            #print(f"D: {d}")
            if w.entryId == previous_square_id or previous_square_id == 255:
                if d != 255:
                    destinations.append(d)
    #print(f"Destinations: {destinations}")
    return list(set(destinations))


def get_paths_count(squares, previous_square_id, current_square_id, dice, limit):
    count = 0
    if dice == 0:
        count += 1
        return count
    
    destinations = get_destinations(squares=squares, previous_square_id=previous_square_id, current_square_id=current_square_id)
    for d in destinations:
        if d < len(squares):
            count += get_paths_count(squares=squares, previous_square_id=current_square_id, current_square_id=d, dice=(dice-1), limit=limit)
    return count

def get_paths_count_without_previous_square(squares, current_square_id, dice, limit):
    paths_count = 0
    paths_count = get_paths_count(squares=squares, current_square_id=current_square_id, previous_square_id=255, dice=dice, limit=limit)
    return paths_count


def calculate_max_paths(squares, dice, limit):
    max_paths_count = 0
    square_id_with_max_paths_count = 255
    for i in range(len(squares)):
        paths_count = get_paths_count_without_previous_square(squares=squares, current_square_id=i, dice=dice, limit=limit)
        #print(f"Paths Count: {paths_count}")
        if paths_count > max_paths_count:
            max_paths_count = paths_count
            square_id_with_max_paths_count = i
        paths_count = 0
    
    #print(f"Max Paths Count: {max_paths_count}")
    #print(f"Square ID with Max Paths Count:: {square_id_with_max_paths_count}")

    return [square_id_with_max_paths_count, max_paths_count]


def check_max_paths(frb, name):
    strWarnings = [] # this should be done better, it sucks rn
    print(f'{" ":24} Max Paths Check..............', end="")
    search_depth = int(len(frb._board_data.squares) / 3)
    if search_depth < 16:
        search_depth = 16
    #print(f'Search Depth: {search_depth}...', end="")
    result = calculate_max_paths(squares=frb._board_data.squares, dice=search_depth, limit=1000)
    #print(f'Maximum Paths: {result[1]} on square {result[0]}...', end="")
    if result[1] > 100:
        strWarnings.append(get_path_warning(name, result[1], 100))
    process_strWarnings(strWarnings=strWarnings)