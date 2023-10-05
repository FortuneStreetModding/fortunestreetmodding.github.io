from termcolor import colored

from validation.errors import process_strWarnings


max_paths_warning =  (
    f'({colored("{filename}", "green")}): The Max Paths value of '
    f'{colored("{max_paths}", "red")} is higher than {colored("{limit}", "yellow")}.'
)


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
        for d in w.destinations:
            if w.entryId == previous_square_id or previous_square_id == 255:
                if d != 255:
                    destinations.append(d)
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
        if paths_count > max_paths_count:
            max_paths_count = paths_count
            square_id_with_max_paths_count = i
        paths_count = 0

    return [square_id_with_max_paths_count, max_paths_count]


def check_max_paths(frb, name):
    strWarnings = []
    print(f'{" ":24} Max Paths Check....................', end="")
    search_depth = int(len(frb._board_data.squares) / 3)
    if search_depth < 16:
        search_depth = 16
    result = calculate_max_paths(squares=frb._board_data.squares, dice=search_depth, limit=1000)
    if result[1] > 100:
        strWarnings.append(max_paths_warning.format(filename=name, max_paths=result[1], limit=100))
    process_strWarnings(strWarnings=strWarnings)