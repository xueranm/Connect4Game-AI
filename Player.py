import numpy as np

class AIPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'ai'
        self.player_string = 'Player {}:ai'.format(player_number)
        self.max_depth = 4;
        self.evaluationValue = [[3, 4, 5, 7, 5, 4, 3],    
                                [4, 6, 8, 10, 8, 6, 4], 
                                [5, 8, 11, 13, 11, 8, 5], 
                                [5, 8, 11, 13, 11, 8, 5],
                                [4, 6, 8, 10, 8, 6, 4],   
                                [3, 4, 5, 7, 5, 4, 3]]

    def get_alpha_beta_move(self, board):
        """
        Given the current state of the board, return the next move based on
        the alpha-beta pruning algorithm

        This will play against either itself or a human player

        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The 0 based index of the column that represents the next move
        """
        move = self.alpha_beta_search(board, self.max_depth, True, -138, 138, -10000)[1]
        #print (move)
        return move
        #raise NotImplementedError('Whoops I don\'t know what to do')

    def alpha_beta_search(self, board, depth, ismax, alpha, beta, col):

        succ = self.get_succ(board, ismax)
        
        if depth == 0 or not succ: # Evaluate the non-terminal nodes
            #print("column")
            #print(col)
            #print("---")
            #print("One depth: ", depth)
            #print("---")
            evaluation = self.evaluation_function(board)
            #print(evaluation)
            return evaluation, col

        #check if it is the initailization case
        if col == -10000:
            move = succ[0][1]
        else:
            move = col
        if ismax:

            val = -138
            for new_board, column  in succ:
                # check if connect 4, if so just prune
                check = self.connect_four(new_board)
                if check == 1000:
                    return 1000, column
                temp = self.alpha_beta_search(new_board, depth - 1, False, alpha, beta, column)
                #if the opponent will win 
                #if (temp == -1000):

                if temp[0] > val:
                    val = temp[0]
                    move = column
                #alpha_beta_prune
                if val >= beta:
                    return val, move
                alpha = max(alpha, val)
            return val, move 
        #ismin
        else:

            val = 138
            for new_board, column  in succ:
                # check if connect 4
                check = self.connect_four(new_board)
                if check == -1000:
                    #print(col)
                    #print(-1000)
                    #print(column)
                    return -1000, column
                temp = self.alpha_beta_search(new_board, depth - 1, True, alpha, beta, column)
                if temp[0] < val:
                    val = temp[0]
                    move = column
                #alpha_beta_prune
                if val <=  alpha:
                    return val, move
                beta = min(beta, val)
            return val, move 



    """
    Given the current state of the board, return all the achievable states after next move
    """
    def get_succ(self, board, ismax):

        valid_cols = self.get_valid_cols(board)
        if not valid_cols:
            return []

        succ = []
        for col in valid_cols:
            new_board = board.copy()
            #update the new board
            self.update_board(new_board, col, ismax)
            succ.append((new_board, col))

        return succ


    #Credit: from ConnectFour.py which is provided by the class assignment2
    def update_board(self, board, move, ismax):
        
        update_row = -1
        for row in range(1, board.shape[0]):
            update_row = -1
            if board[row, move] > 0 and board[row-1, move] == 0:
                update_row = row-1
            elif row== board.shape[0]-1 and board[row, move] == 0:
                update_row = row
            
            if update_row >= 0:
                if (ismax):
                    board[update_row, move] = self.player_number
                else:
                    if self.player_number == 1:
                        board[update_row, move] = 2
                    else:
                        board[update_row, move] = 1
                break
       


    def get_valid_cols(self, board):

        valid_cols = []
        for col in range(board.shape[1]):
            if 0 in board[:,col]:
                valid_cols.append(col)
        return valid_cols




    def get_expectimax_move(self, board):
        """
        Given the current state of the board, return the next move based on
        the expectimax algorithm.

        This will play against the random player, who chooses any valid move
        with equal probability

        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The 0 based index of the column that represents the next move
        """
        #raise NotImplementedError('Whoops I don\'t know what to do')
        move = self.expectimax_search(board, self.max_depth, True, 0)[1]
        #print("expectimax_search move:")
        #print (move)
        return move


    def expectimax_search(self, board, depth, ismax, col):

        succ = self.get_succ(board, ismax)
        if depth == 0 or not succ: # Evaluate the non-terminal nodes
            #print("column")
            #print(col)
            return self.evaluation_function(board), col

        
        if ismax:
            move = col
            val = -10000
            for new_board, column  in succ:
                # check if connect 4, if so just prune
                temp = self.expectimax_search(new_board, depth - 1, False, column)
                if temp[0] > val:
                    val = temp[0]
                    move = column
                
            return val, move 
        #isexp
        else:
            val = 0
            for new_board, column  in succ:
                check = self.connect_four(new_board)
                if check == -1000:
                    
                    return -1000, column
                temp = self.expectimax_search(new_board, depth - 1, True, column)
                p = 1/len(succ)
                val += temp[0] * p 
                
            return val, -1
            


    def evaluation_function(self, board):
        """
        Given the current stat of the board, return the scalar value that 
        represents the evaluation function for the current player
       
        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The utility value for the current board
        """
        # Initial each state; the range of untility is between -138 to 138 
        util = 0;

        #block opponent/connect 4 for current player
        check = self.connect_four(board)
        if check != 0:
            return check

        for row in range(board.shape[0]):
            for col in range(board.shape[1]):
                if board[row][col] == self.player_number:
                    util += self.evaluationValue[row][col]
                elif board[row][col] != 0:
                    util -= self.evaluationValue[row][col]
        #print(util)
        return util 

    #check if the state has a connect four 
    # return: 276 if current player has connect4, 
    #         0 if no connect4,
    #         -276 if opponent has connect4
    def connect_four(self, board):
        connect_four = False
        for i in range(board.shape[0]):
            #print("i: ")
            #print(i)
            if i < board.shape[0] - 3:
                for j in range(board.shape[1]):
                    check = self.connect_four_for_position(board, i, j)
                    if check != 0:
                        return check
            else:
                for j in range(board.shape[1] - 3):
                    check = self.connect_four_for_position(board, i, j)
                    if check != 0:
                        return check
        return 0

    def connect_four_for_position(self, board, row, col):
        connect_four = False
        #check if connect 4 from current position down
        if row < board.shape[0] - 3:
            #check for current player
            curr_player = True
            #check for opponent
            opponent = True
            for r in range(4):
                if (board[row + r][col] != self.player_number):
                    curr_player = False
                if (board[row + r][col] == self.player_number or board[row + r][col] == 0):
                    opponent = False
            
            if (curr_player):
                return 1000
            if (opponent):
                return -1000

            #check diagonal if connect 4 from current position down and to right 
            if col < board.shape[1] - 3:
                #check for current player
                curr_player = True
                #check for opponent
                opponent = True
                for r in range(4):
                    if (board[row + r][col + r] != self.player_number):
                        curr_player = False
                    if (board[row + r][col + r] == self.player_number or board[row + r][col + r] == 0):
                        opponent = False
                
                if (curr_player):
                    return 1000
                if (opponent):
                    return -1000

        #check if connect 4 from current position to right 
        if col < board.shape[1] - 3:
            #check for current player
            curr_player = True
            #check for opponent
            opponent = True
            for r in range(4):
                if (board[row][col + r] != self.player_number):
                    curr_player = False
                if (board[row][col + r] == self.player_number or board[row][col + r] == 0):
                    opponent = False
            if (curr_player):
                return 1000
            if (opponent):
                return -1000
            #check diagonal if connect 4 from current position up and to right 
            if row > 2:
                #check for current player
                curr_player = True
                #check for opponent
                opponent = True
                for r in range(4):
                    if (board[row - r][col + r] != self.player_number):
                        curr_player = False
                    if (board[row - r][col + r] == self.player_number or board[row - r][col + r] == 0):
                        opponent = False
                if (curr_player):
                    return 1000
                if (opponent):
                    return -1000

        return 0




#It seems that random and human didn't consider the corner case, like no place to put
class RandomPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'random'
        self.player_string = 'Player {}:random'.format(player_number)

    def get_move(self, board):
        """
        Given the current board state select a random column from the available
        valid moves.

        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The 0 based index of the column that represents the next move
        """
        valid_cols = []
        for col in range(board.shape[1]):
            if 0 in board[:,col]:
                valid_cols.append(col)

        return np.random.choice(valid_cols)


class HumanPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'human'
        self.player_string = 'Player {}:human'.format(player_number)

    def get_move(self, board):
        """
        Given the current board state returns the human input for next move

        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The 0 based index of the column that represents the next move
        """

        valid_cols = []
        for i, col in enumerate(board.T):
            if 0 in col:
                valid_cols.append(i)

        move = int(input('Enter your move: '))

        while move not in valid_cols:
            print('Column full, choose from:{}'.format(valid_cols))
            move = int(input('Enter your move: '))

        return move

