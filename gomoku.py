def is_empty(board):
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] != ' ':
                return False
    return True

def is_full(board):
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == ' ':
                return False
    return True


def is_bounded(board, y_end, x_end, length, d_y, d_x):
    is_bounded_top = False
    is_bounded_bottom = False
    is_bounded_right = False
    is_bounded_left = False
    is_bounded_topleft = False
    is_bounded_bottomright = False
    is_bounded_topright = False
    is_bounded_bottomleft = False

    # vertical sequence
    if d_y == 1 and d_x == 0:
        y_start = y_end - length + 1

        # check if bounded at bottom
        if y_end == 7 or board[y_end+1][x_end] != ' ':
            is_bounded_bottom = True

        # check if bounded at top
        if y_start == 0 or board[y_start-1][x_end] != ' ':
            is_bounded_top = True

        # determine openness
        if is_bounded_bottom and is_bounded_top:
            return "CLOSED"
        elif is_bounded_bottom or is_bounded_top:
            return "SEMIOPEN"
        else:
            return "OPEN"

    # horizontal sequence
    if d_y == 0 and d_x == 1:
        x_start = x_end - length + 1

        # check if bounded at left
        if x_start == 0 or board[y_end][x_start - 1] != ' ':
            is_bounded_left = True

        # check if bounded at right
        if x_end == 7 or board[y_end][x_end + 1] != ' ':
            is_bounded_right = True

        # determine openness
        if is_bounded_left and is_bounded_right:
            return "CLOSED"
        elif is_bounded_left or is_bounded_right:
            return "SEMIOPEN"
        else:
            return "OPEN"

    # top-left to bottom-right sequence
    if d_y == 1 and d_x == 1:
        x_start = x_end - length + 1
        y_start = y_end - length + 1

        # check if bounded at top-left
        if x_start == 0 or y_start == 0 or board[y_start-1][x_start-1] != ' ':
            is_bounded_topleft = True

        # check if bounded at bottom-right
        if x_end == 7 or y_end == 7 or board[y_end+1][x_end+1] != ' ':
            is_bounded_bottomright = True

        # determine openness
        if is_bounded_topleft and is_bounded_bottomright:
            return "CLOSED"
        elif is_bounded_topleft or is_bounded_bottomright:
            return "SEMIOPEN"
        else:
            return "OPEN"

    # top-right to bottom-left sequence
    if d_y == 1 and d_x == -1:
        x_start = x_end + length - 1
        y_start = y_end - length + 1

        # check if bounded at top-right
        if x_start == 7 or y_start == 0 or board[y_start-1][x_start+1] != ' ':
            is_bounded_topright = True

        # check if bounded at bottom-left
        if x_end == 0 or y_end == 7 or board[y_end+1][x_end-1] != ' ':
            is_bounded_bottomleft = True

        # determine openness
        if is_bounded_bottomleft and is_bounded_topright:
            return "CLOSED"
        elif is_bounded_bottomleft or is_bounded_topright:
            return "SEMIOPEN"
        else:
            return "OPEN"

def detect_row(board, col, y_start, x_start, length, d_y, d_x):
    y_length = y_start
    x_length = x_start
    y = y_start
    x = x_start

    run = 0

    seq_length = 0
    iterations = 0
    semi_counter = 0
    open_counter = 0


    while 0 <= y_length <= 7 and 0 <= x_length <= 7:
        y_length += d_y
        x_length += d_x
        seq_length += 1


    while iterations < seq_length:
        square = board[y][x]
        if square == col:
            run += 1
        else:
            run = 0
        if run == length:
            if is_bounded(board, y, x, length, d_y, d_x) == "OPEN":
                open_counter += 1
            elif is_bounded(board, y, x, length, d_y, d_x) == "SEMIOPEN":
                if iterations + 1 == seq_length:
                    semi_counter += 1
                elif board[y + d_y][x + d_x] != col:
                    semi_counter += 1
                else:
                    pass
        y += d_y
        x += d_x
        iterations += 1

    return (open_counter, semi_counter)

def detect_rows(board, col, length):
    open_counter = 0
    semi_counter = 0
    i = 0
    for j in range(8):
        # checks all vertical rows
        temp = detect_row(board, col, i, j, length, 1, 0)
        open_counter += temp[0]
        semi_counter += temp[1]

        # checks all horizontal rows
        temp = detect_row(board, col, j, i, length, 0, 1)
        open_counter += temp[0]
        semi_counter += temp[1]

        # checks all top right to bottom left diagonals starting from 0,0 to 0,7
        temp = detect_row(board, col, i, j, length, 1, -1)
        open_counter += temp[0]
        semi_counter += temp[1]

        if j == 7:
            for k in range(1, 8):
                # checks all top right to bottom left diagonals starting from 1,7 to 7,7
                temp = detect_row(board, col, k, j, length, 1, -1)
                open_counter += temp[0]
                semi_counter += temp[1]

        # checks all top left to bottom right diagonals starting from 0,0 to 7,0
        temp = detect_row(board, col, j, i, length, 1, 1)
        open_counter += temp[0]
        semi_counter += temp[1]

        if j == 0:
            for l in range(1, 8):
                # checks all top left to bottom right diagonals starting from 0,1 to 0, 7
                temp = detect_row(board, col, j, l, length, 1, 1)
                open_counter += temp[0]
                semi_counter += temp[1]

    return (open_counter, semi_counter)

