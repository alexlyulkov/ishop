import datetime

def current_month():
    now = datetime.datetime.now()
    lead_zero = ''
    if now.month < 10:
        lead_zero = '0'
    return str(now.year) + '-' + lead_zero + str(now.month) 
    
