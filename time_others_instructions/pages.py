from otree.api import Currency as c, currency_range
from .builtin import Page, WaitPage
from .models import Constants


class InitialInstructions_1(Page):
    form_model = 'player'
    form_fields = ['time_InitialInstructions_1']

    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return {'participation_fee': self.session.config['participation_fee']}

class InitialInstructions_2(Page):
    form_model = 'player'
    form_fields = ['time_InitialInstructions_2']

    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return {'participation_fee': self.session.config['participation_fee']}

class InitialInstructions_3(Page):
    form_model = 'player'
    form_fields = ['time_InitialInstructions_3']

    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return {'participation_fee': self.session.config['participation_fee']}

class InitialInstructions_4(Page):
    form_model = 'player'
    form_fields = ['time_InitialInstructions_4']

    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return {'participation_fee': self.session.config['participation_fee']}


page_sequence = [InitialInstructions_1, 
                InitialInstructions_2, 
                InitialInstructions_3,
                InitialInstructions_4]
