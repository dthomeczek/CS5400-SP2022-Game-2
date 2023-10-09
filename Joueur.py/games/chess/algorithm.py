from games.chess.movement import *
import random

# Characters for all pieces to associate with a score
PIECES = ["p", "r", "n", "b", "q", "k"]

# Function to run the actual algorithm
# In this case, Iterative-Deepening Depth-Limited Min-Max
def algorithm(board_list, color):
    # Dictionary to hold moves
    move_dict = {}
    move = ""
    score = 0 # Initial score value
    start_depth = 0 # Starting depth of 0
    max_depth = 2 # Cap depth

    # Gets action list, followed by the score for each action, and returns to move_list
    action_list = actions(color, board_list)
    move_dict = get_score(board_list, action_list)

    # Assigns the score and move variables for a move
    score, move = set_min_max(move_dict, start_depth)

    # Reassigns the action list based on min_max
    action_list = min_max(board_list, color, move, score, start_depth, max_depth)

    return action_list

# Performs the min max part of the algorithm
def min_max(board_list, color, parent, score, depth, max_depth):
    selected = () # Tuple for the selected move and score
    move_dict = {} # Dictionary for the moves
    h_val = 0 # Heuristic value

    # If max depth reached, return score and parent
    if (depth == max_depth):
        return (score, parent)

    # Determines player and enemy color
    if (color == "white"):
        enemy = "black"
    else:
        enemy = "white"

    # Gets a list of valid actions
    action_list = actions(color, board_list)

    # If no actions are possible, return the score and parent
    if len(action_list) == 0:
        return (score, parent)

    # Update the scores for the moves
    move_dict = get_score(board_list, action_list)

    # Checks each action and generates a state based on that move
    for action in action_list:
        
        new_board = next_move(board_list, action, color == "white")

        for key, values in move_dict.items(): 
            if action in values:
                move_score = key
                break

        # Gets the move(s) that can follow from the current one
        child_move = min_max(new_board, enemy, action, move_score, depth + 1, max_depth)

        # Applies a heuristic value to assess best move options
        h_val = h(depth, move_score, child_move[0])

        # Appends the move dictionary, or empties it if the heuristic is not present
        if h_val not in move_dict:
            move_dict[h_val] = []
        move_dict[h_val] = move_dict[h_val] + [action]

    # Get the selected move from the move dictionary at a specified depth
    selected = set_min_max(move_dict, depth)
    return selected

# Gets the score for all possible moves
def get_score(board_list, action_list):
    PIECE_VALS = {"p": 1, "n":3, "b": 3, "r": 5, "q": 9, "k": 10} # Scores by piece
    move_scores = {} # Holds the scores
    for action in action_list:
        # Converts the given move to coordinates
        move = uci_to_coords(action)
        cap_val = 0 # Value of a capture (0 if none captured)
        piece = board_list.board[move[2]][move[3]]

        # Checks through the pieces and their values to assess each piece
        # and assign a score based on if said piece is taken
        if piece.lower() in PIECES:
            cap_val = PIECE_VALS[piece.lower()]
            if cap_val not in move_scores:
                move_scores[cap_val] = []
            move_scores[cap_val] = move_scores[cap_val] + [action]
        elif piece == ".":
            if cap_val not in move_scores:
                move_scores[cap_val] = []
            move_scores[cap_val] = move_scores[cap_val] + [action]

    return move_scores

# Heuristic function that determines whether a move will result in a gain to the player or not
def h(depth, parent, child):
    gain = 0
    if depth % 2 == 0:
        gain = child + parent
    else:
        gain = child - parent
    return gain

# Sets the min max values
def set_min_max(move_scores, depth):
    score = 0
    move = ""

    if depth % 2 == 0:
        score = max(move_scores)
    else:
        score = min(move_scores)
    
    # Gets a list of all moves with a given score (best score)
    moves_with_score = move_scores[score]

    # If multiple moves have the same score (best score), picks a move among those 
    # with the same score and runs with it, otherwise takes the best score
    if len(moves_with_score) > 1:
        move = random.choice(moves_with_score)
    else:
        move = moves_with_score[0]

    return (score, move)
