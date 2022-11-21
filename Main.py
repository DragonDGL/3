# -*- coding: UTF-8 -*-
import logging
import random
import time
import telebot
import requests
import Main
import DatabaseLogicAdminPanel
import DatabaseLogicBuyData
import DatabaseLogicContact
import DatabaseLogicJobs
import DatabaseLogicMarket
import DatabaseLogicProduct
import DatabaseLogicReferalCode
import DatabaseLogicStat
import KeybordClass

YOUR_CODE = '5628829381:AAETGSXiF3K4h4I4gAs0NWRg2jGEHiPPDrs'

logging.basicConfig(
    format='[%(levelname)s] %(name)s (%(lineno)d) >> %(module)s.%(funcName)s: %(message)s',
    level=logging.INFO
)
log = logging.getLogger('Bot')
bot = telebot.TeleBot(YOUR_CODE)
dbProduct = DatabaseLogicProduct.DBProductClass()
kb = KeybordClass.ListKeyBoard()
NS = KeybordClass.NameSpace()
MESSAGE_YOURCODE = '👥 Пригласить друга'
MESSAGE_ENTERCODE = '📝 Ввести код'
MESSAGE_STAT = '📊 Статистика'
MESSAGE_SELFRIGHTS = "Какие у меня права?"
MESSAGE_BUYDATA = '💰 Реквизиты'
MESSAGE_QIWI = 'Изменить QIWI'
MESSAGE_BITCOIN = 'Изименить BTC'
MESSAGE_MAINMENU = "⏮ Главное Меню"
MESSAGE_MENUADMIN = "👽 Меню Админки"
MESSAGE_CONTROLADMIN = '🔑 Управление Админами'
MESSAGE_CITYANDAREA = 'Города и Районы'
MESSAGE_ADDADMIN = 'Добавить Админа'
MESSAGE_DELETEADMIN = 'Удалить Админа'
MESSAGE_JOB = "☘️ Предзаказ | Горячий клад 🔥"
MESSAGE_MARKET = "🏪 Магазин"
MESSAGE_REQUESTJOB = '✅ Заказы'
MESSAGE_SENDJOB = "✉️ Оформить заказ"
MESSAGE_ALLREQUESTJOB = "Все заказы"
MESSAGE_LASTREQUESTJOB = "Последний"
MESSAGE_DELETEJOB = "УДАЛИТЬ ВСЕ"
MESSAGE_SETTING = '🔧 Настройки'
MESSAGE_WORLD = "🌏 Территории"
MESSAGE_CANCEL = "ОТМЕНА"
MESSAGE_CANCEL_S = "❌ Отмена"

dbAdmin = DatabaseLogicAdminPanel.DBAdminPanelClass()
dbMarket = DatabaseLogicMarket.DBMarketClass()
dbContact = DatabaseLogicContact.DBContactClass()
dbBuy = DatabaseLogicBuyData.DBBuyDataClass()
dbJob = DatabaseLogicJobs.DBJobClass()
dbStat = DatabaseLogicStat.DBStat()

def pushSale(msg_sale):
    listIDs = dbStat.listUser()
    if not len(listIDs) > 0:
        return
    answer = "🎁 Скидка {}% на все товары 🎁".format(msg_sale)
    for id in listIDs:
        try:
            bot.send_message(id, answer, reply_markup=kb.KB_SALE_JOIN, parse_mode='html')
        except BaseException:
            continue
def pushWork():
    listIDs = dbStat.listUser()
    if not len(listIDs) > 0:
        return
    for id in listIDs:
        try:
            bot.send_message(id, NS.ANSWER_JOBMESSAGE, parse_mode='html',reply_markup=kb.KB_WORL_JOIN)
        except BaseException:
            continue
def pushProduct():
    listIDs = dbStat.listUser()
    if not len(listIDs) > 0:
        return
    for id in listIDs:
        try:
            bot.send_message(id, "🏢️ Новый товар в твоем районе, чекай 🏃‍♂", parse_mode='html',reply_markup=kb.KB_SALE_JOIN)
        except BaseException:
            continue
def push(id, msg):
    bot.send_message(id, msg, parse_mode='html')


def pushAll(msg,onlyAdmin):
    if onlyAdmin == True:
        id = dbAdmin.onlyAllRights()
    else:
        id = dbAdmin.writeListAdminAll()
    for item in id:
        try:
            push(item, msg)
        except BaseException:
            continue

def show(message):
    db = DatabaseLogicReferalCode.MainDBClass()
    id = message.from_user.id
    code = db.add(id)
    answer = "&#128077; Ваш реферальный код: {}".format(code)
    bot.send_message(message.chat.id, answer, parse_mode='html')
    countActivation(message)


def countActivation(message):
    db = DatabaseLogicReferalCode.MainDBClass()
    id = message.from_user.id
    count = db.showMyRefEnter_ID(id)
    answer = "&#127939;  Кол-во активаций: {}".format(count)
    bot.send_message(message.chat.id, answer, parse_mode='html')


def enter(message):
    global answer
    try:
        msg = int(message.text)
        db = DatabaseLogicReferalCode.MainDBClass()
        answer = db.update(message.from_user.id, msg)
    except ValueError:
        answer = "Допустимы только цифры"
    bot.send_message(message.chat.id, answer, parse_mode='html')




def state(message):
    print("stat activate")
    db = DatabaseLogicAdminPanel.DBAdminPanelClass()
    if not db.isAdmin(message.from_user.id):
        return
    answer = db.stateAll()
    KB = kb.KB_STAT
    KB.add(kb.button_stat_all)
    bot.send_message(message.chat.id, answer, parse_mode='html', reply_markup=KB)


def join(message):
    db = DatabaseLogicStat.DBStat()
    db.join(message.from_user.id)

def add(message):
    db = DatabaseLogicAdminPanel.DBAdminPanelClass()
    if not db.isAdmin(message.from_user.id):
        return
    bot.send_message(message.chat.id, NS.ANSWER_LEVELADMIN, parse_mode='html', reply_markup=kb.KB_CREATEADMIN)
    bot.register_next_step_handler(message, addAdmin)


def requestJob(message):
    msg = message.text
    if message.text == "ОТМЕНА":
        start(message)
        return
    if not msg.count("\n") >= 4:
        bot.send_message(message.chat.id,
                         "&#10060;  Не верно заполненна форма заказа\n\n&#9888;  Кол-во полей меньше требуемого.",
                         parse_mode='html', reply_markup=kb.KB_JOBMENU)
        return
    dbJob = DatabaseLogicJobs.DBJobClass()
    print("Вносимые данные : {}".format(message.text))
    dbJob.setData(message.text)
    id = dbJob.getID()
    pushAll(
        "&#128276;  Мамонтёнок <b>#{}</b> ждёт установки бивней!".format(id),False)
    bot.send_message(message.chat.id, "&#128193; Заказ в обработке\n&#128193; ID заказа {}".format(id),
                     parse_mode='html', reply_markup=kb.KB_DEFAULT)


def start(message):
    db = DatabaseLogicAdminPanel.DBAdminPanelClass()
    if (db.isAdmin(message.from_user.id)):
        bot.send_message(message.chat.id, NS.ANSWER_WELCOM, parse_mode='html',
                         reply_markup=kb.KB_DEFAULTANDADRMIN)
    else:
        bot.send_message(message.chat.id, NS.ANSWER_WELCOM, parse_mode='html',
                         reply_markup=kb.KB_DEFAULT)


