"""
This is the main module of the game.
https://github.com/MykhailoSobko/skyscrapers
"""
def read_input(path: str) -> list:
    """
    Read game board file from path.
    Return list of str.

    >>> read_input("check.txt")
    ['***21**', '412453*', '423145*', '*543215', '*35214*', '*41532*', '*2*1***']
    """
    board = []
    file = open(path, mode='r', encoding='utf-8')
    for line in file:
        line = line.strip()
        board.append(line)
    file.close()

    return board


def left_to_right_check(input_line: str, pivot: int) -> bool:
    """
    Check row-wise visibility from left to right.
    Return True if number of building from the left-most hint is visible looking to the right,
    False otherwise.

    input_line - representing board row.
    pivot - number on the left-most hint of the input_line.

    >>> left_to_right_check("412453*", 4)
    True
    >>> left_to_right_check("452453*", 5)
    False
    """
    if input_line[0] == str(pivot):
        return True

    return False


def check_not_finished_board(board: list) -> bool:
    """
    Check if skyscraper board is not finished, i.e., '?' present on the game board.

    Return True if finished, False otherwise.

    >>> check_not_finished_board(['***21**', '4?????*', '4?????*', '*?????5', '*?????*', '*?????*', '*2*1***'])
    False
    >>> check_not_finished_board(['***21**', '412453*', '423145*', '*543215', '*35214*', '*41532*', '*2*1***'])
    True
    >>> check_not_finished_board(['***21**', '412453*', '423145*', '*5?3215', '*35214*', '*41532*', '*2*1***'])
    False
    """
    for row in board[1:-1]:
        if '?' in row[1:-1]:
            return False

    return True


def check_uniqueness_in_rows(board: list) -> bool:
    """
    Check buildings of unique height in each row.

    Return True if buildings in a row have unique length, False otherwise.

    >>> check_uniqueness_in_rows(['***21**', '412453*', '423145*', '*543215', '*35214*', '*41532*', '*2*1***'])
    True
    >>> check_uniqueness_in_rows(['***21**', '452453*', '423145*', '*543215', '*35214*', '*41532*', '*2*1***'])
    False
    >>> check_uniqueness_in_rows(['***21**', '412453*', '423145*', '*553215', '*35214*', '*41532*', '*2*1***'])
    False
    """
    for row in board[1:-1]:
        for building in row[1:-1]:
            if row[1:-1].index(building) != row[1:-1].rindex(building):
                return False

    return True


def check_horizontal_visibility(board: list) -> bool:
    """
    Check row-wise visibility (left-right and vice versa)

    Return True if all horizontal hints are satisfiable,
     i.e., for line 412453* , hint is 4, and 1245 are the four buildings
      that could be observed from the hint looking to the right.

    >>> check_horizontal_visibility(['***21**', '412453*', '423145*', '*543215', '*35214*', '*41532*', '*2*1***'])
    True
    >>> check_horizontal_visibility(['***21**', '452453*', '423145*', '*543215', '*35214*', '*41532*', '*2*1***'])
    False
    >>> check_horizontal_visibility(['***21**', '452413*', '423145*', '*543215', '*35214*', '*41532*', '*2*1***'])
    False
    """
    for row in board[1:-1]:
        if row[0].isnumeric():
            pivot = int(row[0])
            row = row[1:-1]
            count = 1
            highest = int(row[0])
            for i, _ in enumerate(row):
                if int(row[i]) > highest:
                    highest = int(row[i])
                    count += 1
            if count != pivot:
                return False

        elif row[-1].isnumeric():
            pivot = int(row[-1])
            row = row[1:-1]
            count = 1
            highest = int(row[-1])
            for i, _ in reversed(list(enumerate(row))):
                if int(row[i]) > highest:
                    highest = int(row[i])
                    count +=1
            if count != pivot:
                return False

    return True


def check_columns(board: list) -> bool:
    """
    Check column-wise compliance of the board for uniqueness (buildings of unique height) and visibility (top-bottom and vice versa).

    Same as for horizontal cases, but aggregated in one function for vertical case, i.e. columns.

    >>> check_columns(['***21**', '412453*', '423145*', '*543215', '*35214*', '*41532*', '*2*1***'])
    True
    >>> check_columns(['***21**', '412453*', '423145*', '*543215', '*35214*', '*41232*', '*2*1***'])
    False
    >>> check_columns(['***21**', '412553*', '423145*', '*543215', '*35214*', '*41532*', '*2*1***'])
    False
    """
    for j, pivot in enumerate(board[0]):
        if pivot.isnumeric():
            pivot = int(pivot)
            count = 1
            highest = board[1][j]
            for i in range(2, len(board)-1):
                if board[i][j] > highest:
                    highest = board[i][j]
                    count += 1
            if count != pivot:
                return False

    for j, pivot in enumerate(board[-1]):
        if pivot.isnumeric():
            pivot = int(pivot)
            count = 1
            highest = board[-2][j]
            for i in range(len(board)-2, 1, -1):
                if board[i][j] > highest:
                    highest = board[i][j]
                    count += 1
            if count != pivot:
                return False

    return True


def check_skyscrapers(input_path: str) -> bool:
    """
    Main function to check the status of skyscraper game board.
    Return True if the board status is compliant with the rules,
    False otherwise.

    >>> check_skyscrapers("check.txt")
    True
    """
    board = read_input(input_path)

    return (check_not_finished_board(board)
        and check_uniqueness_in_rows(board)
        and check_horizontal_visibility(board)
        and check_columns(board)
        )


if __name__ == "__main__":
    print(check_skyscrapers("check.txt"))
