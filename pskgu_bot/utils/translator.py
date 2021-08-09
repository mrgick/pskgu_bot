from googletrans import LANGUAGES, Translator


def translate_message(mess: str, language_prefix: str) -> str:
    """
        Перевод текста на другой язык.
    """
    if not LANGUAGES.get(language_prefix):
        return 'Данный префикс языка не обнаружен в базе данных.\n' + mess

    try:
        mess = 'Перевод может содержать ошибки.\n' + mess
        mess = Translator().translate(mess, src="ru",
                                      dest=language_prefix).text
    except Exception:
        mess = 'Перевод завершился ошибкой. Попробуйте позднее.\n' + mess

    return mess
