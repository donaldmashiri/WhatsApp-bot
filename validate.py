import re

class Validate:
    def econet(phone):
        pattern = re.compile(r'^(077|078)\d{7}$')
        return pattern.match(phone) is not None
    
    def netone(phone):
        pattern = re.compile(r'^(071)\d{7}$')
        return pattern.match(phone) is not None