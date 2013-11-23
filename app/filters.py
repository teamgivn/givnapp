def _jinja2_filter_datetime(dt, format=None):
    """Jinja tempate filter to format a datetime object."""
    if dt is None:
        # by default, render an empty string
        return ""
    if format is None:
        # No format is given in the template call
        # use a default format
        #
        # Format time in its own strftime call in order to:
        # 1. Left-strip leading 0 in hour display
        # 2. use 'am'/'pm' (lower case) instead of 'AM'/'PM'
        formatted_date = dt.strftime('%Y-%m-%d - %A')
        formatted_time = \
            dt.strftime('%I:%M%p').lstrip('0').lower()
        formatted = "%s at %s" %(formatted_date, formatted_time)
    else:
        formatted = dt.strftime(format)
    return formatted


def _jinja2_filter_strftime(date, fmt='%Y-%b-%d %I:%M%p'):
    if date == None:
        return 'None'
    return date.strftime(fmt)

def _jinja2_filter_boolean_js(value):
    if value:
        return 1
    return 0

def _jinja2_filter_boolean_html (value):
    if value:
        return 'Yes'
    return 'No' 

def init_app(app):
    """Initialize a flask application with custom filters"""
#    app.jinja_env.filters['datetime'] = _jinja2_filter_datetime
    app.jinja_env.filters['strftime'] = _jinja2_filter_strftime
    app.jinja_env.filters['boolean_js'] = _jinja2_filter_boolean_js
    app.jinja_env.filters['boolean_html'] = _jinja2_filter_boolean_html



