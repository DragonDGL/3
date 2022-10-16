import logging
import sqlite3
import DatabaseLogicProduct
import DatabaseQuery
import random
import DatabaseLogicJobs
import Main
import DatabaseLogicMarket
import DatabaseLogicStat
import KeybordClass
import DatabaseLogicReferalCode


log = logging.getLogger('DatabaseLogicAdminPanel')


class DBAdminPanelClass:
    db = DatabaseQuery.MainDatabaseQuery()
    NS = KeybordClass.NameSpace()
    dbMain = Main
    queryCreate = "CREATE TABLE admin(id integer, uname text)"
    queryCreateRefAdmin = "CREATE TABLE adminRef(key integer, rights integer)"
    queryCheckAdmin = "SELECT * FROM admin WHERE id = {}"
    queryName = "SELECT uname FROM admin WHERE id = {}"
    queryAddAdmin = "INSERT INTO admin VALUES({},'{}',{})"
    queryRightsRefCode = "SELECT rights FROM adminRef WHERE key = {}"
    queryAdminRefCode = "SELECT key FROM adminRef WHERE key = {}"
    queryCheckAdminRights = "SELECT rights FROM admin WHERE id = {}"
    queryNametoID = "SELECT id FROM admin WHERE uname = '{}'"
    queryAllAdminPush = "SELECT id FROM admin"
    queryInsertAdminRefCode = "INSERT INTO adminRef VALUES({},{})"
    queryCountAdmin = "SELECT * FROM admin"
    queryRightsName = "SELECT rights FROM admin WHERE uname = '{}'"
    queryDelete = "DELETE FROM adminRef"
    queryDeleteAdmin = "DELETE FROM admin WHERE uname = '{}'"
    queryAlready = "SELECT * FROM admin"
    queryCheckName = "SELECT * FROM admin where uname = '{}'"

    def allAdmin(self) -> list[str]:
        '''Возвращает список имен админов.

        Returns:
            list[str]: Списко имён админов.
        '''
        return [i[0] for i in self.db.queryAndAnswerDB('SELECT uname FROM admin')]

    def deleteAdmin(self, admin_id: int, rights: int) -> bool:
        '''Удаляет админа из БД.

        Args:
            admin_id (int): Telegram user_id админа подлежащего удалению.
            rights (int): Уровень доступа удаляющего.

        Returns:
            bool: True или False.
        '''
        log.info(f'Called with args: ({admin_id}, {rights})')
        if rights == 1:
            log.warning('Not enough rights!')
            return False
        self.db.queryDB(f'DELETE FROM admin WHERE id={admin_id}')
        return True

    def listAdmins(self) -> list:
        '''Возвращает список админов.

        Returns:
            list: Списко админов формата: [($id, $uname, $rights),]
        '''
        log.info('Called!')
        res = self.db.queryAndAnswerDB('SELECT * FROM admin')
        log.debug(f'Result: {res}')
        return res

    def isAdmin(self, id):
        query = self.queryCheckAdmin.format(id)
        row = self.db.queryAndAnswerDB(query)
        log.debug(f'Returns: {len(row) > 0}')
        return len(row) > 0
    def isName(self, id):
        query = self.queryName.format(id)
        row = self.db.queryAndAnswerDB(query)
        if(len(row) > 0):
            return row[0][0]
        return False
    def exportDB(self):
        file = open('sqlitedb.db', 'rb')
        return file
    def checkAlready(self):
        query = self.queryAlready
        row = self.db.queryAndAnswerDB(query)
        if(len(row) == 0):
            return True
        return False
    def checkName(self,name):
        try:
            userName = str(name)
        except:
            return False
        query = self.queryCheckName.format(userName)
        row = self.db.queryAndAnswerDB(query)
        return len(row) > 0
    def addDefaultAdmin(self,message):
        id = message.from_user.id
        name = message.chat.username
        query = self.queryAddAdmin.format(id, name, 0)
        self.db.queryDB(query)
    def welcome(self, id):
        if (self.isAdmin(id)):
            return self.NS.ANSWER_ADMIN_WELCOME.format(self.isName(id))

    def stateJoinActivate(self):
        db = DatabaseLogicStat.DBStat()
        answer = db.joinStat()
        return answer

    def stateRefActivate(self):
        db = DatabaseLogicReferalCode.MainDBClass()
        answer = db.countActivate()
        return answer

    def stateAll(self):
        dbProduct = DatabaseLogicProduct.DBProductClass()
        dbJob = DatabaseLogicJobs.DBJobClass()
        dbMarket = DatabaseLogicMarket.DBMarketClass()
        statMarket = dbMarket.countForStat()
        stateJoin = self.stateJoinActivate()
        stateRefActivate = self.stateRefActivate()
        statProduct = dbProduct.countProduct()
        stateCountAdmin = len(self.db.queryAndAnswerDB(self.queryCountAdmin))
        stateJobs = dbJob.getID()
        answer = self.NS.ANSWER_ADMIN_STAT.format(stateCountAdmin, stateJoin, stateRefActivate, stateJobs,statMarket[0],statMarket[1],statProduct)
        return answer
    def checkRights(self,id):
        query = self.queryCheckAdminRights.format(id)
        row = self.db.queryAndAnswerDB(query)
        print(row[0][0])
        return row[0][0]
    def generateCode(self):
        return random.randint(10000,50000)
    def generateAdminRefCode(self, id, rights):
        log.info(f'Called with args: ({id}, {rights})')
        if self.checkRights(id) == 1 and rights == 2:
            code = self.generateCode()
            query = self.queryInsertAdminRefCode.format(code, rights)
            self.db.queryDB(query)
            return "ACTIVATE_CODE {}".format(code)
        if(int(self.checkRights(id)) == 0):
            code = self.generateCode()
            query = self.queryInsertAdminRefCode.format(code, rights)
            self.db.queryDB(query)
            return "ACTIVATE_CODE {}".format(code)
        else:
            return "У вас нет прав на такие вещи :("
    def selfRights(self, id):
        rights = self.checkRights(id)
        if rights == 2:
            return "<b>{}</b> уровень доступа\n\nВам доступно только чтение информации, без изменение.".format(rights)
        elif rights == 1:
            return "<b>{}</b> уровень доступа\n\nВам доступно чтение информации и изменение её. Вы можете добавлять/удалять товар\nИзменять реквизиты\nДобавлять администратора(только 2 уровень)".format(rights)
        elif rights == 0:
            return "<b>{}</b> уровень доступа\n\nВы имеете все права администратора, вам доступен весь функционал.".format(rights)
        else:
            return "Ошибка. Не удалось найти ваши права"
    def isAlreadyAdminRefCode(self,key):
        query = self.queryAdminRefCode.format(key)
        row = self.db.queryAndAnswerDB(query)
        log.debug(f'Returns: {len(row) > 0}')
        return len(row) > 0
    def addAdmin(self,message,key):
        log.info(f'Called with args: ({message}, {key})')
        if(not self.isAlreadyAdminRefCode(key) or self.isAdmin(message.from_user.id)):
            log.warning('User is already ADMIN or used wrong key!')
            return False
        else:
            log.info(f'Adding a new ADMIN #{message.chat.id}')
            queryKey = self.queryRightsRefCode.format(key)
            id = message.from_user.id
            name = message.chat.username
            rights = self.db.queryAndAnswerDB(queryKey)[0][0]
            query = self.queryAddAdmin.format(id, name, rights)
            queryDelete = self.queryDelete
            print(query)
            self.db.queryDB(query)
            self.db.queryDB(queryDelete)
            dbMain = Main
            messagePush = "&#128276; Уведомление. Добавлен новый админ\nИмя <b>{}</b> | Уровень админа <b>{}</b>".format(name, rights)
            dbMain.pushAll(messagePush, True)
            return True
    def adminNametoID(self,keyName):
        query = self.queryNametoID.format(keyName)
        print("query = {}",query)
        row = self.db.queryAndAnswerDB(query)
        print("adminNamtoID return {}",row[0][0])
        if len(row) > 0:
            return row[0][0]
        return "No data"
    def adminList(self):
        log.info('Called!')
        query = self.queryCountAdmin
        row = self.db.queryAndAnswerDB(query)
        list = "\n"
        for i in row:
            list += "Имя {} | Уровень доступа {}\n".format(i[1], i[2])
        log.debug(f'List: {list}')
        return list
    def adminListMinimal(self):
        query = self.queryCountAdmin
        row = self.db.queryAndAnswerDB(query)
        list = []
        print(row)
        for i in row:
            print(i[1])
            list.append(i[1])
        list.append("ОТМЕНА")
        return list
    def nameToRights(self,keyName):
        query = self.queryRightsName.format(keyName)
        row = self.db.queryAndAnswerDB(query)
        if len(row) > 0:
            return row[0][0]
        return "No data"
    def delete(self, message,keyName):
        if not self.checkName(keyName):
            return "Ошибка. Такого админа нет"
        print("keyName = {}".format(keyName))
        yourRights = int(self.checkRights(message.from_user.id))
        deleteUserRights = int(self.nameToRights(keyName))
        id = self.adminNametoID(keyName)
        if(yourRights == 2):
            return self.NS.ANSWER_ERROR
        if(deleteUserRights == 0 and yourRights != 0):
            return self.NS.ANSWER_ERROR
        else:
            query = self.queryDeleteAdmin.format(keyName)
            print(query)
            self.db.queryDB(query)
            dbMain = Main
            messagePush = "Уведомление. Был удален админ\n Админ {} с правами {} был удален.".format(keyName, deleteUserRights)
            dbMain.pushAll(messagePush)
            dbMain.push(id, "&#128125;  ВНИМАНИЕ! Вы остались без админ прав.  &#128125;")
            return "Пользователь {} удален и остался без админ прав.".format(keyName)
    def writeListAdminAll(self):
        list = []
        query = self.queryAllAdminPush
        row = self.db.queryAndAnswerDB(query)
        for item in row:
            list.append(item[0])

        return list

    def onlyAllRights(self):
        return [i[0] for i in self.db.queryAndAnswerDB('SELECT id FROM admin WHERE rights = 0')]
