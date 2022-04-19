from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from actions import appointments
from rasa_sdk.events import AllSlotsReset


class ActionUpdateAppointement(Action):

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

class ActionDeleteAppointement(Action):

    def name(self) -> Text:
        return "action_delete_appointment"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

            app = appointments.instance().delete(tracker.get_slot("nome"), tracker.get_slot("ora"), tracker.get_slot("giorno"))
            if app:
                dispatcher.utter_message(text = f"Ok {tracker.get_slot('nome')}, l'appuntamento per {tracker.get_slot('giorno')} alle {tracker.get_slot('ora')} è stato cancellato.\nAlla prossima!")
            else:
                dispatcher.utter_message(text = f"Non ho trovato nessun appuntamento per {tracker.get_slot('nome')} alle {tracker.get_slot('ora')} il {tracker.get_slot('giorno')}")
            ret = [] if tracker.latest_message['intent'].get('name') == "intent_modifica" else [AllSlotsReset()]
            return ret