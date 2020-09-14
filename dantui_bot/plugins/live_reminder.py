import nonebot
# from bilibili_api.user import UserInfo
from dantui_bot.plugins.utils import read_config, update_config
from dantui_bot.plugins.utils import User, log
from nonebot.log import logger
import asyncio


@nonebot.scheduler.scheduled_job('cron',  second='*/10')
# @nonebot.scheduler.scheduled_job('cron', minute='*') # DD机为一分钟
@log
async def _():
    # logger.debug('开始直播推送')
    config = await read_config()
    ups = config['status']
    
    uid_list = config['live']['uid_list']
    if not uid_list:
        return
    if config['live']['index'] >= len(uid_list):
        uid = uid_list[0]
        config['live']['index'] = 1
    else:
        uid = uid_list[config['live']['index']]
        config['live']['index'] += 1
    # if not config['uid'][uid]['live_reminder']:
    #     return
    await update_config(config)

    old_status = ups[uid]
    # for uid, old_status in ups.items():
    user = User(uid)
    user_info = await user.get_live_info()
    # print(user_info)
    new_status = user_info['liveStatus']
    if new_status != old_status:
        # ups[uid] = new_status
        # config['status'] = ups
        config['status'][uid] = new_status
        await update_config(config)

        bot = nonebot.get_bot()
        if new_status:
            name = (await user.get_info())['name'] # 获取昵称应转移至配置文件
            live_msg = f"{name} 开播啦！\n\n{user_info['title']}\n传送门→{user_info['url']}\n[CQ:image,file={user_info['cover']}]"
            groups = config["uid"][uid]["groups"]
            for group_id, bot_id in groups.items():
                # logger.debug(f"group_id: {group_id}, bot_id: {bot_id}")
                # live_reminder = config["groups"][group_id]['uid'][uid]["live_reminder"]
                # logger.debug(f"live_reminder: {live_reminder}")
                if config["groups"][group_id]['uid'][uid]["live_reminder"]:
                    # at = config['groups'][group_id]['uid'][uid]['at']
                    # logger.debug(f"{at}")
                    if config['groups'][group_id]['uid'][uid]['at']:
                        await bot.send_group_msg(group_id=group_id, message="[CQ:at,qq=all] "+live_msg, self_id=bot_id)
                    else:
                        await bot.send_group_msg(group_id=group_id, message=live_msg, self_id=bot_id)
            users = config["uid"][uid]["users"]
            for user_id, bot_id in users.items():
                if config["users"][user_id]['uid'][uid]["live_reminder"]:
                    await bot.send_private_msg(user_id=user_id, message=live_msg, self_id=bot_id)
