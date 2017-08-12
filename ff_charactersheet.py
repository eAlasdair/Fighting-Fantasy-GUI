"""
Alasdair Smith
Started 20/12/2016

Module for the Fighting Fantasy Program
Defines the Character Sheet GUI Class and Character Object Class

For Fighting Fantasy Gamebooks:
Ian Livingstone's Caverns of the White Witch & similar

Inlcudes all global value declarations except for the logbook globals

Initial stats are rolled using a 6-sided die as follows:
    1 roll + 6 for skill
    1 roll + 6 for luck
    2 rolls + 12 for stamina
"""
from tkinter import *
from tkinter.font import *
#from tkinter.ttk import * #Can't use because it's buttons don't support fonts
import ff_extras
import ff_combatscreen
import ff_logbook

FONT_FAMILY = "courier" #Use a monospaced font to make things easier
BIG_FONT = 24    #Standard font size
MIDDLE_FONT = 16 #For buttons
SMALL_FONT = 9   #For credits and the logbook
RATION_RESTORES = 4 #Stamina
DEFAULT_STATS = {"skill": 1, "luck": 1, "stamina": 1, "rations": 0}
NO_NAME = "Hero"
ENEMY_NAME = "Enemy"
INVENTORY_TEXT = "Items: "
CREDITS_TEXT = """
Made by Alasdair Smith (@ealasdair) for the Yogscast Charity Jingle Jam livesteams through December 2017

Started: Dec 2016    Last Edit: Aug 2017
"""

class Character:
    """Defines the Character class for Fighting Fantasy Main Characters
    
    Attributes:
    str   name - the character name, unique identifier
    dict  stats - dictionary of ints: {'skill', 'luck', 'stamina', 'rations'}
    str   potion - a separate item held by the character, no particular value
    str   inventory - all other items held by the character, formatted by the player
    
    Methods:
    change_char_stat: Changes the given stat of the character by the given amount
    roll_stats: Automatically assigns valid stats to the character
    """
    def __init__(self, name="Type Name Here", stats=DEFAULT_STATS, potion="", inventory=INVENTORY_TEXT):
        """Initialises the character, based on given data input"""
        self.name = name
        self.stats = stats
        self.potion = potion
        self.inventory = inventory
        if stats == DEFAULT_STATS:
            stats = self.roll_stats()
    
    def change_char_stat(self, stat, amount):
        """Changes the primary stat given by amount."""
        self.stats[stat] += amount
    
    def roll_stats(self):
        """Assigns valid skill, luck & stamina stats"""
        self.stats['skill'] = ff_extras.roll_dice() + 6
        self.stats['luck'] = ff_extras.roll_dice() + 6
        self.stats['stamina'] = ff_extras.roll_dice(dice=2) + 12