def generateNumberBuy():
    return random.randint(10000, 100000)


def editContact(contact):
    if contact.text == "ОТМЕНА":
        bot.send_message(contact.chat.id, "&#9989Отмена", parse_mode='html', reply_markup=kb.KB_DELETE)
        bot.send_message(contact.chat.id, "&#9989 Успешная отмена смены контакта", parse_mode='html',
                         reply_markup=kb.KB_SETTING)
        return
    dbContact = DatabaseLogicContact.DBContactClass()
    dbContact.add(contact.text)
    contactNew = dbContact.show()
    answer = "Контакт обновлен. Новый контакт: {}".format(contactNew)
    bot.send_message(contact.chat.id, "&#9989 Успешно", parse_mode='html', reply_markup=kb.KB_DELETE)
    bot.send_message(contact.chat.id, answer, parse_mode='html', reply_markup=kb.KB_SETTING)


def addCityAsk(message, call):
    if message.text == "❌ Отмена":
        answer = "✅ Отмена"
    elif not dbMarket.isAlreadyCityCheck(message.text):
        answer = "⚠️ Такой город уже есть"
    else:
        answer = dbMarket.addCity(message.text)
    bot.send_message(message.chat.id, answer, parse_mode='html', reply_markup=kb.KB_DELETE)
    bot.send_message(call.message.chat.id, "🌏 Раздел Территории", reply_markup=kb.KB_CITYCONTROL)


def addAreaAsk(message, infoCity, call):
    answer = "⚠️ Ошибка."
    if message.text == "❌ Отмена":
        answer = "✅ Отмена"
    else:
        if '\n' in message.text:
            answer = dbMarket.addAreaList(infoCity, message.text)
            dbProduct.randomProductForNull()
        if not '\n' in message.text:
            answer = dbMarket.addArea(infoCity, message.text)
            dbProduct.randomProductForNull()
    bot.send_message(message.chat.id, answer, parse_mode='html', reply_markup=kb.KB_DELETE)
    bot.send_message(message.chat.id, "🌏 Раздел Территории", reply_markup=kb.KB_CITYCONTROL)


def editBitcoin(call, calldelete):
    answer = dbBuy.updateBitcoin(call, call.text)
    bot.send_message(call.chat.id, answer, parse_mode='html')
    KB = telebot.types.InlineKeyboardMarkup()
    KB.add(kb.button_edit_qiwi)
    KB.add(kb.button_edit_bitcoin)
    KB.add(kb.button_menu_admin)
    bot.delete_message(calldelete.message.chat.id, calldelete.message.message_id)
    bot.send_message(call.chat.id, dbBuy.allDataBuy(), reply_markup=KB, parse_mode='html')
    pushAll("🔔 Реквизиты Bitcoin были обновленны", False)

def editQiwi(call, calldelete):
    try:
        answer = dbBuy.updateQiwi(call, call.text)
    except TypeError:
        answer = "⚠️ Ошибка. Попробуйте еще раз"
    bot.send_message(call.chat.id, answer, parse_mode='html')
    KB = telebot.types.InlineKeyboardMarkup()
    KB.add(kb.button_edit_qiwi)
    KB.add(kb.button_edit_bitcoin)
    KB.add(kb.button_menu_admin)
    bot.delete_message(calldelete.message.chat.id, calldelete.message.message_id)
    bot.send_message(call.chat.id, dbBuy.allDataBuy(), reply_markup=KB, parse_mode='html')
    pushAll("🔔 Реквизиты Qiwi были обновленны",False)


def editContact(call, calldelete):
    bot.delete_message(calldelete.message.chat.id, calldelete.message.message_id)
    answer = dbContact.add(call.text)
    bot.send_message(call.chat.id, answer, parse_mode='html')
    answer = dbContact.show()
    KB = telebot.types.InlineKeyboardMarkup()
    KB.add(kb.kb_setting_back, kb.button_edit_contact)
    bot.send_message(call.chat.id, answer, reply_markup=KB)
def addAdmin(message):
    log.info(f'Called with arg: ({message})')
    if dbAdmin.isAdmin(message.from_user.id):
        log.warning('Current user already is ADMIN!')
        return False
    key = message.text.replace('ACTIVATE_CODE','')
    log.debug(f'ACTIVATE_CODE: {key}')
    if not len(key) > 0:
        log.warning('Admin activation code has 0 length!')
        return False
    if dbAdmin.addAdmin(message,key):
        log.info('Added a new ADMIN.')
        bot.send_message(message.chat.id,"✅ Успешно.",reply_markup=kb.KB_ADMIN)
        pushAll("🔔 Новый администратор",False)
def btcpay(message,data):
    if not 'Я оплатил'  in message.text:
        bot.send_message(message.chat.id,"❌ Оплата не потверждена, создайте новый запрос на подверждение ")
    else:
        bot.send_message(message.chat.id,"✅ Оплата в обработке, ожидайте")
        cost = dbProduct.productInfoForBuy(data[1])[1]
        pushAll("✅ Подтверждение оплаты\n🔔 Кто-то оплатил заказ на сумму <b>{}</b>₽\n🌨 Способ оплаты: <b>BitCoin</b>".format(
            cost
        ), True)
def pay(message,data):
    if not 'Я оплатил'  in message.text:
        bot.send_message(message.chat.id,"❌ Оплата не потверждена, создайте новый запрос на подверждение ")
    else:
        bot.send_message(message.chat.id,"✅ Оплата в обработке, ожидайте")
        cost = dbProduct.productInfoForBuy(data[1])[1]
        pushAll("✅ Подтверждение оплаты\n🔔 Кто-то оплатил заказ на сумму <b>{}</b>₽\n🌨 Способ оплаты: <b>💳 Банковская карта</b>".format(
            round (cost*1.1)
        ), True)
def sendJob(message):
    bot.send_message(message.chat.id, NS.ANSWER_REQUESTJOB, parse_mode='html', reply_markup=kb.KB_JOBCANCEL)
    bot.register_next_step_handler(message, requestJob)
def converBtc(rub):
    url = "https://blockchain.info/ticker"
    curs = requests.get(url).json()['RUB']['last']
    return format(rub/curs,'8f')
@bot.message_handler(commands=['start'])
def start_message(message):
    start(message)
    join(message)
    return


@bot.message_handler(content_types=['text'])
def send_text(message):
    if (message.text == MESSAGE_YOURCODE):
        show(message)
    elif (message.text == MESSAGE_ENTERCODE):
        bot.send_message(message.chat.id, NS.ANSWER_ENTERREFCODE, parse_mode='html')
        bot.register_next_step_handler(message, enter)
    elif (message.text == MESSAGE_MAINMENU):
        start_message(message)
    elif ("ACTIVATE_CODE" in message.text):
        addAdmin(message)
        return
    elif message.text == MESSAGE_JOB:
        bot.send_message(message.chat.id, NS.ANSWER_JOBMESSAGE, reply_markup=kb.KB_JOBMENU, parse_mode='html')
    elif message.text == MESSAGE_SENDJOB:
        sendJob(message)
    elif (message.text == MESSAGE_MARKET):
        KB_CITY = kb.createCity(False)
        bot.send_message(message.chat.id, NS.ANSWER_STARTMARKET, reply_markup=KB_CITY, parse_mode='html')
    elif message.text == "ACTIVATE_ADMIN":
        dbAdmin = DatabaseLogicAdminPanel.DBAdminPanelClass()
        if dbAdmin.checkAlready():
            dbAdmin.addDefaultAdmin(message)
            bot.send_message(message.chat.id, "&#10004;  Код успешно активирован.Вы теперь администратор",
                             reply_markup=kb.KB_ADMIN, parse_mode='html')
    elif message.text == MESSAGE_MENUADMIN:
        dbAdmin = DatabaseLogicAdminPanel.DBAdminPanelClass()
        if not dbAdmin.isAdmin(message.from_user.id):
            return
        bot.send_message(message.chat.id, "👽 Вы в разделе Администрирование", reply_markup=kb.KB_ADMIN)


