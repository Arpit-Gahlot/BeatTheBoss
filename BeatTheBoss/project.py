from tkinter import *
import mysql.connector
import PIL
import customtkinter
from PIL import Image
from tkinter.ttk import Progressbar
import time


def check_answer(answer, current_question):

    global numberOfCorrectAnswers
    global gameOver
    if not gameOver:
        if answer.lower() == answersList[questionsList.index(current_question)]:
            if bar['value'] == 100:
                game_won()
                gameOver = True
            else:
                numberOfCorrectAnswers += 1
                resultLabel.set('Correct Answer')
                healthpoints_manager(True)
        else:
            healthpoints_manager(False)
            resultLabel.set('Wrong Answer')

        display_question()


def healthpoints_manager(is_answer_correct):

    current_damage = 0
    required_damage = 25
    damage_speed = 1

    if is_answer_correct:
        while current_damage < required_damage:
            time.sleep(0.05)
            bar['value'] += (damage_speed/required_damage)*25
            damage.set('current damage dealt: '+str(int(bar['value'])))
            current_damage += damage_speed
            window.update_idletasks()


def display_question():

    global gameOver
    if not gameOver:
        if len(question_indexes_already_answered) < 5:
            display_question_helper()
        else:
            game_lost()
            gameOver = True


def display_question_helper():

    import random

    unique_question_found = False
    while not unique_question_found:
        question_index = random.randint(0, len(questionsList) - 1)

        if not check_if_question_asked(question_index):
            unique_question_found = True
            current_question = questionsList[question_index]
            questionLabel.set(current_question)
            display_options(question_index)


def check_if_question_asked(question_index):

    if question_index not in question_indexes_already_answered:
        question_indexes_already_answered.append(question_index)
        return False
    else:
        return True


def display_options(question_index):

    option_a = optionsList[question_index][0]
    option_b = optionsList[question_index][1]
    option_c = optionsList[question_index][2]
    option_d = optionsList[question_index][3]

    current_question = questionsList[question_index]

    update_button_a(option_a, current_question)
    update_button_b(option_b, current_question)
    update_button_c(option_c, current_question)
    update_button_d(option_d, current_question)


def update_button_a(text, current_question):
    button_a = Button(frame, text=text, height=1, width=10, font=('Arial', 20, 'bold'),
                      command=lambda: check_answer(text, current_question))
    button_a.grid(row=0, column=0)


def update_button_b(text, current_question):
    button_b = Button(frame, text=text, height=1, width=10, font=('Arial', 20, 'bold'),
                      command=lambda: check_answer(text, current_question))
    button_b.grid(row=0, column=1)


def update_button_c(text, current_question):
    button_c = Button(frame, text=text, height=1, width=10, font=('Arial', 20, 'bold'),
                      command=lambda: check_answer(text, current_question))
    button_c.grid(row=0, column=2)


def update_button_d(text, current_question):
    button_d = Button(frame, text=text, height=1, width=10, font=('Arial', 20, 'bold'),
                      command=lambda: check_answer(text, current_question))
    button_d.grid(row=0, column=3)


def game_won():
    resultLabel.set('You defeated the boss')


def game_lost():
    resultLabel.set('You couldn\'t deal enough damage, you lost' )


# connect to the database

databasePassword = input('To begin, enter the root@localhost password to connect to the database:')

myDB = mysql.connector.connect(host='localhost',
                               user='root',
                               passwd=databasePassword)

# Create a cursor object
myCursor = myDB.cursor()
myCursor.execute("CREATE DATABASE IF NOT EXISTS game1")
myCursor.execute("USE game1")

print('Successfully connected to the localhost! Enter your name below once your\'re ready')
print('')
name = input('Enter your name:')
print('Now switch to the window which just opened')


# Create a window object
window = Tk()
window.title('Beat The Boss')
window.geometry('800x600')

# Assign the background image to a variable
image = PIL.Image.open('Images/Mordekaiser.png')
backgroundImage = customtkinter.CTkImage(image, size=(800, 600))

# Label for placing the background image
bgLabel = customtkinter.CTkLabel(window, image=backgroundImage)
bgLabel.place(x=0,y=0)

# Create the required variables
gameOver = False
numberOfCorrectAnswers = 0
question_indexes_already_answered = []
questionsList = ['what is the square root of 169?',
                 'which game recently crossed 1 trillion views on Youtube?',
                 'Which is the only mammal that can fly?',
                 'Which is the hottest planet in the Solar system?',
                 'Which is the largest bone in the human body?']
answersList = ['13', 'minecraft', 'bat', 'venus', 'femur']
optionsList = [['16', '13', '15', '11'],
               ['Fortnite', 'Battlefield', 'Minecraft', 'PUBG'],
               ['Ostrich', 'Swan', 'Bat', 'Flamingo'],
               ['Venus', 'Mercury', 'Mars', 'Jupiter'],
               ['Sternum', 'Maxilla', 'Ulna', 'Femur']]

# Label1 for displaying the question
questionLabel = StringVar()
label1 = Label(window,
               textvariable=questionLabel,
               font=('Arial', 15, 'bold'),
               bg='white',
               width=60,
               height=3)
label1.pack(pady=10)

# Add Label1 to the window
frame = Frame(window)
frame.pack(pady=10)

# Progressbar to display the damage dealt to the boss
bar = Progressbar(window, orient=HORIZONTAL, length=500)
bar.pack(pady=10)

# label for showing the damage dealt
damage = StringVar()
damageLabel = Label(window, textvariable=damage)
damageLabel.pack()
damage.set('current damage dealt: 0')

# label2 for showing the question result and game result
resultLabel = StringVar()
label2 = Label(window,
               textvariable=resultLabel,
               font=('Arial', 15, 'bold'),
               foreground='white',
               bg='brown',
               width=60,
               height=3)
label2.pack(pady=10)

display_question()

window.mainloop()

if gameOver:

    # Upload the scores to the connected database
    data = "insert into scores values(%s, %s)"
    myCursor.execute(data,(name, numberOfCorrectAnswers ))
    myDB.commit()

    # Display the scores of the players who have played the game so far
    print('scores of the players are:-')
    print('Name\tScore')
    myCursor.execute('select * from scores')
    results = myCursor.fetchall()
    for j in results:
        print(j[0] + '\t' + str(j[1]))
    print('Thanks for playing!')