class CharacterSheetGui:
    """
    The entire Fighting Fantasy character sheet window for this program.
    Works closely with the Character class to show and edit information
    
    Non-GUI Attributes:
    obj character: Character class object - The GUI is linked to this character
    All widgets are classified by self.widgetname
    Frames are classified just as framename
    
    Methods:
    run_character_gui: Builds the main window of the character sheet
    clear_potion: Clears the potion entry widget and Character.potion
    eat_ration: reduce rations by 1 and raise stamina by [RATION_RESTORES]
    change_stat: Calls Character.change_char_stat; which changes the given
        stat of the character by the given amount, then refreshes the stat labels
    update_primary_labels: Catch-all that updates the values of all primary stat labels
    auto_stats: Calls Character.roll_stats(), which assigns new valid stats to the
        character, then updates all relevant fields in the GUI
    update_from_entrys: Updates character attributes from the values of user-input text fields
    fight_battle: Runs the combat gui
    """
    def __init__(self, window, character):
        """Initialises the class with the character it is representing
        Then brings up the character sheet window"""
        self.character = character
        self.character_window = window
        self.std_val = '{:2d}' #To display ints with at least 2 digits
        self.character_logbook = ff_logbook.Logbook()
        
        #Set custom fonts
        self.headerfont = Font(family=FONT_FAMILY, size=BIG_FONT)
        self.buttonfont = Font(family=FONT_FAMILY, size=MIDDLE_FONT)
        self.smallfont = Font(family=FONT_FAMILY, size=SMALL_FONT)
        
        #Finish by running the main character gui
        self.run_character_gui()
    
    def run_character_gui(self):
        """Brings up a window displaying all attributes of the character,
        plus options"""
        stamina_text = "Stamina:"
        skill_text = "Skill:"
        luck_text = "Luck:"
        rations_text = "Rations:"
        potion_text = "Potion:"
        fight_text = "FIGHT\nBATTLE"
        logs_text = "Logbook:"
        help_text = "How to"
        reroll_stats_text = "REROLL STATS"
        clear_text = "CLEAR"
        eat_text = "EAT"
        stats_frame_xpad = 20 #x-axis padding for the main stats row
        #ADD (SMALL) IMAGES FOR THE PLUS AND MINUS BUTTONS
        plus_image = PhotoImage(file='plus.gif')
        minus_image = PhotoImage(file='minus.gif')
        
        #This block specifies the layout of all the different widgets
        #----------------------------------------------------------------------#
        
        title_frame = Frame(self.character_window)
        title_frame.grid(row=0, column=0, columnspan=5, pady=10)
        stats_frame = Frame(self.character_window)
        stats_frame.grid(row=1, column=0, columnspan=5, pady=10)
        items_frame = Frame(self.character_window)
        items_frame.grid(row=2, column=0, columnspan=3, pady=10)
        logs_frame = Frame(self.character_window)
        logs_frame.grid(row=2, column=3, columnspan=3, pady=10, sticky='n')
        credits_frame = Frame(self.character_window)
        credits_frame.grid(row=5, column=0, columnspan=5, pady=10)
        
        self.name_entry = Entry(title_frame, font=self.headerfont)
        self.name_entry.insert(END, self.character.name)
        self.name_entry.grid(row=0, column=0, columnspan=4)
        
        #STAMINA SECTION
        stamina_frame = Frame(stats_frame)
        stamina_frame.grid(row=0, column=0, columnspan=2, padx=stats_frame_xpad)
        self.stamina_label = Label(stamina_frame, font=self.headerfont, text=stamina_text)
        self.stamina_label.grid(row=0, column=0)
        self.stamina_value_label = Label(stamina_frame, font=self.headerfont,
                                         text=self.std_val.format(self.character.stats['stamina']))
        self.stamina_value_label.grid(row=0, column=1)
        stamina_button_frame = Frame(stamina_frame)
        stamina_button_frame.grid(row=0, column=2)
        self.stamina_p_button = Button(stamina_button_frame, image=plus_image,
                                       command=lambda: self.change_stat('stamina', +1))
        self.stamina_p_button.grid(row=0, column=0)
        self.stamina_m_button = Button(stamina_button_frame, image=minus_image,
                                       command=lambda: self.change_stat('stamina', -1))
        self.stamina_m_button.grid(row=1, column=0)
        
        #Keep a reference - not sure how these two lines work
        #but they are necessary to keep the 8 images on the screen
        #It's something to do with the Python garbage collector
        self.stamina_p_button.image = plus_image
        self.stamina_m_button.image = minus_image
        
        #SKILL SECTION
        skill_frame = Frame(stats_frame)
        skill_frame.grid(row=0, column=2, columnspan=2, padx=stats_frame_xpad)
        self.skill_label = Label(skill_frame, font=self.headerfont, text=skill_text)
        self.skill_label.grid(row=0, column=0)
        self.skill_value_label = Label(skill_frame, font=self.headerfont,
                                       text=self.std_val.format(self.character.stats['skill']))
        self.skill_value_label.grid(row=0, column=1)
        skill_button_frame = Frame(skill_frame)
        skill_button_frame.grid(row=0, column=2)
        self.skill_p_button = Button(skill_button_frame, image=plus_image,
                                     command=lambda: self.change_stat('skill', +1))
        self.skill_p_button.grid(row=0, column=0)
        self.skill_m_button = Button(skill_button_frame, image=minus_image,
                                     command=lambda: self.change_stat('skill', -1))
        self.skill_m_button.grid(row=1, column=0)
        
        #LUCK SECTION
        luck_frame = Frame(stats_frame)
        luck_frame.grid(row=0, column=4, columnspan=2, padx=stats_frame_xpad)
        self.luck_label = Label(luck_frame, font=self.headerfont, text=luck_text)
        self.luck_label.grid(row=0, column=0)
        self.luck_value_label = Label(luck_frame, font=self.headerfont,
                                       text=self.std_val.format(self.character.stats['luck']))
        self.luck_value_label.grid(row=0, column=1)
        luck_button_frame = Frame(luck_frame)
        luck_button_frame.grid(row=0, column=2)
        self.luck_p_button = Button(luck_button_frame, image=plus_image,
                                    command=lambda: self.change_stat('luck', +1))
        self.luck_p_button.grid(row=0, column=0)
        self.luck_m_button = Button(luck_button_frame, image=minus_image,
                                    command=lambda: self.change_stat('luck', -1))
        self.luck_m_button.grid(row=1, column=0)
        
        #RATIONS SECTION
        rations_frame = Frame(items_frame)
        rations_frame.grid(row=0, column=0, columnspan=3, sticky='w')
        self.rations_label = Label(rations_frame, font=self.headerfont, text=rations_text)
        self.rations_label.grid(row=0, column=0)
        self.rations_value_label = Label(rations_frame, font=self.headerfont,
                                         text=self.std_val.format(self.character.stats['rations']))
        self.rations_value_label.grid(row=0, column=1)
        rations_button_frame = Frame(rations_frame)
        rations_button_frame.grid(row=0, column=2)
        self.rations_p_button = Button(rations_button_frame, image=plus_image,
                                    command=lambda: self.change_stat('rations', +1))
        self.rations_p_button.grid(row=0, column=0)
        self.rations_m_button = Button(rations_button_frame, image=minus_image,
                                    command=lambda: self.change_stat('rations', -1))
        self.rations_m_button.grid(row=1, column=0)
        self.rations_eat_button = Button(rations_button_frame, font=self.buttonfont,
                                         text=eat_text, command=self.eat_ration)
        self.rations_eat_button.grid(row=0, column=1, rowspan=2)
        
        #POTION SECTION
        potion_frame = Frame(items_frame)
        potion_frame.grid(row=1, column=0, columnspan=3, sticky='w')
        self.potion_label = Label(potion_frame, font=self.headerfont, text=potion_text)
        self.potion_label.grid(row=0, column=0)
        self.potion_entry = Entry(potion_frame, font=self.headerfont)
        self.potion_entry.insert(END, self.character.potion)
        self.potion_entry.grid(row=0, column=1)
        self.clear_potion_button = Button(potion_frame, font=self.buttonfont,
                                          text=clear_text, command=self.clear_potion)
        self.clear_potion_button.grid(row=0, column=2)
        
        #INVENTORY SECTION
        inventory_frame = Frame(items_frame)
        inventory_frame.grid(row=2, column=0, columnspan=3, sticky='w')
        #Text box and scroll bar for user to list on
        self.inventory_text=Text(inventory_frame, font=self.headerfont, height=8, width=32)
        self.inventory_text.grid(row=0, column=0, columnspan=2)
        self.inventory_text.insert(END, self.character.inventory)
        self.inventory_scroll=Scrollbar(inventory_frame)
        self.inventory_scroll.grid(row=0, column=2, sticky='nsw')
        self.inventory_scroll.config(command=self.inventory_text.yview)
        self.inventory_text.config(yscrollcommand=self.inventory_scroll.set)
        
        #REROLL STATS BUTTON
        self.reroll_stats_button = Button(title_frame, font=self.buttonfont,
                                          text=reroll_stats_text, command=self.auto_stats)
        self.reroll_stats_button.grid(row=0, column=4)
        
        #FIGHT SECTION
        self.fight_button = Button(logs_frame, font=self.headerfont,
                                   text=fight_text, command=self.fight_battle)
        self.fight_button.grid(row=0, column=0)
        
        #ACTION LOG SECTION
        logs_label = Label(logs_frame, font=self.buttonfont, text=logs_text)
        logs_label.grid(row=1, column=0)
        log_values = Label(logs_frame, font=self.smallfont, height=10, width=24)
        log_values.grid(row=2, column=0, sticky='n')
        log_values['text'] = self.character_logbook.__repr__()
        
        #CREDITS SECTION
        self.credits_label = Label(credits_frame, font=self.smallfont, text=CREDITS_TEXT)
        self.credits_label.grid(row=1, column=0)
        
        #----------------------------------------------------------------------#
        #End of widget layout block
    
    def clear_potion(self):
        """Clears the potion entry widget and updates Character attributes"""
        self.potion_entry.delete(0, "end")
        self.update_from_entrys()
    
    def eat_ration(self):
        """Consume a ration and increase stamina by default value"""
        self.change_stat('rations', -1)
        self.change_stat('stamina', RATION_RESTORES)
    
    def change_stat(self, stat, change):
        """Calls the change_char_stat method of the character,
        then updates primary labels"""
        self.character.change_char_stat(stat, change)
        #Should I update all labels or use if statements and only update the one changed?
        #I prefer the former as it's more of a catch-all and still isn't too taxing
        self.update_primary_labels()
        
    def update_primary_labels(self):
        """Catch-all update of all primary stat labels: Stamina, Skill, Luck & Rations"""
        self.stamina_value_label['text'] = self.std_val.format(self.character.stats['stamina'])
        self.skill_value_label['text'] = self.std_val.format(self.character.stats['skill'])
        self.luck_value_label['text'] = self.std_val.format(self.character.stats['luck'])
        self.rations_value_label['text'] = self.std_val.format(self.character.stats['rations'])
    
    def auto_stats(self):
        """Calls the roll_stats method of the character, then updates related labels"""
        self.character.roll_stats()
        self.update_primary_labels()
        self.update_from_entrys()
    
    def update_from_entrys(self):
        """Takes values from the name, potion and items fields to update their
        associated character class attributes"""
        self.character.name = self.name_entry.get()
        self.character.potion = self.potion_entry.get()
        #Read as: inventory_text.get(from line 1.0, to end of Text, delete last char ('\n')
        self.character.inventory = self.inventory_text.get("1.0", "end-1c")
    
    def fight_battle(self):
        """Ensures consistency between the character attributes and displayed information,
        then runs the main combat gui, then displays information again"""
        
        #Ensure all Character attributes are correct,
        #and save them to a new Character object
        self.update_from_entrys()
        saved_character = self.character
        
        #Destroy the window
        #Not sure if I should use root.destroy() or root.quit() when destroying the window
        #as I want as little of the old gui class as possible to be saved in memory
        self.character_window.destroy()
        
        #Do the fight
        ff_combatscreen.run_combat_gui(saved_character.name, saved_character.stats)
        
        #Get the window back again (Well actually make a new one with the saved character)
        #This could overextend the memory if the old classes are still saved
        new_characterwindow = Tk()
        new_character_gui = CharacterSheetGui(new_characterwindow, saved_character)
        new_characterwindow.mainloop()