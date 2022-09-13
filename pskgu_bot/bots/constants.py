from . import messages
from vkbottle.bot import rules

available_commands = {
	'begin': {
		'keywords': ['start', 'начать'],
		'PayloadRule': rules.PayloadRule({"command": "start"}),
	},

	'help': {
		'keywords': ['help', 'справка', 'info', 'помощь'],
		'on_help': messages.MSG_HELP,
	},

	'show': {
		'keywords': ['show', 'показать'],
		'soft_keywords': ['расписание', 'покажи'],
		'on_help': messages.MSG_HELP_SHOW,
	},

	'find': {
		'keywords': ['find', 'поиск'],
		'soft_keywords': ['найти'],
		'on_help': messages.MSG_HELP_FIND,
	},

	'map': {
		'keywords': ['map', 'карта'],
		'photos': ("photo-176090321_457239022," +
		           "photo-176090321_457239021," +
                   "photo-176090321_457239020," +
                   "photo-176090321_457239019"),
		'on_help': messages.MSG_HELP_MAP,
	},

	'timetable': {
		'keywords': ['classes_time', 'расписание_пар'],
		'soft_keywords': ['timetable', 'time', 'время', 'время_пар'],
		'on_help': messages.MSG_HELP_TIMETABLE,
	},

	'url': {
		'keywords': ['url', 'ссылка'],
		'soft_keywords': ['link'],
		'on_help': messages.MSG_HELP_URL,
	},

	'subscribe': {
		'keywords': ['subscribe', 'подписаться'],
		'soft_keywords': ['подписатся', 'подписка'],
		'on_help': messages.MSG_HELP_SUBSCRIBE,
	},

	'unsubscribe': {
		'keywords': ['unsubscribe', 'отписаться'],
		'soft_keywords': ['отписатся', 'отписка'],
		'on_help': messages.MSG_HELP_UNSUBSCRIBE,
	},

	'buttons': {
		'keywords': ['unsubscribe', 'отписаться'],
		'soft_keywords': ['отписатся', 'отписка'],
		'on_help': messages.MSG_BUTTON_HELP,
	},

	'delete': {
		'keywords': ['delete', 'удалить'],
	}
}

button_commands = {
	'buttons': {
		'keywords': ['buttons', 'кнопки'],
	}
}

button_presets = {
	'main': {
		'keywords': ['show', 'показать'],
		'buttons': [
			['/show'  , 'const', 'show'  ],
			'row',
			['/show 1', 'const', 'show 1'],
		],
		'on_select': messages.MSG_BUTTON_SHOW
	},

	'shifted': {
		'keywords': ['show_shifted', 'смещение'],
		'special': 'special_shifted',
		'on_select': messages.MSG_BUTTON_SHOW_SHIFTED
	},

	'shifted_2': {
		'keywords': ['show_shifted_2', 'смещение_2'],
		'special': 'special_shifted_2',
		'on_select': messages.MSG_BUTTON_SHOW_SHIFTED
	}
}