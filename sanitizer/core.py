
import re

EMAIL_PATTERN=re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9_.+-]+\.[a-zA-Z0-9_.+-]+$")
BANNED_PREFIXES=("info@","sales@","support@","admin@","cannot@")
def clean_name(name:str)->str:
    if not name:
        return "unknown"
    clean_chars = re.sub(r'[^a-zA-Z\s\-]', '', name)
    return clean_chars.strip().title()

def is_valid_email(email:str)->bool:
    clean_email=email.strip().lower()

    if not clean_email:
        return False

    if not EMAIL_PATTERN.match(clean_email):
        return False
    if clean_email.startswith(BANNED_PREFIXES):
        return False
    
    return True