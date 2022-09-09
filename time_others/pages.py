from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants
from . import config
import random

"""
Principal maintainer: Eli Pandolfo <epandolf@ucsc.edu>
Contributors:
    Kristian Lopez Vargas <kristianlvargas@gmail.com>
    Rachel Chen <me@rachelchen.me>
"""

class Secuencia_bloques(Page):
    form_model = 'player'

    def is_displayed(self):
        return self.round_number == 1 or self.round_number == 16 or self.round_number == 36 or self.round_number == 41

    def vars_for_template(self):
        dynamic_values = self.player.participant.vars['dynamic_values']
        round_data = dynamic_values[self.round_number - 1]
        mode = round_data['mode']
        # this will be used in the conditional display of instructions
        return {'dynamic_values': dynamic_values,
                'mode': mode,
                'sec0': '' if mode in ['probability', 'det_giv'] else mode.split('_')[0],
                'sec1': '' if mode in ['probability', 'det_giv'] else mode.split('_')[1],
                'sec2': '' if mode in ['probability', 'det_giv', 'sec_ownrisk'] else mode.split('_')[2],
                }

class AntesdelBloque(Page):
    form_model = 'player'

    def is_displayed(self):
        return self.round_number == 1 or self.round_number == 6 or self.round_number == 11 or self.round_number == 16  or self.round_number == 21 or self.round_number == 26 or self.round_number == 31 or self.round_number == 36 or self.round_number == 41
    
    def vars_for_template(self):
        random_number=Constants.random_number
        # this will be used in the conditional display of instructions
        return {'random_number': random_number}

class TaskInstructions(Page):
    form_model = 'player'
    form_fields = ['time_TaskInstructions']

    def is_displayed(self):
        return self.round_number == 1 or self.round_number == 16 or self.round_number == 36 or self.round_number == 41

    def vars_for_template(self):
        dynamic_values = self.player.participant.vars['dynamic_values']
        round_data = dynamic_values[self.round_number - 1]
        mode = round_data['mode']
        # this will be used in the conditional display of instructions
        return {'dynamic_values': dynamic_values,
                'mode': mode,
                'sec0': '' if mode in ['probability', 'det_giv'] else mode.split('_')[0],
                'sec1': '' if mode in ['probability', 'det_giv'] else mode.split('_')[1],
                'sec2': '' if mode in ['probability', 'det_giv', 'sec_ownrisk'] else mode.split('_')[2],
                }

        
class ControlQuestions(Page):
    form_model = 'player'
    form_fields = ['time_ControlQuestions', 'cq_failed_attempts', 'cq_a1', 'cq_a2']

    def is_displayed(self):
        mode = self.player.participant.vars['dynamic_values'][self.round_number - 1]['mode']
        if self.round_number > 1:
            prevmode = self.player.participant.vars['dynamic_values'][self.round_number - 2]['mode']
        return self.round_number == 1 or mode != prevmode

    def vars_for_template(self):
        dynamic_values = self.player.participant.vars['dynamic_values']
        round_data = dynamic_values[self.round_number - 1]
        mode = round_data['mode']

        return {'mode': mode}

    #def get_form_fields(self):


class Task(Page):
    form_model = 'player'

    def get_form_fields(self):
        dynamic_values = self.player.participant.vars['dynamic_values']
        round_data = dynamic_values[self.round_number - 1]
        if round_data is not None and round_data['mode'] is not None:
            if round_data['mode'] == 'det_giv':
                return ['mode', 'me_a', 'me_b', 'time_Graph', 'm', 'px', 'py']
            elif round_data['mode'] == 'probability':
                return ['mode', 'prob_a', 'prob_b', 'time_Graph', 'ax', 'ay', 'bx', 'by']
            elif round_data['mode'] == 'sec_ownrisk':
                return ['mode', 'me_a', 'me_b', 'prob_a', 'prob_b', 'time_Graph', 'm', 'px', 'py']
            elif round_data['mode'] == 'sec_ownrisk_fixedother' or round_data['mode'] == 'sec_otherrisk_ownfixed':
                return ['mode', 'partner_a', 'partner_b', 'me_a', 'me_b', 'prob_a',
                        'prob_b', 'time_Graph', 'm', 'px', 'py', 'a', 'b']
            else:
                return ['mode', 'partner_a', 'partner_b', 'me_a', 'me_b', 'prob_a',
                        'prob_b', 'time_Graph', 'm', 'px', 'py']
        else:
            return ['mode', 'partner_a', 'partner_b', 'me_a', 'me_b', 'prob_a', 'prob_b', 'time_Graph']

    def vars_for_template(self):
        dynamic_values = self.player.participant.vars['dynamic_values']
        mode = self.player.participant.vars['dynamic_values'][self.round_number - 1]['mode']
        #create random number(1: block 1, 2: block 2) for block 3:
        random_number = Constants.random_number
        print('MODE MODE MODE', mode)
        if self.round_number > 1:
            counter = 1
            prevmode = self.player.participant.vars['dynamic_values'][self.round_number - 2]['mode']
            while mode == prevmode:
                counter += 1;
                if counter == self.round_number:
                    break
                prevmode = self.player.participant.vars['dynamic_values'][self.round_number - (counter + 1)]['mode']
        else:
            counter = 1
        return {'dynamic_values': dynamic_values,
                'mode': mode,
                'counter': counter,
                'sec1': '' if mode in ['probability', 'det_giv'] else mode.split('_')[1],
                'sec2': '' if mode in ['probability', 'det_giv', 'sec_ownrisk'] else mode.split('_')[2],
                'random_number': random_number
                }

    def before_next_page(self):
        if self.group.get_player_by_id(1).participant.vars['pr_dict']['mode'] == 'sec_ownrisk' \
                and self.round_number == self.player.participant.vars['pr']:
            self.player.set_payoffs()
        elif self.player.id_in_group == 1 and self.round_number == self.player.participant.vars['pr']:
            self.group.set_payoffs()


