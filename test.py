import pprint
import tkinter as tk
from tkinter import ttk, messagebox
window = tk.Tk()
window.title("Tic-Tac-Toe")
window.geometry("600x600")
canvas = tk.Canvas(window, width=300, height=300)
buttons = []
for i in range(3):
    row = []
    for j in range(3):
        button = ttk.Button(canvas, command=lambda row=i, column=j: click(row, column))
        row.append(button)
    buttons.append(row)


pprint.pp(buttons)

def click(n, m):
    pass