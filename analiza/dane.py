"""Zliczenie unikatowych klientów dziennie po obróbce danych przez Anie"""

import pymysql, numpy



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

def days_list(company_name):
    """Import danych z SQL i zwrot listy szczegołowych dni vs. ilość klientów"""
    cur = connection()
    statement = "SELECT DATE(FROM_UNIXTIME(starttime/1000)), COUNT(DATE(FROM_UNIXTIME(starttime/1000))) FROM %s \
WHERE doubled = 0 AND age_4>0 GROUP BY DATE(FROM_UNIXTIME(starttime/1000))" %("analytic_data_" + company_name)   #wykluczamy przypadki, gdy track nie zostal jeszcze zweryfikowany (age_4 > 0)
    cur.execute(statement)
    data = cur.fetchall()
    return data

#statement = SELECT DATE(FROM_UNIXTIME(starttime/1000)), COUNT(DATE(FROM_UNIXTIME(starttime/1000))) FROM `analytic_data_komfort` WHERE doubled = 0 AND age_4>0 GROUP BY DATE(FROM_UNIXTIME(starttime/1000))

def weekdays_dict(company_name):
    """Import danych z SQL i stworzenie słownika ostrukturze: dzień tygodnia: ilość klientów"""
    weekdays = {'Monday': [], 'Tuesday': [], 'Wednesday': [], 'Thursday': [], 'Friday': [], 'Saturday': [], 'Sunday': []}
    cur = connection()
    statement = "SELECT DATE_FORMAT(FROM_UNIXTIME(starttime/1000), '%s') as dzien_tygodnia, COUNT(DATE(FROM_UNIXTIME(starttime/1000))) as klienci FROM %s \
WHERE doubled = 0 AND age_4>0 GROUP BY DATE(FROM_UNIXTIME(starttime/1000))" %("%W", "analytic_data_" + company_name)   #wykluczamy przypadki, gdy track nie zostal jeszcze zweryfikowany (age_4 > 0) - otrzymuje po nazwach wszystki edni tygodnia
    cur.execute(statement)
    data = cur.fetchall()
    for i in range(0,len(data)):
        if data[i][0] in weekdays:
            weekdays[data[i][0]].append(data[i][1])
    return weekdays

def weekdays_dict_female(company_name):
    """Import danych z SQL i stworzenie słownika ostrukturze: dzień tygodnia: ilość kobiet"""
    weekdays_female = {'Monday': [], 'Tuesday': [], 'Wednesday': [], 'Thursday': [], 'Friday': [], 'Saturday': [], 'Sunday': []}
    cur = connection()
    statement = "SELECT DATE_FORMAT(FROM_UNIXTIME(starttime/1000), '%s') as dzien_tygodnia, COUNT(IF(gender_4 = 1, 1, NULL)) as kobiety FROM %s \
WHERE doubled = 0 AND age_4>0 GROUP BY DATE(FROM_UNIXTIME(starttime/1000))" %("%W", "analytic_data_" + company_name)   #wykluczamy przypadki, gdy track nie zostal jeszcze zweryfikowany (age_4 > 0) - otrzymuje po nazwach wszystki edni tygodnia
    cur.execute(statement)
    data = cur.fetchall()
    for i in range(0,len(data)):
        if data[i][0] in weekdays_female:
            weekdays_female[data[i][0]].append(data[i][1])
    return weekdays_female

def days_min(company_name):
    """Sprawdzenie 5 najsłabszych wyników"""
    cur = connection()
    statement = "SELECT DATE(FROM_UNIXTIME(starttime/1000)), COUNT(DATE(FROM_UNIXTIME(starttime/1000))) as ilosc, DATE_FORMAT(FROM_UNIXTIME(starttime/1000), '%s') FROM %s \
WHERE doubled = 0 AND age_4>0 GROUP BY DATE(FROM_UNIXTIME(starttime/1000)) ORDER BY ilosc LIMIT 5" %("%W", "analytic_data_" + company_name)
    cur.execute(statement)
    data = cur.fetchall()
    return data

def days_max(company_name):
    """Sprawdzenie 5 najjelpszych wyników"""
    cur = connection()
    statement = "SELECT DATE(FROM_UNIXTIME(starttime/1000)), COUNT(DATE(FROM_UNIXTIME(starttime/1000))) as ilosc, DATE_FORMAT(FROM_UNIXTIME(starttime/1000), '%s') FROM %s \
WHERE doubled = 0 AND age_4>0 GROUP BY DATE(FROM_UNIXTIME(starttime/1000)) ORDER BY ilosc DESC LIMIT 5" %("%W", "analytic_data_" + company_name)
    cur.execute(statement)
    data = cur.fetchall()
    return data

def weather_clients(company_name):
    """Lista zawierają zarówno ilość klientów jak i warunki pogodowe"""
    cur = connection()
    statement = "SELECT pogoda2016.dat AS dat1, pogoda2016.temperatura AS temperatura, pogoda2016.cisnienie AS cisnienie, pogoda2016.opady AS opady, sub.ilosc \
FROM pogoda2016 INNER JOIN ((SELECT DATE(FROM_UNIXTIME(starttime/1000)) as data1, COUNT(DATE(FROM_UNIXTIME(starttime/1000))) as ilosc FROM %s WHERE doubled = 0 AND age_4>0 GROUP BY data1) AS sub) \
ON pogoda2016.dat = sub.data1" %("analytic_data_" + company_name)
    cur.execute(statement)
    data = cur.fetchall()
    return data
