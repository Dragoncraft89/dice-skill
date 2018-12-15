from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill, intent_handler
from mycroft.util.log import LOG

import random

class DiceSkill(MycroftSkill):

    def __init__(self):
        super(DiceSkill, self).__init__(name="DiceSkill")

    @intent_handler(IntentBuilder("").require("Roll").require("Dice"))
    def handle_roll_dice_intent(self, message):
        dice = message.data.get('Dice')

        # Dice defaults
        dice_count = 1
        dice_range = 6

        if dice != 'dice':
            split = dice.split('d')
            dice_range = int(split[1].strip())
            if split[0] != '':
                try:
                    dice_count = int(split[0].strip())
                except:
                    pass

        numbers = [random.randint(1, dice_range) for i in range(dice_count)]

        if len(numbers) == 1:
            self.speak_dialog("single.result", data={"result" : numbers[0]})
        else:
            self.speak_dialog("multiple.result", data={"result" : ', '.join([str(x) for x in numbers])})

    @intent_handler(IntentBuilder("").require("Number").optionally("Range"))
    def handle_generate_number_intent(self, message):
        range_input = message.data.get('Range')
        low = 1
        high = 10
        
        if range_input:
            range_split = range_input.split(' ')
            
            low = int(range_split[0])
            high = int(range_split[2])
        else:
            self.speak_dialog("range.needed")
            return
        
        if low > high:
            low, high = high, low
        self.speak_dialog("single.result", data={"result" : random.randint(low, high)})

def create_skill():
    return DiceSkill()
