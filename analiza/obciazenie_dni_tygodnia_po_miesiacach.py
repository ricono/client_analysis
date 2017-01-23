import pymysql, numpy, dane, numpy

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

def weekdays_dict(company_name, month):
    #funkcje można rozbudować o wybrany rok - celowo nie robię tego
    """Import danych z SQL i stworzenie słownika ostrukturze: dzień tygodnia: ilość klientów"""
    weekdays = {'Monday': [], 'Tuesday': [], 'Wednesday': [], 'Thursday': [], 'Friday': [], 'Saturday': [], 'Sunday': []}
    cur = connection()
    statement = "SELECT DATE_FORMAT(FROM_UNIXTIME(starttime/1000), '%s') as dzien_tygodnia, COUNT(DATE(FROM_UNIXTIME(starttime/1000))) as klienci FROM %s \
WHERE MONTH(FROM_UNIXTIME(starttime/1000)) = '%s' AND doubled = 0 AND age_4>0 GROUP BY DATE(FROM_UNIXTIME(starttime/1000))" %("%W", "analytic_data_" + company_name, month)
    cur.execute(statement)
    data = cur.fetchall()
    for i in range(0,len(data)):
        if data[i][0] in weekdays:
            weekdays[data[i][0]].append(data[i][1])
    return weekdays
#SELECT DATE(FROM_UNIXTIME(starttime/1000)) FROM analytic_data_vox WHERE MONTH(FROM_UNIXTIME(starttime/1000)) = 8

def week_day(company_name, month):
    """Obliczenie średniej ilości odwiedzić dla poszczegolnych dni tygodnia"""
    weekday_qunatity = weekdays_dict(company_name, month)
    weekday_list = [['Monday'], ['Tuesday'], ['Wednesday'], ['Thursday'], ['Friday'], ['Saturday'], ['Sunday']]
    for i in weekday_qunatity:
        if weekday_qunatity[i] != []:
            avg = int(round(numpy.mean(weekday_qunatity[i]),0))
            for j in range(0, len(weekday_list)):
                if i == weekday_list[j][0]:
                    weekday_list[j].append(avg)

    print("\nŚrednia ilość odwiedzin w danym dniu tygodnia dla miesiąca nr", month, ": ")
    for k in range(0, len(weekday_list)):
        try:
            print(weekday_list[k][0], ": \t", weekday_list[k][1])
        except IndexError:
            print(weekday_list[k][0], ": brak danych")
            

def main():
    company_name = str(input("Podaj nazwę firmy do analizy: ")).lower()
    for i in range(1,13):
        week_day(company_name, i)

main()
