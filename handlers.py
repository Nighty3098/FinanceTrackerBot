import asyncio

import pretty_errors
from aiogram import *
from aiogram.enums import *
from aiogram.filters import *
from aiogram.types import *
from aiogram.utils.keyboard import *
from aiogram.utils.markdown import *
from requests.models import *

from categories import *
from categories import change_category
from config import *
from db import *
from MESSAGES_TEXT import *


@dp.message(CommandStart())
async def start_command(message: Message):
    global user_id
    user_id = str(message.from_user.id)

    await create_connection(user_id)
    await create_table(user_id)

    logger.info(f"User {user_id} started the bot")

    if user_id in whitelist:
        await message.answer(HELLO_MESSAGE)
        await create_connection(user_id)

    else:
        await message.answer(NO_ACCESS)


@dp.message(Command("in"))
async def income(message: Message):
    if message.text.startswith("/in"):
        user_msg = message.text
        user_msg = user_msg.split(" ")

        if len(user_msg) == 3:
            value = int(user_msg[1])
            category = await change_category(str(user_msg[2]))
            await add_income(user_id, value, category)
            await message.answer(f"{value} рублей добавлено в {category}")
            logger.debug(f"{user_id} add {value} _income_ to {category}")
        else:
            await message.answer("Неправильный формат ввода")
    else:
        pass


@dp.message(Command("out"))
async def income(message: Message):
    if message.text.startswith("/out"):
        user_msg = message.text
        user_msg = user_msg.split(" ")

        if len(user_msg) == 3:
            value = int(user_msg[1])
            category = await change_category(str(user_msg[2]))
            await add_consumption(user_id, value, category)
            await message.answer(f"{value} рублей добавлено в {category}")
            logger.debug(f"{user_id} add {value} _consumption_ to {category}")
        else:
            await message.answer("Неправильный формат ввода")
    else:
        pass


@dp.message(Command("summary"))
async def summary(message: Message):
    try:
        summarize = await get_summary(user_id)
        summarize = summarize.split(" ")
        sum_income = int(summarize[0])
        sum_consumption = int(summarize[1])

        await message.answer(
            f"Ваши расходы: {sum_consumption} руб\nВаши доходы: {sum_income} руб"
        )
        logger.debug(f"User: {user_id}, summarize: -{sum_consumption} +{sum_income}")
    except ValueError as err:
        await message.answer("Отстутствуют данные в одной из таблиц")
        logger.info(err)
