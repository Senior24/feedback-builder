from handlers import pro, start, new_bot, manage_bots

routers_list = [
    pro.router,
    start.router,
    new_bot.router,
    manage_bots.router
]
