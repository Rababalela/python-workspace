# PROJECT 3

import random 

# Board setup

def  create_board():
    """ 
    Creates a fresh 3x3 board numbered 1-9.
    """
    return [str(i) for i in range(1,10)]

def display_board(board):
    """ 
    Displays the current state of the board.
    """
    print("\n")
    print(f"{board[0]} | {board[1]} | {board[2]}")
    print("--+---+--")
    print(f"{board[3]} | {board[4]} | {board[5]}")
    print("--+---+--")
    print(f"{board[6]} | {board[7]} | {board[8]}")
    print("\n")

# win / draw conditions

win_conditions = [
    [0, 1, 2],  # Row 1
    [3, 4, 5],  # Row 2
    [6, 7, 8],  # Row 3
    [0, 3, 6],  # Column 1
    [1, 4, 7],  # Column 2
    [2, 5, 8],  # Column 3
    [0, 4, 8],  # Diagonal top-left to bottom-right
    [2, 4, 6]   # Diagonal top-right to bottom-left
]

def check_win(board, player):
    """ 
    Checks if the given player has won the game.
    """
    for condition in win_conditions:
        if all(board[i] == player for i in condition):
            return True
    return False

def check_draw(board):
    """ 
    Checks if the game is a draw (no empty spaces left).
    """
    return all(space in ['X', 'O'] for space in board)

# Player move

def player_move(board):
    """ 
    Prompts the player to make a move and updates the board.
    """
    while True:
        try:
            move = input("Enter your move (1-9): ")
            if not move.isdigit():
                print("Invalid input. Please enter a number between 1 and 9.")
                continue
            move = int(move) - 1
            if move < 0 or move > 8:
                print("Invalid move. Please enter a number between 1 and 9.")
            elif board[move] in ['X', 'O']:
                print("That space is already taken. Please choose another one.")
            else:
                board[move] = 'X'
                break
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 9.")
            
# Computer move

def computer_move(board):
    """ 
    Computer makes a random move on the board.
    """
    available_moves = [i for i in range(9) if board[i] not in ['X', 'O']]
    
    # 1. Try to win
    for move in available_moves:
        board[move] = 'O'
        if check_win(board, 'O'):
            print(f"Computer chose position {move + 1}")
            return True
        board[move] = str(move + 1)

    # 2. Try to block player
    for move in available_moves:
        board[move] = 'X'
        if check_win(board, 'X'):
            board[move] = 'O'
            print(f"Computer chose position {move + 1}")
            return True
        board[move] = str(move + 1)

    # 3. Take center
    if board[4] not in ['X', 'O']:
        board[4] = 'O'
        print("Computer chose position 5")
        return True
    
    # 4. Take corner
    corners = [0, 2, 6, 8]
    available_corners = [i for i in corners if board[i] not in ['X', 'O']]
    if available_corners:
        move = random.choice(available_corners)
        board[move] = 'O'
        print(f"Computer chose position {move + 1}")
        return True

    # 5. Take any remaining
    if available_moves:
        move = random.choice(available_moves)
        board[move] = 'O'
        print(f"Computer chose position {move + 1}")
        return True
    return False


# score tracking

def display_score(scores):
    """ 
    Displays the current score of the player and computer.
    """
    print(f"Score - Player: {scores['Player']} | Computer: {scores['Computer']} | Draws: {scores['Draws']}")
    
# main game loop

def play_game(scores):
    """
    run a single game of tic-tac-toe and update scores
    """
    board = create_board()
    
    print("\n/------------------------------/")
    print("  NEW GAME STARTED! GOOD LUCK! ")
    print("/------------------------------/") 
    print("You are 'X' and the computer is 'O'.")
    
    while True:
        display_board(board)
        print("Your turn!")
        player_move(board)
        
        if check_win(board, 'X'):
            display_board(board)
            print("Congratulations! You win!")
            scores['Player'] += 1
            break
        
        if check_draw(board):
            display_board(board)
            print("It's a draw!")
            scores['Draws'] += 1
            break
        
        print("Computer's turn...")
        computer_move(board)
        
        if check_win(board, 'O'):
            display_board(board)
            print("Computer wins! Better luck next time.")
            scores['Computer'] += 1
            break
        
        if check_draw(board):
            display_board(board)
            print("It's a draw!")
            scores['Draws'] += 1
            break
    
# Entry point
def main():
     print("\n" + "-" * 35)
     print("WELCOME TO TIC TAC TOE!")
     print("-" * 35)
     
     scores = {"Player": 0, "Computer": 0, "Draws": 0}
     
     while True:
         play_game(scores)
         display_score(scores)
         
         again = input("\nDo you want to play again? (y/n): ").lower().strip()
         if again != 'y':
           print("Thanks for playing! Goodbye!")
           break

if __name__ == "__main__":
    main()
