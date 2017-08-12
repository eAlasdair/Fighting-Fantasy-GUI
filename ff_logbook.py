"""
Alasdair Smith
Started 12/08/2016

Module for the Fighting Fantasy Program
Includes the Log and Logbook classes - for representing action logs in the
    charactersheet and combatscreen GUIs

For Fighting Fantasy Gamebooks:
Ian Livingstone's Caverns of the White Witch & similar

#Contains its own set of globals
"""
#Standard logs can't have more than 3 different format vars!
STANDARD_LOGS = {
    "eat" : "{0} ate a ration,\nrestored {1} stamina.", #0 = player, 1 = value restored
    "roll_die" : "{0} rolled a {1}", #0 = player, 1 = roll
    "roll_die_ext" : " and a {0}", #0 = roll
    "total_roll" : ", totalling {0}", #0 = sum
    "attack_val" : "for an attack value of {0}.", #0 = attack value
    "take_dmg" : "{0} was hit for {1} damage.", #0 = player, 1 = dmg
    "roll_luck" : "{0} rolled for luck, got {1}.", #0 = player, 1 = roll
    "less_dmg" : "{0} took {1} less damage!", #0 = player, 1 = dmg
    "more_dmg" : "{0} took {1} more damage!", #0 = player, 1 = dmg
    "success" : "Success!",
    "failure" : "Failure!",
    "stat_up" : "{0} increased by 1.", #0 = stat
    "stat_down" : "{0} reduced by 1." #0 = stat
    }

class Log:
    """
    Logs can be individual or a block of multiple log strings in the one log attribute
    """
    def __init__(self, log, format1=None, format2=None, format3=None):
        """Creates the new Log object
        Cannot be called with more than 3 formatting strings"""
        if log in STANDARD_LOGS.keys():
            self.log_string = STANDARD_LOGS[log].format(format1, format2, format3)
        elif type(log) == Log:
            self.log_string = log.log_string
        else:
            self.log_string = log
    
    def __repr__(self):
        """Returns the string value of the log, as it's representation"""
        return self.log_string
    
    def append_log(self, otherlog):
        """Returns a new Log object, where otherlog.log_string was added to
        the end of self.log_string WITH NO OTHER FORMATTING
        """
        return Log(self.log_string + otherlog.log_string)
    
    def add_newline_log(self, otherlog):
        """Returns a new Log object, where a newline character followed by
        otherlog.log_string was added to self.log_string
        """
        return Log(self.log_string + "\n" + otherlog.log_string)

class Logbook:
    """
    """
    def __init__(self, logs=[]):
        """"""
        self.log_list = logs
    
    def __repr__(self):
        """Returns a string formatted correctly as a logbook"""
        pass
    
    def add_log(self, log):
        """Adds the block of text to the list to be displayed"""
        self.log_list.append(block)