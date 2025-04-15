
import random
import tkinter as tk
from tkinter import ttk, messagebox
import time


class TicTacToe:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Tic-Tac-Toe")
        self.window.geometry("600x600")
        self.player_turn = "X"  # These variable keeps track of whose turn it is (takes X and Y), will start with player 'X'
        self.scores = {"X": 0, "Y": 0}  # Keeps track os scores.
        self.load_scores()
        self.canvas = tk.Canvas(self.window, width=300, height=300)  # Placed at the top left corner of the window.
        self.canvas.pack()
        self.style = ttk.Style()  # This is used to configure the visual appearance of widgets. For its styles to be applied we need the configure method

        self.style.configure("My.TButton", background="green", font=("sans serif", 12))
        # self.canvas.create_image(0, 0, anchor="nw")
        self.buttons = []  # The list to hold the overall grid, which is a list, with three list items,
        # representing each row
        for i in range(3):
            # Create a 3 by 3 grid of buttons, where each button represent a space in the Tic-Ta-teo board
            # We use the lambda function to define command for each button. When a button is clicked,
            # it will call the click method with the row and column of the button as arguments
            row = []  # First loop creates a single list
            for j in range(3):  # Second loop creates 3 buttons, add them to the row list which was initialized. This
                # represents a single row of three buttons in the row list
                button = ttk.Button(self.canvas, text="", command=lambda row=i, column=j: self.click(row, column), style="My.TButton")
                button.place(x=j*100, y=i*100, width=100, height=100)
                self.x = j*100 + random.randint(0, 90)
                self.y = i*100 + random.randint(0, 90)
                row.append(button)
            self.buttons.append(row)  # The row of three buttons is added to the buttons overall list, as list items.
            print(self.buttons)
            # after three consecutive loops, will have three list or row button list inside the main button list.
            # this will typically be our 3 by 3 button grid, or more metaphorically a three by three map grid if we use
            # the line break \n
            self.style.map("My.TButton", foreground=[("active", "green"), ("disabled", "red"), ("pressed", "#ffd700")])
        # self.style.map("My.TButton", foreground=[("pressed", "red"), ("active", "green")], background=[("pressed", "!disabled", "orange"), ("active", "lightgreen")])

    def load_scores(self):
        """
        Opens a score.txt file in read mode, then it updates a player score.
        The for loop reads the file line by line, splitting each line via a comma as delimiter.

        :return:
        """
        try:
            with open("score.txt", "r") as file:
                for line in file:
                    player, score = line.strip().split(",")
                    self.scores[player] = int(score)  # Updates the scores dictionary with player's name as key and their score as value
        except FileNotFoundError:
            pass

    def save_scores(self):
        """
        Initializes the score.txt file in w mode and write the players name and score to it.
        Opens the score file and write the score and name to it. It uses f-string formatting.
        :return:
        """
        with open("score.txt", "w") as file:
            for player, score in self.scores.items():
                file.write(f"{player}, {score}\n")

    def click(self, row, column):
        """
        This function update buttons with the right player text when clicked after checking if the button is empty.
        From the the it calls the check_win and check draw function to confirm this states and end the game.
        The check win function must be called before the check draw so the game works as intended.

        :param row: The row gotten from the lambda function when a button is created.
        :param column: The column gotten from the lambda function when a button is created.
        :return: None
        """
        if self.buttons[row][column]['text'] == "":
            self.buttons[row][column]['text'] = self.player_turn
            buttons = self.check_win()
            if buttons:
                self.blink_win_line(winning_line=buttons)
                self.game_over()
            elif self.check_draw():
               self.game_over(message="It's a Draw!")
            self.player_turn = "Y" if self.player_turn == "X" else "X"
        else:
            self.buttons[row][column]["style"] = "Red.TButton"

    def check_win(self):
        """
        The first for loop picks a row(A list) on each iteration the variable
        row is simply a list of three buttons.
        Then, the if uses indexing to check if the text of the 0th,
         first and second are all the same and not empty strings.
         The second for loop iterates three times over the list,
         for each iteration the value of each nested column is held
          constant and we index row 1, 2 and 3, essentially checking a column on each iteration.

        :return:
        """
        for row in self.buttons:
            if row[0]['text'] == row[1]['text'] == row[2]['text'] != "":
                return row[0], row[1], row[2]
        for column in range(3):
            if self.buttons[0][column]['text'] == self.buttons[1][column]['text'] == self.buttons[2][column]['text'] != "":
                return self.buttons[0][column], self.buttons[1][column], self.buttons[2][column]
        if self.buttons[0][0]['text'] == self.buttons[1][1]['text'] == self.buttons[2][2]['text'] != "":
            # Checks leading diagonal
            return self.buttons[0][0], self.buttons[1][1], self.buttons[2][2]
        if self.buttons[0][2]['text'] == self.buttons[1][1]['text'] == self.buttons[2][0]['text'] != "":
            # Checks lagging diagonal
            return self.buttons[0][2], self.buttons[1][1], self.buttons[2][0]
        return None

    def check_draw(self):
        """
        This button iterates over each row(nested button list).
        It checks if any of the buttons have and empty text field.
        If yes, it returns false meaning the game is still going on.
        If all buttons are with text, it returns true meaning its a draw.
        :return:
        """
        for row in self.buttons:
            for button in row:
                if button["text"] == "":
                    return False
        for row in self.buttons:
            for button in row:
                button["state"] = "disabled"
            self.window.update()
            time.sleep(0.5)
        for row in self.buttons:
            for button in row:
                button["state"] = "normal"
            self.window.update()
            time.sleep(0.5)
        return True

    def blink_win_line(self, winning_line: tuple):
        """
        This function b links the wining line, as a firm of feedback to user.
        It accepts a tuple of the winning line from the check win function.
        :param winning_line: The wining line tuple.
        It uses the .update_idletask() method which essentially process any idle GUI but deos not listen to user input.
        This ensures players can't bypass the win to continue playing.
        Creates a top level window, with button. The buttons are listen to  by a lambda function which takes no
          argument, but rather a list of expression to be executed.
        :return: None
        """
        self.window.update_idletasks()  # Updates window and not process events.
        for _ in range(3):

            for button in winning_line:
                button["state"] = "disabled"
            self.window.update_idletasks()
            time.sleep(0.5)
            for button in winning_line:
                button["state"] = "normal"
            self.window.update_idletasks()
            time.sleep(0.5)
        self.window.update_idletasks()  # Update display one last time

    def game_over(self, message=""):
        if message:
            messagebox.showinfo("Game Over", message)
        else:
            self.scores[self.player_turn] += 1
            messagebox.showinfo("Game Over", f"Player {self.player_turn} wins!\nScore - X:    {self.scores['X']},     Y:    {self.scores['Y']}")
        self.save_scores()

        caffetti_canvas = tk.Canvas(self.window, width=300, height=300)
        caffetti_canvas.place(x=self.x, y=self.y)
        for _ in range(50):
            x = random.randint(0, 300)
            y = random.randint(0, 300)
            caffetti_canvas.create_oval(self.x, self.y, x+5, y+5, fill="blue")
            self.window.update_idletasks()
            self.window.after(50)
        self.window.after(2000, caffetti_canvas.destroy)
        game_over_window = tk.Toplevel(self.window)
        game_over_window.title("Game Over")
        reset_button = tk.Button(game_over_window, text="Reset Game", command=lambda: [game_over_window.destroy(), self.reset_game()])
        reset_button.pack(pady=10)
        game_over_button = tk.Button(game_over_window, text="Game Over", command=lambda: [game_over_window.destroy(), self.window.quit()])
        game_over_button.pack(pady=10)

    def reset_game(self):
        """
        Clears all button text and return the button to their normal state.
        It also sets the current player to the initial player, (X)
        :return:
        """
        for row in self.buttons:
            for button in row:
                button["text"] = ""
                button["style"] = "My.TButton"
        self.player_turn = "X"


    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    game = TicTacToe()
    game.run()
