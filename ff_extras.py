"""
Alasdair Smith
Started 20/12/2016

Module for the Fighting Fantasy Program
Includes the initial decision question GUI, a few helper functions,
    and code to run the whole program

For Fighting Fantasy Gamebooks:
Ian Livingstone's Caverns of the White Witch & similar
"""
from tkinter import *
from tkinter.font import *
#from tkinter.ttk import * #Can't use because it's buttons don't support fonts
import ff_charactersheet
import ff_combatscreen
import random
import copy

#THIS IS THE INITIAL QUESTION GUI FOR THE PROGRAM
class QuestionGui:
    """
    Full program or just combat calculator button window
    
    Attributes:
    questionwindow: the window holding the gui
    full_or_combat: the word states the program to be run, None if not chosen
    """
    
    def __init__(self, window):
        """Initialises, then opens the gui for the question to be answered"""
        self.questionwindow = window
        self.full_or_combat = None
        
        #Set custom fonts
        self.headerfont = Font(family=ff_charactersheet.FONT_FAMILY, size=ff_charactersheet.BIG_FONT)
        
        #Finish by running the main question screen
        self.run_question()
    
    def run_question(self):
        """Brings up a window asking whether the user wants to run just the
        combat calculator or the full gui"""
        text_question = "What do you want to do?"
        text_full =   "Build Character Sheet"
        text_combat = "   Fight a Battle!   " #Try get it with equal spacing to the above line
        question_label = Label(self.questionwindow, font=self.headerfont, text=text_question)
        combat_button = Button(self.questionwindow, font=self.headerfont, text=text_combat,
                               command=lambda: self.choose_mode("combat"))
        full_button = Button(self.questionwindow, font=self.headerfont, text=text_full,
                             command=lambda: self.choose_mode("full"))
        question_label.grid(row=0, column=0, columnspan=2, pady=10)
        combat_button.grid(row=1, column=1, padx=10, pady=10, ipadx=35, ipady=5)
        full_button.grid(row=1, column=0, padx=10, pady=10, ipadx=35, ipady=5)
    
    def choose_mode(self, mode_choice):
        """Saves mode choice and closes the question window"""
        self.questionwindow.destroy()
        self.full_or_combat = mode_choice


def roll_dice(dice=1, sides=6):
    """Returns an integer representing a throw of [dice] [sides] sided dice"""
    return random.randint(dice, (dice * sides))

def make_default_enemy():
    """Creates a basic enemy Character from charactersheet global ENEMY_NAME"""
    return ff_charactersheet.Character(name=ff_charactersheet.ENEMY_NAME)

def copy_dict(dictionary):
    """Returns a NEW dictionary with the same values as the old one"""
    return copy.deepcopy(dictionary)

def run_code():
    """Little bit of code that runs everything"""
    questionwindow = Tk()
    question_gui = QuestionGui(questionwindow)
    questionwindow.mainloop()
    
    blank_character = ff_charactersheet.Character()
    
    if question_gui.full_or_combat == "combat":
        ff_combatscreen.run_combat_gui(blank_character, make_default_enemy())
    elif question_gui.full_or_combat == "full":
        characterwindow = Tk()
        character_gui = ff_charactersheet.CharacterSheetGui(characterwindow, blank_character)
        characterwindow.mainloop()
    #else window was closed by other means, so take no further action

def main():
    """Starts the entire program"""
    if __name__ == "__main__":
        run_code()

main()