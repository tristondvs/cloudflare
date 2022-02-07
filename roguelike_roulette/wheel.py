from tkinter import *
from tkinter import messagebox
from db import Database
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

db = Database('games.db')

# lole
def bake_pie():
    plt.figure(figsize=(3,3))
    labels = db.fetch()
    values = []
    i = 0
    while i <= len(labels):
        values.append(len(labels)/100)
        i += 1
    game_wheel = plt.pie(values, labels=labels)
    return game_wheel

# Imports list of games from games.db
def populate_list():
    games_list.delete(0, END)
    for row in db.fetch():
        if games_list == []:
            print('Games database is completely empty!')
        else:
            print('Refreshing list of games within games.db...')
            games_list.insert(END, row)
            bake_pie()
            plt.show()

def add_game():
    if game_name.get() == '':
        messagebox.showerror('Required Fields', 'Please enter a game name within the Enter Game Name field.')
        return
    db.insert(game_name.get())
    games_list.delete(0, END)
    games_list.insert(END, (game_name.get()))
    populate_list()
    print('Added Game: ' + (game_name.get()))
    games_entry.delete(0, END)

def select_game(event):
    global game_choice
    try:
        index_of_games = games_list.curselection()[0]
        game_choice = games_list.get(index_of_games)
    except IndexError:
        print('Games database is completely empty, no selection made!')
    else:
        games_entry.delete(0, END)

def remove_game():
    #global game_choice
    try:
        print('Removing Game: ' + str(game_choice[1]))
    except NameError:
        messagebox.showerror('Select Game', 'Please select a game from the list, and then use the Remove Game option.')
        return
    else:
        games_list.delete(0, END)
        db.remove(game_choice[0])
        populate_list()



#def clear_games():
#    messagebox.askquestion('Clear All Games', 'Are you sure you want to remove all games from the list?', icon='warning')
#    if messagebox == 'yes':
#        db.clear_list()

# create window object
app = Tk()

# Add games to list
game_name = StringVar()
games_label = Label(app, text='Enter Game Name', font=('bold', 14), pady=10, padx=5)
games_label.grid(row=0, column=0, sticky=W)
games_entry = Entry(app, textvariable=game_name)
games_entry.grid(row=0, column=1)
#Show a list of games
games_list = Listbox(app, height=5, width=65, border=1)
games_list.grid(row=2, column=0, columnspan=3, rowspan=1, padx=10, pady=10, sticky=W)
# Adding a scroll bar
scrollbar = Scrollbar(app)
scrollbar.grid(row=2, column=4)
# Bind the scrollbar to the list of games if it gets too large
games_list.configure(yscrollcommand=scrollbar.set)
scrollbar.configure(command=games_list.yview)
# Bind select
games_list.bind('<<ListboxSelect>>', select_game)

# Adding buttons
add_button = Button(app, text='Add Game', width=12, command=add_game)
add_button.grid(row=0, column=3, padx=10)
remove_button = Button(app, text='Remove Game', width=12, command=remove_game)
remove_button.grid(row=4, column=0, padx=10, pady=10)
# Adding wheel

app.title('Roguelike Roulette Spinwheel')
#Adjust the size of the window when the app opens
app.geometry('600x200')

# Populate list of games
populate_list()

## TODOS:
# Find a way to make the wheel spin and lands on a choice
#   - See if we can add the game names within the pie slices; or hide them until a choice is made
# Find a way to determine the string within the object
# Should I worry about creating the pie chart on screen before the wheel is spun? Or should I focus on hosting the 
# piechart on a webpage so it can be used as a browser source via OBS?
# Integrate twitchio to change game name based on selection?

# Start program
app.mainloop()
