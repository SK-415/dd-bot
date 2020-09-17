import nonebot
from nonebot.permission import GROUP_ADMIN, PRIVATE_FRIEND, SUPERUSER, check_permission
from .utils import Dynamic, Dydb, User, log
from .utils import read_config, update_config
import asyncio
from collections import Counter
from nonebot import on_command, CommandSession


__plugin_name__ = 'DD机'
__plugin_usage__ = r"""DD机目前支持的功能有：

主播列表
添加主播 uid
删除主播 uid
开启动态 uid
关闭动态 uid
开启直播 uid
关闭直播 uid


只有管理员（群聊）或者机器人好友（私聊）才会生效，输入命令时不要忘记空格

其中“uid”请替换为UP的uid，注意是uid不是直播间id

添加后默认开启直播和动态推送，在哪里（群聊/私聊）添加就会在哪里推送
"""

# @nonebot.on_command('添加主播', permission=GROUP_ADMIN | PRIVATE_FRIEND | SUPERUSER)
@nonebot.on_command('添加主播')
@log
async def add_up(session):
    """添加主播并创建对应配置文件"""
    config = await read_config()
    if not await permission_check(session, config):
        return
    uid = session.current_arg_text.strip()
    dydb = Dydb()
    if uid not in config["status"]: # uid不在配置文件就创建一个
        user = User(uid)
        try: # 应该改uid有效检测逻辑
            user_info = await user.get_info()
            name = user_info["name"]
        except:
            await session.finish("请输入有效的uid")
        config['status'][uid] = 0
        config['uid'][uid] = {'groups': {}, 'users': {}, 'dynamic': 0, 'live': 0, 'name': name}
        config['dynamic']['uid_list'].append(uid) # 主播uid添加至动态列表，在DD机中应删除
        config['live']['uid_list'].append(uid) # 主播uid添加至直播列表
    else:
        name = config['uid'][uid]['name']

    tables = dydb.get_table_list()
    if 'uid' + uid not in tables:
        dydb.create_table('uid'+uid, '(time int primary key, url varchar(50), is_recall boolean)') # 创建uid表

    if session.event.detail_type == "group": # 检测是否群消息
        group_id = str(session.event.group_id)
        if 'qq' + group_id not in tables:
            dydb.create_table('qq'+group_id, '(url varchar(50) primary key, message_id int, bot_id int)')
        if group_id not in config["uid"][uid]["groups"]:
            config["uid"][uid]["groups"][group_id] = session.self_id
        else:
            await session.finish(f"您已将{name}（{uid}）添加至该群，请勿重复添加")
        if group_id in config["groups"]:
            config["groups"][group_id]["uid"][uid] = {"live_reminder": True, "dynamic": True, 'at': False}
        else:
            config["groups"][group_id] = {"uid": {uid: {"live_reminder": True, "dynamic": True, 'at': False}}, 'admin': True}
        config['uid'][uid]['dynamic'] += 1
        config['uid'][uid]['live'] += 1
        await update_config(config)
        await session.send(f"已将{name}（{uid}）添加至该群")

    elif session.event.detail_type == "private": # 检测是否私聊消息
        user_id = str(session.event.user_id)
        if user_id not in config["uid"][uid]["users"]:
            config["uid"][uid]["users"][user_id] = session.self_id
        else:
            await session.finish(f"您已添加{name}（{uid}），请勿重复添加")
        if user_id in config["users"]:
            config["users"][user_id]["uid"][uid] = {"live_reminder": True, "dynamic": True} # DD机中应改为 False
        else:
            config["users"][user_id] = {"uid": {uid: {"live_reminder": True, "dynamic": True}}} # DD机中应改为 False
        config['uid'][uid]['dynamic'] += 1 # 动态推送数加一DD机中应注释
        config['uid'][uid]['live'] += 1
        await update_config(config)
        await session.send(f"已添加{name}（{uid}）")

