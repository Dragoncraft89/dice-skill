# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring,redefined-outer-name
import random

from ovos_workshop.decorators import intent_handler
from ovos_workshop.skills import OVOSSkill
from lingua_franca.parse import extract_number


class DiceSkill(OVOSSkill):
    def __init__(self, *args, **kwargs):
        super(*args, **kwargs).__init__()

    @intent_handler("Dice.intent")
    def handle_roll_dice_intent(self, message):
        dice_count = message.data.get("count") or "1"
        dice_count = int(extract_number(dice_count))
        dice_type = message.data.get("type") or "6"
        modificator = message.data.get("modifier")
        if modificator:
            modificator = int(extract_number(modificator))

        self.roll(dice_count, int(dice_type), modificator)

    @intent_handler("NormalDice.intent")
    def handle_roll_normal_intent(self, message):
        dice_count = message.data.get("count") or "1"
        dice_count = int(extract_number(dice_count))
        self.roll(dice_count, 6, None)

    def roll(self, dice_count, dice_range, modificator):
        numbers = [random.randint(1, dice_range) for i in range(dice_count)]
        if modificator:
            total = sum(numbers) + modificator
            if len(numbers) == 1:
                self.speak_dialog("single.modificator.result", data={"result": numbers[0], "total": total})
            else:
                self.speak_dialog(
                    "multiple.modificator.result",
                    data={"result": ", ".join([str(x) for x in numbers]), "total": total},
                )
        else:
            if len(numbers) == 1:
                self.speak_dialog("single.result", data={"result": numbers[0]})
            else:
                self.speak_dialog("multiple.result", data={"result": ", ".join([str(x) for x in numbers])})

    @intent_handler("Range.intent")
    def handle_generate_number_intent(self, message):
        low = extract_number(message.data.get("low"))
        high = extract_number(message.data.get("high"))

        if low > high:
            low, high = high, low
        self.speak_dialog("single.result", data={"result": random.randint(low, high)})
