import inspect
import io
import logging
import os
import threading
from logging.handlers import RotatingFileHandler


current_dir = os.path.dirname(__file__)
project_dir = os.path.join(current_dir, '..')
project_dir = os.path.normpath(project_dir)

log_dir = os.path.join(project_dir, 'logs')

loggers = {}
preset_loggers = ['retrieve_log']


def setup_one_logger(logger_name, sub_folders=None, log_level=logging.DEBUG):
    """
    asctime: 日志事件的时间。默认格式为“2003-07-08 16:49:45,896”（逗号后的数字是毫秒）。你可以通过给 Formatter 的构造函数传递 datefmt 参数来自定义时间格式。
    name: 使用该 Logger 的名称。
    levelname: 文本形式的日志级别（'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'）。
    message: 日志消息，通过 LogRecord 的 getMessage() 方法计算得到。
    filename: 调用日志函数的源文件的文件名。
    pathname: 调用日志函数的源文件的完整路径名。
    module: 调用日志函数的模块名。它是 pathname 的文件名部分，去掉扩展名。
    funcName: 调用日志函数的函数名。
    lineno: 发生日志调用的源代码行号。
    thread: 调用日志函数的线程ID。
    threadName: 调用日志函数的线程名。
    process: 调用日志函数的进程ID。
    processName: 调用日志函数的进程名。
    :param sub_folders:
    :param log_level:
    :param logger_name:
    :return:
    """
    if sub_folders:
        log_path = os.path.join(log_dir, *sub_folders, f"{logger_name}.log")
    else:
        log_path = os.path.join(log_dir, f"{logger_name}.log")

    directory = os.path.dirname(log_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

    new_logger = logging.getLogger(logger_name)
    fh = RotatingFileHandler(log_path, maxBytes=20 * 1024 * 1024, backupCount=200)
    # formatter = logging.Formatter('%(asctime)s  - %(levelname)s - %(message)s ')
    # formatter = logging.Formatter('%(asctime)s - %(funcName)s - %(lineno)d - %(levelname)s - %(message)s ',
    #                               datefmt='%Y-%m-%d %H:%M:%S')
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(caller)s - %(message)s',
                                  datefmt='%Y-%m-%d %H:%M:%S')
    fh.setFormatter(formatter)
    new_logger.addHandler(fh)
    new_logger.setLevel(log_level)
    loggers[logger_name] = new_logger
    return new_logger


for ln in preset_loggers:
    loggers[ln] = setup_one_logger(ln)


def get_caller_info(level: int = 2):
    caller = inspect.stack()[level]
    filename = caller.filename
    lineno = caller.lineno
    funcname = caller.function
    caller_info = f'{filename}:{lineno}:{funcname}'
    return caller_info


def get_logger(logger_name) -> logging.Logger:
    cur_logger_name = logger_name
    # cur_thread_name = threading.current_thread().name
    # cur_logger_name = f"{cur_thread_name}_{logger_name}"
    if cur_logger_name not in loggers:
        setup_one_logger(cur_logger_name)
    return loggers[cur_logger_name]


def log_info(msg, logger_name="retrieve_log"):
    # ic(msg)
    cur_logger = get_logger(logger_name)
    cur_logger.info(msg, extra={'caller': get_caller_info()})


def log_error(msg, logger_name="retrieve_log"):
    # ic(msg)
    cur_logger = get_logger(logger_name)
    cur_logger.error(msg, extra={'caller': get_caller_info()})


def log_debug(msg, logger_name="retrieve_log"):
    # ic(msg)
    cur_logger = get_logger(logger_name)
    cur_logger.debug(msg, extra={'caller': get_caller_info()})
