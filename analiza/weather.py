from urllib.request import urlopen
import json, pymysql
import datetime, time

"""Program zaciąga dane ze strony wunderground.com a następnie ładuje do bazdy danych sql"""

def weathercon(url):
    """Wyciągnięcie ze strony pogodowej danych do sql"""
    address = url
    f = urlopen(address)
#ja wpisałem kod poznańskiego lotniska EPPO, po mieście (q/Poland/Poznan.json)
#przykłady wpisywania miejsc  https://slovak.wunderground.com/weather/api/d/docs?d=data/geolookup&MR=1
#przykłady oznaczeń do zaciągnięcia https://slovak.wunderground.com/weather/api/d/docs?d=data/history

    json_string = f.read().decode('utf8')
    parsed_json = json.loads(json_string)   # na tym etapie odczytuje dane - masę jakiś danych a mnei interesuje tylko dailysummary

    tempm = parsed_json['history']['dailysummary'][0]['meantempm']
    pressurem = parsed_json['history']['dailysummary'][0]['meanpressurem']
    precipm = parsed_json['history']['dailysummary'][0]['precipm']

    print("Dane zostały pobrane: temperatura ", tempm, "stopni", "ciśnienie ", pressurem, "suma opadów ", precipm)

    f.close()
    return tempm, pressurem, precipm

def sql(url, date):
    """Połączenie z SQL, test danych i przesłanie ich na serwer"""
    history_dates_list = []
    try:
        mydb = pymysql.connect(user = 'root', password = '', host = '127.0.0.1', db = 'aegton', charset='utf8')
        cur = mydb.cursor()
    except pymysql.Error:
        print("There was a problem in connecting to the database.  Please ensure that the 'aegton' database exists on the local host system.")
        raise pymysql.Error
    except pymysql.Warning:
        pass
    tempm, pressurem, precipm = weathercon(url)
    statement = "SELECT DATE_FORMAT(dat, '%Y%m%d') FROM pogoda2016"
    cur.execute(statement)
    history_dates = cur.fetchall()
    for i in range(0, len(history_dates)):
        history_dates_list.append(history_dates[i][0])
    if date in history_dates_list:
        print("Dane dla tej daty już istnieją w bazie danych.")
    else:
        cur = mydb.cursor()
        statement = "INSERT INTO pogoda2016 VALUES (STR_TO_DATE('%s', '%s'), %s, %s, %s)" %(date,'%Y%m%d', tempm, pressurem, precipm)
        cur.execute(statement)
        mydb.commit()
        mydb.close()
        print("Dane dla wybranej daty zostały dodane do bazy.")
            
                

def main():
    date = input("Podaj datę za zaimportowania danych w formacie RRRRMMDD: ")
    url = ('http://api.wunderground.com/api/my_key/history_' + '%s' + '/conditions/q/EPPO.json') %(date)
    sql(url, date)

main()

