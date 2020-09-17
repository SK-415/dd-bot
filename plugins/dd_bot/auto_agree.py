import nonebot
from nonebot import on_request, RequestSession
from nonebot.permission import SUPERUSER, PRIVATE_FRIEND, check_permission


@on_request('friend')
async def friend_req(session: RequestSession):
    if await check_permission(session.bot, session.event, SUPERUSER):
        await session.bot.set_friend_add_request(flag=session.event.flag, approve=True)

@on_request('group')
async def group_invite(session: RequestSession):
    if session.event.sub_type == 'invite' and await check_permission(session.bot, session.event, PRIVATE_FRIEND):
        await session.bot.set_group_add_request(flag=session.event.flag, sub_type='invite', approve=True)