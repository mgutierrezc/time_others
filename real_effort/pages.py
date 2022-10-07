from otree.api import Currency as c, currency_range
from .builtin import Page, WaitPage
from .models import Constants
from .models import levenshtein, distance_and_ok
from PIL import Image, ImageDraw, ImageFont
import math
from random import *
import random
import string

def writeText(text, fileName):
    """"This method generates the image with the garbled/randomized transcription text on it
    and saves it to fileName"""

    image = Image.open('real_effort/background.png')
    image = image.resize((650, 100))
    image.save('real_effort/background.png')
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('real_effort/roboto/Roboto-Regular.ttf', size=19)
    imageChars = 100
    numLines = len(text) / imageChars
    numLines = math.ceil(numLines)
    lines = []

    for i in range(numLines):
        if(imageChars * (i + 1) < len(text)):
            lines.append(text[imageChars * i : imageChars * (i+1)])
        else:
            lines.append(text[imageChars * i : len(text)])

    for i in range(numLines):
        (x, y) = (10, 20 * i)
        message = lines[i]
        print("Message is: ", message)
        color = 'rgb(0, 0, 0)' # black color
        draw.text((x, y), message, fill=color, font=font)

    image.save(fileName)

def generateText1(difficulty):
    """This method generates randomized garbled text whose difficulty to transcribe is based on the difficulty paramaeter
    (between 1 to 3) that's passed in."""

    min_char = 4 * difficulty
    max_char = min_char + 6
    allchar = string.ascii_lowercase + string.digits + string.punctuation
    vowels = ('a','e','i','o','u')

    #generated = "$eub:uuwhui eiu,u.ead^)ie{hp/irle.eug aw2x~auao`u.pi-[n+eaoqej."
    generated=""

    if(difficulty == 1):
        allchar = string.ascii_lowercase
    if(difficulty == 2):
        allchar = string.ascii_lowercase + string.digits
    for i in range(10):
        for i in range(5):
             allchar += vowels[i]
    
    while(len(generated) < 50 - max_char):
        add = "".join(choice(allchar) for x in range(randint(min_char, max_char)))
        generated += (add +".")

    return generated


def generateText2(difficulty):
    """This method generates randomized garbled text whose difficulty to transcribe is based on the difficulty paramaeter
    (between 1 to 3) that's passed in."""

    min_char = 4 * difficulty
    max_char = min_char + 6
    allchar = string.ascii_lowercase + string.digits + string.punctuation
    vowels = ('a', 'e', 'i', 'o', 'u')

    #generated = "$abgfnu% hgancnya @mk.o)qwbn[apzxc[*}-en45a.m_nbczpi45&|jsn-omn^"
    generated=""

    if (difficulty == 1):
        allchar = string.ascii_lowercase
    if (difficulty == 2):
        allchar = string.ascii_lowercase + string.digits
    for i in range(10):
        for i in range(5):
            allchar += vowels[i]

    while (len(generated) < 50 - max_char):
        add = "".join(choice(allchar) for x in range(randint(min_char, max_char)))
        generated += (add + ".")

    return generated


class InstructionsB(Page):
    """Description of the game block"""
    def is_displayed(self):
        return self.round_number == 1
    
class Transcribe1(Page):
    """First transcription task that's shown to the player that is merely for practice and does not determine the ratio
    for the player's starting income"""
    form_model = 'player'
    form_fields = ['transcribed_text2']

    def is_displayed(self):
        self.player.refText = generateText1(Constants.difficulty)
        # Don't display this Transcribe2 page if the "transcription" value in
        # the dictionary representing this round in config.py is False
        print("Inside Transcribe1 page")
        

        # if self.group.transcription_required == False or self.round_number != 1:
        #     self.player.ratio = 1 # income = endowment
        #     return False
        # else:
        #     return True

    def vars_for_template(self):
        
        writeText(self.player.refText, 'real_effort/static/real_effort2/paragraphs/{}.png'.format(self.player.id_in_group))
        return {
            'image_path': 'real_effort/static/real_effort2/paragraphs/{}.png'.format(1),
            'reference_text': self.player.refText,
            'round_num': self.player.round_number,
            'required_accuracy': 100 * (1 - Constants.allowed_error_rates[1]),
        }

    def before_next_page(self):
        """Initialize payoff to have a default value of 0"""
        self.player.payoff = 0


class Transcribe2(Page):
    """Second transcription task that's shown to the player that determines the ratios for the player's starting income"""
    form_model = 'player'
    form_fields = ['transcribed_text']

    # la transcripcion se aproxima al entero mas cercano si la parte decimal es mayor a .5 (no mayor igual)
    def is_displayed(self):
        print("Inside Transcribe2 page")
        # creating an image with the text to be transcribed
        self.player.refText = generateText2(Constants.difficulty)            
        writeText(self.player.refText, 'real_effort/static/real_effort2/paragraphs/{}.png'.format(2))
            
        return True

    def vars_for_template(self):
        return {
            'image_path': 'real_effort2/paragraphs/{}.png'.format(2),
            'reference_text': self.player.refText,
            'required_accuracy': 100 * (1 - Constants.allowed_error_rates[1]), # allows .8  error rate
            'round_num': self.player.round_number
        }

    def transcribed_text_error_message(self, transcribed_text):
        """Determines the player's transcription accuracy."""

        reference_text = self.player.refText
        allowed_error_rate = Constants.allowed_error_rates[1] # allows .8 error rate
        distance, ok = distance_and_ok(transcribed_text, reference_text,
                                       allowed_error_rate)
        if ok:
            self.player.levenshtein_distance = distance
            self.player.ratio = 1 - distance / Constants.maxdistance2
        else:
            if allowed_error_rate == 0:
                return "La transcripción debe ser exactamente igual a la original."
            else:
                return "Para avanzar, debes transcribir más caracteres similares a la transcripción original."

page_sequence = [InstructionsB, 
                Transcribe2]
