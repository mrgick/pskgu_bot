"""
    Файл с дополнительными, вспомогательными переменным и функциями.
"""
from typing import Optional


def str_to_int(x: str) -> Optional[int]:
    """
        Перевод строки в число.
    """
    try:
        x = int(x)
        return x
    except Exception:
        return None


STRUCTED_DICT = {
    "преподаватель": {
        'Институт гуманитарных наук и языковых коммуникаций': {
            'исторический факультет': {
                'Кафедра отечественной истории': [],
                'Кафедра всеобщей истории и регионоведения': [],
                'Кафедра философии и теологии': []
            },
            'факультет русской филологии и иностранных языков': {
                'Кафедра европейских языков и культур': [],
                'Кафедра иностранных языков для нелингвистических направлений':
                [],
                'Кафедра филологии, коммуникаций и русского языка как иностранного':
                []
            }
        },
        'Институт инженерных наук': {
            'факультет отсутствует': {
                'Кафедра инженерных технологий и техносферной безопасности':
                [],
                'Кафедра электроэнергетики, электропривода и систем автоматизации':
                [],
                'Кафедра архитектуры и строительства': [],
                'Кафедра автомобильного транспорта': [],
                'Кафедра информационно-коммуникационных технологий': []
            }
        },
        'Институт математического моделирования и игропрактики': {
            'факультет отсутствует': {
                'Кафедра математики и теории игр': [],
                'Кафедра физики': [],
                'Кафедра прикладной информатики и моделирования': [],
                'Кафедра дизайна': []
            }
        },
        'Институт медицины и экспериментальной биологии': {
            'медицинский факультет': {
                'Кафедра фундаментальной медицины и биохимии': [],
                'Кафедра клинической медицины': [],
                'Кафедра медицинской информатики и кибернетики': []
            },
            'естественно-географический факультет': {
                'Кафедра ботаники и экологии растений': [],
                'Кафедра зоологии и экологии животных': [],
                'Кафедра географии': [],
                'Кафедра химии': []
            }
        },
        'Институт права, экономики и управления': {
            'факультет отсутствует': {
                'Кафедра управления и административного права': [],
                'Кафедра экономики, финансов и финансового права': [],
                'Кафедра национальной безопасности и правозащитной деятельности':
                [],
                'Кафедра гражданского права и процесса': [],
                'Кафедра правоохранительной деятельности, уголовного права и процесса':
                [],
                'Кафедра государственно-правовых дисциплин и теории права': [],
            }
        },
        'Институт образования и социальных наук': {
            'факультет отсутствует': {
                'Кафедра среднего общего образования и социального проектирования':
                [],
                'Кафедра психологии и сопровождения развития ребенка': [],
                'Кафедра технологии работы с лицами с особыми потребностями':
                [],
                'Кафедра физической культуры и здоровьесбережения': [],
                'Кафедра образовательных технологий': []
            }
        },
        'Прочее': {
            'прочее': {
                'Кафедра отсутствует': []
            }
        }
    },
    "ОФО": {},
    "ЗФО": {}
}
