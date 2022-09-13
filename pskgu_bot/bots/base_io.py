"""
    Вк бот
"""

from pskgu_bot import Config
from pskgu_bot.utils import logger
from vkbottle.bot import Message
from .constants import available_commands
from pskgu_bot.db.services import find_vk_user_by_id
from pskgu_bot.db.services.group import check_group
from typing import Optional
from .messages import MSG_WARNING_SOFT_KEYWORD


class Parsed_message:
    def __init__ (self, message: Message, username: str = '', from_: Optional[str] = '', commands = None):
        self.cls_message = message

        self.from_id = message.from_id
        self.username = username
        self.from_ = from_

        if commands is None: commands = available_commands
        self.commands = commands

        self.message = message.text.replace('/', ' ').strip()
        self.params = None
        self.__int_i = 0
        self.__str_i = 0

        cmd = get_command_from(self.message, commands = self.commands)

        if cmd is None:
            self.cmd = None
            self.keyword = None
            self.keyword_index = 0
            self.is_soft_keyword = False

            self.params = {'ints': [], 'strs': []}

        else:
            self.cmd = cmd[0]
            self.keyword = cmd[1]
            self.keyword_index = cmd[2]
            self.is_soft_keyword = cmd[3]

            self.params = self.parse_message_to_params(self.message, self.keyword)

    def __contains__ (self, arg: int | str) -> bool:
        if type(arg) is int: 
            if arg in self.params['ints']:
                self.params['ints'].remove(arg)
                return True
            else: return False

        elif type(arg) is str:
            if arg in self.params['strs']:
                self.params['strs'].remove(arg)
                return True
            else: return False

        elif type(arg) is list:
            return any(self.__contains__(i) for i in arg)

        else: return False

    @staticmethod
    def parse_message_to_params (message: str, keyword: str = None):
        params = {'ints': [], 'strs': []}

        if keyword: raw_params = message.replace(keyword, '', 1).split()

        for param in raw_params:
            try: params['ints'].append(int(param))
            except: params['strs'].append(param)

        return params

    def next_int (self) -> int | None:
        if self.__int_i < len(self.params['ints']):
            self.__int_i += 1
            return self.params['ints'][self.__int_i - 1]
        else: 
            return None

    def next_str (self) -> str | None:
        if self.__str_i < len(self.params['strs']):
            self.__str_i += 1

            while (self.__str_i < len(self.params['strs']) and
                   self.params['strs'][self.__str_i - 1] == ''
                  ):
                self.__str_i += 1

            return self.params['strs'][self.__str_i - 1]

        else: 
            return None

    def reset (self) -> None:
        self.__int_i = 0
        self.__str_i = 0

    async def get_user_group (self) -> str:
        user = await find_vk_user_by_id(self.from_id)
        if user: return user.group
        else: return ''

    async def try_find_group (self) -> str:
        group_name = (self.next_str() or 
                      await self.get_user_group() or 
                      None)

        if group_name is None:
            value = self.next_int()
            if value is not None: group_name = str(value)

        return group_name


def get_command_from (text: str, commands: Optional[dict] = None) -> list | None: # [str, str, int] | None:
    text = text.lower()
    if commands is None: commands = available_commands

    for cmd in commands: # В первую очередь ищем основные ключевые слова в начале
        for keyword in commands[cmd]['keywords']:
            if text.startswith(keyword): 
                return [cmd, keyword, 0, False]

    for cmd in commands: # Потом основные ключевые слова во всём сообщении
        for keyword in commands[cmd]['keywords']:
            result = text.find(keyword)
            if result != -1:
                return [cmd, keyword, result, False]

    for cmd in commands: # Если их нет, то ищем среди вспомогательных в начале
        for keyword in commands[cmd].get('soft_keywords', []):
            if text.startswith(keyword): 
                return [cmd, keyword, 0, True]

    for cmd in commands: # И последним шагом - вспомогательные во всём тексте
        for keyword in commands[cmd].get('soft_keywords', []):
            result = text.find(keyword)
            if result != -1: 
                return [cmd, keyword, result, True]

    return None # Если ключевых слов нет - сообщение игнорируется


async def input_message(message: Parsed_message) -> str:
    """
        Принимает обработанное сообщение пользователя и возвращает ответ на него.
    """
    try:
        if message.cmd:
            answer = await available_commands[message.cmd]['func'](message)
        else:
            answer = ''

        if message.is_soft_keyword: 
            answer += MSG_WARNING_SOFT_KEYWORD.format(
                cmd = message.keyword,
                better = '\n'.join(available_commands[message.cmd]['keywords'])
            )

        return answer

    except Exception as e:
        logger.error('Failed to parse input message from user {}:\n{}'.format(message.username, message.message))
        logger.error(e)
        return ''