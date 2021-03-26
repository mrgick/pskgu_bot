
import rasp.logger

def test_logger():
    rasp.logger.log("A test log message.")
    rasp.logger.log_warning("A test warning message.")
    rasp.logger.log_fatal("A test fatal message.")
