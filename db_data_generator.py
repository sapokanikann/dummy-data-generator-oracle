import cx_Oracle
import string
import random
cx_Oracle.init_oracle_client("D:\instantclient_19_10")

hostname = " "
port = " "
SID = " "

dsn_tns = cx_Oracle.makedsn(hostname, port, SID)
connection = cx_Oracle.connect(
    user=" ",
    password=" ",
    dsn=dsn_tns)

print("Connected to Oracle Database\n")

letters = string.ascii_letters
UPletters = string.ascii_uppercase
LOletters = string.ascii_lowercase
cursor = connection.cursor()
cursor.execute("ALTER SESSION SET NLS_DATE_FORMAT = 'DD/MM/YY'")
insert_f = open('inserts.txt','a')

def random_date():
    random_day=str(random.randint(1,28))
    random_month=str(random.randint(1,12))
    random_year=str(random.randint(10,22))
    date=""+random_day+"/"+ random_month +"/"+ random_year +""
    return date

def random_DOB():
    random_day=str(random.randint(1,28))
    random_month=str(random.randint(1,12))
    random_year=str(random.randint(50,99))
    date=""+random_day+"/"+ random_month +"/"+ random_year +""
    return date

table = int(input('Pick a table: \n 0: ALL TABLES \n 1: Car \n 2: OffenceType \n 3: Rank \n 4: Address \n 5: Criminal \n 6: Police \n 7: Civilian \n 8: IncidentReport \n 9: Dog \n 10: Weapon \n'))
rows_c = int(input('How many rows to generate?\n'))

if table==1 or table==0:
    # Car
    insert_f.write("\n-- CAR\n")
    rows = []
    for i in range(rows_c):
        rows.append(''.join(random.choice(UPletters) for i in range(2)) + str(random.randint(10000,99999)))
    for row in rows:
        qry_car = "INSERT INTO Car VALUES (seq_car.nextval, '{}') \n".format(row)
        cursor.execute(qry_car)
        insert_f.write(qry_car)
    connection.commit()

if table==2 or table==0:
    # OffenceType
    off_cat = ["Felony", "Misdemeanor", "Felony-Misdemeanor", "Infraction"]
    insert_f.write("\n-- OFFENCE TYPE\n")
    rows = []
    for i in range(rows_c):
        rows.append([
        ''.join(random.choice(LOletters) for i in range(random.randint(5,15))), 
        random.choice(off_cat)
        ])
    for row in rows:
        qry_off = "INSERT INTO OffenceType VALUES (seq_off.nextval, '{}', '{}') \n".format(row[0],row[1])
        cursor.execute(qry_off)
        insert_f.write(qry_off)
    connection.commit()

if table==3 or table==0:
    # Rank 
    insert_f.write("\n-- RANK\n")
    rank_title = ["Corporal", "Sergeant", "Lieutenant", "Capitan", "Chief"]
    rows = []
    for i in range(rows_c):
        rows.append([
        random.choice(rank_title), 
        ''.join(str(random.randint(3000,9999))) 
        ])
    for row in rows:
        qry_rank = "INSERT INTO Rank VALUES (seq_rank.nextval, '{}', '{}') \n".format(row[0],row[1])
        cursor.execute(qry_rank)
        insert_f.write(qry_rank)
    connection.commit()

if table==4 or table==0:
    # Address 
    insert_f.write("\n-- ADDRESS\n")
    rows = []
    for i in range(rows_c):
        rows.append([
        ''.join(random.choice(UPletters) for i in range(random.randint(3,20))), 
        ''.join(str(random.randint(10,99)) + '-'+ str(random.randint(100,999))),
        ''.join(random.choice(letters) for i in range(random.randint(3,20))),
        ''.join(str(random.randint(1,100)))
        ])
    for row in rows:
        qry_add = "INSERT INTO Address VALUES (seq_add.nextval, '{}','{}','{}','{}')\n".format(row[0],row[1],row[2],row[3])
        cursor.execute(qry_add)
        insert_f.write(qry_add)
    connection.commit()

if table==5 or table==0:
    # Criminal 
    cursor.execute('select addrID from Address')
    possible_address = cursor.fetchall()
    insert_f.write("\n-- CRIMINAL\n")
    rows = []
    for i in range(rows_c):
        rows.append([
        ''.join(random.choice(LOletters) for i in range(random.randint(3,20))), 
        ''.join(random.choice(UPletters) for i in range(random.randint(3,20))),
        random_DOB(),
        ''.join(str(random.randint(100000000,999999999))),
        ''.join(random.choice(UPletters) for i in range(3)) + str(random.randint(100000,999999)),
        random.choice(possible_address)[0]
        ])
    for row in rows:
        qry_crim = "INSERT INTO Criminal VALUES (seq_crim.nextval, '{}','{}','{}','{}','{}','{}')\n".format(row[0],row[1],row[2],row[3],row[4],row[5])
        cursor.execute(qry_crim)
        insert_f.write(qry_crim)
    connection.commit()

