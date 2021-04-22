
import datetime

class DBKey():
    def __init__(self, pkey, identifier=None):
        self.pkey = pkey
        self.identifier = identifier

class UserHeader():
    def __init__(self, client, identifier, dbkey=None):
        self.client = client
        self.identifier = identifier
        self.dbkey = dbkey

class FetchUser():
    def __init__(self, header, meta):
        self.header = header
        self.meta = meta

class FetchSearch():
    def __init__(self, dbkey, title):
        self.dbkey = dbkey
        self.title = title

class MERGE_METHOD:
    KEEP = 0
    APPEND = 1
    DELETE = 2
    CHANGED = 3

class FetchScheduleElement():

    def __init__(self, parent, idx):
        self.parent = parent
        self.idx = idx
        self.has_datetime = False
        self.modified = False
        self.copy_to_restore = None
        self.timestamp = None
        self.datetime = None
    
    def make_datetime(self):
        pass

    def merge(self, old_element, merge_method):
        pass

    def __bool__(self):
        pass

    def __iter__(self):
        pass

    def append(self, element):
        pass

    def copy(self, parent=None):
        pass

    
class FetchClass(FetchScheduleElement):
    def __init__(self, parent, idx, desc):
        super().__init__(parent=parent, idx=idx)
        self.desc = desc

    def make_datetime(self):
        if self.has_datetime:
            return

        CLASS_START_LIST = FetchSchedule.CLASS_START_LIST
        CLASS_DURATION = FetchSchedule.CLASS_DURATION
        self.timestamp = self.parent.timestamp + CLASS_START_LIST[self.idx]
        self.end_timestamp = self.timestamp + CLASS_DURATION
        self.datetime = datetime.datetime.fromtimestamp(
            self.timestamp
        )
        self.end_datetime = datetime.datetime.fromtimestamp(
            self.end_timestamp
        )
        self.has_datetime = True

    def copy_datetime(to_class, from_class):
        to_class.timestamp = from_class.timestamp
        to_class.end_timestamp = from_class.end_timestamp
        to_class.datetime = from_class.datetime 
        to_class.end_datetime = from_class.end_datetime
        to_class.has_datetime = True

    def merge(self, old_class, merge_method):
        merged = None
        if merge_method == MERGE_METHOD.KEEP:
            if self.desc == old_class.desc:
                merged = ApplyClass(merge_method=merge_method,
                                    idx=self.idx, desc=self.desc)
            else:
                merged = ApplyClass(
                            merge_method=MERGE_METHOD.CHANGED, 
                                    idx=self.idx, desc=self.desc, 
                                        old_desc=old_class.desc)

            FetchClass.copy_datetime(merged, old_class)
        else:
            self.make_datetime()
            merged = ApplyClass(merge_method=merge_method,
                            idx=self.idx, desc=self.desc)
            FetchClass.copy_datetime(merged, self)

        return merged

    def copy(self, parent=None):
        copied = FetchClass(parent=parent, idx=self.idx, 
                        desc=self.desc)

        FetchClass.copy_datetime(copied, self)

        return copied
        


class FetchDay(FetchScheduleElement):
    def __init__(self, parent, idx, month, month_day):
        super().__init__(parent=parent, idx=idx)
        self.classes = []
        self.month = month
        self.month_day = month_day

    def make_datetime(self):
        if self.has_datetime:
            return

        DAY_DELTA = FetchSchedule.DAY_DELTA
        self.timestamp = self.parent.timestamp + self.idx*DAY_DELTA
        self.datetime = datetime.datetime.fromtimestamp(
            self.timestamp
        )
        self.has_datetime = True

    def __iter__(self):
        return iter(self.classes)

    def __bool__(self):
        return bool(self.classes)

    def append(self, cls):
        self.classes.append(cls)

    def merge(self, old_day, merge_method):
        merged = ApplyDay(merge_method=merge_method,
                            idx=self.idx)
        return FetchSchedule.merge_elements(merged, 
                                        self, old_day)
                                            
    def copy(self, parent=None):
        copied = FetchDay(parent=parent, idx=self.idx,
                            month=None, month_day=None)
        return FetchSchedule.copy_elements(copied, self)
        

class FetchWeek(FetchScheduleElement):
    def __init__(self, parent, idx=None):
        super().__init__(parent=parent, idx=idx)
        self.days = []
        self.is_new_year = False
        self.is_new_year_boundary = False

    def make_datetime(self):

        if self.has_datetime:
            return

        WEEK_START = int(
            FetchSchedule.SCHEDULE_WEEK_DATETIME_START.timestamp())
        WEEK_DELTA = FetchSchedule.WEEK_DELTA
        self.timestamp = WEEK_START + self.idx*WEEK_DELTA
        self.datetime = datetime.datetime.fromtimestamp(
            self.timestamp
        )
        self.has_datetime = True

    def __iter__(self):
        return iter(self.days)

    def __bool__(self):
        return bool(self.days)

    def append(self, day):
        return self.days.append(day)

    def merge(self, old_week, merge_method):
        merged = ApplyWeek(merge_method=merge_method, 
                            idx=self.idx)
        return FetchSchedule.merge_elements(merged, self, old_week)

    def copy(self, parent=None):
        copied = FetchWeek(parent=parent, idx=self.idx)
        return FetchSchedule.copy_elements(copied, self)



