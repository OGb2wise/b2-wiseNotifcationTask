import re
import types


date_pattern = '(1|2)([0-9]{3})(-|/)([0-9]|1[0-2])(-|/)([0-9]|1[0-2]|[1-2][0-9]|3[0-1])'
time_pattern = '([0-9]|1[0-9]|2[0-4]):([0-9]|[1-5][0-9]):([0-9]|[1-5][0-9])'
decimal = '\.\d{6}'
date_time_pattern = "^" + date_pattern + " " + time_pattern + decimal + "$"

integer_pattern = "^\d+$"

def validate_input(format_type,input):
    if(format_type.lower() == "date"):
        return bool(re.match(date_time_pattern,input))
    if(format_type.lower() == "integer"):
        return bool(re.match(integer_pattern,input))
    return False

