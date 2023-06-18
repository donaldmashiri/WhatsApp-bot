import re

def validate_mobile_number(number):
    pattern = re.compile(r'^(077|078)\d{7}$')
    return pattern.match(number) is not None

# Example usage
print(validate_mobile_number('0771234567'))  # True
print(validate_mobile_number('0789876543'))  # True
print(validate_mobile_number('0712345678'))  # False (invalid prefix)
print(validate_mobile_number('07712345678')) # False (too long)