from cgitb import text
from typing import Any, Text, Dict

from rasa_sdk import Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict

from email_validator import validate_email, EmailNotValidError
from actions import appointments


class ActionCercaPosto(FormValidationAction):

    def name(self) -> Text:
        return "validate_form_modifica_prenotazione"

    def validate_giorno(self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
        ) -> Dict[Text, Any]:

        for day in ["lun", "mar", "mer", "gio", "ven"]:
            if day in slot_value.lower():
                return {"giorno": slot_value}
        else:
            dispatcher.utter_message(text = f"Mi dispiace ma {slot_value} non lavoriamo. Che giorno preferisci?")
            return {"giorno": None}
    
    def validate_ora(self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
        ) -> Dict[Text, Any]:
        
        if slot_value.lower() in tracker.get_slot("disponibilità_oraria"): # Bisogna validare di nuovo l'orario al fine di evitare che qualcuno scriva cose a cazzo
            return {"ora": slot_value}
        else:
            dispatcher.utter_message(text = f"Mi dispiace ma {slot_value} non è un orario valido. Che orario preferisci?")
            return {"ora": None}

    def validate_nome(self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
        ) -> Dict[Text, Any]:

        apps = appointments.instance().appointments
        if not slot_value.lower() in [app.get_name().lower() for app in apps]:
            dispatcher.utter_message(text = f"Mi dispiace ma non ho appuntamenti per {slot_value}. Sicuro di aver scritto bene? Come ti chiami?")
            return {"nome": None}
        
        return {"nome": slot_value}