def detect_row_closed(board, col, y_start, x_start, length, d_y, d_x):
    y_length = y_start
    x_length = x_start
    y = y_start
    x = x_start

    run = 0

    seq_length = 0
    iterations = 0
    closed_counter = 0

    while 0 <= y_length <= 7 and 0 <= x_length <= 7:
        y_length += d_y
        x_length += d_x
        seq_length += 1

    while iterations < seq_length:
        square = board[y][x]
        if square == col:
            run += 1
            if run == 1:
                y_start_row = y
                x_start_row = x
        else:
            run = 0
        if run == length:
            if is_bounded(board, y, x, length, d_y, d_x) == "CLOSED":
                if length == seq_length: # sequence is bounded by edges of board
                    closed_counter += 1
                elif iterations + 1 == seq_length: # sequence is bounded at end by edge of board
                    if board[y_start_row - d_y][x_start_row - d_x] != col:
                        closed_counter += 1
                elif iterations + 1 == run: # sequence is bounded at start by edge of board
                    if board[y + d_y][x + d_x] != col:
                        closed_counter += 1
                elif board[y + d_y][x + d_x] != col:
                    if board[y_start_row - d_y][x_start_row - d_x] != col: # sequence is in middle of board
                        closed_counter += 1
                else:
                    pass
        y += d_y
        x += d_x
        iterations += 1

    return closed_counter

def detect_rows_closed(board, col, length):
    closed_counter = 0
    i = 0
    for j in range(8):
        # checks all vertical rows
        closed_counter += detect_row_closed(board, col, i, j, length, 1, 0)

        # checks all horizontal rows
        closed_counter += detect_row_closed(board, col, j, i, length, 0, 1)

        # checks all top right to bottom left diagonals starting from 0,0 to 0,7
        closed_counter += detect_row_closed(board, col, i, j, length, 1, -1)

        if j == 7:
            for k in range(1, 8):
                # checks all top right to bottom left diagonals starting from 1,7 to 7,7
                closed_counter += detect_row_closed(board, col, k, j, length, 1, -1)

        # checks all top left to bottom right diagonals starting from 0,0 to 7,0
        closed_counter += detect_row_closed(board, col, j, i, length, 1, 1)

        if j == 0:
            for l in range(1, 8):
                # checks all top left to bottom right diagonals starting from 0,1 to 0, 7
                closed_counter += detect_row_closed(board, col, j, l, length, 1, 1)

    return closed_counter

def search_max(board):
    current_score = score(board)
    max_score = 0
    for k in range(8):
        for l in range(8):
            if board[k][l] == ' ':
                coords = (k, l)
                break
    for i in range(8):
        for j in range(8):
            if board[i][j] == ' ':
                board[i][j] = 'b'
                max_score = max(max_score, score(board))
                if max_score == (score(board)):
                    coords = (i, j)
                board[i][j] = ' '
    return coords

def score(board):
    MAX_SCORE = 100000

    open_b = {}
    semi_open_b = {}
    open_w = {}
    semi_open_w = {}

    for i in range(2, 6):
        open_b[i], semi_open_b[i] = detect_rows(board, "b", i)
        open_w[i], semi_open_w[i] = detect_rows(board, "w", i)


    if open_b[5] >= 1 or semi_open_b[5] >= 1:
        return MAX_SCORE

    elif open_w[5] >= 1 or semi_open_w[5] >= 1:
        return -MAX_SCORE

    return (-10000 * (open_w[4] + semi_open_w[4])+
            500  * open_b[4]                     +
            50   * semi_open_b[4]                +
            -100  * open_w[3]                    +
            -30   * semi_open_w[3]               +
            50   * open_b[3]                     +
            10   * semi_open_b[3]                +
            open_b[2] + semi_open_b[2] - open_w[2] - semi_open_w[2])


def is_win(board):
    if detect_rows(board, 'w', 5) != (0, 0):
        return "White won"
    elif detect_rows(board, 'b', 5) != (0, 0):
        return "Black won"
    elif detect_rows_closed(board, 'b', 5) != 0:
         return "Black won"
    elif detect_rows_closed(board, 'w', 5) != 0:
         return "White won"
    elif is_full(board):
        return "Draw"
    else:
        return "Continue playing"


def print_board(board):
    s = "*"
    for i in range(len(board[0])-1):
        s += str(i%10) + "|"
    s += str((len(board[0])-1)%10)
    s += "*\n"

    for i in range(len(board)):
        s += str(i%10)
        for j in range(len(board[0])-1):
            s += str(board[i][j]) + "|"
        s += str(board[i][len(board[0])-1])

        s += "*\n"
    s += (len(board[0])*2 + 1)*"*"

    print(s)


