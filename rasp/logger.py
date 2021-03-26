#rasp/logger
# Предназначен для логирования.

import rasp.config

import io
from datetime import datetime
import sys

# Возвращает штамп времени для логов.
def timestamp():
    date = datetime.now()
    return date.strftime("%d.%m.%Y - %H:%M:%S")

# Обычная функция вывода в лог.
def log_print(*args, file, quiet):
    print(*args, file=file)
    if not quiet:
        print(*args, file=sys.stderr)


# Обычное сообщение.
def log(*args):
    prefix = timestamp(), "[ OK ]:"
    with io.open(rasp.config.LOG_FILE, "a") as logfile:
        log_print(timestamp(), "[ OK ]:", *args, file=logfile, 
            quiet=rasp.config.LOG_QUIET)


# Предупреждение.
def log_warning(*args):
    with io.open(rasp.config.LOG_FILE_WARNING, "a") as logfile:
        log_print(timestamp(), "[ WARNING ]:", *args, file=logfile,
            quiet=rasp.config.LOG_WARNING_QUIET)


# Ошибка.
def log_fatal(*args):
    with io.open(rasp.config.LOG_FILE_FATAL, "a") as logfile:
        log_print(timestamp(), "[ *FATAL* ]:", *args, file=logfile,
            quiet=rasp.config.LOG_FATAL_QUIET)

