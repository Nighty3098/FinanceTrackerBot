import asyncio

import pretty_errors
from aiogram import *
from aiogram.enums import *
from aiogram.filters import *
from aiogram.types import *
from aiogram.utils.keyboard import *
from aiogram.utils.markdown import *
from requests.models import *

from config import *

async def month_list_kb():
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text="Декабрь", callback_data="December"))
    builder.add(types.InlineKeyboardButton(text="Январь", callback_data="January"))
    builder.add(types.InlineKeyboardButton(text="Февраль", callback_data="February"))
    builder.add(types.InlineKeyboardButton(text="Март", callback_data="March"))
    builder.add(types.InlineKeyboardButton(text="Апрель", callback_data="April"))
    builder.add(types.InlineKeyboardButton(text="Май", callback_data="May"))
    builder.add(types.InlineKeyboardButton(text="Июнь", callback_data="June"))
    builder.add(types.InlineKeyboardButton(text="Июль", callback_data="July"))
    builder.add(types.InlineKeyboardButton(text="Август", callback_data="August"))
    builder.add(types.InlineKeyboardButton(text="Сентябрь", callback_data="September"))
    builder.add(types.InlineKeyboardButton(text="Октябрь", callback_data="October"))
    builder.add(types.InlineKeyboardButton(text="Ноябрь", callback_data="November"))
    builder.add(types.InlineKeyboardButton(text="<<<", callback_data="Back2"))
    builder.adjust(2)

    return builder.as_markup()

async def back_kb():
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text="<<<", callback_data="Back"))
    builder.adjust(1)
    return builder.as_markup()