def make_empty_board(sz):
    board = []
    for i in range(sz):
        board.append([" "]*sz)
    return board



def analysis(board):
    for c, full_name in [["b", "Black"], ["w", "White"]]:
        print("%s stones" % (full_name))
        for i in range(2, 6):
            open, semi_open = detect_rows(board, c, i);
            print("Open rows of length %d: %d" % (i, open))
            print("Semi-open rows of length %d: %d" % (i, semi_open))

def play_gomoku(board_size):
    board = make_empty_board(board_size)
    board_height = len(board)
    board_width = len(board[0])

    while True:
        print_board(board)
        if is_empty(board):
            move_y = board_height // 2
            move_x = board_width // 2
        else:
            move_y, move_x = search_max(board)

        print("Computer move: (%d, %d)" % (move_y, move_x))
        board[move_y][move_x] = "b"
        print_board(board)
        analysis(board)

        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res

        print("Your move:")
        move_y = int(input("y coord: "))
        move_x = int(input("x coord: "))
        board[move_y][move_x] = "w"
        print_board(board)
        analysis(board)

        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res


def put_seq_on_board(board, y, x, d_y, d_x, length, col):
    for i in range(length):
        board[y][x] = col
        y += d_y
        x += d_x


def test_is_empty():
    board  = make_empty_board(8)
    if is_empty(board):
        print("TEST CASE for is_empty PASSED")
    else:
        print("TEST CASE for is_empty FAILED")


def test_is_bounded():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)

    y_end = 3
    x_end = 5

    if is_bounded(board, y_end, x_end, length, d_y, d_x) == 'OPEN':
        print("TEST CASE for is_bounded PASSED")
    else:
        print("TEST CASE for is_bounded FAILED")


def test_detect_row():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    if detect_row(board, "w", 0,x,length,d_y,d_x) == (1,0):
        print("TEST CASE for detect_row PASSED")
    else:
        print("TEST CASE for detect_row FAILED")

def test_detect_rows():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    if detect_rows(board, col,length) == (1,0):
        print("TEST CASE for detect_rows PASSED")
    else:
        print("TEST CASE for detect_rows FAILED")

def test_search_max():
    board = make_empty_board(8)
    x = 5; y = 0; d_x = 0; d_y = 1; length = 4; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    x = 6; y = 0; d_x = 0; d_y = 1; length = 4; col = 'b'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    print_board(board)
    if search_max(board) == (4,6):
        print("TEST CASE for search_max PASSED")
    else:
        print("TEST CASE for search_max FAILED")

def easy_testset_for_main_functions():
    test_is_empty()
    test_is_bounded()
    test_detect_row()
    test_detect_rows()
    test_search_max()

def some_tests():
    board = make_empty_board(8)

    board[0][5] = "w"
    board[0][6] = "b"
    y = 5; x = 2; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    analysis(board)

    # Expected output:
    #       *0|1|2|3|4|5|6|7*
    #       0 | | | | |w|b| *
    #       1 | | | | | | | *
    #       2 | | | | | | | *
    #       3 | | | | | | | *
    #       4 | | | | | | | *
    #       5 | |w| | | | | *
    #       6 | |w| | | | | *
    #       7 | |w| | | | | *
    #       *****************
    #       Black stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 0
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0
    #       White stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 1
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0

    y = 3; x = 5; d_x = -1; d_y = 1; length = 2

    put_seq_on_board(board, y, x, d_y, d_x, length, "b")
    print_board(board)
    analysis(board)

    # Expected output:
    #        *0|1|2|3|4|5|6|7*
    #        0 | | | | |w|b| *
    #        1 | | | | | | | *
    #        2 | | | | | | | *
    #        3 | | | | |b| | *
    #        4 | | | |b| | | *
    #        5 | |w| | | | | *
    #        6 | |w| | | | | *
    #        7 | |w| | | | | *
    #        *****************
    #
    #         Black stones:
    #         Open rows of length 2: 1
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 0
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #         White stones:
    #         Open rows of length 2: 0
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 1
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #

    y = 5; x = 3; d_x = -1; d_y = 1; length = 1
    put_seq_on_board(board, y, x, d_y, d_x, length, "b");
    print_board(board);
    analysis(board);

    #        Expected output:
    #           *0|1|2|3|4|5|6|7*
    #           0 | | | | |w|b| *
    #           1 | | | | | | | *
    #           2 | | | | | | | *
    #           3 | | | | |b| | *
    #           4 | | | |b| | | *
    #           5 | |w|b| | | | *
    #           6 | |w| | | | | *
    #           7 | |w| | | | | *
    #           *****************
    #
    #
    #        Black stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0
    #        Open rows of length 3: 0
    #        Semi-open rows of length 3: 1
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0
    #        White stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0
    #        Open rows of length 3: 0
    #        Semi-open rows of length 3: 1
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0


if __name__ == '__main__':
    play_gomoku(8)