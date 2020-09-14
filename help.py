import nonebot
from nonebot import on_command, CommandSession

@nonebot.on_command('菜单', aliases=['帮助', '功能'])
async def _(session: CommandSession):
    plugins = list(filter(lambda p: p.name, nonebot.get_loaded_plugins()))

    arg = session.current_arg_text.strip()
    if not arg:
        await session.send(
            "发送“帮助 功能名”可查看详细信息，注意空格\n目前支持的功能有：\n\n" + '\n'.join(p.name for p in plugins)
        )
        return
    
    for p in plugins:
        if p.name == arg:
            await session.send(p.usage)