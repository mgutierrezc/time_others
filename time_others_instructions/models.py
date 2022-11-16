from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

class Constants(BaseConstants):
    name_in_url = 'time_others_instructions'
    num_rounds = 1
    #num_groups = 1
    players_per_group = None

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    time_InitialInstructions_1 = models.LongStringField()
    time_InitialInstructions_2 = models.LongStringField()
    time_InitialInstructions_3 = models.LongStringField()
    time_InitialInstructions_4 = models.LongStringField()