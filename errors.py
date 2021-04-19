

class StatusSuccess(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return "<STATUS OK> %s" % self.msg

class BaseError(Exception):
    def __str__(self):
        return self.msg

class CreationError(BaseError):
    def __init__(self, msg):
        self.msg = "<CREATION ERROR> %s" % msg

class StatusError(BaseError):
    def __init__(self, msg):
        self.msg = "<STATUS FAILED> %s" % msg

class RequestError(BaseError):
    def __init__(self, url, msg):
        self.msg = "Request '%s' failed: %s" % (url, msg)