@bot.callback_query_handler(func=lambda call: call.data in 'main_menu')
def menu(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    bot.send_message(call.message.chat.id, "⏮ Главное меню", reply_markup=kb.KB_DEFAULTANDADRMIN)

@bot.callback_query_handler(func=lambda call: call.data in 'admin_menu')
def admin_menu(call):
    bot.answer_callback_query(call.id)
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=kb.KB_ADMIN,
        text="👽 Вы в разделе Администрирование"
    )
@bot.callback_query_handler(func=lambda call: call.data in 'join_market')
def joinMarket(call):
    KB_CITY = kb.createCity(False)
    bot.edit_message_text(
        message_id=call.message.message_id,
        chat_id=call.message.chat.id,
        text=NS.ANSWER_STARTMARKET,
        reply_markup=KB_CITY,
        parse_mode='html'
    )
@bot.callback_query_handler(func=lambda call: call.data in 'job_join')
def workJoin(call):
    bot.answer_callback_query(call.id)
    sendJob(call.message)
@bot.callback_query_handler(func=lambda call: call.data in 'close')
def close(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)
@bot.callback_query_handler(func=lambda call: call.data in 'push_product')
def PushProduct(call):
    print("activate pushProduct")
    KB = kb.KB_SALE
    answer = "✅ Рассылка пользователям бот"
    pushProduct()
    bot.answer_callback_query(call.id)
    if answer == call.message.text:
        return
    bot.edit_message_text(
        message_id=call.message.message_id,
        chat_id=call.message.chat.id,
        text=answer,
        reply_markup=KB
    )
@bot.callback_query_handler(func=lambda call: call.data in 'push_work')
def workPush(call):
    bot.answer_callback_query(call.id)
    if not dbAdmin.isAdmin(call.message.chat.id):
        return
    if dbAdmin.checkRights(call.message.chat.id) == 2:
        bot.answer_callback_query(call.id, NS.ANSWER_ERROR)
    pushWork()
    answer = "✅ Рассылка пользователям бот"
    if answer == call.message.text:
        return
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=answer,
        reply_markup=kb.KB_SALE
    )
@bot.callback_query_handler(func=lambda call: call.data in 'sale_data')
def sale_data(call):
    if not dbAdmin.isAdmin(call.message.chat.id):
        return
    if dbAdmin.checkRights(call.message.chat.id) == 2:
        bot.answer_callback_query(call.id,NS.ANSWER_ERROR)
        return
    bot.answer_callback_query(call.id)
    bot.edit_message_reply_markup(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=kb.KB_SALE
    )
@bot.callback_query_handler(func=lambda call: call.data in ['control_admin', 'admin_info_data','all_admin'])
def controlAdmin(call):
    log.info('Called!')
    if not dbAdmin.isAdmin(call.message.chat.id):
        return
    bot.answer_callback_query(call.id)
    KB = kb.KB_CONTROL_ADMIN
    if call.data in 'control_admin':
        bot.edit_message_reply_markup(
            message_id=call.message.message_id,
            chat_id=call.message.chat.id,
            reply_markup=KB
        )
    elif call.data in 'all_admin':
        admins = dbAdmin.allAdmin()
        answer = '\n'.join(admins)
        if not admins:
            return
        bot.edit_message_text(
            message_id=call.message.message_id,
            chat_id=call.message.chat.id,
            text=answer,
            reply_markup=KB
        )
    else:
        answer = dbAdmin.selfRights(call.message.chat.id)
        if answer.replace('\n', '') == call.message.text.replace('\n', ''):
            return
        bot.edit_message_text(
            message_id=call.message.message_id,
            chat_id=call.message.chat.id,
            reply_markup=KB,
            text=answer
        )


@bot.callback_query_handler(func=lambda call: call.data in ['admin_add_admin'])
def stepAddAdmin(call):
    log.info('Called!')
    if not dbAdmin.isAdmin(call.message.chat.id):
        log.warning(f'User #{call.message.chat.id} is not ADMIN!')
        return
    if dbAdmin.checkRights(call.message.chat.id) == 2:
        log.warning(f'Admin #{call.message.chat.id} is trying add a new ADMIN!')
        bot.answer_callback_query(call.id, NS.ANSWER_ERROR)
        return
    bot.answer_callback_query(call.id)
    KB = kb.createAddAdmin(dbAdmin.checkRights(call.message.chat.id))
    bot.edit_message_reply_markup(
        reply_markup=KB,
        message_id=call.message.message_id,
        chat_id=call.message.chat.id
    )

@bot.callback_query_handler(func=lambda call: call.data in ['admin_delete_data'])
def delAdmin(call):
    log.info('Called!')
    if not dbAdmin.isAdmin(call.message.chat.id):
        log.warning(f'User #{call.message.chat.id} is not ADMIN!')
        return
    if dbAdmin.checkRights(call.message.chat.id) == 2:
        log.warning(f'Admin #{call.message.chat.id} trying delete ADMIN without rights!')
        bot.answer_callback_query(call.id, NS.ANSWER_ERROR)
        return
    bot.answer_callback_query(call.id)
    KB = kb.createAdminDelete(dbAdmin.checkRights(call.message.chat.id))
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=KB,
        text="Выберите администратора"
    )


@bot.callback_query_handler(func=lambda call: 'deladmin' in call.data)
def deleteAdmin(call):
    log.info(f'Called with call: {call}')
    if not dbAdmin.isAdmin(call.message.chat.id):
        return
    if dbAdmin.checkRights(call.message.chat.id) == 2:
        bot.answer_callback_query(call.id, NS.ANSWER_ERROR)
        return
    bot.answer_callback_query(call.id)
    rights = dbAdmin.checkRights(call.data.replace('deladmin', ''))
    answer = dbAdmin.deleteAdmin(call.message.chat.id, call.data.replace('deladmin', ''))
    if answer:
        pushAll("🔔 Удален админстратор с правами {}".format(rights), False)
        push(call.data.replace('deladmin', ''), "🔔 Вы остались без прав администратора.")
    if not dbAdmin.isAdmin(call.message.chat.id):
        bot.delete_message(call.message.chat.id, call.message.message_id)
        return
    KB = kb.createAdminDelete(rights)
    bot.edit_message_reply_markup(
        message_id=call.message.message_id,
        chat_id=call.message.chat.id,
        reply_markup=KB
    )

