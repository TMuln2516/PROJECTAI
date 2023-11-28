import support_function as spf 
import time

def DFS_Search(board, list_check_point):
    start_time = time.time()

    if spf.check_win(board, list_check_point):
        print("Found win")
        return [board]

    start_state = spf.state(board, None, list_check_point)
    stack = [start_state]
    list_state = [start_state]

    while stack:
        now_state = stack.pop()
        cur_pos = spf.find_position_player(now_state.board)

        # Uncomment the following block if you want to see step-by-step execution
        '''
        time.sleep(1)
        clear = lambda: os.system('cls')
        clear()
        print_matrix(now_state.board)
        print("State visited : {}".format(len(list_state)))
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
            stack.append(new_state)

            end_time = time.time()
            if end_time - start_time > spf.TIME_OUT:
                return []

    print("Not Found")
    return []