import tkinter as tk
import random

class BingoCard:
    def __init__(self, master):
        self.master = master
        self.master.title("Bingo Card Generator")
        
        self.bingo_card = []
        self.label_refs = []
        self.selected = [[False for _ in range(5)] for _ in range(5)]
        self.card_hash = None
        self.create_card()
        self.draw_card()

    def create_card(self):
        self.bingo_card = []
        columns = {
            0: list(range(1, 16)),
            1: list(range(16, 31)),
            2: list(range(31, 46)),
            3: list(range(46, 61)),
            4: list(range(61, 76))
        }
        
        for col in range(5):
            random.shuffle(columns[col])
            column_values = columns[col][:5]
            self.bingo_card.append(column_values)

        self.bingo_card[2][2] = "Free"
        self.selected[2][2] = True

        # カード全体のハッシュ値を計算
        self.card_hash = hash(tuple(tuple(row) for row in self.bingo_card))
        print(f"Card Hash: {self.card_hash}")

    def draw_card(self):
        for i in range(5):
            row_labels = []
            for j in range(5):
                value = self.bingo_card[j][i]
                bg_color = "yellow" if self.selected[j][i] else "white"
                label = tk.Label(self.master, text=value, width=8, height=4, relief="solid", bg=bg_color)
                label.grid(row=i, column=j, padx=5, pady=5)
                label.bind("<Button-1>", lambda e, i=i, j=j: self.select_number(i, j))
                row_labels.append(label)
            self.label_refs.append(row_labels)

    def select_number(self, row, col):
        if not self.selected[row][col]:
            self.selected[row][col] = True
            self.label_refs[row][col].config(bg="yellow")
            print(f"Selected: {self.bingo_card[col][row]}")
            self.check_bingo()

    def check_bingo(self):
        self.clear_highlights()

        for i in range(5):
            if all(self.selected[i][j] for j in range(5)):
                self.highlight_row(i, "green")
            elif sum(self.selected[i][j] for j in range(5)) == 4:
                self.highlight_row(i, "orange", highlight_unselected=False)

            if all(self.selected[j][i] for j in range(5)):
                self.highlight_column(i, "green")
            elif sum(self.selected[j][i] for j in range(5)) == 4:
                self.highlight_column(i, "orange", highlight_unselected=False)

        if all(self.selected[i][i] for i in range(5)):
            self.highlight_diagonal(True, "green")
        elif sum(self.selected[i][i] for i in range(5)) == 4:
            self.highlight_diagonal(True, "orange", highlight_unselected=False)

        if all(self.selected[i][4 - i] for i in range(5)):
            self.highlight_diagonal(False, "green")
        elif sum(self.selected[i][4 - i] for i in range(5)) == 4:
            self.highlight_diagonal(False, "orange", highlight_unselected=False)

    def highlight_row(self, row, color, highlight_unselected=True):
        for col in range(5):
            if self.selected[row][col] or highlight_unselected:
                self.label_refs[row][col].config(bg=color)

    def highlight_column(self, col, color, highlight_unselected=True):
        for row in range(5):
            if self.selected[row][col] or highlight_unselected:
                self.label_refs[row][col].config(bg=color)

    def highlight_diagonal(self, left_to_right, color, highlight_unselected=True):
        if left_to_right:
            for i in range(5):
                if self.selected[i][i] or highlight_unselected:
                    self.label_refs[i][i].config(bg=color)
        else:
            for i in range(5):
                if self.selected[i][4 - i] or highlight_unselected:
                    self.label_refs[i][4 - i].config(bg=color)

    def clear_highlights(self):
        for i in range(5):
            for j in range(5):
                if not self.selected[i][j]:
                    self.label_refs[i][j].config(bg="white")

if __name__ == "__main__":
    root = tk.Tk()
    bingo = BingoCard(root)
    root.mainloop()
