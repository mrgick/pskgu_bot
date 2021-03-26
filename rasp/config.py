# rasp_config.py
# файл конфигурации.

# Путь к расписанию
REMOTE_URL = "http://rasp.pskgu.ru"

# Файлы для логирования
LOG_FILE = "logs/log.txt"
LOG_FILE_WARNING = LOG_FILE # Предупреждения
LOG_FILE_FATAL = LOG_FILE # Ошибки

# Вывод логов в консоль
LOG_QUIET = False
LOG_WARNING_QUIET = LOG_QUIET # Предупреждения
LOG_FATAL_QUIET = False # Ошибки