@bot.callback_query_handler(func=lambda call: 'sale' in call.data)
def sale(call):
    if not dbAdmin.isAdmin(call.message.chat.id):
        return
    if dbAdmin.checkRights(call.message.chat.id) == 2:
        bot.answer_callback_query(call.id,NS.ANSWER_ERROR)
        return
    bot.answer_callback_query(call.id)
    KB = kb.KB_SALE
    if not dbProduct.countProduct() > 0:
        answer = "⚠️ Нет товаров.\nℹ️ Зайдите в раздел Настройки"
    else:
        dbProduct.sale(call.data.replace('sale_',''))
        pushSale(call.data.replace('sale_',''))
        answer = "✅ Скидка 10% на все товары\n✅ Рассылка пользователям бота"
    if answer.replace('\n','') == call.message.text.replace('\n',''):
        return
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=answer,
        reply_markup=KB
    )
@bot.callback_query_handler(func=lambda call: call.data in ['buy_data', 'edit_qiwi', 'edit_bitcoin'])
def buy(call):
    if not dbAdmin.isAdmin(call.message.chat.id):
        return
    print("activate buy")
    if call.data in 'buy_data':
        bot.answer_callback_query(call.id)
        answer = dbBuy.allDataBuy()
        KB = telebot.types.InlineKeyboardMarkup()
        KB.add(kb.button_edit_qiwi)
        KB.add(kb.button_edit_bitcoin)
        KB.row(kb.button_menu_admin)
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=KB,
            text=answer,
            parse_mode='html'
        )
    elif call.data in 'edit_qiwi':
        if dbAdmin.checkRights(call.message.chat.id) == 2:
            bot.answer_callback_query(call.id, NS.ANSWER_ERROR)
            return
        bot.answer_callback_query(call.id)
        bot.edit_message_text(
            message_id=call.message.message_id,
            chat_id=call.message.chat.id,
            text="✍️ Введите новые данные для QIWI\n\n⚠️ Никнейм либо ссылка на оплату(вместе с https ://)"
        )
        bot.register_next_step_handler(call.message, editQiwi, call)
    elif call.data in 'edit_bitcoin':
        if dbAdmin.checkRights(call.message.chat.id) == 2:
            bot.answer_callback_query(call.id, NS.ANSWER_ERROR)
            return
        bot.answer_callback_query(call.id)
        bot.edit_message_text(
            message_id=call.message.message_id,
            chat_id=call.message.chat.id,
            text="✍️ Введите новые данные для Bitcoin\n\n⚠️ Полный адрес для оплаты"
        )
        bot.register_next_step_handler(call.message, editBitcoin, call)


@bot.callback_query_handler(func=lambda call: call.data in ['order_data', 'order_all', 'order_last', 'order_delete'])
def order(call):
    if not dbAdmin.isAdmin(call.message.chat.id):
        return
    KB = telebot.types.InlineKeyboardMarkup()
    KB.row(kb.kb_button_order_all, kb.kb_button_order_last)
    KB.add(kb.kb_button_order_delete)
    KB.add(kb.button_menu_admin)
    if call.data in 'order_data':
        bot.answer_callback_query(call.id)
        answer = "✅ Раздел Заказы"
        KB = telebot.types.InlineKeyboardMarkup()
        KB.row(kb.kb_button_order_all, kb.kb_button_order_last)
        KB.add(kb.kb_button_order_delete)
        KB.add(kb.button_menu_admin)
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=answer,
            reply_markup=KB)
        return
    elif call.data in 'order_all':
        bot.answer_callback_query(call.id)
        answer = dbJob.getAllData()
        if answer.replace('\n', '') == call.message.text.replace('\n', ''):
            return
        KB = telebot.types.InlineKeyboardMarkup()
        KB.row(kb.kb_button_order_all, kb.kb_button_order_last)
        KB.add(kb.kb_button_order_delete)
        KB.add(kb.button_menu_admin)
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=answer,
            parse_mode='html',
            reply_markup=KB)
        return
    elif call.data in 'order_last':
        bot.answer_callback_query(call.id)
        answer = dbJob.getData()
        if answer.replace('\n', '') == call.message.text.replace('\n', ''):
            return
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=answer,
            parse_mode='html',
            reply_markup=KB)
        return
    elif call.data in 'order_delete':
        if dbAdmin.checkRights(call.message.chat.id) == 2:
            bot.answer_callback_query(call.id, NS.ANSWER_ERROR)
            return
        bot.answer_callback_query(call.id)
        answer = dbJob.clearData()
        print(answer)
        if answer == call.message.text:
            return
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=answer,
            reply_markup=KB,
            parse_mode='html'
        )
        return


@bot.callback_query_handler(func=lambda call: call.data in 'delete_product_data')
def deleteProductData(call):
    if not dbAdmin.isAdmin(call.message.chat.id):
        return
    bot.answer_callback_query(call.id, "⚠️ После удаление нажмите Закрепить Товар !")
    KB = kb.createProductDelete()
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=KB,
        parse_mode='html',
        text="⚠️ После удаление товара нажмите на кнопку <b>Закрепить Товары</b>"
    )


@bot.callback_query_handler(func=lambda call: '/delete_product' in call.data)
def deleteProduct(call):
    if not dbAdmin.isAdmin(call.message.chat.id):
        return
    if dbAdmin.checkRights(call.message.chat.id) == 2:
        bot.answer_callback_query(call.id, NS.ANSWER_ERROR)
        return
    bot.answer_callback_query(call.id)
    dbProduct.productDelete(call.data.replace('/delete_product', ''))
    KB = kb.createProductDelete()
    bot.edit_message_reply_markup(
        message_id=call.message.message_id,
        chat_id=call.message.chat.id,
        reply_markup=KB
    )


@bot.callback_query_handler(func=lambda call: call.data in ['stat_data', 'stat_all'])
def stat(call):
    if not dbAdmin.isAdmin(call.message.chat.id):
        return
    bot.answer_callback_query(call.id)
    if call.data in 'stat_data':
        answer = dbAdmin.stateAll()
        KB = telebot.types.InlineKeyboardMarkup()
        KB.row(kb.button_menu_admin, kb.button_stat_all)
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=KB,
            parse_mode='html',
            text=answer
        )
    else:
        answer = dbMarket.statisticMarket()
        KB = telebot.types.InlineKeyboardMarkup()
        KB.add(kb.button_stat_default)
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=KB,
            parse_mode='html',
            text=answer
        )


@bot.callback_query_handler(func=lambda call: call.data in ['contact', 'edit_contact'])
def contact(call):
    if not dbAdmin.isAdmin(call.message.chat.id):
        return
    if call.data in 'contact':
        bot.answer_callback_query(call.id)
        answer = dbContact.show()
        KB = telebot.types.InlineKeyboardMarkup()
        KB.add(kb.kb_setting_back, kb.button_edit_contact)
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=KB,
            text=answer,
            parse_mode='html'
        )
    elif call.data in 'edit_contact':
        if dbAdmin.checkRights(call.message.chat.id) == 2:
            bot.answer_callback_query(call.id, NS.ANSWER_ERROR)
            return
        bot.answer_callback_query(call.id)
        bot.edit_message_text(
            message_id=call.message.message_id,
            chat_id=call.message.chat.id,
            text="✍️ Введите <b>новый</b> адрес оператора",
            parse_mode='html'
        )
        bot.register_next_step_handler(call.message, editContact, call)


