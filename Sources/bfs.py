import support_function as spf
from collections import deque
import time

def BFS_search(board, list_check_point):
    start_time = time.time()

    if spf.check_win(board, list_check_point):
        print("Found win")
        return [board]

    start_state = spf.state(board, None, list_check_point)
    list_state = deque([start_state])
    list_visit = deque([start_state])

    while list_visit:
        now_state = list_visit.popleft()
        cur_pos = spf.find_position_player(now_state.board)

        # Uncomment to use if necessary
        '''
        time.sleep(1)
        clear = lambda: os.system('cls')
        clear()
        print_matrix(now_state.board)
        print("State visited: {}".format(len(list_state)))
        print("State in queue: {}".format(len(list_visit)))
        '''

        list_can_move = spf.get_next_pos(now_state.board, cur_pos)

        for next_pos in list_can_move:
            new_board = spf.move(now_state.board, next_pos, cur_pos, list_check_point)

            if spf.is_board_exist(new_board, list_state):
                continue

            if spf.is_board_can_not_win(new_board, list_check_point):
                continue

            if spf.is_all_boxes_stuck(new_board, list_check_point):
                continue

            new_state = spf.state(new_board, now_state, list_check_point)

            if spf.check_win(new_board, list_check_point):
                print("Found win")
                return (new_state.get_line(), len(list_state))

            list_state.append(new_state)
            list_visit.append(new_state)

        # Compute the timeout
        end_time = time.time()
        if end_time - start_time > spf.TIME_OUT:
            return []

    print("Not Found")
    return []
