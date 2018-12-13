from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill, intent_handler
from mycroft.util.log import LOG

class DiceSkill(MycroftSkill):

    def __init__(self):
        super(TemplateSkill, self).__init__(name="DiceSkill")

    @intent_handler(IntentBuilder("").require("Roll").require("Dice"))
    def handle_roll_dice_intent(self, message):
        pass

    @intent_handler(IntentBuilder("").require("Generate").require("Number").require("Range"))
    def handle_generate_number_intent(self, message):
        pass

def create_skill():
    return DiceSkill()
