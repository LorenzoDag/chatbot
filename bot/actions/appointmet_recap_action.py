from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class AppointmentRecapAction(Action):

    def name(self) -> Text:
        return "action_appointment_recap"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        response_builder = AppointmentRecapAction.Utils()
        dispatcher.utter_message(text = response_builder.build_response(tracker), buttons = response_builder.get_buttons())

        return []

    class Utils:

        def build_response(self, tracker: Tracker):
            return f"""
            Allora, facciamo un recap:
            Per {tracker.get_slot("nome")}
            Appuntamento per {tracker.get_slot("giorno")} alle {tracker.get_slot("ora")}
            
            Per qualunque cosa mi faccio sentire al recapito {tracker.get_slot("recapito")}

            Va bene?
            """
        
        def get_buttons(self) -> List[Dict[Text, Any]]:
            return [
                {"title": "Confermo", "payload": "/intent_conferma"},
                {"title": "Annulla", "payload": "/intent_annulla"},
                {"title": "Modifica", "payload": "/intent_modifica"}          
            ]