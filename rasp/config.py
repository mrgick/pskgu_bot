# файл конфигурации.

# Путь к расписанию
REMOTE_URL = "http://rasp.pskgu.ru"

# Файлы для логирования
LOG_FILE = "logs/log.txt"
LOG_FILE_WARNING = LOG_FILE # Предупреждения
LOG_FILE_FATAL = LOG_FILE # Ошибки
LOG_PAGE_FILE = "logs/page.txt" # Страница для бенчмарка.

# Вывод логов в консоль
LOG_QUIET = False
LOG_WARNING_QUIET = LOG_QUIET # Предупреждения
LOG_FATAL_QUIET = False # Ошибки

# Максимальное количество запросов
MAX_REQUESTS = 100

# Длительность одной пары (в сек. от 00:00)
SCHEDULE_CLASS_DURATION = 5400.0

# Таблица времени начала пар (в сек. от 00:00)
SCHEDULE_TIME_TABLE = [
    
    30600.0, # 1
    36900.0, # 2
    45000.0, # 3
    51300.0, # 4
    57600.0, # 5
    64800.0, # 6
    70800.0, # 7
]

# Минимальное количество совпадений для поиска преподавателей
TEACHER_SEARCH_MINMATCH = 5
