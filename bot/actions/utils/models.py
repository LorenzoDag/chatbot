class Appointment:
    def __init__(self, date: str, hour: str, duration_min: str, name: str, contact: str):
        self.date = date
        self.hour = hour
        self.duration_min = duration_min
        self.name = name
        self.contact = contact

    #Write getters and setters
    def get_date(self):
        return self.date    
    def get_hour(self):
        return self.hour
    def get_duration(self):
        return self.duration_min
    def get_name(self):
        return self.name
    def get_contact(self):
        return self.contact
    def set_date(self, date):
        self.date = date
    def set_hour(self, hour):
        self.hour = hour
    def set_duration(self, duration_min):
        self.duration_min = duration_min
    def set_name(self, name):
        self.name = name
    def set_contact(self, contact):
        self.contact = contact
    
    #write function that returns a dictionary from the object
    def to_dict(self):
        return {
            'date': self.date,
            'hour': self.hour,
            'duration_min': self.duration_min,
            'name': self.name,
            'contact': self.contact
        }
