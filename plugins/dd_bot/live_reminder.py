import nonebot
from .utils import read_config, update_config
from .utils import User, log
import asyncio


@nonebot.scheduler.scheduled_job('cron',  second='*/10')
# @nonebot.scheduler.scheduled_job('cron', minute='*') # DD机为一分钟
@log
async def _():
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
    await update_config(config)

    old_status = ups[uid]
    user = User(uid)
    user_info = await user.get_live_info()
    new_status = user_info['liveStatus']
    if new_status != old_status:
        config['status'][uid] = new_status
        await update_config(config)

        bot = nonebot.get_bot()
        if new_status:
            name = (await user.get_info())['name'] # 获取昵称应转移至配置文件
            live_msg = f"{name} 开播啦！\n\n{user_info['title']}\n传送门→{user_info['url']}\n[CQ:image,file={user_info['cover']}]"
            groups = config["uid"][uid]["groups"]
            for group_id, bot_id in groups.items():
                if config["groups"][group_id]['uid'][uid]["live_reminder"]:
                    if config['groups'][group_id]['uid'][uid]['at']:
                        await bot.send_group_msg(group_id=group_id, message="[CQ:at,qq=all] "+live_msg, self_id=bot_id)
                    else:
                        await bot.send_group_msg(group_id=group_id, message=live_msg, self_id=bot_id)
            users = config["uid"][uid]["users"]
            for user_id, bot_id in users.items():
                if config["users"][user_id]['uid'][uid]["live_reminder"]:
                    await bot.send_private_msg(user_id=user_id, message=live_msg, self_id=bot_id)