class Finalizar_tareas(Page):
    form_model = 'player'

    def is_displayed(self):
        return self.round_number == Constants.num_rounds

class Determinar_tareas(Page):
    form_model = 'player'

    def is_displayed(self):
        return self.round_number == Constants.num_rounds
    
    def vars_for_template(self):
        role = self.player.role()
        return {'role' : role}

class ResultsWaitPage(WaitPage):

    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def after_all_players_arrive(self):
        pass

class Results(Page):

    form_model = 'player'
    form_fields = ['time_Results']

    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def vars_for_template(self):

        modeMap = {
        'probability': 'PR',
        'sec_1bl_1ch': 'S-1B-1C',
        'sec_1bl_2ch': 'S-1B-2C',
        'sec_2bl_1ch': 'S-2B-1C',
        'sec_ownrisk': 'S-OwnRisk',
        'det_giv': 'DG',
        'sec_ownrisk_fixedother': 'S-OwnRisk-FixedOther',
        'sec_otherrisk_ownfixed': 'S-OtherRisk-OwnFixed',
        'sec_new_graph':'S-newone'}

        modeNum = {
        'probability': '1',
        'sec_1bl_1ch': '2',
        'sec_1bl_2ch': '4',
        'sec_2bl_1ch': '3',
        'sec_ownrisk': '5',
        'det_giv': '8',
        'sec_new_graph':'9',
        'sec_ownrisk_fixedother': '6',
        'sec_otherrisk_ownfixed': '7'}

        # variables:
        mode = self.group.get_player_by_id(1).participant.vars['pr_dict']['mode']

        decider = self.group.get_player_by_id(1)
        nondecider = self.group.get_player_by_id(2)

        pr = decider.participant.vars['pr']
        pr2 = nondecider.participant.vars['pr']
        # if mode == 'probability':
        #     deci_a = round(decider.in_round(pr).prob_a, 1)
        #     deci_b = round(decider.in_round(pr).prob_b, 1)
        # elif mode == 'det_giv':
        #     if self.player.id_in_group == 1:
        #         deci_a = round(decider.in_round(pr).me_a, 1) 
        #         deci_b = None
        #     else:
        #         deci_a = round(decider.in_round(pr).me_b, 1)
        #         deci_b = None
        # else:
        if self.player.id_in_group == 1:
                dec_yo_hoy = round(decider.in_round(pr).me_a, 1)
                dec_yo_manana = round(decider.in_round(pr).me_b, 1)
                dec_partner_hoy = round(decider.in_round(pr).partner_a, 1)
                dec_partner_manana = round(decider.in_round(pr).partner_b, 1)
                
        elif mode != 'sec_ownrisk':
                dec_yo_hoy = round(decider.in_round(pr).partner_a, 1)
                dec_yo_manana = round(decider.in_round(pr).partner_b, 1)
                dec_partner_hoy = round(decider.in_round(pr).me_a, 1)
                dec_partner_manana = round(decider.in_round(pr).me_b, 1)

            # single mode
            # else:
            #     deci_a = round(nondecider.in_round(pr2).me_a, 1)
            #     deci_b = round(nondecider.in_round(pr2).me_b, 1)

        outcome = self.player.in_round(self.player.participant.vars['pr']).outcome
        #payoff = self.player.in_round(Constants.num_rounds).payoff

        payoff = self.player.in_round(self.player.participant.vars['pr']).payoff
        if self.player.id_in_group == 1:
            partner_payoff = nondecider.in_round(self.group.get_player_by_id(2).participant.vars['pr']).payoff
        else:
            partner_payoff = decider.in_round(self.group.get_player_by_id(1).participant.vars['pr']).payoff

        role = self.player.role()

        if self.player.participant.vars['pr'] - 1 > 0:
            counter = 1
            prevmode = self.player.participant.vars['dynamic_values'][self.player.participant.vars['pr'] - 2]['mode']
            while mode == prevmode:
                counter += 1;
                if counter == self.player.participant.vars['pr']:
                    break
                prevmode = self.player.participant.vars['dynamic_values'] \
                            [self.player.participant.vars['pr'] - (counter + 1)]['mode']
        else:
            counter = 1
        
        return {'mode': modeMap[mode], 'mode_num': modeNum[mode],  'role': role,
                    'counter': counter, 'outcome': outcome, 'payoff': payoff, 'partner_payoff': partner_payoff,
                    'dec_yo_hoy': dec_yo_hoy, 'dec_partner_hoy': dec_partner_hoy, 'dec_yo_manana': dec_yo_manana, 
                    'dec_partner_manana': dec_partner_manana}



page_sequence = [
    Secuencia_bloques,
    TaskInstructions,
    AntesdelBloque,
    Task,
    Finalizar_tareas,
    Determinar_tareas,
    ResultsWaitPage,
    Results
]


# yes | otree resetdb && otree runserver
