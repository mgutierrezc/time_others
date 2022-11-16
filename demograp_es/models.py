# -*- coding: utf-8 -*-
# <standard imports>
from __future__ import division
from otree.db import models
from otree.constants import BaseConstants
from otree.models import BaseSubsession, BaseGroup, BasePlayer
from django.utils.translation import ugettext_lazy as _
from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
from otree.common import Currency as c, currency_range
import random
# </standard imports>




class Constants(BaseConstants):
    name_in_url = 'demograp_es'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    time_Demographics = models.TextField(widget=widgets.HiddenInput(attrs={'id': 'arrive_time'}))
    time_CognitiveReflectionTest = models.TextField(widget=widgets.HiddenInput(attrs={'id': 'arrive_time'}))

    def set_payoff(self):
        """Calculate payoff, which is zero for the survey"""
        self.payoff = 0

    q_country = models.CharField(verbose_name=_('What country are you from?'))

    q_major = models.CharField(verbose_name=_('What is your major?'))

    q_age = models.PositiveIntegerField(verbose_name=_('What is your age?'),
                                        min=18,
                                        max=120)

    q_school_year = models.CharField(initial=None,
                                 verbose_name=_('What is your school year?'),
                                 choices=[_('Freshman'), _('Sophomore'),_('Junior'),_('Senior'),_('Postgraduate'),_('Other')],
                                 widget=widgets.RadioSelect())

    q_station = models.PositiveIntegerField(verbose_name=_('What is your computer station number? (see white sticker on computer or ask experimenter)'),
                                        choices=range(1, 24),
                                        initial=None)

    q_gender = models.CharField(verbose_name=_('What do you identify as?'))

    q_income = models.PositiveIntegerField(verbose_name=_('What is the approximate annual income of your family?'),
                                           choices=[
                                               [1, _('less than $15,000')],
                                               [2, '$15,000 - $29,999'],
                                               [3, '$30,000 - $59,999'],
                                               [4, '$60,000 - $99,999'],
                                               [5, '$100,000 - $199,999'],
                                               [6, '$200,000 or more'],
                                               [7, _('I rather not answer this question')],
                                           ]
                                           )

    q_zipcode = models.PositiveIntegerField(verbose_name=_('What is the zip code where you grew up?'))

    q_opinion = models.CharField(initial=None,
                                 verbose_name=_('Were the instructions provided in this experiment clear and useful?'),
                                 choices=[_('Yes'), 'No'],
                                 widget=widgets.RadioSelect())

    q_linda = models.CharField(initial=None,
                                 verbose_name=_('Linda is 31 years old, single, outspoken, and very bright. She majored in philosophy. As a student, she was deeply concerned with issues of discrimination and social justice, and also participated in anti-nuclear demonstrations.\n\n Which of the following two alternatives is more probable?'),
                                 choices=[_('Linda is a bank teller.'), _('Linda is a bank teller and active in the feminist movement.')],
                                 widget=widgets.RadioSelect())

    q_monty = models.CharField(initial=None,
                                 verbose_name=_('Assume that a room is equipped with three doors. Behind two are goats, and behind the third is a shiny new car. You are asked to pick a door, and will win whatever is behind it. Someone who knows what is behind the doors opens one of the other two, revealing a goat and asks you if you wish to change your selection, you:'),
                                 choices=[_('change the door.'), _('do not change the door.')],
                                 widget=widgets.RadioSelect())

    q_how = models.CharField(verbose_name=_('How did you make your choices?'))

    q_rule = models.CharField(verbose_name=_('Did you have any rule you applied to your choices?'))

    q_number = models.PositiveIntegerField(verbose_name=_('How many studies have you participated in?'))

    crt_bat = models.PositiveIntegerField()

    crt_widget = models.PositiveIntegerField()

    crt_lake = models.PositiveIntegerField()
