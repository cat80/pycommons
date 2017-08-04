import logging
import os
from logging.handlers import TimedRotatingFileHandler


##
# <p>Copyright (c) 2016-2017 cat80 </p>
# <p>该文件是对日志操作的简单封装</p>
# <p>一般情况下，只需要使用logger.default()可使用默认的日志对象，支持debug,info,error三种日志记录方法 </p>
# <p>默认情况下，日志保存在方前py执行目录的log目录下</p>
# <p>默认的日志级别为info,不会记录debug日志。如果需要调整日志级别，可自行初始化logging或者设置全局的global_logger_level变量 来指定日志</p>
#
# <br/><br/>
# <p>该文件引用的日志类为系统自带的日志组件，不需要额外引用包</p>
#
##

class logger:
    log = None
    __default_log = None

    @classmethod
    def default(cls):
        if cls.__default_log is None:
            cls.__default_log = logger("default")
        return cls.__default_log

    @classmethod
    def __get_logging_level(cls, set_level=None):
        if set_level is not None:
            return set_level
        global global_logger_level
        if global_logger_level is not None:
            return global_logger_level
        return logging.INFO

    def __init__(self, name=None, logger_level=None):

        self.log = logging.getLogger(name)
        self.log.setLevel(self.__get_logging_level(logger_level))
        if os.path.exists("log") is False:
            os.makedirs("log")
        fh = TimedRotatingFileHandler('log/log.log', when='D', interval=1, backupCount=30)
        date_fmt = '%Y-%m-%d %H:%M:%S'
        format_str = '%(asctime)s  %(filename)s[line:%(lineno)d]  %(levelname)s %(message)s '
        # formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        formatter = logging.Formatter(format_str, date_fmt)
        fh.setFormatter(formatter)
        self.log.addHandler(fh)

    def error(self, msg):
        self.log.error(msg)

    def info(self, msg):
        self.log.info(msg)

    def debug(self, msg):
        self.log.debug(msg)


# global_logger_level = logging.INFO
if __name__ == "__main__":
    # log = logger("main")
    # log.info("dd")
    logger.default().error("eeee...")
    logger.default().info("iiiiiii...")
    log = logger("test")
    log.debug("this is debugging....")
    log.info("this is info....")
    log.error("this is error....")
    # logger.get_default_log().error('error best...')
