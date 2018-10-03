from datetime import datetime

class ValidInterval:
    def __init__(self, valid_from, valid_to):
        if isinstance(valid_from, str):
            self.valid_from = datetime.strptime(valid_from, '%Y-%m-%d')
        else:
            self.valid_from = valid_from

        if isinstance(valid_to, str):
            self.valid_to = datetime.strptime(valid_to, '%Y-%m-%d')
        else:
            self.valid_to = valid_to        
