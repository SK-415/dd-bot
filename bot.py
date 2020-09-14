from os import path

import nonebot, json, requests, datetime

import config

import logging
from nonebot.log import logger

if __name__ == '__main__':
    nonebot.init(config)
    nonebot.load_builtin_plugins()
    nonebot.load_plugin('help')
    nonebot.load_plugins(
        path.join(path.dirname(__file__), 'dantui_bot', 'plugins'),
        'dantui_bot.plugins'
    )
    nonebot.load_plugins(
        path.join(path.dirname(__file__), 'group_helper', 'plugins'),
        'group_helper.plugins'
    )

    # 设置日志输出格式
    f_path = path.dirname(path.abspath(__file__))
    debug_handler = logging.FileHandler(path.join(f_path, 'debug.log'), encoding='utf-8', mode='a')
    debug_handler.setLevel(logging.DEBUG)
    debug_handler.setFormatter(logging.Formatter("[%(asctime)s] %(levelname)s: %(message)s"))
    logger.addHandler(debug_handler)
    error_handler = logging.FileHandler(path.join(f_path, 'error.log'), encoding='utf-8', mode='a')
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(logging.Formatter("[%(asctime)s] %(levelname)s: %(message)s"))
    logger.addHandler(error_handler)

    nonebot.run()