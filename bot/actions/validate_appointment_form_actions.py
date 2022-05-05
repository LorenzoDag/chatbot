from cgitb import text
from typing import Any, Text, Dict

from rasa_sdk import Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict

import phonenumbers
from email_validator import validate_email, EmailNotValidError


class ActionCercaPosto(FormValidationAction):

    def name(self) -> Text:
        return "validate_form_prenotazione"

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
        
        if slot_value.lower() in tracker.get_slot("disponibilità_oraria"): # Bisogna validare di nuovo l'orario al fine di evitare che qualcuno scriva cose a caso
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

        if(len(tracker.get_slot("nome")) < 3 and tracker.get_slot("nome") == None):
            dispatcher.utter_message(text = f"Mi dispiace ma {slot_value} non è un nome valido. Che nome preferisci?")
            return {"nome": None}
        
        return {"nome": slot_value}

    def validate_recapito(self, 
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
        ) -> Dict[Text, Any]:

        recapito = slot_value.lower()
        try:
            phonenumbers.is_possible_number(phonenumbers.parse(recapito, "IT"))
            return {"recapito": recapito}
        except phonenumbers.phonenumberutil.NumberParseException:
            try:
                validate_email(recapito)
                return {"recapito": recapito}
            except EmailNotValidError:
                dispatcher.utter_message(text = f"Mi dispiace ma {recapito} non è una mail valida. Vuoi darmi un numero di telefono?")
                return {"recapito": None}


