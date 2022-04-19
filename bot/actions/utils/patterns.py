from typing import List
from actions.utils.models import Appointment
from actions.utils import appointment_path
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

import threading


# Based on tornado.ioloop.IOLoop.instance() approach.
# See https://github.com/facebook/tornado
class Singleton(object):
	__singleton_lock = threading.Lock()
	__singleton_instance = None

	@classmethod
	def instance(cls):
		if not cls.__singleton_instance:
			with cls.__singleton_lock:
				if not cls.__singleton_instance:
					cls.__singleton_instance = cls()
		return cls.__singleton_instance


class AppointmentDao(Dao, Singleton):
    def __init__(self):
        self.appointments = [Appointment(row['date'], row['hour'], row['duration_min'], row['name'], row['contact']) \
            for _, row in pd.read_csv(appointment_path).iterrows() ]
        self.c = 1
        self.last_deleted = None

    def create(self, Obj: Appointment) -> bool:
        if Obj in self.appointments:
            return False
        self.appointments.append(Obj)
        with open(appointment_path, 'a') as f:
            f.write(f"{Obj.date},{Obj.hour},{Obj.duration_min},{Obj.name},{Obj.contact}\n")
        return True

    def restore_last(self):
        if self.last_deleted:
            self.create(self.last_deleted)
            self.last_deleted = None

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
            if app.name.lower() == name.lower() and hour in app.hour and date in app.date:
                self.last_deleted = self.appointments.pop(idx)
                self._save()
                return self.last_deleted
        return None

    def find(self, name: str, date: str) -> List[Appointment]:
        return list(filter(lambda x : x.name.lower() == name.lower() and date.lower() in x.date.lower(), self.appointments))

    def _save(self):
        df = pd.DataFrame([app.to_dict() for app in self.appointments])
        df.to_csv(appointment_path, index=False)

    def _debug(self, stringa: str = "NULL"):
        print(f"IM HERE! from {stringa}")
        print(self.c)
        self.c += 1