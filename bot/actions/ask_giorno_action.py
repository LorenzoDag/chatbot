from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionAskGiorno(Action):

    def __init__(self) -> None:
        super().__init__()
        self.giorni = ["Lunedì", "Martedì", "Mercoledì", "Giovedì", "Venerdì"]

    def name(self) -> Text:
        return "action_ask_giorno"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Ok, che giorno preferisci?", buttons = ActionAskGiorno.Buttons().get_buttons(self.giorni))

        return []

    class Buttons:
        
        def get_buttons(self, giorni) -> List[Dict[Text, Any]]:
            return [{"title": giorno, "payload": "/intent_sceglie_giorno{\"giorno\":\"" + giorno + "\"}"} for giorno in giorni]