from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import pandas as pd
import os.path as path


class ActionAskOra(Action):

    # Caricare il calendario
    ore = ["9:30", "10:00", "10:30"]
    database_dir = "databases"
    appointments_csv_name = "appointments.csv"
    orari_di_lavoro =[[9,13], [14,18]]

    def __init__(self) -> None:
        super().__init__()

    def name(self) -> Text:
        return "action_ask_ora"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        giorno_scelto = tracker.get_slot("giorno")

        orari_disponibili = self.get_disponibilità_oraria(str(giorno_scelto).lower())
        disponibilita_orarie =  ActionAskOra.Buttons().get_buttons(orari_disponibili)
        dispatcher.utter_message(text = f"{giorno_scelto} avrei posto alle", buttons = disponibilita_orarie)

        return [SlotSet(key = "disponibilità_oraria", value = orari_disponibili)]
    
    def parse_appointments(self, data: pd.DataFrame) -> pd.DataFrame:
        df = data.copy()
        df["time_begin"] = pd.to_timedelta(df.Date)
        df["duration"] = pd.to_timedelta(df.Duration)
        data["appointment_end"] = df.time_begin + df.duration
        return data

    def get_disponibilità_oraria(self, giorno: str) -> List[str]:
        # Ottenere la disponibilità oraria per il giorno
        self.appointments = pd.read_csv(path.join(ActionAskOra.database_dir, ActionAskOra.appointments_csv_name))
        appuntamenti_giorno = self.appointments.loc[self.appointments.Date.str.lower() == giorno]
        return self.get_free_slots(appuntamenti_giorno)

    def get_free_slots(self, appuntamenti_giorno: pd.DataFrame) -> List[str]:
        # Ottenere le ore libere per il giorno
        ore_libere = []
        df = appuntamenti_giorno.copy()
        for mezza_giornata in self.orari_di_lavoro:
            for ora in range(mezza_giornata[0], mezza_giornata[1]):
                ora_libera = f"{ora}:00"
                if df[df.Hour.str.contains(ora_libera)].empty:
                    ore_libere.append(ora_libera)
                ora_libera = f"{ora}:30"
                if df[df.Hour.str.contains(ora_libera)].empty:
                    ore_libere.append(ora_libera)
        return ore_libere
    
    class Buttons:
        
        # dovrà poi prendere in input la connessione al db e cercare le disponibilità
        def get_buttons(self, ore: List[str]) -> List[Dict[Text, Any]]:
            # Filtrare il calendario
            return [{"title": ora, "payload": "/intent_sceglie_ora{\"ora\":\"" + ora +"\"}"} for ora in ore]