from aiogram import Bot, types
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

#Кнопки основного меню клавиатуры:
button_buy = KeyboardButton('Купить 💰')
button_info = KeyboardButton('Информация 🤔')
button_steam = KeyboardButton('Steam')
button_origin = KeyboardButton('Origin')
button_back = KeyboardButton("Возврат в главное меню")
button_profile = KeyboardButton("Профиль 👤")
button_stock = KeyboardButton("Наличие товаров 🛒")


button_confirm = InlineKeyboardButton('Да', callback_data='yes')
button_cancel = InlineKeyboardButton('Нет', callback_data='no')

#Кнопки товарных позиций:

button_origin_item1 = InlineKeyboardButton('Аккаунт с играми (10+) | 250р', callback_data='1')
button_origin_item2 = InlineKeyboardButton('Аккаунт с играми (50+) | 500р', callback_data='2')
button_origin_item3 = InlineKeyboardButton('Аккаунт с играми (100+) | 750р', callback_data='3')

button_steam_item1 = InlineKeyboardButton('Аккаунт CS:GO с Prime Status (Silver Elite) | 500р', callback_data='4')
button_steam_item2 = InlineKeyboardButton('Аккаунт CS:GO с Prime Status (BigStar) | 750р', callback_data='5')
button_steam_item3 = InlineKeyboardButton('Аккаунт CS:GO с Prime Status (Global Elite) | 1000р', callback_data='6')


#Клавиатуры:
main_klava = ReplyKeyboardMarkup(resize_keyboard = True).add(button_buy, button_stock).add(button_profile, button_info)
catalog_clava = ReplyKeyboardMarkup(resize_keyboard = True).add(button_steam,button_origin).add(button_back)
info_clava = ReplyKeyboardMarkup(resize_keyboard=True).add(button_back)
markupInline_steam = InlineKeyboardMarkup(row_width=1).add(button_steam_item1, button_steam_item2, button_steam_item3)
markupInline_origin = InlineKeyboardMarkup(row_width=1).add(button_origin_item1, button_origin_item2, button_origin_item3)
markupInline_confirm = InlineKeyboardMarkup(row_width=1).add(button_confirm, button_cancel)

#Переменные:
stock = ['   <b>Origin:</b>\n','Аккаунт с играми (10+) | 250р\n', 'Аккаунт с играми (50+) | 500р\n', 'Аккаунт с играми (100+) | 750р\n', '  <b>Steam:</b>\n', 'Аккаунт CS:GO с Prime Status (Silver Elite) | 500р\n', 'Аккаунт CS:GO с Prime Status (BigStar) | 750р\n', 'Аккаунт CS:GO с Prime Status (Global Elite) | 1000р']


