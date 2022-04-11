from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class GoodbyeConfirmAction(Action):
    # Viene chiamata quando il cliente conferma
    # dovrebbe salvare l'appuntamento e creare il messaggio di saluto
    # Successivamente viene chiamata ActionReset che resetta tutti gli slots (è inutile farlo anche qui)
    def name(self) -> Text:
        return "action_goodbye_confirmed"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        try:
            utils = GoodbyeConfirmAction.Utils()
            utils.save_appointment(tracker)
            dispatcher.utter_message(text = utils.build_response(tracker))
        except:
            dispatcher.utter_message(text = utils.build_response(tracker))

        return []

    class Utils:
        def build_response(self, tracker: Tracker):
            return f"Perfetto. Allora ciao {tracker.get_slot('nome')}, ci vediamo {tracker.get_slot('giorno')}"

        def error_response(self, tracker: Tracker):
            return f"Mi dispiace, qualcosa è andato storto. Riprova"

        def save_appointment(self, tracker: Tracker):
            print("OK")