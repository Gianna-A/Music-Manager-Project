from django.core.exceptions import ValidationError
import datetime
    
def dateValidator(value):
    today = datetime.date.today()
    
    three_years_later = today + datetime.timedelta(days=3*365)
    
    if (value > three_years_later):
        raise ValidationError(f"{value} this date is not less than 3 years")