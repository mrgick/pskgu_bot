from ..messages import MSG_HELP, MSG_TIMETABLE, msg_start


def begin(name: str) -> str:
    """
        Начальное сообщение пользователю.
    """
    return msg_start(name)


def help() -> str:
    """
        Справка по боту.
    """
    return MSG_HELP


def time_classes() -> str:
    """
        Справку о времени начала пар.
    """
    return MSG_TIMETABLE
