"""
Alasdair Smith
Started 20/12/2016

Module for the Fighting Fantasy Program
Defines the Character Sheet GUI Class and Character Object Class

For Fighting Fantasy Gamebooks:
Ian Livingstone's Caverns of the White Witch & similar

Inlcudes all global (used by more than one module) global value declarations

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
SMALL_FONT = 10  #For credits and the logbook
RATION_RESTORES = 4 #Stamina
DEFAULT_STATS = {"skill": 1, "luck": 1, "stamina": 1, "rations": 0}
DEFAULT_NAME = "Champion"
ENEMY_NAME = "Enemy"
INVENTORY_TEXT = "Items:\n"
CREDITS_TEXT = """
Made by Alasdair Smith (@ealasdair) for the Yogscast Charity Jingle Jam livesteams through December 2017

Started: Dec 2016    Last Edit: Aug 2017
"""

class Character:
    """
    Defines the Character class for Fighting Fantasy Main Characters
    
    Attributes:
    str   name - the character name, unique identifier
    dict  stats - dictionary of ints: {'skill', 'luck', 'stamina', 'rations'}
    str   potion - a separate item held by the character, no particular value
    str   inventory - all other items held by the character, formatted by the player
    
    Methods:
    change_char_stat: Changes the given stat of the character by the given amount
    roll_stats: Automatically assigns valid stats to the character
    """
    def __init__(self, name=DEFAULT_NAME, stats=None, potion=None, inventory=INVENTORY_TEXT):
        """Initialises the character, based on given data input"""
        self.name = name
        self.stats = stats
        self.potion = potion
        self.inventory = inventory
        if self.stats is None:
            self.stats = ff_extras.copy_dict(DEFAULT_STATS)
        if self.potion is None:
            self.potion = ""
    
    def __repr__(self):
        """For testing"""
        template = "Name: {}\nStats: {}\nPotion: {}\n"
        return template.format(self.name, self.stats, self.potion)
    
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
    str std_val: Empty string with braces to display ints as though at least
        2 digits existed
    
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
    refresh_logbook: Updates the logbook label
    """
    def __init__(self, window, character):
        """Initialises the class with the character it is representing
        Then brings up the character sheet window"""
        self.character = character #This just points self.character at the same place as character (good)
        self.character_window = window
        self.std_val = '{:2d}' #To display ints as though 2 digits existed
        self.char_logs = ff_logbook.Logbook()
        
        #Set custom fonts
        self.headerfont = Font(family=FONT_FAMILY, size=BIG_FONT)
        self.buttonfont = Font(family=FONT_FAMILY, size=MIDDLE_FONT)
        self.smallfont = Font(family=FONT_FAMILY, size=SMALL_FONT)
        
        #Finish by running the main character gui
        self.run_character_gui()
    
    def run_character_gui(self):
        """Brings up a window displaying all attributes of the character,
        plus options"""
        g_text = {"stamina" : "Stamina:",
                  "skill"   : "Skill:",
                  "luck"    : "Luck:",
                  "rations" : "Rations:",
                  "potion"  : "Potion:",
                  "fight"   : "FIGHT\nBATTLE",
                  "logs"    : "Logbook:",
                  "help"    : "More Info",
                  "reroll"  : "REROLL STATS",
                  "clear"   : "CLEAR",
                  "eat"     : "EAT",
                  "roll"    : "ROLL"
                  }
        stats_frame_xpad = 20 #x-axis padding for the main stats row
        #ADD (SMALL) IMAGES FOR THE PLUS AND MINUS BUTTONS
        plus_image = PhotoImage(file='plus.gif')
        minus_image = PhotoImage(file='minus.gif')
        
        #This block specifies all the different widgets
        #----------------------------------------------------------------------#
        #ALL THE MAIN FRAMES
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
        
        #NAME SECTION
        self.name_entry = Entry(title_frame, font=self.headerfont, width=16)
        self.name_entry.insert(END, self.character.name)
        self.name_entry.grid(row=0, column=0, columnspan=4)
        
        #STAMINA SECTION
        stamina_frame = Frame(stats_frame)
        stamina_frame.grid(row=0, column=0, columnspan=2, padx=stats_frame_xpad)
        self.stamina_label = Label(stamina_frame, font=self.headerfont, text=g_text['stamina'])
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
        self.skill_label = Label(skill_frame, font=self.headerfont, text=g_text['skill'])
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
        self.luck_label = Label(luck_frame, font=self.headerfont, text=g_text['luck'])
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
        self.luck_roll_button = Button(luck_frame, font=self.buttonfont, text=g_text['roll'],
                                       command=self.roll_luck)
        self.luck_roll_button.grid(row=0, column=3)
        
        #RATIONS SECTION
        rations_frame = Frame(items_frame)
        rations_frame.grid(row=0, column=0, columnspan=3, sticky='w')
        self.rations_label = Label(rations_frame, font=self.headerfont, text=g_text['rations'])
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
                                         text=g_text['eat'], command=self.eat_ration)
        self.rations_eat_button.grid(row=0, column=1, rowspan=2)
        
        #POTION SECTION
        potion_frame = Frame(items_frame)
        potion_frame.grid(row=1, column=0, columnspan=3, sticky='w')
        self.potion_label = Label(potion_frame, font=self.headerfont, text=g_text['potion'])
        self.potion_label.grid(row=0, column=0)
        self.potion_entry = Entry(potion_frame, font=self.headerfont)
        self.potion_entry.insert(END, self.character.potion)
        self.potion_entry.grid(row=0, column=1)
        self.clear_potion_button = Button(potion_frame, font=self.buttonfont,
                                          text=g_text['clear'], command=self.clear_potion)
        self.clear_potion_button.grid(row=0, column=2)
        
        #INVENTORY SECTION
        inventory_frame = Frame(items_frame)
        inventory_frame.grid(row=2, column=0, columnspan=3, sticky='w')
        #Text box and scroll bar for user to list on
        self.inventory_text = Text(inventory_frame, font=self.headerfont, height=8, width=32)
        self.inventory_text.grid(row=0, column=0, columnspan=2)
        self.inventory_text.insert(END, self.character.inventory)
        self.inventory_scroll = Scrollbar(inventory_frame)
        self.inventory_scroll.grid(row=0, column=2, sticky='nsw')
        self.inventory_scroll.config(command=self.inventory_text.yview)
        self.inventory_text.config(yscrollcommand=self.inventory_scroll.set)
        
        #REROLL STATS BUTTON
        self.reroll_stats_button = Button(title_frame, font=self.buttonfont,
                                          text=g_text['reroll'], command=self.auto_stats)
        self.reroll_stats_button.grid(row=0, column=4)
        
        #FIGHT SECTION
        self.fight_button = Button(logs_frame, font=self.headerfont,
                                   text=g_text['fight'], command=self.fight_battle)
        self.fight_button.grid(row=0, column=0)
        
        #ACTION LOG SECTION
        self.logs_label = Label(logs_frame, font=self.buttonfont, text=g_text['logs'])
        self.logs_label.grid(row=1, column=0)
        self.log_values = Label(logs_frame, font=self.smallfont, height=ff_logbook.NUM_LOGS,
                                width=32, anchor='nw', justify='left')
        self.log_values.grid(row=2, column=0)
        self.log_values['text'] = self.char_logs.__repr__(is_rev=True)
        
        #CREDITS SECTION
        self.credits_label = Label(credits_frame, font=self.smallfont, text=CREDITS_TEXT)
        self.credits_label.grid(row=1, column=0)
        
        #----------------------------------------------------------------------#
        #End of widget definition block
    
    def clear_potion(self):
        """Clears the potion entry widget and updates Character attributes"""
        self.potion_entry.delete(0, 'end')
        self.update_from_entrys()
        self.char_logs.add_log(ff_logbook.Log('clear_pot'))
        self.refresh_logbook()
    
    def eat_ration(self):
        """Consume a ration and increase stamina by default value"""
        self.char_logs.add_log(ff_logbook.Log('space'))
        self.change_stat('stamina', RATION_RESTORES)
        self.change_stat('rations', -1)
        self.update_from_entrys()
        self.char_logs.add_log(ff_logbook.Log('eat', self.character.name))
        self.refresh_logbook()
    
    def roll_luck(self):
        """Determine whether a luck roll was successful"""
        roll = ff_extras.roll_dice(dice=2) #Is it one or two dice? Neither seem quite right
        self.char_logs.add_log(ff_logbook.Log('space'))
        if roll <= self.character.stats['luck']:
            self.change_stat('luck', -1)
            self.char_logs.add_log(ff_logbook.Log('success'))
        else:
            self.char_logs.add_log(ff_logbook.Log('unchanged', "Luck"))
            self.char_logs.add_log(ff_logbook.Log('failure'))
        self.char_logs.add_log(ff_logbook.Log('roll_luck', roll))
        self.refresh_logbook()
    
    def change_stat(self, stat, change):
        """Calls the change_char_stat method of the character,
        then updates primary labels"""
        self.character.change_char_stat(stat, change)
        #Should I update all labels or use if statements and only update the one changed?
        #I prefer the former as it's more of a catch-all and still isn't too taxing
        self.update_primary_labels()
        if change >= 0:
            self.char_logs.add_log(ff_logbook.Log("stat_up", stat.title(), change))
        else:
            self.char_logs.add_log(ff_logbook.Log("stat_down", stat.title(), change * -1))
        self.refresh_logbook()
        
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
        self.char_logs.add_log(ff_logbook.Log("new_stats"))
        self.refresh_logbook()
    
    def update_from_entrys(self):
        """Takes values from the name, potion and items fields to update their
        associated character class attributes"""
        self.character.name = self.name_entry.get()
        self.character.potion = self.potion_entry.get()
        #Read as: inventory_text.get(from line 1.0, to end of Text without last char ('\n'))
        self.character.inventory = self.inventory_text.get("1.0", "end-1c")
    
    def refresh_logbook(self):
        """Updates the logbook label with the up-to-date logbook"""
        #A bit more fiddling than just changing is_rev is required to get messages
        #in order when displaying them un-reversed
        self.log_values['text'] = self.char_logs.__repr__(is_rev=True)
    
    def fight_battle(self):
        """Ensures consistency between the character attributes and displayed information,
        then runs the main combat gui, using a function outside of the class"""
        
        #Ensure all Character attributes are correct
        self.update_from_entrys()
        
        #Destroy the window
        self.character_window.destroy()
        
        #Do the fight and get the window back; I beleive self.character is still
        #just a reference to the original character object passed to __init__()
        external_fight(self.character, None)
        
        #I want as little of the old gui class object as possible to be saved in memory
        #But I'm not sure how to do that :/        
        #This method of course ends up being a recursive process
        #print("END OF CLASS")

def external_fight(player1, player2):
    """It is 'external' cos it is outside of the CharacterSheetGui class object that calls it.
    Runs the combat gui with the two characters specified. player2 is a standard enemy if None.
    Afterwards it brings up a new CharacterSheetGui with the updated player1.
    
    Currently the updated player2 is ignored, but some framework exists for a potential
    combat between two 'main' characters
    """
    #Do the fight
    ff_combatscreen.run_combat_gui(player1, player2)
    
    #Get the window back again (Well actually make a new one with the saved character)
    #This could potentially overextend the memory, depending on how much of the old classes are kept
    new_characterwindow = Tk()
    new_character_gui = CharacterSheetGui(new_characterwindow, player1)
    new_character_gui.char_logs.add_log(ff_logbook.Log('space'))
    new_character_gui.char_logs.add_log(ff_logbook.Log('refresh'))
    new_character_gui.char_logs.add_log(ff_logbook.Log('battle', player1.name))
    new_character_gui.refresh_logbook()
    new_characterwindow.mainloop()

def main():
    """Starts the entire program"""
    if __name__ == "__main__":
        ff_extras.run_code()

main()