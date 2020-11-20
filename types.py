from enum import Enum


class InputData:
    def __init__(self):
        self.job_id = 0
        self.client_id= 0
        self.processing_region=""
        self.message=""
        self.status=""
        self.date_time= ""
        self.metadata=""

class Format(Enum):
    DateTime =1
    Integer =2