if table==6 or table==0:
    # Police 
    cursor.execute('select rankID from Rank')
    possible_rank = cursor.fetchall()
    cursor.execute('select carID from Car')
    possible_car = cursor.fetchall()
    cursor.execute('select addrID from Address')
    possible_address = cursor.fetchall()
    insert_f.write("\n-- POLICE\n")
    rows = []
    for i in range(rows_c):
        rows.append([
        ''.join(random.choice(LOletters) for i in range(random.randint(3,20))),
        ''.join(random.choice(UPletters) for i in range(random.randint(3,20))),
        random_DOB(),
        ''.join(str(random.randint(100000000,999999999))),
        random.choice(possible_rank)[0],
        random.choice(possible_car)[0],
        random.choice(possible_address)[0]
        ])
    for row in rows:
        qry_pol = "INSERT INTO Police VALUES (seq_pol.nextval, '{}','{}','{}','{}','{}','{}', '{}')\n".format(row[0],row[1],row[2],row[3],row[4],row[5],row[6])
        cursor.execute(qry_pol)
        insert_f.write(qry_pol)
    connection.commit()

if table==7 or table==0:
    # Civilian 
    cursor.execute('select addrID from Address')
    possible_address = cursor.fetchall()
    civ_status = ["Witness", "Victim"]
    insert_f.write("\n-- CIVILIAN\n")
    rows = []
    for i in range(rows_c):
        rows.append([
        ''.join(random.choice(LOletters) for i in range(random.randint(3,20))),
        ''.join(random.choice(UPletters) for i in range(random.randint(3,20))),
        random_DOB(),
        ''.join(str(random.randint(100000000,999999999))),
        random.choice(civ_status),
        random.choice(possible_address)[0]
        ])
    for row in rows:
        qry_civ = "INSERT INTO Civilian VALUES (seq_civ.nextval, '{}','{}','{}','{}','{}', '{}')\n".format(row[0],row[1],row[2],row[3],row[4],row[5])
        cursor.execute(qry_civ)
        insert_f.write(qry_civ)
    connection.commit()

if table==8 or table==0:
    # IncidentReport
    cursor.execute('select polID from Police')
    possible_police = cursor.fetchall()
    cursor.execute('select crimID from Criminal')
    possible_criminal = cursor.fetchall()
    cursor.execute('select offID from OffenceType')
    possible_offence = cursor.fetchall()
    cursor.execute('select civID from Civilian')
    possible_civilian = cursor.fetchall()
    insert_f.write("\n-- INCIDENT REPORT\n")
    rows = []
    for i in range(rows_c):
        rows.append([
        random_date(),
        ''.join(random.choice(letters) for i in range(random.randint(5,40))),
        random.choice(possible_police)[0],
        random.choice(possible_criminal)[0],
        random.choice(possible_offence)[0],
        random.choice(possible_civilian)[0]
        ])
    for row in rows:
        qry_inc = "INSERT INTO IncidentReport VALUES (seq_inc.nextval, '{}','{}','{}','{}','{}', '{}')\n".format(row[0],row[1],row[2],row[3],row[4],row[5])
        cursor.execute(qry_inc)
        insert_f.write(qry_inc)
    connection.commit()

if table==9 or table==0:
    # Dog
    cursor.execute('select polID from Police')
    dog_breed = ["Belgian Malinois", "German Shepherd"]
    possible_police = cursor.fetchall()
    insert_f.write("\n-- DOG\n")
    rows = []
    for i in range(rows_c):
        rows.append([
        ''.join(random.choice(UPletters) for i in range(random.randint(5,10))), 
        random.choice(dog_breed),
        random.choice(possible_police)[0]
        ])
    for row in rows:
        qry_dog = "INSERT INTO Dog VALUES (seq_dog.nextval, '{}', '{}', '{}') \n".format(row[0],row[1],row[2])
        cursor.execute(qry_dog)
        insert_f.write(qry_dog)
    connection.commit()

if table==10 or table==0:
    # Weapon
    cursor.execute('select polID from Police')
    possible_police = cursor.fetchall()
    weap_type = ["Taser", "Gun"]
    insert_f.write("\n-- WEAPON\n")
    rows = []
    for i in range(rows_c):
        rows.append([
        random.choice(weap_type), 
        ''.join(random.choice(letters) for i in range(random.randint(5,20))),
        ''.join(str(random.randint(100000,999999))),
        random.choice(possible_police)[0]
        ])
    for row in rows:
        qry_weap = "INSERT INTO Weapon VALUES (seq_weap.nextval, '{}', '{}', '{}', '{}') \n".format(row[0],row[1],row[2],row[3])
        cursor.execute(qry_weap)
        insert_f.write(qry_weap)
    connection.commit()
print('FINISHED')