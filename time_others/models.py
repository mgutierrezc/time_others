from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
from . import config
import random

"""
Principal maintainer: Eli Pandolfo <epandolf@ucsc.edu>
Contributors:
    Kristian Lopez Vargas <kristianlvargas@gmail.com>
    Rachel Chen <me@rachelchen.me>
"""


class Constants(BaseConstants):
    name_in_url = 'time_others'
    players_per_group = 2
    num_rounds = config.numberOfPeriod()
    participation_fee = c(5)
    random_number = random.randint(1,2) #si es 1, el bloque 3 tendrá las decisiones del bloque 1. Si es 2, del bloque 2.

    # I'm offloading the heavy lifting to JavaScript because I'm very bad at Python
    static_values = {
        'precision': 1,         # number of decimals
        'scale': {
            'type': 'fixed',    # axis scaling, could be "fixed" or "dynamic"
            'max': 100          # only used in "fixed"
        },
        # only used in probability mode
        'constants': {
            'k': 0.4,          # scaling factor, only used in 'probability' mode
            'maxArea': 100
        },
        'width': 600,            # width of the graph
        'height': 600,           # height of the graph
        'margin': {              # graph margins
            'top': 20,
            'right': 20,
            'bottom': 50,
            'left': 50
        }
    }
    default_values = {
        'mode': 'sec_2bl_1ch',
        'label': {
            'x': 'State A',
            'y': 'State B'
        },
        # only used in security mode (aka non-probability mode)
        'equation': {
            'm': 100,           # income
            'px': 1,            # price of X
            'py': 2,            # price of Y
            #'m2': 100,           # income
            #'px2': 1,            # price of X
            #'py2': 2,            # price of Y
            'a_x': 30,        # x value of point A
            'a_y': 80,         # y value of point A
            'b_x': 65,        # x value of point B
            'b_y': 45         # y value of point B
        },
        'prob': {
            'a': 100,
            'b': 0
        }
    }
    
    # not flattened
    dynamic_values = config.getDynamicValues()

    # number of different task types
    number_types_of_tasks = len(set([d['mode'] for d in config.flatten(dynamic_values)]))


    # INSTRUCTIONS PATHS
    # list instruction templates
    trial_period = 'time_others/trial_period.html'


class Player(BasePlayer):

    # each player has its own shuffled data, and its own paying round number (starting at 1)
    # (the paying round is the same for all players, but the index of that round is unique for each shuffled dataset)

    mode = models.StringField()
    partner_a = models.FloatField() # Circle is other
    partner_b = models.FloatField()
    me_a = models.FloatField() # Square is me
    me_b = models.FloatField()
    prob_a = models.FloatField()
    prob_b = models.FloatField()
    outcome = models.StringField()
    cq_failed_attempts = models.IntegerField()
    cq_a1 = models.LongStringField()
    cq_a2 = models.LongStringField()
    time_TaskInstructions =  models.LongStringField()
    time_ControlQuestions = models.LongStringField()
    time_Graph =  models.LongStringField()
    time_Results =  models.LongStringField()

    m = models.FloatField()
    px = models.FloatField()
    py = models.FloatField()
    #nuevas variables del modelo
    m2 = models.FloatField()
    px2 = models.FloatField()
    py2 = models.FloatField()

    a = models.FloatField()
    b = models.FloatField()
    ax = models.FloatField()
    ay = models.FloatField()
    bx = models.FloatField()
    by = models.FloatField()
    bloque = models.StringField()
    

    def role(self):
        if self.id_in_group == 1:
            return 'Decider'
        else:
            return 'Non-Decider'
    
    def set_payoffs(self):
        round_data = self.participant.vars['dynamic_values'][self.round_number - 1]
        print('round data in set payoffs', round_data)

        rnd = random.random()
        print('random rnd', rnd)

        self.payoff = (rnd < round_data['prob_a'] / 100) * self.me_a + (rnd >= round_data['prob_a'] / 100) * self.me_b
        self.outcome = 'A' if rnd < round_data['prob_a'] / 100 else 'B'
            
