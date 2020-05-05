def minimax(board, depth, colour, alpha=-100, beta=100, max_turn=True):
    if depth == 0:
        return

    # The first turn must be max_turn
    if max_turn:
        max_eval = -100; max_action = None
        for action in board.possible_actions(colour):
            board_copy = board.copy()
            if type(action) == tuple:
                board_copy.set_move(action[1], board_copy.get_p(action[0]), board_copy.get_p(action[2]))
            else:
                board_copy.set_boom(action)
            minimax(board_copy, depth-1, colour, not max_turn)

            current_eval = board_copy.get_eval(colour)
            if current_eval > max_eval:
                max_eval = current_eval
                max_action = action
            alpha = max(alpha, max_eval)
            if beta <= alpha:
                break
        # return max_eval, max_action
        return max_action

    else:
        min_eval = 100; min_action = None
        for action in board.possible_actions(colour):
            board_copy = board.copy()
            if type(action) == tuple:
                board_copy.set_move(action[1], board_copy.get_p(action[0]), board_copy.get_p(action[2]))
            else:
                board_copy.set_boom(action)
            minimax(board_copy, depth-1, colour)

            current_eval = board_copy.get_eval(colour)
            if current_eval < min_eval:
                min_eval = current_eval
                min_action = action
            beta = min(beta, min_eval)
            if beta <= alpha:
                break
        # return min_eval, min_action
        return min_action
