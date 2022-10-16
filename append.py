import sqlite3
conn = sqlite3.connect("sqlitedb.db")
query = "SELECT name, area FROM city"
queryInsertArea = "INSERT INTO city(name, area) VALUES('{}', '{}')"
queryAdd  = "INSERT INTO city(name) VALUES('{}')"
queryDeleteNone = "DELETE FROM city WHERE name = None"
queryAddArea = "INSERT INTO area(city, area) VALUES('{}','{}')"
def show():
    cursor = conn.cursor()
    cursor.execute(query)
    row = cursor.fetchall()
    list = ""
    for i in row:
        list += "{} - {}\n".format(i[0],i[1])
    cursor.close()
    return list
def add(city):
    cursor = conn.cursor()
    cursor.execute(queryAdd.format(city))
    cursor.close()
    conn.commit()
def allAdd(city):
    for i in city:
        add(i)
def showCity():
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM city")
    row = cursor.fetchall()
    for i in row:
        print(i[0])
def addArea(city,area):
    cursor = conn.cursor()
    query = queryAddArea.format(city,area)
    cursor.execute(query)
    conn.commit()
def alladdArea(city,areaList):
    for i in arealist:
        addArea(city,i)

clist = ['Санкт-Петербург','Москва','Екатеринбург','Красноярск','Новосибирск','Нижний Новгород']
arealist = ['Автозаводский р-н','Канавинский р-н','Ленинский р-н','Московский р-н',
            'Нижегородский р-н','Приокский р-н','Советский р-н','Сормовский р-н']
alladdArea('Нижний Новгород', arealist)