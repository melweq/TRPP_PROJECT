from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from config import TOKEN

import sqlite3

#Функция подключения к БД
async def db_connect() -> None:
    global conn, cursor
    conn = sqlite3.connect('database.db',)
    cursor = conn.cursor()

#Функция добавления данных в БД
async def db_table_val(user_id: int, user_name: str):
	cursor.execute('INSERT INTO MireaShop (user_id, user_name) VALUES (?, ?)', (user_id, user_name))
	conn.commit()


from keyboards import *

bot = Bot(token=TOKEN, parse_mode='HTML')
dp = Dispatcher(bot)


async def on_startup(_):
    await db_connect()
    print("Подключение к БД выполнено успешно!")




#Обработчики команд
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    #await message.reply("<b>Привет!</b>\nДобро пожаловать в <b>MireaShopBot!</b>", reply_markup=main_klava)

    #Присваиваем переменным ID пользователя и Имя
    us_id = message.from_user.id
    us_name = message.from_user.first_name

    #Проверка существует ли пользователь в БД
    cursor.execute('SELECT * FROM MireaShop WHERE user_id=?', (us_id,))
    if cursor.fetchone() is None:
        # Если пользователя нет в БД
        await message.reply("<b>Привет!</b>\nДобро пожаловать в <b>MireaShopBot!</b>", reply_markup=main_klava)

        await db_table_val(user_id=us_id, user_name=us_name)

    else:
        # Если пользователь есть в БД
        await message.reply("<b>Вы уже зарегистрированы! Приятных покупок</b>", reply_markup=main_klava)



#Обработчики кнопок основного меню:

@dp.message_handler(lambda message: message.text =="Купить 💰")
async def buy(message: types.Message):
    await message.reply("<b>Выберите категорию:</b>", reply_markup = catalog_clava)

@dp.message_handler(lambda message: message.text =="Информация 🤔")
async def info(message: types.Message):
    await message.reply("<b>Создано by:</b> Егор", reply_markup = info_clava)

@dp.message_handler(lambda message: message.text =="Наличие товаров 🛒")
async def stocknal(message: types.Message):
    await message.reply("".join(stock), reply_markup = main_klava)

@dp.message_handler(lambda message: message.text =="Профиль 👤")
async def profile(message: types.Message):
    cursor.execute(f'SELECT balance FROM MireaShop WHERE user_id = {message.from_user.id}') #получаем из БД данные баланса
    getbalance1 = cursor.fetchone()
    getbalance = str(getbalance1).replace(')', '').replace('(', '').replace(',', '') #форматируем
    cursor.execute(f'SELECT sum_buy FROM MireaShop WHERE user_id = {message.from_user.id}') #получаем из БД данные суммы покупок
    getsumbuy1 = cursor.fetchone()
    getsumbuy = str(getsumbuy1).replace(')', '').replace('(', '').replace(',', '') #форматируем
    await message.reply(f"<b>🕶️ Ваш ID:</b> {message.from_user.id}\n<b>💰 Баланс:</b> {getbalance}р\n<b>🛒 Покупок на сумму:</b> {getsumbuy}р", reply_markup = catalog_clava)