# @nonebot.on_command('主播列表', permission=GROUP_ADMIN | PRIVATE_FRIEND | SUPERUSER)
@nonebot.on_command('主播列表')
@log
async def list_up(session):
    config = await read_config()
    if not await permission_check(session, config):
        return
    if session.event.detail_type == 'group':
        group_id = str(session.event.group_id)
        try:
            uid_list = config['groups'][group_id]['uid']
        except KeyError:
            uid_list = {}
        message = "以下为该群的订阅列表，可发送“删除主播 uid”进行删除\n\n"
    elif session.event.detail_type == 'private':
        user_id = str(session.event.user_id)
        try:
            uid_list = config['users'][user_id]['uid']
        except KeyError:
            uid_list = {}
        message = "以下为您的订阅列表，可发送“删除主播 uid”进行删除\n\n"
    for uid, status in uid_list.items():
        name = config['uid'][uid]['name']
        message += f"【{name}】"
        message += f"直播推送：{'开' if status['live_reminder'] else '关'}，"
        message += f"动态推送：{'开' if status['dynamic'] else '关'}"
        message += f"（{uid}）\n"
    await session.send(message=message)
    
# @nonebot.on_command('删除主播', permission=GROUP_ADMIN | PRIVATE_FRIEND | SUPERUSER)
@nonebot.on_command('删除主播')
@log
async def delete_up(session):
    config = await read_config()
    if not await permission_check(session, config):
        return
    uid = session.current_arg_text.strip()
    try:
        name = config['uid'][uid]['name']
    except KeyError:
        session.finish("删除失败，uid不存在")
    if session.event.detail_type == 'group':
        group_id = str(session.event.group_id)
        try:
            if config['groups'][group_id]['uid'][uid]['dynamic']:
                config['uid'][uid]['dynamic'] -= 1
            if config['groups'][group_id]['uid'][uid]['live_reminder']:
                config['uid'][uid]['live'] -= 1
            del config['groups'][group_id]['uid'][uid]
            del config['uid'][uid]['groups'][group_id]
            # 如果用户没有关注则删除用户
            if config['groups'][group_id]['uid'] == {} and config['groups'][group_id]['admin']:
                del config['groups'][group_id]
        except KeyError:
            session.finish("删除失败，uid不存在")
    elif session.event.detail_type == 'private':
        user_id = str(session.event.user_id)
        try:
            if config['users'][user_id]['uid'][uid]['dynamic']:
                config['uid'][uid]['dynamic'] -= 1
            if config['users'][user_id]['uid'][uid]['live_reminder']:
                config['uid'][uid]['live'] -= 1
            del config['users'][user_id]['uid'][uid]
            del config['uid'][uid]['users'][user_id]
            # 如果用户没有关注则删除用户
            if config['users'][user_id]['uid'] == {}:
                del config['users'][user_id]
        except KeyError:
            session.finish("删除失败，uid不存在")
    # 如果无人再订阅动态，就从动态列表中移除
    if config['uid'][uid]['dynamic'] == 0 and uid in config['dynamic']['uid_list']:
        config['dynamic']['uid_list'].remove(uid)
    # 如果无人再订阅直播，就从直播列表中移除
    if config['uid'][uid]['live'] == 0 and uid in config['live']['uid_list']:
        config['live']['uid_list'].remove(uid)
    # 如果没人订阅该主播，则将该主播彻底删除
    if config['uid'][uid]['groups'] == {} and config['uid'][uid]['users'] == {}:
        del config['uid'][uid]
        del config['status'][uid]
    
    # user = User(uid)
    # name = (await user.get_info())['name']
    await update_config(config)
    await session.finish(f"已删除 {name}（{uid}）")

