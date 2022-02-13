import io
import tkinter as tk
from tkinter import messagebox
import pandas
from random import choice
from classes import Buttons, Card, Labels
import datetime
from settings import LEARNING_, TRANSLATE_

BACKGROUND_COLOR = "#B1DDC6"
LEARNING = LEARNING_
TRANSLATE = TRANSLATE_

learning_words = {}
translated_words = {}
indexes = []
index = 0


def find_index():
    global indexes, index

    if len(indexes) > 0:
        new = choice(indexes)
        word.checked.add(new)
        index = new
        indexes.remove(new)

    else:
        make_deck()


def to_language():
    language.config(text=LEARNING, bg="white")
    word.configure(text=learning_words[index], bg="white")


def to_english():
    language.config(text="English", bg="#94c4ac")
    word.configure(text=translated_words[index].lower(), bg="#94c4ac")


def make_deck():

    global indexes, learning_words, translated_words
    df = pandas.read_csv("translations.csv")
    dictionary = df.to_dict()

    try:
        with open(f"{LEARNING}known.txt", "r") as f1:
            try:
                known = f1.read().split(",")
            except io.UnsupportedOperation:
                known = []
    except FileNotFoundError:
        f1 = open(f"{LEARNING}known.txt", "w")
        f1.close()
        known = []

    indexes = [i for i in range(len(dictionary[LEARNING])) if i not in known]
    learning_words = dictionary[LEARNING]
    translated_words = dictionary[TRANSLATE]
    update_tracker()


def is_known():
    print(index)
    if index != 0:
        word.known.add(index)
    change_card(2)
    update_tracker()


def not_known():
    print(index)
    if index != 0:
        word.unknown.add(index)
    change_card(3)
    update_tracker()


def update_tracker():
    print(len(word.known), len(word.unknown))
    if len(word.known) != 0 or len(word.unknown) != 0:
        tracker.configure(text=f"{len(word.known) } / {len(word.unknown)}")


def change_card(time):

    if len(word.checked) == len(learning_words):
        word.place_forget()
        language.place_forget()
        congrats.place(x=100, y=200)

    cards.canvas_def.delete(cards.front)
    cards.canvas_def.create_image(405, 275, image=cards.back)
    to_english()
    if time > 0:
        cards.count = root.after(1000, change_card, time - 1)
    else:
        find_index()
        cards.canvas_def.delete(cards.back)
        cards.canvas_def.create_image(405, 275, image=cards.front)
        print(index)
        to_language()


def reset():
    if messagebox.askokcancel(title="Reset Warning", message=f"This will reset all your progress for {LEARNING}, "
                                                             "are you sure?"):
        with open(f"{LEARNING}known.txt", "w") as f2:
            f2.write("")
            print("reset")
        with open(f"progress{LEARNING}.txt", "w") as f2:
            f2.write("")


def change_learn_language():

    global LEARNING, TRANSLATE
    df = pandas.read_csv("translations.csv")
    dictionaries = df.to_dict()

    languages = [key for key in dictionaries if "To" not in key]

    def selected(new):

        global LEARNING, TRANSLATE
        save_data()
        LEARNING = new
        sel.place_forget()
        tracker.configure(text="known / unknown")
        refresh()
        TRANSLATE = [key for key in dictionaries if 'To' in key and LEARNING in key][0]
        make_deck()
        sel.place_forget()
        change_card(0.1)

    language_var = tk.StringVar()
    language_var.set(f"{LEARNING}")
    sel = tk.OptionMenu(root, language_var, *languages, command=selected)
    sel.config(bd=0, font=("Arial", 51, "italic"), bg="grey", indicatoron=0, relief="raised")
    sel.place(x=273, y=160)


def save_data():
    with open(f"progress{LEARNING}.txt", "a") as f2:
        f2.write("*********************\n\n")
        f2.write(f"{datetime.datetime.today().strftime('%Y-%m-%d')}\n")
        f2.write(f"{len(word.known) + len(word.unknown)} words checked:")
        for ele in word.known:
            f2.write(f" {learning_words[ele]} |")
        for ele in word.unknown:
            f2.write(f" {learning_words[ele]} |")

        f2.write(f"\nYou knew {len(word.known)} words, well done!")

        f2.write(f"\n{len(word.unknown)} words to brush up on:")
        for ele in word.unknown:
            f2.write(f"\n{learning_words[ele]}")
        f2.write("\n\n")

    with open(f"{LEARNING}known.txt", "w") as f2:
        try:
            data = f2.read()

        except io.UnsupportedOperation:
            data = ""

        finally:
            string = [str(i) for i in word.known]
            new = ",".join(string)
            f2.write(f"{data},{new}".lstrip(",").rstrip(","))


def refresh():

    global index
    word.checked.clear()
    word.known.clear()
    word.unknown.clear()
    update_tracker()
    index = 0


root = tk.Tk()
root.title("Flashcards")
root.config(bg=BACKGROUND_COLOR, padx=50, pady=50)
root.minsize(800, 500)
cards = Card()

menu_bar = tk.Menu(root)
menu_bar.config(bg="white")
menu_item = tk.Menu(menu_bar, tearoff=0)
menu_item.config(bg="white", activebackground="black")

menu_item.add_command(label="Change Language", command=change_learn_language)
menu_item.add_command(label="Reset Data", command=reset)

menu_bar.add_cascade(label="Options", menu=menu_item)

root.config(menu=menu_bar)

yes_button = Buttons(image="images/right.png", pos=(3, 7), root_in=root, command=is_known)
no_button = Buttons(image="images/wrong.png", pos=(1, 7), root_in=root, command=not_known)

word = Labels(text=f"Word", bd=0, bg="white", font=("Arial", 55, "bold"))
word.checked = set()
word.known = set()
word.unknown = set()
word.place(x=50, y=260)

language = Labels(text=f"German", bd=0, bg="white", font=("Arial", 50, "italic"))
language.place(x=100, y=160)

congrats = Labels(text=f"Congrats! \nYou have mastered all \n{len(learning_words)} \nwords!", bd=0, bg="white",
                  font=("Arial", 30, "bold"))
congrats.config(width=25)

tracker = Labels(text=f"known / unknown", bd=0, bg="white", font=("Arial", 15, "bold"))
tracker.grid(column=2, row=0, sticky="ew")

make_deck()
to_language()

root.mainloop()
save_data()
with open("settings.py", "w") as f:
    f.write(f"LEARNING_ = '{LEARNING}'\nTRANSLATE_ = '{TRANSLATE}'")
