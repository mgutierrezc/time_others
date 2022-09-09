from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


def levenshtein(a, b):
    """Calculates the Levenshtein distance between a and b."""
    n, m = len(a), len(b)
    if n > m:
        # Make sure n <= m, to use O(min(n, m)) space
        a, b = b, a
        n, m = m, n

    current = range(n + 1)

    for i in range(1, m + 1):
        previous, current = current, [i] + [0] * n
        for j in range(1, n + 1):
            add, delete = previous[j] + 1, current[j - 1] + 1
            change = previous[j - 1]

            if a[j - 1] != b[i - 1]:
                change = change + 1
            current[j] = min(add, delete, change)

    return current[n]


def distance_and_ok(transcribed_text, reference_text, max_error_rate):
    error_threshold = len(reference_text) * max_error_rate
    distance = levenshtein(transcribed_text, reference_text)
    ok = distance <= error_threshold
    return distance, ok

class Constants(BaseConstants):
    name_in_url = 'real_effort'
    num_rounds = 1 #10 para los pilotos/produccion
    #num_groups = 1
    players_per_group = None
    info_code = 'real_effort/Code.html'

    #List of the incomprehensible text that the players must transcribe
    reference_texts = [
        "Revealed preference",
        "Hex ton satoha egavecen. Loh ta receso minenes da linoyiy xese coreliet ocotine! Senuh asud tu bubo "
        "tixorut sola, bo ipacape le rorisin lesiku etutale saseriec niyacin ponim na. Ri arariye senayi esoced "
        "behin? Tefid oveve duk mosar rototo buc: Leseri binin nolelar sise etolegus ibosa farare. Desac eno "
        "titeda res vab no mes!",
    ]

    maxdistance1 = len(reference_texts[0])
    maxdistance2 = len(reference_texts[1])

    allowed_error_rates = [0, 0.8]
    difficulty = 1
    ratio = 1
    endowment = 2
    income = 0


class Subsession(BaseSubsession):
    pass



class Group(BaseGroup):
    baseIncome = models.CurrencyField()
    total_report = models.CurrencyField()
    #total_contribution = models.CurrencyField()
    total_earnings = models.CurrencyField()
    #individual_share = models.CurrencyField()
    temp = models.IntegerField()
    transcription_required = models.BooleanField() # True if required, else False
    treatment_tag = models.StringField() # tag of current treatment
    transcription_difficulty = models.IntegerField()


class Player(BasePlayer):
    transcribed_text = models.LongStringField()
    transcribed_text2 = models.LongStringField()
    levenshtein_distance = models.IntegerField()
    ratio = models.FloatField()
    done = models.BooleanField()
    transcriptionDone = models.BooleanField()
    income = models.CurrencyField()
    refText = models.LongStringField()