class FetchSchedule(FetchScheduleElement):

    # Дата понедельника начальной недели.
    # Предназначен для расчёта времени.
    SCHEDULE_WEEK_DATETIME_START = datetime.datetime(2018, 1, 1)

    WEEK_DELTA = 604800 
    DAY_DELTA = 86400

    YEAR_LOOP = 4

    CLASS_DURATION = 5400

    CLASS_START_LIST = [
        30600, # 1-ая пара
        36900, # 2-ая пара
        45000, # 3-ая пара
        51300, # 4-ая пара
        57600, # 5-ая пара
        64800, # 6-ая пара
        70800, # 7-ая пара
    ]


    def merge_collections(new_collection, old_collection):
        new_iter = iter(new_collection)
        old_iter = iter(old_collection)
        new = next(new_iter, None)
        old = next(old_iter, None)
        while True:
            if new == None:
                while old != None: 
                    yield (MERGE_METHOD.DELETE, new, old)
                    old = next(old_iter, None)
                break
                    

            if old == None:
                while new != None:
                    yield (MERGE_METHOD.APPEND, new, old)
                    new = next(new_iter, None)
                break

            if new.idx == old.idx:
                yield (MERGE_METHOD.KEEP, new, old)
                new = next(new_iter, None)
                old = next(old_iter, None)
            elif new.idx < old.idx:
                while new != None and new.idx < old.idx:
                    yield (MERGE_METHOD.APPEND, new, old)
                    new = next(new_iter, None)
            else:
                while old != None and new.idx > old.idx:
                    yield (MERGE_METHOD.DELETE, new, old)
                    old = next(old_iter, None)


    def merge_elements(merged, new, old):
        method = merged.merge_method

        if method == MERGE_METHOD.KEEP:
            changed = False
            for (child_method, new_child, old_child) in FetchSchedule.merge_collections(new, old):

                merged_child = None

                if child_method == MERGE_METHOD.KEEP:
                    merged_child = new_child.merge(old_child, child_method)
                    if merged_child.merge_method != MERGE_METHOD.KEEP:
                        changed = True
                elif child_method == MERGE_METHOD.APPEND:
                    merged_child = new_child.merge(old_child, child_method)
                    changed = True
                else:
                    merged_child = old_child.merge(new_child, child_method)

                    changed = True

                merged.append(merged_child)

            merged.merge_method = (MERGE_METHOD.CHANGED if changed 
                                    else MERGE_METHOD.KEEP)

            merged.timestamp = old.timestamp
            merged.datetime = old.datetime

        else:

            new.make_datetime()

            merged.timestamp = new.timestamp
            merged.datetime = new.datetime
            for child in new:
                merged.append(child.merge(None, method))

        return merged

    def copy_elements(copied, element):

        copied.has_datetime = True
        copied.timestamp = element.timestamp
        copied.datetime = element.datetime
            
        for child in element:
            copied.append(child.copy(parent=copied))

        return copied

    def __init__(self, url_suffix, page_hash, title, 
                    users_to_notify=None):
        super().__init__(parent=None, idx=None)

        self.has_datetime = True
        self.url_suffix = url_suffix 
        self.weeks = []
        self.page_hash = page_hash
        self.title = title
        self.users_to_notify = users_to_notify
        self.prev_day = None
        self.prev_year_day = None
        self.has_new_year = False

    def append(self, week):
        self.weeks.append(week)

    def __iter__(self):
        return iter(self.weeks)

    def __bool__(self):
        return bool(self.weeks)

    def merge(self, old_schedule, method):
        merged = ApplySchedule(page_hash=self.page_hash)
        return FetchSchedule.merge_elements(merged, self, 
                                        old_schedule)

    def copy(self, parent=None):
        copied = FetchSchedule(
            url_suffix=self.url_suffix,
            page_hash=self.page_hash,
            title=self.title,
            users_to_notify=self.users_to_notify)
        return FetchSchedule.copy_elements(copied, self)

    def sync_time(self, cur_datetime):
        start_year = cur_datetime.year
        prev_year_day = self.prev_year_day
        if (prev_year_day and 
            prev_year_day.month - cur_datetime.month > FetchSchedule.YEAR_LOOP):
            start_year -= 1

        for week in self:
            if week.is_new_year:
                start_year += 1
            
            week_datetime = datetime.datetime(start_year,
                                            week.month,
                                            week.month_day)
            week.idx = (int((
                week_datetime -
                    FetchSchedule.SCHEDULE_WEEK_DATETIME_START 
                ).total_seconds())//FetchSchedule.WEEK_DELTA)

    


class ApplyScheduleElement():
    pass

class ApplyClass(ApplyScheduleElement):
    def __init__(self, merge_method, idx, desc, old_desc=None):
        self.merge_method = merge_method
        self.idx = idx
        self.desc = desc
        self.old_desc = old_desc
        

class ApplyDay(ApplyScheduleElement):
    def __init__(self, merge_method, idx):
        self.merge_method = merge_method
        self.idx = idx
        self.classes = []

    def append(self, cls):
        self.classes.append(cls)

    def __iter__(self):
        return iter(self.classes)

class ApplyWeek(ApplyScheduleElement):
    def __init__(self, merge_method, idx):
        self.merge_method = merge_method
        self.idx = idx
        self.days = []

    def append(self, day):
        self.days.append(day)

    def __iter__(self):
        return iter(self.days)

class ApplySchedule(ApplyScheduleElement):
    def __init__(self, page_hash):
        self.merge_method = MERGE_METHOD.KEEP
        self.weeks = []
        self.page_hash = page_hash

    def append(self, week):
        self.weeks.append(week)

    def __iter__(self):
        return iter(self.weeks)

