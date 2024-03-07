import asyncio

import pretty_errors
from aiogram import *
from aiogram.enums import *
from aiogram.filters import *
from aiogram.types import *
from aiogram.utils.keyboard import *
from aiogram.utils.markdown import *
from requests.models import *

from data.categories import *
from config import *
from db import *
from MESSAGES_TEXT import *
from keyboards.kb_builders import *

@dp.message(CommandStart())
async def start_command(message: Message):
    global user_id
    user_id = str(message.from_user.id)

    await create_connection(user_id)
    await create_table(user_id)

    logger.info(f"User {user_id} started the bot")

    if user_id in whitelist:
        # await message.answer_sticker(f'CAACAgIAAxkBAAEDiERlzyTAp3nkbu6T9nilXZcJDS87VQACEA4AAvWHUUj2ASQRaSSfRDQE')
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
        logger.error(err)

@dp.message(Command("month"))
async def month_list(message: Message):
    await message.answer("Выберите месяц:", reply_markup=await month_list_kb())


@dp.callback_query(lambda call: call.data=="December" or call.data=="January" or call.data=="February" or call.data=="March" or call.data=="April" or call.data=="May" or call.data=="June" or call.data=="July" or call.data=="August" or call.data=="September" or call.data=="October" or call.data=="November")
async def summary_by_month(call: CallbackQuery):
    global month
    month = str(call.data)
    await call.message.edit_text("Выберите категорию трат:", reply_markup=await category_list_kb())



@dp.callback_query(lambda call: call.data=="Drive" or call.data=="All" or call.data=="Food" or call.data=="Subscriptions" or call.data=="Books" or call.data=="Other" or call.data=="Courses")
async def categories(call: CallbackQuery):
    category = str(call.data)

    if category == "All":
        result = str(await get_summary_by_month(user_id, month))
        await call.message.edit_text(result, reply_markup=await to_categories())

        logger.debug(f"{result}")
    else:
        result = str(await get_summary_by_category(user_id, category, month))
        await call.message.edit_text(result, reply_markup=await to_categories())

@dp.message(Command("today"))
async def today_summarize(message: Message):
    try:
        result = str(await today(user_id))

        await message.answer(result, reply_markup=await back_main())

        logger.debug(f"User: {user_id}, summarize: {result}")
    except AttributeError as err:
        await message.answer("Отстутствуют данные в одной из таблиц", reply_markup=await back_main())
        logger.error(err) 


@dp.message(Command("year"))
async def year_summary(message: Message):
    result = await get_year_summary(user_id)
    await message.answer(result, reply_markup=await back_kb())

@dp.callback_query(F.data == "Back")
async def to_main_menu(call: CallbackQuery):
    # await call.message.answer(HELLO_MESSAGE)
    await call.message.edit_text("Выберите месяц:", reply_markup=await month_list_kb())

@dp.callback_query(F.data == "Back2")
async def to_main_menu(call: CallbackQuery):
    await call.message.edit_text(HELLO_MESSAGE)

@dp.callback_query(F.data == "Categories")
async def category_list(call: CallbackQuery):
    await call.message.edit_text("Выберите категорию трат:", reply_markup=await category_list_kb())