# @nonebot.on_command('开启动态', permission=GROUP_ADMIN | PRIVATE_FRIEND | SUPERUSER)
@nonebot.on_command('开启动态')
@log
async def dynamic_on(session):
    config = await read_config()
    if not await permission_check(session, config):
        return
    uid = session.current_arg_text.strip()
    if session.event.detail_type == 'group':
        group_id = str(session.event.group_id)
        try:
            if config['groups'][group_id]['uid'][uid]['dynamic'] == True:
                session.finish('请勿重复开启动态推送')
            config['groups'][group_id]['uid'][uid]['dynamic'] = True
            config['uid'][uid]['dynamic'] += 1
        except KeyError:
            session.finish("开启失败，uid不存在")
    elif session.event.detail_type == 'private':
        user_id = str(session.event.user_id)
        try:
            if config['users'][user_id]['uid'][uid]['dynamic'] == True:
                session.finish('请勿重复开启动态推送')
            config['users'][user_id]['uid'][uid]['dynamic'] = True
            config['uid'][uid]['dynamic'] += 1
        except KeyError:
            session.finish("开启失败，uid不存在")
    # 如果是第一个开启的，就添加至动态推送列表
    if config['uid'][uid]['dynamic'] == 1:
        config['dynamic']['uid_list'].append(uid)
    name = config['uid'][uid]['name']
    # user = User(uid)
    # name = (await user.get_info())['name']
    await update_config(config)
    await session.finish(f"已开启 {name}（{uid}）的动态推送")

# @nonebot.on_command('关闭动态', permission=GROUP_ADMIN | PRIVATE_FRIEND | SUPERUSER)
@nonebot.on_command('关闭动态')
@log
async def dynamic_off(session):
    config = await read_config()
    if not await permission_check(session, config):
        return
    uid = session.current_arg_text.strip()
    if session.event.detail_type == 'group':
        group_id = str(session.event.group_id)
        try:
            if config['groups'][group_id]['uid'][uid]['dynamic'] == False:
                session.finish('请勿重复关闭动态推送')
            config['groups'][group_id]['uid'][uid]['dynamic'] = False
            config['uid'][uid]['dynamic'] -= 1
        except KeyError:
            session.finish("关闭失败，uid不存在")
    elif session.event.detail_type == 'private':
        user_id = str(session.event.user_id)
        try:
            if config['users'][user_id]['uid'][uid]['dynamic'] == False:
                session.finish('请勿重复关闭动态推送')
            config['users'][user_id]['uid'][uid]['dynamic'] = False
            config['uid'][uid]['dynamic'] -= 1
        except KeyError:
            session.finish("关闭失败，uid不存在")
    # 如果无人再订阅动态，就从动态列表中移除
    if config['uid'][uid]['dynamic'] == 0:
        config['dynamic']['uid_list'].remove(uid)
    name = config['uid'][uid]['name']
    # user = User(uid)
    # name = (await user.get_info())['name']
    await update_config(config)
    await session.finish(f"已关闭 {name}（{uid}）的动态推送")

# @nonebot.on_command('开启直播', permission=GROUP_ADMIN | PRIVATE_FRIEND | SUPERUSER)
@nonebot.on_command('开启直播')
@log
async def live_on(session):
    config = await read_config()
    if not await permission_check(session, config):
        return
    uid = session.current_arg_text.strip()
    if session.event.detail_type == 'group':
        group_id = str(session.event.group_id)
        try:
            if config['groups'][group_id]['uid'][uid]['live_reminder']:
                session.finish('请勿重复开启直播推送')
            config['groups'][group_id]['uid'][uid]['live_reminder'] = True
            config['uid'][uid]['live'] += 1
        except KeyError:
            session.finish("开启失败，uid不存在")
    elif session.event.detail_type == 'private':
        user_id = str(session.event.user_id)
        try:
            if config['users'][user_id]['uid'][uid]['live_reminder']:
                session.finish('请勿重复开启直播推送')
            config['users'][user_id]['uid'][uid]['live_reminder'] = True
            config['uid'][uid]['live'] += 1
        except KeyError:
            session.finish("开启失败，uid不存在")
    # 如果是第一个开启的，就添加至直播推送列表
    if config['uid'][uid]['live'] == 1:
        config['live']['uid_list'].append(uid)
    name = config['uid'][uid]['name']
    # user = User(uid)
    # name = (await user.get_info())['name']
    await update_config(config)
    await session.finish(f"已开启 {name}（{uid}）的直播推送")