@bot.callback_query_handler(func=lambda call: call.data in 'setting_data')
def setting(call):
    if not dbAdmin.isAdmin(call.message.chat.id):
        return
    bot.answer_callback_query(call.id)
    bot.edit_message_text(
        message_id=call.message.message_id,
        chat_id=call.message.chat.id,
        parse_mode='html',
        reply_markup=kb.KB_SETTING,
        text="🔧 Раздел Настройки"
    )


@bot.callback_query_handler(func=lambda call: '/city' in call.data)
def stepArea(call):
    dbMarket = DatabaseLogicMarket.DBMarketClass()
    cityName = call.data.replace('/city', '')
    if not dbMarket.isAlreadyCity(cityName):
        return
    KB_AREA = kb.createArea(cityName)
    answer = "🏙 Город: <b>{}</b>\n\n🏣 Выберите район".format(cityName)
    bot.answer_callback_query(call.id)
    bot.edit_message_text(
        message_id=call.message.message_id,
        chat_id=call.message.chat.id,
        text=answer,
        parse_mode='html',
        reply_markup=KB_AREA
    )


@bot.callback_query_handler(func=lambda call: 'addadmin' in call.data)
def addAdminRef(call):
    log.info(f'Called with data: {call.data}')
    bot.answer_callback_query(call.id)
    if not dbAdmin.isAdmin(call.message.chat.id):
        log.warning('User #{call.message.chat.id} is not ADMIN!')
        return
    answer = str(dbAdmin.generateAdminRefCode(call.message.chat.id, call.data.replace('addadmin', '')))
    log.debug(f'Answer: {answer}')
    if answer:
        pushAll("🔔 Сгенерированно приглашение для нового администратора", False)
        bot.send_message(call.message.chat.id, answer)

@bot.callback_query_handler(func=lambda call: '/next' in call.data)
def stepCity(call):
    next = call.data.replace('/next', '')
    if next == "one":
        KB = kb.createCity(True)
    else:
        KB = kb.createCity(False)
    bot.answer_callback_query(call.id)
    bot.edit_message_text(message_id=call.message.message_id,
                          chat_id=call.message.chat.id,
                          reply_markup=KB,
                          parse_mode='html',
                          text=NS.ANSWER_STARTMARKET)


@bot.callback_query_handler(func=lambda call: '/area' in call.data)
def stepProduct(call):
    areaID = call.data.replace('/area', '')
    KB = kb.createProduct(areaID)
    info = dbMarket.getInfoArea(areaID)
    answer = "🏙 <b>{}</b>.\n🏣 <b>{}</b>.".format(info[0], info[1])
    bot.answer_callback_query(call.id)
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=answer,
        reply_markup=KB,
        parse_mode='html'
    )


@bot.callback_query_handler(func=lambda call: '/product_back' in call.data)
def backArea(call):
    call.data = call.data.replace('/product_back', '/city')
    stepArea(call)


@bot.callback_query_handler(func=lambda call: '/sell' in call.data)
def sellProduct(call):
    bot.answer_callback_query(call.id)
    areaId = call.data.replace('/sell', '').split('|')[0]
    productId = call.data.replace('/sell', '').split('|')[1]
    print("areaId = {} | productId = {}".format(areaId, productId))
    KB = kb.createBuy(areaId, productId)
    bot.send_message(call.message.chat.id, "Выберите способ оплаты", reply_markup=KB)

@bot.callback_query_handler(func=lambda call: 'sendbtcpay' in call.data)
def sendbtcpay(call):
    bot.send_message(call.message.chat.id, "✍️ Чтобы подтвердить оплату:\nотправьте боту сообщение (Я оплатил)", parse_mode='html')
    bot.register_next_step_handler(call.message,btcpay,call.data.replace('sendbtcpay','').split('|'))
    
@bot.callback_query_handler(func=lambda call: 'sendpay' in call.data)
def sendpay(call):
    bot.send_message(call.message.chat.id, "✍️ Чтобы подтвердить оплату:\nотправьте боту сообщение (Я оплатил)", parse_mode='html')
    bot.register_next_step_handler(call.message,pay,call.data.replace('sendpay','').split('|'))

@bot.callback_query_handler(func=lambda call: '/bitcoin' in call.data)
def buyBitcoin(call):
    bot.answer_callback_query(call.id)
    orderId = generateNumberBuy()
    idProduct = call.data.replace('/bitcoin', '').split('|')[1]
    idArea = call.data.replace('/bitcoin', '').split('|')[0]
    pushAll("🔔 Создан заказ. Способ оплаты: <b>BitCoin</b>\n💰 Ожидаемая сумма: {} btc\n🌿 Товар: {}\n🗺️ idArea: {}\n⚡️ orderId: {}".format(
        converBtc(dbProduct.productInfoForBuy(idProduct)[1]), dbProduct.productInfoForBuy(idProduct)[0],  idArea, orderId
    ), False)
    dbMarket.addCashCity(idProduct, idArea)
    KB = kb.createBuyBitcoin(idArea, idProduct, orderId)

    allInfoProduct = dbProduct.productInfoForBuy(idProduct)
    costToBitcoin = converBtc(allInfoProduct[1])
    NameAndWeight = allInfoProduct[0]
    answer = "📄Order #{}\n🕑 Статус: Ожидание оплаты\n\n📥 Bitcoin адрес: {}\n💰 К оплате: <b>{} btc</b>\n📦 Товар: <b>{}</b>\n\n📥 Оплата через: <b>BitCoin</b>\n\n\n✅ После оплаты в разделе <b>Координаты Клада</b> будут GPS координаты с фото. Если оплата не прошла либо в разделе <b>координаты</b> нет фото - обратитесь к оператору {}".format(
        orderId, dbBuy.bitcoinData(), costToBitcoin, NameAndWeight, dbContact.show()
    )
    if answer.replace('<b>', '').replace('</b>', '').replace('\n', '') == call.message.text.replace('<b>', '').replace(
            '</b>', '').replace('\n', ''):
        return
    bot.edit_message_text(
        message_id=call.message.message_id,
        chat_id=call.message.chat.id,
        text=answer,
        reply_markup=KB,
        parse_mode='html'
    )

@bot.callback_query_handler(func=lambda call: '/infobitcoin' in call.data)
def infoBtc(call):
    bot.answer_callback_query(call.id)
    idArea = call.data.replace('/infobitcoin','').split('|')[0]
    idProduct = call.data.replace('/infobitcoin','').split('|')[1]
    orderId = call.data.replace('/infobitcoin','').split('|')[2]
    KB = kb.createBuyBitcoin(idArea, idProduct, orderId)

    allInfoProduct = dbProduct.productInfoForBuy(idProduct)
    costToBitcoin = converBtc(allInfoProduct[1])
    NameAndWeight = allInfoProduct[0]
    answer = "📄Order #{}\n🕑 Статус: Ожидание оплаты\n\n📥 Bitcoin адрес: <b>{}</b>\n💰 К оплате: <b>{} btc</b>\n📦 Товар: <b>{}</b>\n\n📥 Оплата через: <b>BitCoin</b>\n\n\n✅ После оплаты в разделе <b>Координаты Клада</b> будут GPS координаты с фото. Если оплата не прошла либо в разделе <b>координаты</b> нет фото - обратитесь к оператору {}".format(
        orderId, dbBuy.bitcoinData(), costToBitcoin, NameAndWeight, dbContact.show()
    )
    if answer.replace('<b>', '').replace('</b>', '').replace('\n', '') == call.message.text.replace('<b>', '').replace(
            '</b>', '').replace('\n', ''):
        return
    bot.edit_message_text(
        message_id=call.message.message_id,
        chat_id=call.message.chat.id,
        text=answer,
        reply_markup=KB,
        parse_mode='html'
    )
