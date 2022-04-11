from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionAskOra(Action):

    # Caricare il calendario
    ore = ["9:30", "10:00", "10:30"]

    def __init__(self) -> None:
        super().__init__()

    def name(self) -> Text:
        return "action_ask_ora"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        disponibilita_orarie =  ActionAskOra.Buttons().get_buttons(self.ore)
        giorno_scelto = tracker.get_slot("giorno")
        dispatcher.utter_message(text = f"{giorno_scelto} avrei posto alle", buttons = disponibilita_orarie)

        return []

    class Buttons:
        
        # dovrà poi prendere in input la connessione al db e cercare le disponibilità
        def get_buttons(self, ore: List[str]) -> List[Dict[Text, Any]]:
            # Filtrare il calendario
            return [{"title": ora, "payload": "/intent_sceglie_ora{\"ora\":\"" + ora +"\"}"} for ora in ore]