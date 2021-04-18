
class DBKey():
    def __init__(self, pkey, identifier=None):
        self.pkey = pkey
        self.identifier = identifier

class UserHeader():
    def __init__(self, client, identifier, dbkey=None):
        self.client = client
        self.identifier = identifier
        self.dbkey = dbkey

class Status():
    def __init__(self, msg=None, ex=None):
        self.msg = msg
        self.ex = ex

class FetchUser():
    def __init__(self, header, meta):
        self.header = header
        self.meta = meta

class FetchSearch():
    def __init__(self, dbkey, title):
        self.dbkey = dbkey
        self.title = title

class FetchClass():
    def __init__(self, class_id, desc):
        self.class_id = class_id
        self.desc = desc

class FetchDay():
    def __init__(self, day_id):
        self.classes = []
        self.day_id = day_id

class FetchWeek():
    def __init__(self, week_id):
        self.days = []
        self.week_id = week_id

class FetchSchedule():
    def __init__(self, page_hash, title, users_to_notify=None):
        self.weeks = []
        self.page_hash = page_hash
        self.title = title
        self.users_to_notify = users_to_notify

MERGE_METHOD_KEEP = 0
MERGE_METHOD_APPEND = 1
MERGE_METHOD_DELETE = 2
MERGE_METHOD_CHANGE = 3

class ApplyClassMerge():
    def __init__(self, class_id, method, prev_desc, desc):
        self.method = method
        self.class_id = class_id
        self.prev_desc = prev_desc
        self.desc = desc

class ApplyDayMerge():
    def __init__(self, day_id, method):
        self.method = method
        self.day_id = day_id
        self.classes = []

class ApplyWeekMerge():
    def __init__(self, week_id, method):
        self.method = method
        self.week_id = week_id
        self.days = []

class ApplyScheduleMerge():
    def __init__(self, dbkey, page_hash, changed):
        self.weeks = []
        self.changed = changed
        self.page_hash = page_hash
        self.dbkey = dbkey