@bot.callback_query_handler(func=lambda call: '/geobitcoin' in call.data)
def geoBtc(call):
    bot.answer_callback_query(call.id)
    idArea = call.data.replace('/geobitcoin','').split('|')[0]
    idProduct = call.data.replace('/geobitcoin','').split('|')[1]
    orderId = call.data.replace('/geobitcoin','').split('|')[2]
    KB = kb.createBuyBitcoin(idArea, idProduct, orderId)

    city = dbMarket.getInfoArea(idArea)[0]
    area = dbMarket.getInfoArea(idArea)[1]
    NameAndWeight = dbProduct.productInfoForBuy(idProduct)[0]
    answer = "📄Order #{}\n🕑 Статус:  <b>Ожидает оплаты</b>\n\n\n📦 Товар: <b>{}</b>.\n\n🏙 Город: <b>{}</b>.\n🏣 Район: <b>{}</b>.\n🌐 GPS координаты: <b>Нет данных.</b>\n📷 Фотография: <b>Нет данных.</b>".format(
        orderId, NameAndWeight, city, area
    )
    if answer.replace('<b>', '').replace('</b>', '').replace('\n', '') == call.message.text.replace('<b>', '').replace(
            '</b>', '').replace('\n', ''):
        return
    bot.edit_message_text(
        message_id=call.message.message_id,
        chat_id=call.message.chat.id,
        text=answer,
        reply_markup=KB,
        parse_mode='html'
    )

@bot.callback_query_handler(func=lambda call: '/qiwi' in call.data)
def qiwi(call):
    info = call.data.replace('/qiwi', '').split('|')
    dbMarket.addCashCity(info[1], info[0])
    orderId = generateNumberBuy()
    idArea = call.data.replace('/qiwi', '').split('|')[0]
    idProduct = call.data.replace('/qiwi', '').split('|')[1]
    NameAndWeight = dbProduct.productInfoForBuy(idProduct)[0]
    cost = dbProduct.productInfoForBuy(idProduct)[1]
    pushAll("🔔 Создан заказ. Способ оплаты:\n<b>💳 Банковская карта</b>\n💰 Ожидаемая сумма: {}₽\n🌿 Товар: {}\n🗺️ idArea: {}\n⚡️ orderId: {}".format(
        round (cost*1.1), NameAndWeight, idArea, orderId
    ),False)
    KB = kb.createBuyQiwi(idArea, idProduct, orderId)
    contact = dbContact.show()                           
    # if orderId%2==0:
    #     answer = "📄Order #{}\n\n📦 Товар: <b>{}</b>\n💰 К оплате: <b>{}₽</b>\n\n📥 Оплата через: <b>💳 Банковскую карту</b>\n4890494789061991 карта&#128179;\n79771170841 киви&#129373;\n\n&#10071; ОПЛАТА ДОЛЖНА ПРОХОДИТЬ ОДНИМ ПЛАТЕЖОМ\n&#10071; ВЫДАННЫЕ РЕКВИЗИТЫ ДЕЙСТВУЮТ 60 МИНУТ\n&#10071; ВЫ ПОТЕРЯЕТЕ ДЕНЬГИ, ЕСЛИ ОПЛАТИТЕ ПОЗЖЕ\n&#10069; Цена с учетом части комиссии плат.системы\n\n✅ После оплаты в разделе <b>Координаты Клада</b> будут GPS координаты с фото. Если оплата не прошла либо в разделе <b>координаты</b> нет фото - обратитесь к оператору {}".format(
    #         orderId, NameAndWeight, round (cost*1.1), contact)
    # else:
    #     answer = "📄Order #{}\n\n📦 Товар: <b>{}</b>\n💰 К оплате: <b>{}₽</b>\n\n📥 Оплата через: <b>💳 Банковскую карту</b>\n4890494753026749 карта&#128179;\n79066489114 киви&#129373;\n\n&#10071; ОПЛАТА ДОЛЖНА ПРОХОДИТЬ ОДНИМ ПЛАТЕЖОМ\n&#10071; ВЫДАННЫЕ РЕКВИЗИТЫ ДЕЙСТВУЮТ 60 МИНУТ\n&#10071; ВЫ ПОТЕРЯЕТЕ ДЕНЬГИ, ЕСЛИ ОПЛАТИТЕ ПОЗЖЕ\n&#10069; Цена с учетом части комиссии плат.системы\n\n✅ После оплаты в разделе <b>Координаты Клада</b> будут GPS координаты с фото. Если оплата не прошла либо в разделе <b>координаты</b> нет фото - обратитесь к оператору {}".format(
    #         orderId, NameAndWeight, round (cost*1.1), contact)
    answer = "📄Order #{}\n\n📦 Товар: <b>{}</b>\n💰 К оплате: <b>{}₽</b>\n\n📥 Оплата через: <b>💳 Банковскую карту</b>\n4890494789061991 карта&#128179;\n79771170841 киви&#129373;\n\n&#10071; ОПЛАТА ДОЛЖНА ПРОХОДИТЬ ОДНИМ ПЛАТЕЖОМ\n&#10071; ВЫДАННЫЕ РЕКВИЗИТЫ ДЕЙСТВУЮТ 60 МИНУТ\n&#10071; ВЫ ПОТЕРЯЕТЕ ДЕНЬГИ, ЕСЛИ ОПЛАТИТЕ ПОЗЖЕ\n&#10069; Цена с учетом части комиссии плат.системы\n\n✅ После оплаты в разделе <b>Координаты Клада</b> будут GPS координаты с фото. Если оплата не прошла либо в разделе <b>координаты</b> нет фото - обратитесь к оператору {}".format(
            orderId, NameAndWeight, round (cost*1.1), contact)
    bot.answer_callback_query(call.id)
    print(answer)
    print(call.message.text)
    if answer.replace('<b>', '').replace('</b>', '').replace('\n', '') == call.message.text.replace('<b>', '').replace(
            '</b>', '').replace('\n', ''):
        return
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=KB,
        parse_mode='html',
        text=answer
    )