# @nonebot.on_command('关闭直播', permission=GROUP_ADMIN | PRIVATE_FRIEND | SUPERUSER)
@nonebot.on_command('关闭直播')
@log
async def live_off(session):
    config = await read_config()
    if not await permission_check(session, config):
        return
    uid = session.current_arg_text.strip()
    if session.event.detail_type == 'group':
        group_id = str(session.event.group_id)
        try:
            if not config['groups'][group_id]['uid'][uid]['live_reminder']:
                session.finish('请勿重复关闭直播推送')
            config['groups'][group_id]['uid'][uid]['live_reminder'] = False
            config['uid'][uid]['live'] -= 1
        except KeyError:
            session.finish("关闭失败，uid不存在")
    elif session.event.detail_type == 'private':
        user_id = str(session.event.user_id)
        try:
            if not config['users'][user_id]['uid'][uid]['live_reminder']:
                session.finish('请勿重复关闭直播推送')
            config['users'][user_id]['uid'][uid]['live_reminder'] = False
            config['uid'][uid]['live'] -= 1
        except KeyError:
            session.finish("关闭失败，uid不存在")
    # 如果无人再订阅动态，就从直播列表中移除
    if config['uid'][uid]['live'] == 0:
        config['live']['uid_list'].remove(uid)
    name = config['uid'][uid]['name']
    # user = User(uid)
    # name = (await user.get_info())['name']
    await update_config(config)
    await session.finish(f"已关闭 {name}（{uid}）的直播推送")

@on_command('开启at', permission=GROUP_ADMIN | PRIVATE_FRIEND | SUPERUSER)
@log
async def at_on(session: CommandSession):
    if session.event.detail_type != 'group':
        await session.send("只有群里才能开启@全体")
        return
    uid = session.current_arg_text.strip()
    config = await read_config()
    group_id = session.event.group_id
    if uid not in config['groups'][str(group_id)]['uid']:
        await session.send("开启失败，uid不存在")
        return
    if config['groups'][str(group_id)]['uid'][uid]['at']:
        await session.send("请勿重复开启@全员")
        return
    config['groups'][str(group_id)]['uid'][uid]['at'] = True
    await update_config(config)
    name = config['uid'][uid]['name']
    await session.send(f"已开启 {name}（{uid}）的 @全体成员")

@on_command('关闭at', permission=GROUP_ADMIN | PRIVATE_FRIEND | SUPERUSER)
@log
async def at_off(session: CommandSession):
    if session.event.detail_type != 'group':
        await session.send("只有群里才能关闭@全体")
        return
    uid = session.current_arg_text.strip()
    config = await read_config()
    group_id = session.event.group_id
    if uid not in config['groups'][str(group_id)]['uid']:
        await session.send("关闭失败，uid不存在")
        return
    if not config['groups'][str(group_id)]['uid'][uid]['at']:
        await session.send("请勿重复关闭@全员")
        return
    config['groups'][str(group_id)]['uid'][uid]['at'] = False
    await update_config(config)
    name = config['uid'][uid]['name']
    await session.send(f"已关闭 {name}（{uid}）的 @全体成员")

@on_command('开启权限', permission=GROUP_ADMIN | PRIVATE_FRIEND | SUPERUSER)
@log
async def permission_on(session: CommandSession):
    if session.event.detail_type != 'group':
        await session.send("只有群里才能设置权限")
        return
    config = await read_config()
    group_id = str(session.event.group_id)

    if group_id not in config['groups'] or config['groups'][group_id]['admin']:
        await session.send("请勿重复开启权限")
        return
    else:
        config['groups'][group_id]['admin'] = True

    await update_config(config)
    await session.send(f"已开启权限限制，只有管理员才能触发指令")

