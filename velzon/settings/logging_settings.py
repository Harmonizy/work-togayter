import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Logging configuration
START_DATE = '2025-01-01'
END_DATE = '2030-12-31'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
        'detailed': {
            'format': '{levelname} {asctime} {module} {funcName} {lineno} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'login_success': {
            'level': 'INFO',
            'class': 'common.Services.week_cycle_log_name.DateRangeTimedRotatingFileHandler',
            'start_date': START_DATE,
            'end_date': END_DATE,
            'formatter': 'verbose',
            'when': 'W0',
            'interval': 1,
            'backupCount': 4,
            'base_filename': os.path.join(BASE_DIR, 'logs', 'login_success'),
        },
        'file_downloaded': {
            'level': 'INFO',
            'class': 'common.Services.week_cycle_log_name.DateRangeTimedRotatingFileHandler',
            'start_date': START_DATE,
            'end_date': END_DATE,
            'formatter': 'verbose',
            'when': 'W0',
            'interval': 1,
            'backupCount': 4,        
            'base_filename': os.path.join(BASE_DIR, 'logs', 'file_downloaded'),
        },
        'report_file': {
            'level': 'INFO',
            'class': 'common.Services.week_cycle_log_name.DateRangeTimedRotatingFileHandler',
            'start_date': START_DATE,
            'end_date': END_DATE,
            'formatter': 'verbose',
            'when': 'W0',
            'interval': 1,
            'backupCount': 4,        
            'base_filename': os.path.join(BASE_DIR, 'logs', 'report_file'),
        },
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'detailed',
            'level': 'DEBUG',
        }
    },
    'loggers': {
        'django.security.login_success': {
            'handlers': ['login_success'],
            'level': 'INFO',
            'propagate': False,
        },
        'mylogger.file_download': {
            'handlers': ['file_downloaded'],
            'level': 'INFO',
            'propagate': False,
        },
        'report': {
            'handlers': ['report_file', 'console'],
            'level': 'INFO',
            'propagate': False,
        },
    },

}
