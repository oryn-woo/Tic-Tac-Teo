# Text Base version of Tic-Tac Teo
import pprint

class TicTacTeo:
    def __init__(self):
        self.grid = self.create_positions()
        self.player_turn = "X"

    def create_positions(self):
        """
        Crete the 3by3 grid for buttons.
        :return: a list grid
        """
        button_grid = [[column for column in range(3)] for row in range(3)]
        return button_grid

    def check_win(self):
        """
        Checks win on all sides.
        Builds a new row and column every time to reflect the current state of the grid, with it's entries.
        :return:
        """
        # Dynamically build the winning lines from the current grid
        row1 = self.grid[0]
        row2 = self.grid[1]
        row3 = self.grid[2]
        column1 = [self.grid[0][0], self.grid[1][0], self.grid[2][0]]
        column2 = [self.grid[0][1], self.grid[1][1], self.grid[2][1]]
        column3 = [self.grid[0][2], self.grid[1][2], self.grid[2][2]]
        lead_dig = [self.grid[0][0], self.grid[1][1], self.grid[2][2]]
        lag_dig = [self.grid[0][2], self.grid[1][1], self.grid[2][0]]

        winning_combinations = [
            row1, row2, row3,
            column1, column2, column3,
            lead_dig, lag_dig
        ]

        # Change "Y" to "O" if you intend to use the typical tic-tac-toe symbols.
        # If you're using "Y", then keep it as is.
        for combo in winning_combinations:
            if all(cell == "X" for cell in combo):
                return "X"  # X wins
            elif all(cell == "Y" for cell in combo):
                return "Y"  # Y wins
        # No winning combination found
        return None

    def is_valid_move(self, row, col):
        """
        Ensures chosen spot is empty, input in grid range.
        :param row: The row
        :param col: The colum
        :return: The point if its empty
        """
        return self.grid[row][col] not in ["X", "Y"]

    def switch_player(self):
        """
        dynamically switch player
        :return: None
        """
        self.player_turn = "X" if self.player_turn == "Y" else "Y"

    def is_draw(self):
        """
        check if all cells are occupied, if yes it's a draw
        :return:
        """
        return all(cell in ["X", "Y"] for row in self.grid for cell in row)

    def display_grid(self):
        for row in self.grid:
            print(" | ".join(str(cell) for cell in row))
            print("-" * 9)

    def start_game(self):
        """
        Incorporates all the methods and check to ensure works just fine
        :return: None
        """
        while True:
            self.display_grid()
            move = input("Enter Position (P00, P01, P02, P10, P11, P12, P20, P21, P22)")

            try:
                # Parse the move into row and column indices
                if (move.startswith("P") or move.startswith("p")) and len(move) == 3:
                    row, col = int(move[1]), int(move[2])

                    if self.is_valid_move(row, col):
                        self.grid[row][col] = self.player_turn
                        if self.check_win():
                            self.display_grid()
                            print(f"Player {self.player_turn} wins!")
                            break
                        elif self.is_draw():
                            self.display_grid()
                            print("Its a draw!")
                            break
                        self.switch_player()
                    else:
                        print("Invalid move try again")
                else:
                    print("Invalid format. use Pxy where x and y are grid indices")
            except (ValueError, IndexError):
                print("Invalid move. Use Pxy and ensure the indices are in the grid range.")


game = TicTacTeo()
game.start_game()