class Group(BaseGroup):

    # sets the shuffled dynamic values for each player and stores them in the participant.vars dictionary,
    # which every participant has
    def set_dv(self, chosen_round=None):
        p1 = self.get_player_by_id(1)
        p2 = self.get_player_by_id(2)
        
        # there is no group.vars dictionary, so we use player 1's participant.vars dict to store group data

        # this is the paying round for the group -- a random int between 1 and the number of rounds that 
        # corresponds to a dictionary in dynamic_values. It is stored in player 1's participant.vars
        if chosen_round == None:
            p1.participant.vars['group_pr'] = random.randint(1, Constants.num_rounds)
        else:
            p1.participant.vars['group_pr'] = chosen_round
        
        # this is the dictionary at that line (the data for the paying round). Stored in player 1's
        # participant.vars
        p1.participant.vars['pr_dict'] = config.flatten(Constants.dynamic_values)[p1.participant.vars['group_pr'] - 1]
        
        # the shuffled dynamic_values for player 1
        p1.participant.vars['dynamic_values'] = config.flatten(config.shuffle(Constants.dynamic_values))
        
        # player 1's paying round. Retrieved by getting the index of pr_dict in player 1's dynamic values
        p1.participant.vars['pr'] = p1.participant.vars['dynamic_values'].index(p1.participant.vars['pr_dict']) + 1

        # the shuffled dynamic_values for player 2
        p2.participant.vars['dynamic_values'] = config.flatten(config.shuffle(Constants.dynamic_values))

        # player 2's paying round. Retrieved by getting the index of pr_dict in player 2's dynamic values
        p2.participant.vars['pr'] = p2.participant.vars['dynamic_values'].index(p1.participant.vars['pr_dict']) + 1
        
        # --------------------------------------------------------------------------------------------------------------
        # some print statements for checking the group paying round, the round data at that round,
        # each player's paying round, each player's dynamic values
        # print('GROUP PAYING ROUND', p1.participant.vars['group_pr'])
        # print('\nPR DICT', p1.participant.vars['pr_dict'])
        # print('\nPLAYER 1 PAYING ROUND', p1.participant.vars['pr])
        # print('\nPLAYER 1 DV', p1.participant.vars['dynamic_values'])
        # print('\nPLAYER 2 PAYING ROUND', p2.participant.vars['pr])
        # print('\nPLAYER 2 DV', p2.participant.vars['dynamic_values'])
        # --------------------------------------------------------------------------------------------------------------

    def set_payoffs(self):

        modeMap = {
        'probability': 'probability',
        'sec_1bl_1ch': 'positive',
        'sec_2bl_1ch': 'negative',
        'sec_1bl_2ch': 'independent',
        'sec_ownrisk': 'single',
        'sec_ownrisk_fixedother': 'single_fixedcircle',
        'sec_otherrisk_ownfixed': 'single_fixedsquare',
        'det_giv': 'single_given',
        #nuevo caso añadido
        'sec_new_graph':'newone',
        'dictator': 'new_single'}
        
        # generate pseudo_random number to compare to probabilities  0 <= rnd <= 1
        rnd = random.random()
        print('random rnd', rnd)

        pr = self.get_player_by_id(1).participant.vars['pr']
        pr2 = self.get_player_by_id(2).participant.vars['pr']

        decider = self.get_player_by_role('Decider').in_round(pr)
        nondecider = self.get_player_by_role('Non-Decider').in_round(pr2)

        # pull dictionary of values for current round from decider
        round_data = decider.participant.vars['dynamic_values'][self.round_number - 1]
        print('round data in set payoffs', round_data)

        if modeMap[round_data['mode']] in ['probability']:
            decider.payoff = \
                (rnd < decider.prob_a / 100) * round_data['a_x'] + (rnd >= decider.prob_a / 100) * round_data['b_x']
            decider.outcome = 'A' if rnd < decider.prob_a / 100 else 'B'
            nondecider.payoff = \
                (rnd < decider.prob_a / 100) * round_data['a_y'] + (rnd >= decider.prob_a / 100) * round_data['b_y']
            nondecider.outcome = decider.outcome
        elif modeMap[round_data['mode']] in ['positive', 'negative', 'independent','newone']:
            decider.payoff = \
                (rnd < round_data['prob_a'] / 100) * decider.me_a + (rnd >= round_data['prob_a'] / 100) * decider.me_b
            decider.outcome = 'A' if rnd < round_data['prob_a'] / 100 else 'B'
            nondecider.payoff = \
                (rnd < round_data['prob_a'] / 100) * decider.partner_a + (rnd >= round_data['prob_a'] / 100) * decider.partner_b
            nondecider.outcome = decider.outcome
        elif modeMap[round_data['mode']] == 'single_fixedsquare':
            decider.payoff = \
                (rnd < round_data['prob_a'] / 100) * decider.me_a + (rnd >= round_data['prob_a'] / 100) * decider.me_b
            decider.outcome = 'A' if rnd < round_data['prob_a'] / 100 else 'B'
            nondecider.payoff = \
                (rnd < round_data['prob_a'] / 100) * decider.partner_a + (rnd >= round_data['prob_a'] / 100) * decider.partner_b
            nondecider.outcome = decider.outcome
        elif modeMap[round_data['mode']] == 'single_fixedcircle':
            decider.payoff = \
                (rnd < round_data['prob_a'] / 100) * decider.me_a + (rnd >= round_data['prob_a'] / 100) * decider.me_b
            decider.outcome = 'A' if rnd < round_data['prob_a'] / 100 else 'B'
            nondecider.payoff = \
                (rnd < round_data['prob_a'] / 100) * decider.partner_a + (rnd >= round_data['prob_a'] / 100) * decider.partner_b
            nondecider.outcome = decider.outcome
        elif modeMap[round_data['mode']] == 'single_given':
            decider.payoff = decider.me_a
            nondecider.payoff = decider.me_b # this is really partner_a

class Subsession(BaseSubsession):
    def creating_session(self):
        if self.round_number == 1:
            self.group_randomly()
            chosen_rounds = config.getChosenRounds()
            i = 0
            # the number of groups needs to be the same as the number of elements in chosen_rounds
            for group in self.get_groups():
                if chosen_rounds == None:
                    group.set_dv()
                else:
                    group.set_dv(chosen_rounds[i])
                    i += 1
        else:
            self.group_like_round(1)


# git add
# cd .. && yes | otree resetdb && otree runserver && cd RiskAndFairness_oTree
# yes | otree resetdb && otree runserver
# git add ______ && git commit -m "_______________" && git push
