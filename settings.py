import os
from os import environ

import dj_database_url
from boto.mturk import qualification

import otree.settings


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# the environment variable OTREE_PRODUCTION controls whether Django runs in
# DEBUG mode. If OTREE_PRODUCTION==1, then DEBUG=False
if environ.get('OTREE_PRODUCTION') not in {None, '', '0'}:
    DEBUG = False
else:
    DEBUG = True

# don't share this with anybody.
SECRET_KEY = '2$8ov+&por@ab)d*#v#@upknv=8^^$5a64g$dvsiynxe*7216g'


# DATABASES = {
#     'default': dj_database_url.config(
#         # Rather than hardcoding the DB parameters here,
#         # it's recommended to set the DATABASE_URL environment variable.
#         # This will allow you to use SQLite locally, and postgres/mysql
#         # on the server
#         # Examples:
#         # export DATABASE_URL=postgres://USER:PASSWORD@HOST:PORT/NAME
#         # export DATABASE_URL=mysql://USER:PASSWORD@HOST:PORT/NAME

#         # fall back to SQLite if the DATABASE_URL env var is missing
#         default='sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3')
#     )
# }

# AUTH_LEVEL:
# this setting controls which parts of your site are freely accessible,
# and which are password protected:
# - If it's not set (the default), then the whole site is freely accessible.
# - If you are launching a study and want visitors to only be able to
#   play your app if you provided them with a start link, set it to STUDY.
# - If you would like to put your site online in public demo mode where
#   anybody can play a demo version of your game, but not access the rest
#   of the admin interface, set it to DEMO.

# for flexibility, you can set it in the environment variable OTREE_AUTH_LEVEL
AUTH_LEVEL = environ.get('OTREE_AUTH_LEVEL')
ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = 'billy'


# setting for integration with AWS Mturk
AWS_ACCESS_KEY_ID = environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = environ.get('AWS_SECRET_ACCESS_KEY')


# e.g. EUR, CAD, GBP, CHF, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
#Need to use this for Risk and Fairness
USE_POINTS = True 


# e.g. en, de, fr, it, ja, zh-hans
# see: https://docs.djangoproject.com/en/1.9/topics/i18n/#term-language-code
LANGUAGE_CODE = 'es'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']

# SENTRY_DSN = ''

DEMO_PAGE_INTRO_TEXT = """
<ul>
    <li>
        <a href="https://github.com/oTree-org/otree" target="_blank">
            oTree on GitHub
        </a>.
    </li>
    <li>
        <a href="http://www.otree.org/" target="_blank">
            oTree homepage
        </a>.
    </li>
</ul>
<p>
    Here are various games implemented with oTree. These games are all open
    source, and you can modify them as you wish.
</p>
"""

ROOMS = [
    {
        'name': 'Econ_Lab',
        'display_name': 'Econ_Lab_202',
        'participant_label_file': '_rooms/RP.txt',
        'use_secure_urls': True,
    },
    {
        'name': 'live_demo',
        'display_name': 'Room for live demo (no participant labels)',
    },
]


# from here on are qualifications requirements for workers
# see description for requirements on Amazon Mechanical Turk website:
# http://docs.aws.amazon.com/AWSMechTurk/latest/AWSMturkAPI/ApiReference_QualificationRequirementDataStructureArticle.html
# and also in docs for boto:
# https://boto.readthedocs.org/en/latest/ref/mturk.html?highlight=mturk#module-boto.mturk.qualification

mturk_hit_settings = {
    'keywords': ['easy', 'bonus', 'choice', 'study'],
    'title': 'Title for your experiment',
    'description': 'Description for your experiment',
    'frame_height': 500,
    'preview_template': 'global/MTurkPreview.html',
    'minutes_allotted_per_assignment': 60,
    'expiration_hours': 7*24, # 7 days
    #'grant_qualification_id': 'YOUR_QUALIFICATION_ID_HERE',# to prevent retakes
    'qualification_requirements': [
        # qualification.LocaleRequirement("EqualTo", "US"),
        # qualification.PercentAssignmentsApprovedRequirement("GreaterThanOrEqualTo", 50),
        # qualification.NumberHitsApprovedRequirement("GreaterThanOrEqualTo", 5),
        # qualification.Requirement('YOUR_QUALIFICATION_ID_HERE', 'DoesNotExist')
    ]
}


# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = {
    'real_world_currency_per_point': 2.00,
    'participation_fee': 10.00,
    'doc': "",
    'mturk_hit_settings': mturk_hit_settings,
}
PARTICIPANT_FIELDS = [
        'tareas_yo_hoy',
        'tareas_yo_manana',
        'tareas_partner_hoy',
        'tareas_partner_manana'
]
SESSION_CONFIGS = [ 
  #   {
  #       'name': 'risky_preferences',
  #       'display_name': "Preference for Risk: The Revenge",
  #       'num_demo_participants': 1,
  #       'app_sequence': ['risky_preferences'],
  #   },
  #  {
  #       'name': 'random_reference',
  #      'display_name': "Preferences for Randomization II: Losses or Gains",
  #       'num_demo_participants': 1,
  #      'app_sequence': ['random_reference'],
  #  },
  #  {
  #      'name': 'random_reference2',
  #      'display_name': "Preferences for Randomization II: Gains or Losses",
  #      'num_demo_participants': 1,
  #      'app_sequence': ['random_reference2'],
  #  },
  #  {
  #      'name': 'risky_preferencesAH',
  #      'display_name': "Risk Preferences AH",
  #      'num_demo_participants': 1,
  #      'app_sequence': ['risky_preferencesAH'],
  #  },
    {
        'name': 'demograp_es',
        'name': 'time_others',
        'display_name': 'Time others',
        'num_demo_participants': 2,
        'real_world_currency_per_point': 0.33,
        'participation_fee': 5.00,
        'app_sequence': ['time_others_instructions','real_effort','time_others','real_effort2']
    },
    {
        'name': 'demograp',
        'display_name': 'Questions',
        'num_demo_participants': 1,
        'app_sequence': ['demograp_es']
    },
]

#Activates Sentry:
SENTRY_DSN = 'http://cef5e70f5ff14cfeaefc70c9a320102d:710fd43a8a6e4cecb32c365a1dba5b8a@sentry.otree.org/222'

# anything you put after the below line will override
# oTree's default settings. Use with caution.
otree.settings.augment_settings(globals())
DEBUG = True