import support_function as spf
import time
from queue import PriorityQueue

def UCS_Search(board, list_check_point):
    start_time = time.time()

    if spf.check_win(board, list_check_point):
        print("Found win")
        return [board]
    

    start_state = spf.state(board, None, list_check_point)
    list_state = [start_state]
    

    cost_queue = PriorityQueue()
    cost_queue.put((0, start_state))  # Dùng cặp (cost, state) để sắp xếp theo chi phí
    

    while not cost_queue.empty():

        cost, now_state = cost_queue.get()


        cur_pos = spf.find_position_player(now_state.board)


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
            cost_queue.put((cost + 1, new_state))  # Tăng chi phí lên 1 vì chúng ta không sử dụng h(n) (heuristic)

            end_time = time.time()
            if end_time - start_time > spf.TIME_OUT:
                return []

        end_time = time.time()
        if end_time - start_time > spf.TIME_OUT:
            return []

    print("Not Found")
    return []