@bot.callback_query_handler(func=lambda call: '/info' in call.data)
def orderInfo(call):
    info = call.data.replace('/info', '').split('|')
    KB = kb.createBuyQiwi(info[0], info[1], info[2])
    print("orderInfo = {}".format(info))
    order = info[2]
    product = dbProduct.productInfoForBuy(info[1])
    contact = dbContact.show()
    if product == 0:
        productInfo = "Нет данных."
        cost = "Нет данных."
    else:
        productInfo = product[0]
        cost = product[1]
    answer = "📄Order #{}\n\n📦 Товар: <b>{}</b>\n💰 К оплате: <b>{}₽</b>\n\n📥 Оплата через: <b>💳 Банковскую карту</b>\n4890494789061991 карта&#128179;\n79771170841 киви&#129373;\n\n&#10071; ОПЛАТА ДОЛЖНА ПРОХОДИТЬ ОДНИМ ПЛАТЕЖОМ\n&#10071; ВЫДАННЫЕ РЕКВИЗИТЫ ДЕЙСТВУЮТ 60 МИНУТ\n&#10071; ВЫ ПОТЕРЯЕТЕ ДЕНЬГИ, ЕСЛИ ОПЛАТИТЕ ПОЗЖЕ\n&#10069; Цена с учетом части комиссии плат.системы\n\n✅ После оплаты в разделе <b>Координаты Клада</b> будут GPS координаты с фото. Если оплата не прошла либо в разделе <b>координаты</b> нет фото - обратитесь к оператору {}".format(
        order, productInfo, round (cost*1.1), contact
    )
    bot.answer_callback_query(call.id)
    if answer.replace('<b>','').replace('</b>','').replace('\n','') == call.message.text.replace('<b>','').replace('</b>','').replace('\n',''):
        return
    bot.edit_message_text(
        message_id=call.message.message_id,
        chat_id=call.message.chat.id,
        text=answer,
        parse_mode='html',
        reply_markup=KB
    )
@bot.callback_query_handler(func=lambda call: '/geo' in call.data)
def geo(call):
    info = call.data.replace('/geo', '').split('|')
    print("geo = {}".format(info))
    order = info[2]
    KB = kb.createBuyQiwi(info[0], info[1], info[2])
    city = dbMarket.getInfoArea(info[0])[0]
    area = dbMarket.getInfoArea(info[0])[1]
    answer = "📄Order #{}\n🕑 Статус: <b>Ожидает оплаты</b>\n\n\n🏙 Город: <b>{}</b>.\n🏣 Район: <b>{}</b>.\n🌐 GPS координаты: <b>Нет данных.</b>\n📷 Фотография: <b>Нет данных.</b>".format(
        order, city, area
    )
    bot.answer_callback_query(call.id)
    if answer.replace('<b>','').replace('</b>','').replace('\n','') == call.message.text.replace('<b>','').replace('</b>','').replace('\n',''):
        return
    bot.edit_message_text(
        message_id=call.message.message_id,
        chat_id=call.message.chat.id,
        text=answer,
        parse_mode='html', reply_markup=KB
    )


@bot.callback_query_handler(func=lambda call: call.data in 'stat_all')
def statAll(call):
    if not dbAdmin.isAdmin(call.message.chat.id):
        return
    answer = str(dbMarket.statisticMarket())
    KB = telebot.types.InlineKeyboardMarkup()
    KB.add(kb.button_stat_default)
    bot.edit_message_text(
        message_id=call.message.message_id,
        chat_id=call.message.chat.id,
        text="{}".format(answer),
        reply_markup=KB,
        parse_mode='html'
    )
    bot.answer_callback_query(call.id)


@bot.callback_query_handler(func=lambda call: call.data in 'stat_default')
def statDefault(call):
    if not dbAdmin.isAdmin(call.message.chat.id):
        return
    answer = str(dbAdmin.stateAll())
    KB = telebot.types.InlineKeyboardMarkup()
    KB.add(kb.button_stat_all)
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=KB,
        text="{}".format(answer),
        parse_mode='html'
    )
    bot.answer_callback_query(call.id)


@bot.callback_query_handler(func=lambda call: call.data in 'add_product')
def addProduct(call):
    bot.answer_callback_query(call.id)
    if not dbAdmin.isAdmin(call.message.chat.id):
        return
    KB = kb.KB_CATEGORY_ADD
    answer = "💵 Выберите желаемую ценновую категорию товара\n\n⚠️После добавление новых товаров старые будут уничтоженны."
    bot.edit_message_text(
        message_id=call.message.message_id,
        chat_id=call.message.chat.id,
        reply_markup=KB,
        text=answer,
        parse_mode='html'
    )


@bot.callback_query_handler(func=lambda call: call.data in 'cancel_pay')
def cancel_pay(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)


@bot.callback_query_handler(func=lambda call: call.data in 'random_product')
def randomProduct(call):
    if not dbAdmin.isAdmin(call.message.chat.id):
        return
    if dbAdmin.checkRights(call.message.chat.id) == 2:
        bot.answer_callback_query(call.id, NS.ANSWER_ERROR)
        return
    bot.answer_callback_query(call.id)
    answer = dbProduct.randomProduct()
    if answer == call.message.text:
        return
    KB = kb.KB_SETTING
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=KB,
        text=answer,
        parse_mode='html'
    )


@bot.callback_query_handler(func=lambda call: call.data in 'random_product_last')
def randomProduct(call):
    if not dbAdmin.isAdmin(call.message.chat.id):
        return
    if dbAdmin.checkRights(call.message.chat.id) == 2:
        bot.answer_callback_query(call.id, NS.ANSWER_ERROR)
        return
    bot.answer_callback_query(call.id)
    answer = dbProduct.randomProduct()
    if answer == call.message.text:
        return
    KB = kb.KB_SETTING
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=KB,
        text=answer,
        parse_mode='html'
    )


@bot.callback_query_handler(func=lambda call: 'cost_c' in call.data)
def addNewProduct(call):
    if not dbAdmin.isAdmin(call.message.chat.id):
        return
    if dbAdmin.checkRights(call.message.chat.id) == 2:
        bot.answer_callback_query(call.id, NS.ANSWER_ERROR)
        return
    category = call.data.replace('cost_c', '')
    answerAdd = dbProduct.addProducts(category)
    bot.answer_callback_query(call.id, "⚠️ Нажмите  Закрепить Товар !")
    if not answerAdd:
        answer = "❗️Что то пошло не так..."
    else:
        answer = "✅ Добавленны новые товары, обновите список для просмотра.\n\n⚠️ Нажмите на Закрепить Товары если вас устраивает новые изменение, в противном случае новые товары не будут видны в магазине"
    bot.edit_message_text(
        message_id=call.message.message_id,
        chat_id=call.message.chat.id,
        reply_markup=kb.KB_SETTING,
        parse_mode='html',
        text=answer
    )


@bot.callback_query_handler(func=lambda call: call.data in 'setting_back')
def setting_back(call):
    if not dbAdmin.isAdmin(call.message.chat.id):
        return
    answer = "&#128221;  Вы в разделе настройки товаров  &#128221;"
    KB = kb.KB_SETTING
    bot.answer_callback_query(call.id)
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=KB,
        text=answer,
        parse_mode='html'
    )


@bot.callback_query_handler(func=lambda call: call.data in 'list_product')
def listProduct(call):
    if not dbAdmin.isAdmin(call.message.chat.id):
        return
    bot.answer_callback_query(call.id)
    if not dbProduct.isAlready():
        answer = "⚠️ Нет товаров. Загрузите товары через меню бота."
    else:
        answer = dbProduct.productAll()
    if answer.replace('\n', '') == call.message.text.replace('\n', ''):
        return
    bot.edit_message_text(
        message_id=call.message.message_id,
        chat_id=call.message.chat.id,
        text=answer,
        reply_markup=kb.KB_SETTING,
        parse_mode='html'
    )


@bot.callback_query_handler(func=lambda call: call.data in 'world_data')
def worldData(call):
    bot.answer_callback_query(call.id)
    if not dbAdmin.isAdmin(call.message.chat.id):
        return
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=kb.KB_CITYCONTROL,
        text="🌏 Раздел Территории"
    )


