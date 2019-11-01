from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill, intent_handler, intent_file_handler
from mycroft.util.log import LOG
from mycroft.util.parse import extract_number, normalize

import random
import re

class DiceSkill(MycroftSkill):

    def __init__(self):
        super(DiceSkill, self).__init__(name="DiceSkill")

    @intent_file_handler("Dice.intent")
    def handle_roll_dice_intent(self, message):
        dice_count = extract_number(message.data.get('count')) or 1
        dice_type = message.data.get('type')
        modificator = message.data.get('modifier')
        if modificator:
            modificator = int(extract_number(modificator))

        self.roll(dice_count, int(dice_type), modificator)

    @intent_file_handler("NormalDice.intent")
    def handle_roll_normal_intent(self, message):
        dice_count = extract_number(message.data.get('count'))  or 1
        self.roll(dice_count, 6, 0)
            
    def roll(self, dice_count, dice_range, modificator):
        numbers = [random.randint(1, dice_range) for i in range(dice_count)]
        if modificator:
            total = sum(numbers) + modificator
            if len(numbers) == 1:
                self.speak_dialog("single.modificator.result" , data={"result" : numbers[0], "total" : total})
            else:
                self.speak_dialog("multiple.modificator.result", data={"result" : ', '.join([str(x) for x in numbers]), "total": total})
        else:
            if len(numbers) == 1:
                self.speak_dialog("single.result", data={"result" : numbers[0]})
            else:
                self.speak_dialog("multiple.result", data={"result" : ', '.join([str(x) for x in numbers])})

    @intent_file_handler("Range.intent")
    def handle_generate_number_intent(self, message):
        low = extract_number(message.data.get('low'))
        high = extract_number(message.data.get('high'))
        
        if low > high:
            low, high = high, low
        self.speak_dialog("single.result", data={"result" : random.randint(low, high)})

def create_skill():
    return DiceSkill()
