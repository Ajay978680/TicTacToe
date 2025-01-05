import tkinter as tk
from tkinter import messagebox
import random
from PIL import Image, ImageTk

class TicTacToe:
    def __init__(self, master):
        self.master = master
        self.master.title("Tic Tac Toe")
        self.master.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))  # Set window size to full screen

        # Load background image
        self.background_image = Image.open("back.png")
        self.background_image = self.background_image.resize((root.winfo_screenwidth(), root.winfo_screenheight()))
        self.background_image = ImageTk.PhotoImage(self.background_image)

        # Initialize variables
        self.board = [' ' for _ in range(9)]
        self.current_player = 'X'
        self.difficulty = 'Medium'
        self.player_name = None
        self.player_score = 0
        self.computer_score = 0

        # Create widgets
        self.create_widgets()

    def create_widgets(self):
        # Background Image
        background_label = tk.Label(self.master, image=self.background_image)
        background_label.place(relwidth=1, relheight=1)

        # Title Label with red color and spacing
        title_label = tk.Label(self.master, text="TIC TAC TOE", font=('Times New Roman', 30, 'bold'), fg='black', bg='teal')
        title_label.pack(pady=10)

        # Login Page
        self.login_frame = tk.Frame(self.master, bg='teal')
        self.login_frame.pack(pady=20)

        tk.Label(self.login_frame,font=('Arial', 20), text="Enter Your Name:", bg='teal', fg='black').grid(row=0, column=0)
        self.name_entry = tk.Entry(self.login_frame)
        self.name_entry.grid(row=0, column=1, padx=10)
        login_button = tk.Button(self.login_frame, font=('Arial', 15),text="Start", command=self.start_game, bg='teal', fg='black')
        login_button.grid(row=1, columnspan=2, pady=10)

        # Initialize game board (empty for now)
        self.buttons = []
        self.board_frame = tk.Frame(self.master, highlightthickness=1, highlightbackground="black", bg='teal')
        self.create_board()

        # Difficulty Dropdown with spacing
        tk.Label(self.master, text="Difficulty:",font=('Arial', 15), bg='teal', fg='black').pack()
        self.difficulty_var = tk.StringVar(value="Medium")
        tk.OptionMenu(self.master, self.difficulty_var, "Easy", "Medium", "Hard").pack(pady=5)

        # Player's Turn Label with spacing
        self.status_label = tk.Label(self.master, text="", font=('Arial', 25), bg='teal', fg='black')
        self.status_label.pack(pady=10)

        # Timer Label with clock symbol
        self.timer_label = tk.Label(self.master, text="", font=('Arial', 50, 'bold'), bg='teal', fg='black')
        self.timer_label.place(relx=0.1, rely=0.5, anchor='w')  # Place on the left side center with a bit of offset
        self.timer_label.config(text="⏰")

        # Player and Computer Score Labels
        self.player_score_label = tk.Label(self.master, text=f"Player Score: {self.player_score}", font=('Arial', 25), bg='teal', fg='black')
        self.player_score_label.place(relx=0.85, rely=0.5, anchor='center')  # Place on the right side and center with a bit of offset
        self.computer_score_label = tk.Label(self.master, text=f"Computer Score: {self.computer_score}", font=('Arial', 25), bg='teal', fg='black')
        self.computer_score_label.place(relx=0.85, rely=0.6, anchor='center')  # Place on the right side and center with a bit of offset

        # Initially hide the game board and other widgets
        self.hide_board()

    def create_board(self):
        for i in range(3):
            for j in range(3):
                button = tk.Button(self.board_frame, text='', font=('Arial', 20), width=8, height=4,
                                   command=lambda row=i, col=j: self.make_move(row, col))
                button.grid(row=i, column=j, padx=5, pady=5)
                self.buttons.append(button)

    def hide_board(self):
        self.board_frame.pack_forget()
        self.status_label.pack_forget()
        self.timer_label.pack_forget()
        self.player_score_label.pack_forget()
        self.computer_score_label.pack_forget()

    def show_board(self):
        self.board_frame.pack(padx=10, pady=10)
        self.status_label.pack(pady=10)
        self.timer_label.place(relx=0.1, rely=0.5, anchor='w')
        self.player_score_label.place(relx=0.85, rely=0.5, anchor='center')
        self.computer_score_label.place(relx=0.85, rely=0.6, anchor='center')

    def start_game(self):
        self.player_name = self.name_entry.get()
        if not self.player_name:
            messagebox.showwarning("Warning", "Please enter your name to start the game.")
            return
        self.status_label.config(text=f"{self.player_name}'s Turn")
        self.show_board()

    def make_move(self, row, col):
        self.reset_timer()
        index = 3 * row + col
        if self.board[index] == ' ':
            self.board[index] = self.current_player
            self.buttons[index].config(text=self.current_player)
            if self.current_player == 'X':
                self.buttons[index].config(fg='blue')
            else:
                self.buttons[index].config(fg='red')
            if self.check_winner():
                if self.current_player == 'X':
                    self.player_score += 1
                    messagebox.showinfo("Tic Tac Toe", f"{self.player_name} wins!")
                else:
                    self.computer_score += 1
                    messagebox.showinfo("Tic Tac Toe", "Computer wins!")
                self.update_scores()
                self.reset_board()
            elif ' ' not in self.board:
                messagebox.showinfo("Tic Tac Toe", "It's a draw!")
                self.reset_board()
            else:
                self.current_player = 'O' if self.current_player == 'X' else 'X'
                if self.current_player == 'O':
                    self.status_label.config(text="Computer's Turn")
                    self.computer_move()
                else:
                    self.status_label.config(text=f"{self.player_name}'s Turn")
                    self.start_timer()

    def computer_move(self):
        if self.difficulty == 'Easy':
            index = random.choice([i for i, cell in enumerate(self.board) if cell == ' '])
        elif self.difficulty == 'Medium':
            index = self.find_winning_move('O') or self.find_winning_move('X') or \
                    random.choice([i for i, cell in enumerate(self.board) if cell == ' '])
        else:  # Hard
            best_move = self.minimax(2, 'O')
            index = best_move[0]
        self.make_move(index // 3, index % 3)

    def find_winning_move(self, player):
        for i in range(9):
            if self.board[i] == ' ':
                self.board[i] = player
                if self.check_winner():
                    self.board[i] = ' '
                    return i
                self.board[i] = ' '
        return None

    def minimax(self, depth, player):
        if player == 'O':
            best = [-1, float('-inf')]
        else:
            best = [-1, float('inf')]

        if depth == 0 or self.check_winner():
            score = self.evaluate()
            return [-1, score]

        for i in range(9):
            if self.board[i] == ' ':
                self.board[i] = player
                score = self.minimax(depth - 1, 'O' if player == 'X' else 'X')
                self.board[i] = ' '
                score[0] = i

                if player == 'O':
                    if score[1] > best[1]:
                        best = score
                else:
                    if score[1] < best[1]:
                        best = score
        return best

    def evaluate(self):
        score = 0
        lines = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]
        for line in lines:
            if self.board[line[0]] == self.board[line[1]] == self.board[line[2]] != ' ':
                if self.board[line[0]] == 'O':
                    return 1
                elif self.board[line[0]] == 'X':
                    return -1
        return score

    def check_winner(self):
        lines = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]
        for line in lines:
            if self.board[line[0]] == self.board[line[1]] == self.board[line[2]] != ' ':
                return True
        return False

    def reset_board(self):
        for i in range(9):
            self.board[i] = ' '
            self.buttons[i].config(text='')
        self.current_player = 'X'
        self.status_label.config(text=f"{self.player_name}'s Turn")
        self.reset_timer()

    def start_timer(self):
        self.timer = 10
        self.timer_label.config(text=str(self.timer))
        self.timer_running = True
        self.timer_countdown()

    def timer_countdown(self):
        if self.timer_running:
            if self.timer > 0:
                self.timer -= 1
                self.timer_label.config(text=str(self.timer))
                if self.timer <= 3:
                    if self.timer % 2 == 0:
                        self.timer_label.config(bg='red', fg='white')
                    else:
                        self.timer_label.config(bg=self.master.cget('bg'), fg='red')
                self.master.after(1000, self.timer_countdown)
            else:
                self.timer_running = False
                self.timer_label.config(text="Time's up!")
                self.current_player = 'O'
                self.status_label.config(text="Computer's Turn")
                self.computer_move()

    def reset_timer(self):
        self.timer_running = False
        self.timer_label.config(text="", bg=self.master.cget('bg'), fg='black')

    def update_scores(self):
        self.player_score_label.config(text=f"Player Score: {self.player_score}")
        self.computer_score_label.config(text=f"Computer Score: {self.computer_score}")

root = tk.Tk()
game = TicTacToe(root)
root.mainloop()