#ТЕСТИРУЮ --------------------------------------------------------------------------------------------------------------


    #Проверка достаточно ли баланса у пользователя в БД для покупки аккаунта
    cursor.execute(f'SELECT balance FROM MireaShop WHERE user_id = {message.from_user.id}')
    testbalance = cursor.fetchone()
    cursor.execute(f'SELECT price FROM Products WHERE product_id = 1')
    testprice = cursor.fetchone()

    testbalance = str(testbalance).replace(')', '').replace('(', '').replace(',', '') #форматирование
    testbalance = int(testbalance)
    testprice = str(testprice).replace(')', '').replace('(', '').replace(',', '') #форматирование
    testprice = int(testprice)

    #print(testbalance, testprice)

    if testbalance >= testprice:

        # получаем из БД данные суммы покупок
        cursor.execute(f'SELECT log_pass FROM Products WHERE product_id = 1')
        test1 = cursor.fetchone()

        # форматирование данных для выдачи
        test1 = str(test1).replace(')', '').replace('(', '').replace(',', '').replace("'", '')
        await message.reply(f"Тест:\n{test1} ", reply_markup=catalog_clava)

        #функция для последующего удаления выданного аккаунта из базы данных
        #def delete_product(loginpassword):
            #cursor.execute('DELETE FROM Products WHERE log_pass=?', (loginpassword,))
            #conn.commit()
        #удаление аккаунта
        #delete_product(test1)

        cursor.execute(f'SELECT balance FROM MireaShop WHERE user_id = {message.from_user.id}')
        getbalance2 = cursor.fetchone()
        getbalance2 = str(getbalance2).replace(')', '').replace('(', '').replace(',', '') #форматирование
        getbalance2 = int(getbalance2); getbalance2 -= testprice  #преобразование в INT

        #Обновление данных в таблице пользователей, изменение баланса
        sql_update_query = f"""Update MireaShop set balance = {getbalance2} where user_id = {message.from_user.id}"""
        cursor.execute(sql_update_query)
        conn.commit()

    else:
        await message.reply(f"Тест:\nОшибка! Недостаточно баланса для покупки. ", reply_markup=catalog_clava)






#КОНЕЦ ТЕСТОВОЙ ЧАСТИ --------------------------------------------------------------------------------------------------



@dp.message_handler(lambda message: message.text =="Steam")
async def steam(message: types.Message):
    await message.reply("Выберите товар:", reply_markup = markupInline_steam)

@dp.message_handler(lambda message: message.text =="Origin")
async def origin(message: types.Message):
    await message.reply("<b>Выберите товар:</b>", reply_markup = markupInline_origin)

@dp.message_handler(lambda message: message.text =="Возврат в главное меню")
async def back(message: types.Message):
    await message.reply("<b>Возврат в главное меню!</b>", reply_markup = main_klava)

#Обработчики инлайн кнопок подтверждения покупки

@dp.callback_query_handler(lambda c: c.data == 'yes')
async def process_callback_yes(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,"Вы купили товар!\n\nС вашего баланса списано: 500р")
    await bot.send_message(callback_query.from_user.id, '<b>Данные от аккаунта:</b> login:password')

@dp.callback_query_handler(lambda c: c.data == 'no')
async def process_callback_no(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,"Вы отменили покупку, возврат в главное меню.", reply_markup=main_klava)


#Обработчики кнопок товаров:

@dp.callback_query_handler(lambda c: c.data == '1')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "<b>Для подтверждения покупки, нажмите кнопку ниже:</b>", reply_markup=markupInline_confirm)

@dp.callback_query_handler(lambda c: c.data == '2')
async def process_callback_button2(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "<b>Для подтверждения покупки, нажмите кнопку ниже:</b>", reply_markup=markupInline_confirm)

@dp.callback_query_handler(lambda c: c.data == '3')
async def process_callback_button3(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "<b>Для подтверждения покупки, нажмите кнопку ниже:</b>", reply_markup=markupInline_confirm)

@dp.callback_query_handler(lambda c: c.data == '4')
async def process_callback_button4(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,"<b>Для подтверждения покупки, нажмите кнопку ниже:</b>", reply_markup=markupInline_confirm)


@dp.callback_query_handler(lambda c: c.data == '5')
async def process_callback_button5(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "<b>Для подтверждения покупки, нажмите кнопку ниже:</b>", reply_markup=markupInline_confirm)

@dp.callback_query_handler(lambda c: c.data == '6')
async def process_callback_button6(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "<b>Для подтверждения покупки, нажмите кнопку ниже:</b>", reply_markup=markupInline_confirm)











#Для работы без остановки
if __name__ == '__main__':
    executor.start_polling(dp, on_startup = on_startup)