from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import pandas as pd
import os.path as path
from actions import appointments
from actions.utils.models import Appointment
from rasa_sdk.events import SlotSet



class ActionUpdateAppointement(Action):
    
    def __init__(self) -> None:
        super().__init__()
        appointments.instance()._debug("action_goodbye_confirmed")

    def name(self) -> Text:
        return "action_update_appointment"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

            dispatcher.utter_message(text = "Cosa vuoi Aggiornare?", buttons=ActionUpdateAppointement.Utils().choose_update(tracker))
            return []

        

    class Utils:
        def choose_update(self, tracker: Tracker) -> List[Dict[Text, Any]]:
            l = ["nome", "recapito", "ora", "giorno"]
            return [{"title": choise, "payload": f"/intent_update_{choise}"} for choise in l]

    
            

        