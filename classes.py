import tkinter as tk
BACKGROUND_COLOR = "#B1DDC6"


class MainCanvas(tk.Canvas):
    def __init__(self):
        super().__init__()
        self.canvas_def = tk.Canvas(width=805, height=535, bd=-2, bg=BACKGROUND_COLOR)
        self.canvas_def.grid(column=1, row=2, columnspan=3)


class Card(MainCanvas):

    def __init__(self):
        super().__init__()
        self.time = 3
        self.count = 0
        self.front = tk.PhotoImage(file="images/card_front.png")
        self.back = tk.PhotoImage(file="images/card_back.png")
        self.canvas_def.create_image(405, 275, image=self.front)


class Buttons(tk.Button):
    def __init__(self, image, pos, root_in, command):
        super().__init__()
        self.image = tk.PhotoImage(file=image)
        self.root = root_in
        self.button_def = tk.Button(
            image=self.image, highlightthickness=0, padx=10, pady=10, bd=0, command=command
        )
        self.button_def.grid(column=pos[0], row=pos[1])


class Labels(tk.Label):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.configure(width=15, anchor="center")
