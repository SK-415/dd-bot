import nonebot
import asyncio
import os
from dantui_bot.plugins.utils import Dynamic, Dydb, User, log
from dantui_bot.plugins.utils import read_config, update_config
from nonebot.log import logger
from datetime import datetime, timedelta
# import time


@nonebot.scheduler.scheduled_job('cron', second='*/10')
@log
async def _():
    # start = time.time()
    # logger.debug('开始动态推送')
    config = await read_config()
    ups = config['dynamic']['uid_list']
    if len(ups):
        if config['dynamic']['index'] >= len(ups):
            uid = ups[0]
            config['dynamic']['index'] = 0
        else:
            uid = ups[config['dynamic']['index']]
            config['dynamic']['index'] += 1
    else:
        return

    user = User(uid)
    dynamics = (await user.get_dynamic())['cards'] # 获取最近十二条动态
    # logger.debug(pformat(dynamics))
    config['uid'][uid]['name'] = dynamics[0]['desc']['user_profile']['info']['uname']
    await update_config(config)

    dydb = Dydb()
    data = dydb.run_command(f'select * from uid{uid} order by time desc limit 3 offset 0')
    # logger.debug(data)
    if not data:
        for dynamic in dynamics: # 添加最近十二条动态进数据库
            dynamic = Dynamic(dynamic)
            dydb.insert_uid(uid, dynamic.time, dynamic.url, True)
        return

    last_time = data[0][0]
    for dynamic in reversed(dynamics[:3]): # 取最近3条动态
        dynamic = Dynamic(dynamic)
        if dynamic.time > last_time and dynamic.time > datetime.now().timestamp() - timedelta(minutes=5).seconds:
            # logger.debug(f"dynamic.time={dynamic.time}, last_time={last_time}, time_now={datetime.now().timestamp() - timedelta(minutes=5).seconds}")
            await dynamic.get_screenshot()
            # await dynamic.upload()
            await dynamic.encode()
            os.remove(dynamic.img_path)
            await dynamic.format()
            bot = nonebot.get_bot()
            for group_id, bot_id in config["uid"][uid]["groups"].items():
                if config["groups"][group_id]['uid'][uid]["dynamic"]:
                    message_id = (await bot.send_group_msg(group_id=group_id, message=dynamic.message, self_id=bot_id))['message_id']
                    # print(f'message_id: {message_id}, type: {type(message_id)}\nurl: {dynamic.url}, type: {type(dynamic.url)}\nbot_id: {bot_id}, type: {type(bot_id)}')
                    dydb.insert_qq(group_id, dynamic.url, message_id, bot_id)
            for user_id, bot_id in config["uid"][uid]["users"].items():
                if config["users"][user_id]['uid'][uid]["dynamic"]:
                    await bot.send_private_msg(user_id=user_id, message= dynamic.message, self_id=bot_id)
            dydb.insert_uid(dynamic.uid, dynamic.time, dynamic.url, False)
    # logger.debug(f"总耗时{time.time() - start}")
