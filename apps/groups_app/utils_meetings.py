import datetime
from django.utils.timezone import make_aware, get_default_timezone, make_naive

def date_time_format_form(datetime_var):
    return str(datetime.datetime.strftime(make_naive(datetime_var, get_default_timezone()), "%d de %B de %Y a las %I:%M %p"))


def date_time_format_db(datetime_var):
    UTC_OFFSET_TIMEDELTA = datetime.datetime.utcnow() - datetime.datetime.now()
    local_datetime = datetime.datetime.strptime(str(datetime_var), "%Y-%m-%d %H:%M:%S")
    result_utc_datetime = local_datetime - UTC_OFFSET_TIMEDELTA
    return str(result_utc_datetime.strftime("%d de %B de %Y a las %I:%M %p"))


def remove_gmt(datetime_var):
    dt = str(datetime_var)
    dt_s = dt[:19]
    return str(datetime.datetime.strptime("%s" % (dt_s), "%Y-%m-%d %H:%M:%S"))