@on_command('关闭权限', permission=GROUP_ADMIN | PRIVATE_FRIEND | SUPERUSER)
@log
async def permission_off(session: CommandSession):
    if session.event.detail_type != 'group':
        await session.send("只有群里才能设置权限")
        return
    config = await read_config()
    group_id = str(session.event.group_id)

    if group_id not in config['groups']:
        config['groups'][group_id] = {'uid': {}, 'admin': False}
    elif not config['groups'][group_id]['admin']:
        await session.send("请勿重复关闭权限")
        return
    else:
        config['groups'][group_id]['admin'] = False

    await update_config(config)
    await session.send(f"已关闭权限限制，所有人都能触发指令")

async def permission_check(session: CommandSession, config):
    if session.event.detail_type == 'group':
        group_id = str(session.event.group_id)
        if True if group_id not in config['groups'] else config['groups'][group_id]['admin']:
            if await check_permission(session.bot, session.event, GROUP_ADMIN | PRIVATE_FRIEND | SUPERUSER):
                return True
            else:
                await session.send('权限不足，无法使用')
                return False
        else:
            return True
    else:
        return True

@nonebot.on_command('修复配置', permission=GROUP_ADMIN | PRIVATE_FRIEND | SUPERUSER)
@log
async def fix_config(session):
    config = await read_config()
    dy_counter = Counter() # 动态推送开启用户数统计
    live_counter = Counter() # 直播推送开启用户数统计
    
    del_qq = [] # 没有订阅的QQ号
    # 统计用户开启的订阅数量
    for qq, user in config['users'].items():
        try:
            for uid, status in user['uid'].items():
                if status['dynamic']:
                    dy_counter[uid] += 1
                if 'live' in status and status['live'] or status['live_reminder']:
                    live_counter[uid] += 1
        except KeyError:
            del_qq.append(qq)
    # 删除没有订阅的QQ号
    for qq in del_qq:
        del config['users'][qq]

    del_qq = [] # 没有订阅的QQ号
    # 统计群开启的订阅数量
    for qq, group in config['groups'].items():
        try:
            for uid, status in group['uid'].items():
                if status['dynamic']:
                    dy_counter[uid] += 1
                if 'live' in status and status['live'] or status['live_reminder']:
                    live_counter[uid] += 1
        except KeyError:
            del_qq.append(qq)
    # 删除没有订阅的QQ群号
    for qq in del_qq:
        del config['groups'][qq]
    
    # 给每个QQ号下的 uid 添加@全体设置
    for qq_id in config['groups']:
        for uid in config['groups'][qq_id]['uid']:
            if 'at' not in config['groups'][qq_id]['uid'][uid]:
                config['groups'][qq_id]['uid'][uid]['at'] = False

    # 将 uid 列表中的 live_reminder 替换为 live
    for uid in config['uid']:
        if 'live_reminder' in config['uid'][uid]:
            del config['uid'][uid]['live_reminder']

    # 检查是否有权限选项
    for group_id in config['groups']:
        if 'admin' not in config['groups'][group_id]:
            config['groups'][group_id]['admin'] = True

    # 将动态和直播订阅总数填入对应uid
    for uid, sub_num in dy_counter.items():
        config['uid'][uid]['dynamic'] = sub_num
    for uid, sub_num in live_counter.items():
        config['uid'][uid]['live'] = sub_num
    # 重置动态和直播的爬取列表
    config['dynamic'] = {'uid_list': list(dy_counter), 'index': 0}
    config['live'] = {'uid_list': list(config['status']), 'index': 0}
    await update_config(config)
    await session.send('修复完成')