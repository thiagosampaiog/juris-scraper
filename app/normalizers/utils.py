from datetime import datetime
from app.models.models import ParticipantType

def parse_date(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except:
        return None
    
def parse_datajud_date(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.strptime(value, "%Y%m%d%H%M%S")
    except:
        return None
    

def parse_participant_type(value: str | None) -> ParticipantType | None:
    if not value:
        return None    
    if(value == "RÉU"):
        return ParticipantType.defendant
    if(value == "AUTOR"):
        return ParticipantType.author
    else:
        return ParticipantType.third_party

def parse_br_date(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.strptime(value, "%d/%m/%Y")
    except:
        return None