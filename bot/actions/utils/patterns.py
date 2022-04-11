from actions.utils.models import Appointment
from actions.utils import database_path
import pandas as pd

class Dao:
    def create(self, Obj: any):
        raise NotImplementedError()

    def read(self, name: str, hour: str, date: str):
        raise NotImplementedError()

    def update(self, name: str, hour: str, date: str, Obj: any):
        raise NotImplementedError()
    
    def delete(self, name: str, hour: str, date: str):
        raise NotImplementedError()


class AppointmentDao(Dao):
    def __init__(self):
        self.appointments = [Appointment(row['date'], row['hour'], row['duration_min'], row['name'], row['contact']) for _, row in pd.read_csv(database_path) ]

    def create(self, Obj: Appointment) -> bool:
        if Obj in self.appointments:
            return False
        self.appointments.append(Obj)
        with open(database_path, 'a') as f:
            f.write(f"{Obj.date},{Obj.hour},{Obj.duration_min},{Obj.name},{Obj.contact}\n")
        return True


    def read(self, name: str, hour: str, date: str) -> Appointment:
        return list(filter(lambda x : x.name == name and x.hour == hour and x.date == date, self.appointments))[0] or None

    def update(self, name: str, hour: str, date: str, Obj: Appointment) -> Appointment:
        
        for idx, app in enumerate(self.appointments):
            if app.name == name and app.hour == hour and app.date == date:
                self.appointments[idx] = Obj
                self._save()
                return Obj
        return None



    def delete(self, name: str, hour: str, date: str ) -> Appointment:
        for idx, app in enumerate(self.appointments):
            if app.name == name and app.hour == hour and app.date == date:
                self._save()
                return self.appointments.pop(idx)
        return None

    def _save(self):
        df = pd.DataFrame([app.to_dict() for app in self.appointments])
        df.to_csv(database_path, index=False)