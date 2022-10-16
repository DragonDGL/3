import sqlite3
import DatabaseQuery


class DBJobClass:
    db = DatabaseQuery.MainDatabaseQuery()

    queryCreate = "CREATE TABLE job(id integer primary key, summery text)"
    queryUpdateJob = "INSERT INTO job(summery) VALUES('{}')"
    queryGetData = "SELECT summery FROM job ORDER BY id DESC LIMIT 1"
    queryGetID = "SELECT id FROM job ORDER BY id DESC LIMIT 1"
    queryGetAll = "SELECT id, summery FROM job"
    queryDelete = "DELETE FROM job"
    queryCount = "SELECT COUNT(*) FROM job"

    def setData(self, summery):
        query = self.queryUpdateJob.format(summery)
        print(query)
        self.db.queryDB(query)
        return True

    def getData(self):
        query = self.queryGetData
        row = self.db.queryAndAnswerDB(query)
        if (len(row) > 0):
            return "✅ Последний заказ\n\n" + row[0][0]
        return "✅ Заказов нет"

    def getAllData(self):
        query = self.queryGetAll
        row = self.db.queryAndAnswerDB(query)
        if len(row) == 0:
            return "✅ Заказов нет"
        list = "✅ Все заказы ✅\n"
        for item in row:
            list += "\n\n☁️ Заказ #{}\n\n{}\n\n".format(str(item[0]), item[1])
        return list

    def getID(self):
        query = self.queryGetID
        row = self.db.queryAndAnswerDB(query)
        if (len(row) > 0):
            return row[0][0]
        return 0

    def clearData(self):
        row = self.db.queryAndAnswerDB(self.queryCount)
        if not int(row[0][0]) > 0:
            return "⚠️ Нет данных для удаление"
        self.db.queryDB(self.queryDelete)
        return "✅ Данные успешно удаленны."
