import logging
import os
from os import path

import nonebot
from nonebot.log import logger

import config

if __name__ == '__main__':
    nonebot.init(config)
    nonebot.load_builtin_plugins()
    nonebot.load_plugin('help')
    
    # 将工作目录切换到 bot.py 所在的文件夹
    os.chdir(path.dirname(__file__))

    # 导入 \plugins 下所有的插件
    for dirname in os.listdir('plugins'):
        if path.isdir(path.join('plugins', dirname)):
            nonebot.load_plugins(
                path.join(path.abspath('.'), 'plugins', dirname),
                'plugins.' + dirname
            )

    # 设置 DEBUG 日志
    debug_handler = logging.handlers.TimedRotatingFileHandler(
        filename=path.join('log', 'debug.log'), 
        when='midnight', 
        interval=1, 
        backupCount=0, # 保留日志个数, 0不删除
        encoding='utf-8'
        )
    debug_handler.setLevel(logging.DEBUG)
    debug_handler.setFormatter(logging.Formatter("[%(asctime)s] %(levelname)s: %(message)s"))
    logger.addHandler(debug_handler)

    # 设置 ERROR 日志
    error_handler = logging.handlers.TimedRotatingFileHandler(
        filename=path.join('log', 'error.log'), 
        when='midnight', 
        interval=1, 
        backupCount=0, # 保留日志个数, 0不删除
        encoding='utf-8'
        )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(logging.Formatter("[%(asctime)s] %(levelname)s: %(message)s"))
    logger.addHandler(error_handler)

    nonebot.run()
