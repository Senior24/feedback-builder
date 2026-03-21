import asyncio

from aiogram import Dispatcher

running_bots: dict[str, asyncio.Task] = dict()
running_dps: dict[str, Dispatcher] = dict()
