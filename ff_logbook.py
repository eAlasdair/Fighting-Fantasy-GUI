"""
Alasdair Smith
Started 12/08/2017

Module for the Fighting Fantasy Program
Includes the Log and Logbook classes - for representing action logs in the
    charactersheet and combatscreen GUIs

For Fighting Fantasy Gamebooks:
Ian Livingstone's Caverns of the White Witch & similar

Cannot be run as the initial program.

Contains its own set of globals
"""
NUM_LOGS = 8 #Number of most recent logs to be formatted

#These can't have more than 3 different format vars!
# - Enforced by the Log initialiser
STANDARD_LOGS = {
    "space"        : "",
    "eat"          : "{0} ate a ration.",               #0 = player
    "roll_die"     : "{0} rolled a {1}",                #0 = player, 1 = roll
    "roll_die_ext" : " and a {0}",                      #0 = roll
    "total_roll"   : ", totalling {0}",                 #0 = sum
    "attack_val"   : ", for an attack value of {0}.",   #0 = attack value
    "take_dmg"     : "{0} was hit for {1} damage.",     #0 = player, 1 = dmg
    "draw"         : "Draw, no damage dealt.",          #No formats
    "roll_luck"    : "Rolled for luck, got {0}.",       #0 = roll
    "less_dmg"     : "{0} took {1} less damage!",       #0 = player, 1 = dmg
    "more_dmg"     : "{0} took {1} more damage!",       #0 = player, 1 = dmg
    "success"      : "Success!",                        #No formats
    "failure"      : "Failure!",                        #No formats
    "stat_up"      : "{0} increased by {1}.",           #0 = stat, 1 = amount
    "stat_down"    : "{0} reduced by {1}.",             #0 = stat, 1 = amount
    "refresh"      : "Stats updated successfully!",     #No formats
    "battle"       : "{0} fought a battle.",            #0 = player
    "new_stats"    : "Stats rerolled! Now updated.",    #No formats
    "clear_pot"    : "Potion cleared.",                 #No formats
    "unchanged"    : "{0} unchanged.",                  #0 = stat
    "err_draw"     : "Cannot do luck check; last round was a draw.", #No formats
    "err_no_fight" : "Cannot do luck check; no new combats.",        #No formats
    "options"      : "Options updated"                  #No formats
    }

class Log:
    """
    Defines objects with one particular attribute:
    A string representing a particular action made by the user or program
    
    Logs can be individual or a block of multiple logs in the one log_string attribute
    
    NOTE: Try to avoid multiline logs, the display becomes erratic
    """
    def __init__(self, log, format1=None, format2=None, format3=None):
        """Creates the new Log object
        Cannot be called with more than 3 formatting strings"""
        if log in STANDARD_LOGS.keys(): #New log with formats
            self.log_string = STANDARD_LOGS[log].format(format1, format2, format3)
        elif type(log) == str: #Unknown or pre-formatted string as new log
            self.log_string = log
        else: #Type cannot be handled
            raise TypeError("Attempted to create Log with {} attribute".format(type(log)))
    
    def __repr__(self):
        """Returns the string log_string for display"""
        return self.log_string
    
    def append_log(self, otherlog):
        """Appends otherlog.log_string to self.log_string
        """
        self.log_string += otherlog.log_string

class Logbook:
    """
    A list of log objects, with some code to format it effectively
    """
    def __init__(self, logs=None):
        """Makes a new logbook object with the attribute log_list as logs
        log_list is an empty list by default"""
        self.log_list = logs
        if self.log_list is None:
            self.log_list = []
        if type(self.log_list) != list:
            raise TypeError("Attempted to create Logbook with non-list attribute")
    
    def __repr__(self, is_rev=False):
        """Returns a string formatted correctly as a logbook of the most recent
        NUM_LOGS logs, if is_rev, logs are shown in reverse order"""
        all_logs = ""
        temp_logs = self.log_list[NUM_LOGS * -1:] #Get the most recent NUM_LOGS logs
        if is_rev:
            for log in reversed(temp_logs):
                all_logs += log.log_string + "\n" #Add them most-recent FIRST to the string
        else:
            for log in temp_logs:
                all_logs += log.log_string + "\n" #Add them most-recent LAST to the string
        return all_logs
    
    def add_log(self, log):
        """Adds a new log object to the list to be displayed"""
        self.log_list.append(log)
    
    def clear(self):
        """Empties log_list"""
        self.log_list = []