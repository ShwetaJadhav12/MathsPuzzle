import tkinter as tk
from tkinter import messagebox
import random
import time

class NumberCrossword:
    
    def __init__(self, parent,score=0):
        self.parent = parent
        
        self.root = tk.Toplevel(parent)
        self.root.title("Number Crossword Puzzle")
        
        self.root.geometry("400x400")
        self.root.configure(bg="lightblue")
        
        self.score = score  # Initialize score
        self.timer_running = False
        self.time_left = 30
        self.start_time = None

        self.create_widgets()
        
        # Start the timer
        self.start_timer()

    def generate_clues(self):
        # Generate random clues for rows and columns
        self.row_clues = [random.randint(1, 10) for _ in range(2)]
        
        # Calculate the sum of the rows
        row_sum = sum(self.row_clues)

        # Generate random clues for columns
        self.column_clues = [random.randint(1, row_sum) for _ in range(2)]
        for i in range(len(self.column_clues)):
            column_sum = sum(self.row_clues[j] for j in range(len(self.row_clues)) if j != i)
            self.column_clues[i] = column_sum
    def create_widgets(self):
        self.generate_clues()

        # Frame to hold puzzle elements
        puzzle_frame = tk.Frame(self.root, bg="lightblue",height="14")
        puzzle_frame.pack(padx=10, pady=10)

        # Display row clues
        for i, clue in enumerate(self.row_clues):
            tk.Label(puzzle_frame, text=str(clue), width=5, height=2, relief="groove", bg="lightgreen").grid(row=i, column=0, padx=5, pady=5)

        # Display column clues
        for j, clue in enumerate(self.column_clues):
            tk.Label(puzzle_frame, text=str(clue), width=5, height=2, relief="groove", bg="lightgreen").grid(row=2, column=j+1, padx=5, pady=5)

        # Entry fields for the grid
        self.entries = []
        for i in range(2):
            row_entries = []
            for j in range(2):
                entry = tk.Entry(puzzle_frame, width=5, font=('Helvetica', 12))
                entry.grid(row=i, column=j+1, padx=5, pady=5)
                row_entries.append(entry)
            self.entries.append(row_entries)

        # Check button
        self.check_button = tk.Button(self.root, text="Check", command=self.check_solution, bg="lightgrey", width=8, height=2, font=('Helvetica', 12))
        self.check_button.pack(pady=10)

        # Timer label
        self.timer_label = tk.Label(self.root, text="Time left: 30", bg="pink", font=('Helvetica', 12))
        self.timer_label.pack(pady=10)

        # Score label
        self.score_label = tk.Label(self.root, text=f"Score: {self.score}", font=('Helvetica', 12))
        self.score_label.pack(pady=10)

        # Menu button
        self.menu_button = tk.Button(self.root, text="Menu",bg="lightgrey", command=self.show_main_menu, width=8, height=2, font=('Helvetica', 12))
        self.menu_button.pack(pady=10)

    def start_timer(self):
        if not self.timer_running:
            self.timer_running = True
            self.start_time = time.time()
            self.update_timer()

    def update_timer(self):
        if self.time_left > 0 and self.timer_running:
            self.timer_label.config(text=f"Time left: {self.time_left}")
            self.time_left -= 1
            self.root.after(1000, self.update_timer)
        else:
            self.timer_running = False
            if self.time_left == 0:
                response = messagebox.askyesno("Time's Up!", "Time's up! Would you like to try again?")
                if response:
                    open_number_crossword_window()
                    self.reset_puzzle()
                else:
                    self.root.destroy()
                    self.parent.deiconify()  # Show the main menu window

    def reset_puzzle(self):
        self.time_left = 30
        self.create_widgets()  # Generate new puzzle widgets
        self.start_timer()  # Start the timer again

    def check_solution(self):
        # Stop the timer
        self.timer_running = False
        elapsed_time = time.time() - self.start_time

        # Check sum of rows
        for i, clue in enumerate(self.row_clues):
            row_sum = sum(int(entry.get() or 0) for entry in self.entries[i])
            if row_sum != clue:
                messagebox.showerror("Incorrect", f"Sum of numbers in Row {i+1} is incorrect.")
                self.start_timer()  # Resume the timer from where it stopped
                return

        # Check sum of columns
        for j, clue in enumerate(self.column_clues):
            column_sum = sum(int(entry.get() or 0) for entry in [row[j] for row in self.entries])
            if column_sum != clue:
                messagebox.showerror("Incorrect", f"Sum of numbers in Column {j+1} is incorrect.")
                self.start_timer()  # Resume the timer from where it stopped
                return

        # If all checks pass, show congratulatory message
        time_taken = int(elapsed_time)
        self.score += 1  # Increase score
        self.score_label.config(text=f"Score: {self.score}")
        messagebox.showinfo("Congratulations", f"Puzzle solved successfully!\nTime taken: {time_taken} seconds\n your score is: {self.score}")
        
       
        response = messagebox.askyesno("More Puzzles", "Would you like to solve more puzzles?")
        self.score_label.config(text=f"Score: {self.score}")
        if response:
            self.root.destroy()
            open_number_crossword_window(self.score)
            
            #self.reset_puzzle()  # Generate new puzzle and start timer immediately
            
        else:
            self.root.destroy()
            self.parent.deiconify()  # Show the main menu window
    def open_number_crossword_window(prev_score):
        #self.score+=1
        root = tk.Tk()
        app = NumberCrossword(root,prev_score)
    def show_main_menu(self):
        self.root.destroy()
        self.parent.deiconify()  # Show the main menu window
    def exit(self):
        self.root.destroy()    
def display_riddle_instructions():
    instructions = "Welcome to the Number Crossword Puzzle Game!\n\n" \
                       "To solve the puzzle, you need to fill in the 2x2 grid with numbers " \
                       "such that the sums of rows and columns match the given clues.\n\n" \
                       "LETS START\n your score and time will be recorded"
    
    messagebox.showinfo("Instructions", instructions)
    open_number_crossword_window(score=0)
def open_number_crossword_window(score):
    root.withdraw()  # Hide the main window
    game = NumberCrossword(root,score)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Main Menu")
    root.geometry("250x150")
    root.configure(bg="lightblue")
    label = tk.Label(root, text="Welcome to Number Crossword Puzzle!",font="arial 26 bold",bg="pink")
    label.pack(padx=20,pady=10)
    riddles_button = tk.Button(root, text="2x2 Puzzle", command=display_riddle_instructions, bg="lightgreen", width=13, height=3, font=('Helvetica', 12))
    riddles_button.pack(pady=10)
    riddles_button = tk.Button(root, text="EXIT", command=exit, bg="lightgreen", width=10, height=3, font=('Helvetica', 12))
    riddles_button.pack(pady=10)


    root.mainloop()