@bot.callback_query_handler(func=lambda call: call.data in 'deletearea')
def deleteArea(call):
    if not dbAdmin.isAdmin(call.message.chat.id):
        return
    if dbAdmin.checkRights(call.message.chat.id) == 2:
        bot.answer_callback_query(call.id, NS.ANSWER_ERROR)
        return
    bot.answer_callback_query(call.id)
    KB = kb.createCityForDeleteArea()
    answer = "🌁 Выберите город для которого хотите удалить район"
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=KB,
        text=answer
    )


@bot.callback_query_handler(func=lambda call: call.data in 'deletecity')
def deleteCity(call):
    dbAdmin = DatabaseLogicAdminPanel.DBAdminPanelClass()
    if not dbAdmin.isAdmin(call.message.chat.id):
        return
    if dbAdmin.checkRights(call.message.chat.id) == 2:
        bot.answer_callback_query(call.id, NS.ANSWER_ERROR)
        return
    bot.answer_callback_query(call.id)
    KB = kb.createCityDelete()
    bot.edit_message_reply_markup(
        message_id=call.message.message_id,
        chat_id=call.message.chat.id,
        reply_markup=KB
    )


@bot.callback_query_handler(func=lambda call: call.data in 'addcity')
def addCity(call):
    dbAdmin = DatabaseLogicAdminPanel.DBAdminPanelClass()
    if not dbAdmin.isAdmin(call.message.chat.id):
        return
    if dbAdmin.checkRights(call.message.chat.id) == 2:
        bot.answer_callback_query(call.id, NS.ANSWER_ERROR)
        return
    bot.answer_callback_query(call.id)
    answer = "🏙 Ведите название города\n\n" \
             "📌 Правила:\n\n❗✏️ Нельзя добавлять города который <b>уже есть в списке</b>\n" \
             "⚠️ Название города должно начинается с <b>Б</b>ольшой буквы."
    bot.delete_message(call.message.chat.id, call.message.message_id)
    bot.send_message(call.message.chat.id, answer, parse_mode='html', reply_markup=kb.kb_all_cancel)
    bot.register_next_step_handler(call.message, addCityAsk, call)


@bot.callback_query_handler(func=lambda call: call.data in 'addarea')
def addArea(call):
    dbAdmin = DatabaseLogicAdminPanel.DBAdminPanelClass()
    if not dbAdmin.isAdmin(call.message.chat.id):
        return
    if dbAdmin.checkRights(call.message.chat.id) == 2:
        bot.answer_callback_query(call.id,NS.ANSWER_ERROR)
        return
    answer = "📜 Выберите город для которого хотите добавить новый районы"
    KB = kb.createCityEdit()
    bot.answer_callback_query(call.id)
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=answer,
        reply_markup=KB
    )

@bot.callback_query_handler(func=lambda call: call.data in 'allworld')
def allworld(call):
    bot.answer_callback_query(call.id)
    if not dbAdmin.isAdmin(call.message.chat.id):
        return
    answer = dbMarket.listAll()
    KB = kb.KB_CITYCONTROL
    if call.message.text.replace('\n', '') == answer.replace('\n', ''):
        return
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=KB,
        text=answer
    )


@bot.callback_query_handler(func=lambda call: '/ac' in call.data)
def addArea(call):
    bot.answer_callback_query(call.id)
    bot.delete_message(call.message.chat.id, call.message.message_id)
    cityName = call.data.replace('/ac', '')
    answer = "🏙 Город: <b>{}</b>\nВведите районы для этого города\nМаксимальное кол-во районов: <b>12</b>\n\n".format(
        cityName
    )
    answer_help = "⚠️ Если вы добавляете <b>больше</b> 1 района за раз то каждый новый район вводится с новой строки\n" \
                  "📌 Пример:\n\nЦентральный район\nАдмиралтейский район\nКрасносельский район"

    bot.send_message(call.message.chat.id, answer + answer_help, reply_markup=kb.kb_all_cancel, parse_mode='html')
    bot.register_next_step_handler(call.message, addAreaAsk, cityName, call)


@bot.callback_query_handler(func=lambda call: '/cda' in call.data)
def deleteArea(call):
    bot.answer_callback_query(call.id)
    nameCity = call.data.replace('/cda', '')
    KB = kb.createAreaDelete(nameCity)
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=KB,
        text="🏙 Выберите район"
    )


@bot.callback_query_handler(func=lambda call: '/da' in call.data)
def deleteAreaIndex(call):
    bot.answer_callback_query(call.id)
    info = call.data.replace('/da', '').split('|')
    cityName = dbMarket.getNameCity(info[1])
    areaName = info[0]
    dbMarket.deleteArea(cityName, areaName)
    KB = kb.createAreaDelete(cityName)
    bot.edit_message_reply_markup(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=KB
    )


@bot.callback_query_handler(func=lambda call: '/dc' in call.data)
def deleteCity(call):
    dbMarket = DatabaseLogicMarket.DBMarketClass()
    cityName = call.data.replace('/dc', '')
    dbMarket.deleteCity(cityName)
    KB = kb.createCityDelete()
    answer = "🌁 Выберите город который хотите удалить"
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=answer,
        parse_mode='html',
        reply_markup=KB
    )


@bot.callback_query_handler(func=lambda call: call.data == "close_world")
def back(call):
    KB = kb.KB_CITYCONTROL
    answer = MESSAGE_WORLD
    bot.delete_message(call.message.chat.id, call.message.message_id)


@bot.callback_query_handler(func=lambda call: call.data == 'editcontact')
def queryEditContact(call):
    dbAdmin = DatabaseLogicAdminPanel.DBAdminPanelClass()
    if dbAdmin.checkRights(call.message.chat.id) == 2:
        bot.send_message(call.message.chat.id, NS.ANSWER_ERROR)
        return
    bot.send_message(call.message.chat.id, NS.ANSWER_EDITCONTACT, parse_mode='html', reply_markup=kb.KB_JOBCANCEL)
    bot.register_next_step_handler(call.message, editContact)


@bot.callback_query_handler(func=lambda call: call.data == 'contact')
def queryContact(call):
    print("ACTIVATE contact")
    dbAdmin = DatabaseLogicAdminPanel.DBAdminPanelClass()
    print("{}".format(call.message.from_user.id))
    if not dbAdmin.isAdmin(call.message.chat.id):
        return
    print("continue")
    dbContact = DatabaseLogicContact.DBContactClass()
    contact = dbContact.show()
    answer = "&#128221; Конаткы оператора: {}".format(contact)
    bot.send_message(call.message.chat.id, answer, parse_mode='html', reply_markup=kb.KB_SETTING)


@bot.callback_query_handler(func=lambda call: call.data in 'export')
def queryExport_ask(call):
    dbAdmin = DatabaseLogicAdminPanel.DBAdminPanelClass()
    if not dbAdmin.isAdmin(call.message.chat.id):
        return
    if dbAdmin.checkRights(call.message.chat.id) == 2:
        bot.answer_callback_query(call.id,NS.ANSWER_ERROR)
        return
    bot.answer_callback_query(call.id)
    file = dbAdmin.exportDB()
    bot.send_document(call.message.chat.id, file)


while True:
    try:
        bot.polling()
    except:
        time.sleep(15)
