import support_function as spf
import time
from queue import PriorityQueue

def AStar_Search(board, list_check_point):
    start_time = time.time()
    if spf.check_win(board, list_check_point):
        print("Found win")
        return [board]

    start_state = spf.state(board, None, list_check_point)
    list_state = [start_state]

    heuristic_queue = PriorityQueue()
    heuristic_queue.put((start_state.compute_heuristic(), start_state))

    while not heuristic_queue.empty():
        _, now_state = heuristic_queue.get()
        cur_pos = spf.find_position_player(now_state.board)
        list_can_move = spf.get_next_pos(now_state.board, cur_pos)

        for next_pos in list_can_move:
            new_board = spf.move(now_state.board, next_pos, cur_pos, list_check_point)

            if spf.is_board_exist(new_board, list_state) or spf.is_board_can_not_win(new_board, list_check_point) or spf.is_all_boxes_stuck(new_board, list_check_point):
                continue

            new_state = spf.state(new_board, now_state, list_check_point)

            if spf.check_win(new_board, list_check_point):
                print("Found win")
                return (new_state.get_line(), len(list_state))

            # Tính giá trị g(n) (chi phí thực tế)
            g_n = now_state.cost + 1  # Thay đổi ở đây, có thể là một giá trị thực tế phù hợp

            # Tính giá trị heuristic h(n)
            h_n = new_state.compute_heuristic()

            # Tổng chi phí f(n)
            f_n = g_n + h_n

            # Cập nhật giá trị chi phí thực tế và ước lượng
            new_state.cost = g_n
            new_state.heuristic = h_n

            list_state.append(new_state)
            heuristic_queue.put((f_n, new_state))

            end_time = time.time()
            if end_time - start_time > spf.TIME_OUT:
                return []

    print("Not Found")
    return []
