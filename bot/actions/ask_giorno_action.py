from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from actions import appointments

from actions.utils.date_utils import *
from datetime import date


class ActionAskGiorno(Action):

    def __init__(self) -> None:
        super().__init__()
        self.giorni = ["Lunedì", "Martedì", "Mercoledì", "Giovedì", "Venerdì"]
        appointments.instance()._debug("action_ask_giorno")

    def name(self) -> Text:
        return "action_ask_giorno"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        if tracker.active_loop.get("name") == "form_modifica_prenotazione":    
            msg = "Che giorno avevi apuntamento?"
        else:
            msg = "Che giorno vuoi prenotare?"

        giorni = [f"{giorno} {next_weekday(date.today(), day_code)}" for giorno, day_code in zip(self.giorni, days_code.values())]
        dispatcher.utter_message(text=msg, buttons = ActionAskGiorno.Buttons().get_buttons(giorni))

        return []

    class Buttons:
        
        def get_buttons(self, giorni) -> List[Dict[Text, Any]]:
            return [{"title": giorno, "payload": "/intent_sceglie_giorno{\"giorno\":\"" + giorno + "\"}"} for giorno in giorni]