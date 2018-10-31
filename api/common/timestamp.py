from datetime import datetime
import time
import dateutil.parser

def fromDateTime(dt):
    return round(time.mktime(dt.timetuple()) + dt.microsecond/1e6)