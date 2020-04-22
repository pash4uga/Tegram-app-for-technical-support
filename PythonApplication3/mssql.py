import pyodbc

server = '192.168.27.149' 
database = 'telebot' 
username = 'sa' 
password = '358355' 

try:
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = cnxn.cursor()
    #cnxn.autocommit = True
except pyodbc.Error as err:
    print("Error: ", err)


def create():
    try:
       cursor.execute('create table inn (RV rowversion, user_id int not null, inn varchar(255) not null);')
       cursor.execute('create table adress (RV rowversion, user_id int not null, adress varchar(255) not null);')
       cursor.execute('create table users (RV rowversion, user_id int not null, phone varchar(255) not null, name varchar(255) not null);')
       cursor.commit()
    except pyodbc.Error as err:
        print("Error: ", err)
        pass

def insert(user_id, name, phone, inn, adress):
    try:
        cursor.execute(""" 
        UPDATE inn 
        SET inn.inn = """+inn+"""   
        WHERE inn.user_id = '"""+str(user_id)+"""' AND inn.inn = '"""+inn+"""'
        IF @@ROWCOUNT = 0
            INSERT INTO inn (inn.user_id, inn.inn) 
            VALUES ('"""+str(user_id)+"""', '"""+inn+"""')
        """)
    except pyodbc.Error as err:
        print("Error: ", err)
    else:
       cursor.commit()
    try:
        cursor.execute(""" 
        UPDATE adress WITH (serializable) 
        SET adress.adress = '"""+adress+"""'    
        WHERE adress.user_id = '"""+str(user_id)+"""' AND adress.adress = '"""+adress+"""'
        IF @@ROWCOUNT = 0
            INSERT INTO adress (adress.user_id, adress.adress) 
            VALUES ('"""+str(user_id)+"""', '"""+adress+"""')
        """)
    except pyodbc.Error as err:
        print("Error: ", err)
    else:
       cursor.commit()
    try:
        cursor.execute(""" 
        UPDATE users WITH (serializable) 
        SET users.name = '"""+name+"""', users.phone = '"""+phone+"""'    
        WHERE users.user_id = '"""+str(user_id)+"""' AND users.name = '"""+name+"""' AND users.phone = '"""+phone+"""'
        IF @@ROWCOUNT = 0
            INSERT INTO users (users.user_id, users.name, users.phone) 
            VALUES ('"""+str(user_id)+"""', '"""+name+"""', '"""+phone+"""')
        """)
    except pyodbc.Error as err:
        print("Error: ", err)
        cursor.rollback()
    else:
       cursor.commit()

def select_last_user(user_id):
    cursor.execute("""
        SELECT TOP 1 *
        FROM users
        JOIN inn
        ON users.user_id=inn.user_id
        JOIN adress
        ON users.user_id=adress.user_id
        WHERE users.user_id = """+str(user_id)+"""
        ORDER BY users.rv DESC, inn.rv DESC, adress.rv DESC
    """)

    rows = cursor.fetchall()
    return rows

def select_user(user_id):
    cursor.execute("SELECT name, phone FROM users WHERE user_id = '"+str(user_id)+"'")
    rows = cursor.fetchall()
    return rows

def select_inn(user_id):
    cursor.execute("SELECT inn FROM inn WHERE user_id = '"+str(user_id)+"'")
    rows = cursor.fetchall()
    return rows

def select_adress(user_id):
    cursor.execute("SELECT adress FROM adress WHERE user_id = '"+str(user_id)+"'")
    rows = cursor.fetchall()
    return rows

def del_user(user_id, name, phone):
    try:
        cursor.execute("DELETE FROM users WHERE user_id = "+str(user_id)+" AND name = '"+str(name)+"' AND phone = '"+str(phone)+"'")
    except pyodbc.Error as err:
        print("Error: ", err)
        cursor.rollback()
    else:
       cursor.commit()

def del_inn(user_id, inn):
    try:
        cursor.execute("DELETE FROM inn WHERE user_id = "+str(user_id)+" AND inn = '"+str(inn)+"'")
    except pyodbc.Error as err:
        print("Error: ", err)
        cursor.rollback()
    else:
        cursor.commit()

def del_adress(user_id, adress):
    try:
        cursor.execute("DELETE FROM adress WHERE user_id = "+str(user_id)+" AND adress = '"+str(adress)+"'")
    except pyodbc.Error as err:
        print("Error: ", err)
        cursor.rollback()
    else:
       cursor.commit()
