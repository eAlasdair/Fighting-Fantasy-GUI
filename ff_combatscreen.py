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
    luck roll is successful if the roll made is less than or equal to the luck stat
"""
from tkinter import *
from tkinter.font import *
#from tkinter.ttk import * #Can't use because it's buttons don't support fonts
import ff_extras
import ff_charactersheet
import ff_logbook

CHANGE_ON_LUCK = 1 #This amount is added to or subtracted from the damage done,
                   #based on luck roll and situation
STD_DMG = 2 #Amount of damage taken on a round loss

def run_combat_gui(player, enemy):
    """Runs the gui with the player Character against an enemy
    whose skill and stamina are entered by the user"""
    if enemy is None:
        enemy = ff_extras.make_default_enemy()
    combat_window = Tk()
    combat_gui = CombatGui(combat_window, player, enemy)
    combat_window.mainloop()
    
class CombatGui:
    """
    This gui handles each combat stage in the game
    
    Player and enemy stats can be modified at any time
    Finish and apply changes button at end of match to close window and modify
    player character attributes as appropriate
    
    Non-GUI Attributes:
    obj player: Character object
    obj enemy: Character object
    str last_round: Result of previous round, "p_win", "e_win", "draw", or None
    
    All widgets are classified by self.widgetname
    Frames are classified just as framename
    """
    
    def __init__(self, window, player, enemy):
        """Initialises the class with the two characters it is representing
        then brings up the combat window"""
        
        self.combat_window = window
        self.player = player
        self.enemy = enemy
        self.combat_logs = ff_logbook.Logbook()
        self.last_round = None
        
        #Set custom fonts
        self.headerfont = Font(family=ff_charactersheet.FONT_FAMILY,
                               size=ff_charactersheet.BIG_FONT)
        self.buttonfont = Font(family=ff_charactersheet.FONT_FAMILY,
                               size=ff_charactersheet.MIDDLE_FONT)
        self.smallfont = Font(family=ff_charactersheet.FONT_FAMILY,
                              size=ff_charactersheet.SMALL_FONT)
        
        #Finish by running the main combat gui
        self.build_combat_gui()
    
    def build_combat_gui(self):
        """Brings up the main combat window with all its widgets"""
        g_text = {"versus"    : "VERSUS",
                  "fight"     : "FIGHT",
                  "roll_luck" : "ROLL LUCK",
                  "settings"  : "SETTINGS",
                  "end_fight" : "END FIGHT",
                  "logs"      : "Logbook:",
                  "stamina"   : "STAMINA:",
                  "skill"     : "SKILL:  ",
                  "luck"      : "LUCK:   ",
                  "s_change"  : "SET STATS",
                  "empty"     : "{}"
                  }
        
        #BUILD FRAMES
        combat_frame = Frame(self.combat_window)
        combat_frame.grid(row=0, column=0)
        log_frame = Frame(self.combat_window)
        log_frame.grid(row=1, column=0)
        credits_frame = Frame(self.combat_window)
        credits_frame.grid(row=2, column=0)
        
        player_stats_frame = Frame(combat_frame)
        player_stats_frame.grid(row=1, column=0, sticky='n')
        actions_frame = Frame(combat_frame)
        actions_frame.grid(row=1, column=1, padx=20, sticky='n')
        enemy_stats_frame = Frame(combat_frame)
        enemy_stats_frame.grid(row=1, column=2, sticky='n')
        
        #PLAYER STATS FRAME
        self.player_name_entry = Entry(player_stats_frame, font=self.headerfont,
                                       width=16, justify='right')
        self.player_name_entry.insert(END, self.player.name)
        self.player_name_entry.grid(row=0, column=0, columnspan=2)
        self.p_stamina_label = Label(player_stats_frame, font=self.headerfont,
                                     text=g_text['stamina'])
        self.p_stamina_label.grid(row=1, column=0, sticky='e')
        self.p_stamina_entry = Entry(player_stats_frame, font=self.headerfont,
                                     width=3, justify='right')
        self.p_stamina_entry.grid(row=1, column=1, sticky='e')
        self.p_stamina_entry.insert(END, g_text['empty'].format(self.player.stats['stamina']))
        self.p_skill_label = Label(player_stats_frame, font=self.headerfont,
                                   text=g_text['skill'])
        self.p_skill_label.grid(row=2, column=0, sticky='e')
        self.p_skill_entry = Entry(player_stats_frame, font=self.headerfont,
                                     width=3, justify='right')
        self.p_skill_entry.grid(row=2, column=1, sticky='e')
        self.p_skill_entry.insert(END, g_text['empty'].format(self.player.stats['skill']))
        self.p_luck_label = Label(player_stats_frame, font=self.headerfont,
                                  text=g_text['luck'])
        self.p_luck_label.grid(row=3, column=0, sticky='e')
        self.p_luck_entry = Entry(player_stats_frame, font=self.headerfont,
                                     width=3, justify='right')
        self.p_luck_entry.grid(row=3, column=1, sticky='e')
        self.p_luck_entry.insert(END, g_text['empty'].format(self.player.stats['luck']))        
        
        #ENEMY STATS FRAME
        self.enemy_name_entry = Entry(enemy_stats_frame, font=self.headerfont,
                                      width=16, justify='left')
        self.enemy_name_entry.insert(END, self.enemy.name)
        self.enemy_name_entry.grid(row=0, column=0)
        self.e_stamina_entry = Entry(enemy_stats_frame, font=self.headerfont,
                                     width=3, justify='left')
        self.e_stamina_entry.grid(row=1, column=0, sticky='w')
        self.e_stamina_entry.insert(END, g_text['empty'].format(self.enemy.stats['stamina']))
        self.e_skill_entry = Entry(enemy_stats_frame, font=self.headerfont,
                                   width=3, justify='left')
        self.e_skill_entry.grid(row=2, column=0, sticky='w')
        self.e_skill_entry.insert(END, g_text['empty'].format(self.enemy.stats['skill']))
        #self.empty_e_luck_label = Label(enemy_stats_frame, font=self.headerfont, text="")
        #self.empty_e_luck_label.grid(row=3, column=0, sticky='w')
        
        #ACTIONS FRAME
        self.versus_label = Label(actions_frame, font=self.headerfont, text=g_text['versus'])
        self.versus_label.grid(row=0, column=0, padx=30)
        self.fight_button = Button(actions_frame, font=self.buttonfont, text=g_text['fight'],
                                   command=self.fight_round, width=10)
        self.fight_button.grid(row=1, column=0)
        self.roll_button = Button(actions_frame, font=self.buttonfont, text=g_text['roll_luck'],
                                       command=self.roll_luck, width=10)
        self.roll_button.grid(row=2, column=0)        
        #self.other_button = Button(actions_frame, font=self.buttonfont, text=g_text['settings'],
                                 #command=None, width=10)
        #self.other_button.grid(row=3, column=0)
        ##Put this somewhere
        self.end_button = Button(actions_frame, font=self.buttonfont, text=g_text['end_fight'],
                                 command=self.end_fight, width=10)
        self.end_button.grid(row=3, column=0)
        
        #LOG FRAME
        self.logs_label = Label(log_frame, font=self.buttonfont, text=g_text['logs'])
        self.logs_label.grid(row=0, column=0)
        self.logs_text = Label(log_frame, font=self.smallfont, height=ff_logbook.NUM_LOGS,
                               width=88, anchor='n', justify='left')
        self.logs_text.grid(row=1, column=0, sticky='w')
        self.logs_text['text'] = self.combat_logs.__repr__(is_rev=True)
        
        #CREDITS FRAME
        self.credits_label = Label(credits_frame, font=self.smallfont,
                                   text=ff_charactersheet.CREDITS_TEXT)
        self.credits_label.grid(row=0, column=0)
    
    def end_fight(self):
        """Ends the fight, that's it"""
        self.combat_window.destroy()
    
    def refresh_logbook(self):
        """Updates the logbook label with the up-to-date logbook"""
        self.logs_text['text'] = self.combat_logs.__repr__(is_rev=True)
    
    def update_from_entrys(self):
        """Opposite of update_primary_entrys, plus update of names
        Updates the player & enemy name and stats from user input"""
        self.player.name = self.player_name_entry.get()
        self.enemy.name = self.enemy_name_entry.get()
        
        self.player.stats['stamina'] = int(self.p_stamina_entry.get())
        self.enemy.stats['stamina'] = int(self.e_stamina_entry.get())
        
        self.player.stats['skill'] = int(self.p_skill_entry.get())
        self.enemy.stats['skill'] = int(self.e_skill_entry.get())
        
        self.player.stats['luck'] = int(self.p_luck_entry.get())
        #self.enemy.stats['luck'] = int(self.e_luck_entry.get())
        
    
    def update_primary_entrys(self):
        """Opposite of update_from_entrys, minus updating names
        Updates the entrys of player & enemy stats"""
        self.p_stamina_entry.delete(0, 'end')
        self.p_stamina_entry.insert('end', self.player.stats['stamina'])
        self.e_stamina_entry.delete(0, 'end')
        self.e_stamina_entry.insert('end', self.enemy.stats['stamina'])
        
        self.p_skill_entry.delete(0, 'end')
        self.p_skill_entry.insert('end', self.player.stats['skill'])
        self.e_skill_entry.delete(0, 'end')
        self.e_skill_entry.insert('end', self.enemy.stats['skill'])   
        
        self.p_luck_entry.delete(0, 'end')
        self.p_luck_entry.insert('end', self.player.stats['luck'])
        #self.e_luck_entry.delete(0, 'end')
        #self.e_luck_entry.insert(self.enemy.stats['luck'], 'end')        
    
    def fight_round(self):
        """Initiates one phase of combat between the player and enemy
        Two dice rolls + skill level = attack value
        Character with lowest attack value takes 2 damage, this ends the 'round'
        Tie if equal attack value - ends 'round' with no damage"""
        self.update_from_entrys()
        
        p_power, p_log = self.get_attack('p')
        e_power, e_log = self.get_attack('e')
        if p_power > e_power:
            #Player wins round
            self.last_round = 'p_win'
            self.change_stat('e', 'stamina', STD_DMG * -1, sle=True)
            r_log = ff_logbook.Log('take_dmg', self.enemy.name, STD_DMG)
        elif p_power < e_power:
            #Enemy wins round
            self.last_round = 'e_win'
            self.change_stat('p', 'stamina', STD_DMG * -1, sle=True)
            r_log = ff_logbook.Log('take_dmg', self.player.name, STD_DMG)
        else: #Draw
            self.last_round = 'draw'
            r_log = ff_logbook.Log('draw')
            
        self.combat_logs.add_log(ff_logbook.Log('space'))
        self.combat_logs.add_log(r_log)
        self.combat_logs.add_log(e_log)
        self.combat_logs.add_log(p_log)
        self.refresh_logbook()
        self.update_primary_entrys()
    
    def get_attack(self, character):
        """Returns attack power and a new Log, for the given character"""
        roll1 = ff_extras.roll_dice()
        roll2 = ff_extras.roll_dice()
        total = roll1 + roll2
        if character == 'p': #Player
            power = total + self.player.stats['skill']
            log = ff_logbook.Log('roll_die', self.player.name, roll1)
            log.append_log(ff_logbook.Log('roll_die_ext', roll2))
            log.append_log(ff_logbook.Log('total_roll', total))
            log.append_log(ff_logbook.Log('attack_val', power))
        elif character == 'e': #Enemy
            power = total + self.enemy.stats['skill']
            log = ff_logbook.Log('roll_die', self.enemy.name, roll1)
            log.append_log(ff_logbook.Log('roll_die_ext', roll2))
            log.append_log(ff_logbook.Log('total_roll', total))
            log.append_log(ff_logbook.Log('attack_val', power))
        return power, log
    
    def roll_luck(self):
        """Depending on the result of the previous engagement, makes a luck roll"""
        self.update_from_entrys()
        self.combat_logs.add_log(ff_logbook.Log('space'))        
        if self.last_round == "p_win":
            self.luck_check("more")
        elif self.last_round == "e_win":
            self.luck_check("less")
        elif self.last_round == "draw":
            self.combat_logs.add_log(ff_logbook.Log('err_draw'))
        elif self.last_round is None:
            self.combat_logs.add_log(ff_logbook.Log('err_no_fight'))
        else: #impossible
            raise ValueError("Previous round set to unknown value: {}".format(self.last_round))
        self.last_round = None
        self.refresh_logbook()
    
    def luck_check(self, more_or_less):
        """On a successful luck roll, reduces or increases damage done by CHANGE_ON_LUCK"""
        roll = ff_extras.roll_dice(dice=2) #Is it one or two dice? Neither seem quite right
        if roll <= self.player.stats['luck']:
            self.change_stat('p', 'luck', -1)
            if more_or_less == 'less':
                self.combat_logs.add_log(ff_logbook.Log('less_dmg', self.player.name,
                                                        CHANGE_ON_LUCK))
                self.change_stat('p', 'stamina', CHANGE_ON_LUCK * 1, sle=True)
            elif more_or_less == 'more':
                self.combat_logs.add_log(ff_logbook.Log('more_dmg', self.enemy.name,
                                                        CHANGE_ON_LUCK))
                self.change_stat('e', 'stamina', CHANGE_ON_LUCK * -1, sle=True)
            else: #Impossible
                raise ValueError("more_or_less is somehow not more or less, dude you broke it")
            self.combat_logs.add_log(ff_logbook.Log('success'))
        else:
            self.combat_logs.add_log(ff_logbook.Log('unchanged', "Luck"))
            self.combat_logs.add_log(ff_logbook.Log('failure'))
        self.combat_logs.add_log(ff_logbook.Log('roll_luck', roll))
        self.refresh_logbook()
    
    def change_stat(self, p_or_e, stat, change, sle=False):
        """sle: Suppress Log Entry - Used if a new log entry about the change is not required
        Changes the [stat] of the player or enemy by [change]"""
        if p_or_e == 'p':
            self.player.change_char_stat(stat, change)
        elif p_or_e == 'e':
            self.enemy.change_char_stat(stat, change)
        else: #Impossible
            raise ValueError("p_or_e is somehow not p and not e, geez you broke it wth man")
        #Should I update all labels or use if statements and only update the one changed?
        #I prefer the former as it's more of a catch-all and still isn't too taxing
        self.update_primary_entrys()
        if not sle:
            if change >= 0:
                self.combat_logs.add_log(ff_logbook.Log("stat_up", stat.title(), change))
            else: #change < 0:
                self.combat_logs.add_log(ff_logbook.Log("stat_down", stat.title(), change * -1))
        self.refresh_logbook()        


def main():
    """Starts the entire program"""
    if __name__ == "__main__":
        ff_extras.run_code()

main()