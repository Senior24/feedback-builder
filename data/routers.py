from handlers import commands, new_bot, manage_bots, pro

routers_list = [
    commands.router,
    new_bot.router,
    manage_bots.router,
    pro.router,
]
