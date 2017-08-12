"""
Alasdair Smith
Started 20/12/2016

Module for the Fighting Fantasy program
Includes entire combat process

For Fighting Fantasy Gamebooks:
Ian Livingstone's Caverns of the White Witch & similar

Two dice rolls + skill level = attack value
Character with lowest attack value takes 2 damage, this ends the 'round'
Tie if equal attack value - ends 'round' with no damage
Can do luck check after a 'round' which (if successful) either reduces damage
taken or increases damage done by 1
    If successful character luck will always go down by 1
    Checkbox to include whether luck goes down on an unsuccessful roll
"""
from tkinter import *
from tkinter.font import *
#from tkinter.ttk import * #Can't use because it's buttons don't support fonts
import ff_extras
import ff_charactersheet
import ff_logbook

def run_combat_gui(player_name, player_stats):
    """Runs the gui with the player Character against an enemy
    whose skill and stamina are entered by the user"""
    combat_window = Tk()
    combat_gui = CombatGui(combat_window, player_name, player_stats)
    combat_window.mainloop()
    
class CombatGui:
    """This gui handles each combat stage in the game
    
    Player and enemy stats can be modified at any time
    Finish and apply changes button at end of match to close window and modify
    player character attributes as appropriate"""
    
    def __init__(self, window, player_name, player_stats):
        """"""
        
        self.combat_window = window
        self.std_val = '{:2d}' #To display ints with at least 2 digits
        
        self.player_name = player_name
        self.player_stats = player_stats
        self.enemy_name = ff_charactersheet.ENEMY_NAME
        self.enemy_stats = ff_charactersheet.DEFAULT_STATS