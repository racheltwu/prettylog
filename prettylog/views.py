from os import path

from django.shortcuts import render_to_response
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.cache import never_cache
from django.conf import settings


@never_cache
@staff_member_required
def error_log(request):

    error_counts = {}
    errors = []

    log = open(path.join(settings.LOG_DIR, 'prettylog.txt'), 'r')
    trace = ''
    currently_reading_trace = False
    for line in log:
        if line.startswith('ERROR'):
            timestamp = line
            currently_reading_trace = True
        elif currently_reading_trace and not line.startswith('Traceback') and not line.startswith(' '):
            currently_reading_trace = False
            error_type = line
            if trace not in error_counts:
                error_count = 1
                errors.append({'type': error_type, 'trace': trace})
            else:
                error_count = error_counts[trace]['count'] + 1
            error_counts[trace] = {'count': error_count, 'timestamp': timestamp}
            trace = ''
        elif currently_reading_trace:
            trace += line
    log.close()

    for error in errors:
        error.update(error_counts[error['trace']])
        error['frequency'] = 'high' if error['count'] > 10 else 'medium' if error['count'] > 5 else 'low'
        error['trace'] = error['trace'].split('\n')
        filepaths = []
        current_filepath = ''
        for line in error['trace'][1:]:
            if line.startswith('  File'):
                previous_file = current_filepath
                if previous_file:
                    filepaths.append(previous_file.replace('\n',''))
                current_filepath = line
            else:
                current_filepath += line
        error['trace'] = {'first_line': error['trace'][0], 'filepaths': filepaths}

    errors.sort(key = lambda e: e['timestamp'])
    errors.reverse()

    return render_to_response('prettylog.html', {
        'LOG_CSS_PATH': getattr(settings, 'LOG_CSS_PATH', path.join(settings.STATIC_URL, 'css', 'prettylog.css')),
        'total_errors': str(len(errors)),
        'errors': errors,
    })
