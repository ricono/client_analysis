import pymysql, numpy, datetime, time

"""Program sprawdza dla jakich dat zostały poprawnie wprowadzone dane"""

def connection():
    """Połączenie z bazą w pymysql"""
    try:
        mydb = pymysql.connect(user = 'root', password = '', host = '127.0.0.1', db = 'xxx', charset='utf8')
        cur = mydb.cursor()
        return cur
    except pymysql.Error:
        print("There was a problem in connecting to the database.  Please ensure that the 'xxx' database exists on the local host system.")
        raise pymysql.Error
    except pymysql.Warning:
        pass

def import_data(company_name):
    """Import danych z SQL"""
    cur = connection()
    statement = "SELECT DISTINCT starttime FROM %s WHERE age_4 > 0" %("analytic_data_" + company_name)    #wykluczamy przypadki, gdy track nie zostal jeszcze zweryfikowany (age_4 > 0)
    cur.execute(statement)
    data = cur.fetchall()
    print("Dane zostały pobrane\n")
    return data

def main():
    company_name = str(input("Podaj nazwę firmy do analizy: ")).lower()
    full_data = import_data(company_name)
    dates = []
    for i in range(0, len(full_data)):
        x = datetime.date.fromtimestamp((full_data[i][0])/1000)
        if x not in dates:
            dates.append(x)
    for i in range (0, len(dates)):
        print("%s. %s" %(i+1, dates[i]))
    
main()
