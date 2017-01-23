import pymysql, numpy, datetime, time

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

def calender():
    """Konwersja daty pod SQL w formacie UNIX"""
    print("\nData poczatkowa: ")
    year_start = int(input("Podaj rok: "))
    month_start = int(input("Podaj miesiąc: "))
    day_start = int(input("Podaj dzień: "))
    date_start = datetime.date(year_start, month_start, day_start)
    print("\nData końcowa: ")
    year_end = int(input("Podaj rok: "))
    month_end = int(input("Podaj miesiąc: "))
    day_end = int(input("Podaj dzień: "))
    date_end = datetime.date(year_end, month_end, day_end)
    unix_start = (time.mktime(date_start.timetuple()))*1000
    unix_end = (time.mktime(date_end.timetuple()))*1000
    if unix_start <= unix_end:
        return unix_start, unix_end

def import_data(company_name):
    """Import danych z SQL"""
    cur = connection()
    start, end = calender()
    statement = "SELECT gender, age, gender_4, age_4 FROM %s WHERE age_4 > 0 AND starttime >= %s AND starttime <= %s" %("analytic_data_" + company_name, start, end)    #wykluczamy przypadki, gdy track nie zostal jeszcze zweryfikowany (age_4 > 0)
    cur.execute(statement)
    data = cur.fetchall()
    print("Dane zostały pobrane\n")
    return data

def diff(full_data):
    """Przekształcenie danych na mniejszą listę zawierającą różnice w wieku między typem Ani a algorytmem"""
    age_diff = []
    for i in range(0,len(full_data)):
        age_diff.append((full_data[i][3], full_data[i][3]-full_data[i][1], full_data[i][1]))
    return age_diff

def gender_tab(full_data):
    """Przekształcenie danych na listę do analizy płci"""
    gender_list = []
    for i in range(0,len(full_data)):
        gender_list.append((full_data[i][0], full_data[i][2]))
    return gender_list
        
def global_stat(age_stat):
    diff = []
    for i in range(0, len(age_stat)):
        diff.append((age_stat[i][1]))    
    print("Średnia różnica w wieku: ", round(numpy.mean(diff),2))
    print("Odchylenie standardowe różnic wieku: ", round(numpy.std(diff),2))

def group_stat(age_stat):
    """Podstawowe stytystyki dla analizy wieku"""
    diff_0_17, diff_18_24, diff_25_34, diff_35_44, diff_45_54, diff_55_64, diff_65 = [], [], [], [], [], [], [] #pełne listy przyporządkownia przez Anie(Ania podaje prawidłowy wiek) przedziały z google adwords
    algorithm_0_17, algorithm_18_24, algorithm_25_34, algorithm_35_44, algorithm_45_54, algorithm_55_64, algorithm_65 = [], [], [], [], [], [], [] #tylko te przyporządkowania algorytmu, które pokrywają się z grupą Ania
    for i in range(0, len(age_stat)):
        if age_stat[i][0] > 0 and age_stat[i][0] <=17:
            diff_0_17.append((age_stat[i][1]))
        elif age_stat[i][0] > 17 and age_stat[i][0] <=24:
            diff_18_24.append((age_stat[i][1]))
        elif age_stat[i][0] > 24 and age_stat[i][0] <=34:
            diff_25_34.append((age_stat[i][1]))
        elif age_stat[i][0] > 34 and age_stat[i][0] <=44:
            diff_35_44.append((age_stat[i][1]))
        elif age_stat[i][0] > 44 and age_stat[i][0] <=54:
            diff_45_54.append((age_stat[i][1]))
        elif age_stat[i][0] > 54 and age_stat[i][0] <=64:
            diff_55_64.append((age_stat[i][1]))
        elif age_stat[i][0] > 64:
            diff_65.append((age_stat[i][1]))
    for i in range(0, len(age_stat)):
        if age_stat[i][0] > 0 and age_stat[i][0] <=17 and age_stat[i][2] > 0 and age_stat[i][2]<=17:
            algorithm_0_17.append((age_stat[i][2]))
        elif age_stat[i][0] > 17 and age_stat[i][0] <=24 and age_stat[i][2] > 17 and age_stat[i][2]<=24:
            algorithm_18_24.append((age_stat[i][2]))
        elif age_stat[i][0] > 24 and age_stat[i][0] <=34 and age_stat[i][2] > 24 and age_stat[i][2]<=34:
            algorithm_25_34.append((age_stat[i][2]))
        elif age_stat[i][0] > 34 and age_stat[i][0] <=44 and age_stat[i][2] > 34 and age_stat[i][2]<=44:
            algorithm_35_44.append((age_stat[i][2]))
        elif age_stat[i][0] > 44 and age_stat[i][0] <=54 and age_stat[i][2] > 44 and age_stat[i][2]<=54:
            algorithm_45_54.append((age_stat[i][2]))
        elif age_stat[i][0] > 54 and age_stat[i][0] <=64 and age_stat[i][2] > 54 and age_stat[i][2]<=64:
            algorithm_55_64.append((age_stat[i][2]))
        elif age_stat[i][0] > 64 and age_stat[i][2] > 64:
            algorithm_65.append((age_stat[i][2]))
    diff_all = diff_0_17 + diff_18_24 + diff_25_34 + diff_35_44 + diff_45_54 + diff_55_64 + diff_65
    algorithm_all = algorithm_0_17 + algorithm_18_24 + algorithm_25_34 + algorithm_35_44 + algorithm_45_54 + algorithm_55_64 + algorithm_65
    print("Liczebność grupy 0-17: ", len(diff_0_17), "\tŚrednia różnica wieku w grupie: ", round(numpy.mean(diff_0_17),2), \
          "\tOdchylenie standardowe różnic wieku w grupie: ", round(numpy.std(diff_0_17),2), "\tPoprawność algorytmu dla grupy: ", round(len(algorithm_0_17)/len(diff_0_17)*100,2),"%")
    print("Liczebność grupy 18-24: ", len(diff_18_24), "\tŚrednia różnica wieku w grupie: ", round(numpy.mean(diff_18_24),2), \
          "\tOdchylenie standardowe różnic wieku w grupie: ", round(numpy.std(diff_18_24),2), "\tPoprawność algorytmu dla grupy: ", round(len(algorithm_18_24)/len(diff_18_24)*100,2),"%")
    print("Liczebność grupy 25-34: ", len(diff_25_34), "\tŚrednia różnica wieku w grupie: ", round(numpy.mean(diff_25_34),2), \
          "\tOdchylenie standardowe różnic wieku w grupie: ", round(numpy.std(diff_25_34),2), "\tPoprawność algorytmu dla grupy: ", round(len(algorithm_25_34)/len(diff_25_34)*100,2),"%")
    print("Liczebność grupy 35-44: ", len(diff_35_44), "\tŚrednia różnica wieku w grupie: ", round(numpy.mean(diff_35_44),2), \
          "\tOdchylenie standardowe różnic wieku w grupie: ", round(numpy.std(diff_35_44),2), "\tPoprawność algorytmu dla grupy: ", round(len(algorithm_35_44)/len(diff_35_44)*100,2),"%")
    print("Liczebność grupy 45-54: ", len(diff_45_54), "\tŚrednia różnica wieku w grupie: ", round(numpy.mean(diff_45_54),2), \
          "\tOdchylenie standardowe różnic wieku w grupie: ", round(numpy.std(diff_45_54),2), "\tPoprawność algorytmu dla grupy: ", round(len(algorithm_45_54)/len(diff_45_54)*100,2),"%")
    print("Liczebność grupy 55-64: ", len(diff_55_64), "\tŚrednia różnica wieku w grupie: ", round(numpy.mean(diff_55_64),2), \
          "\tOdchylenie standardowe różnic wieku w grupie: ", round(numpy.std(diff_55_64),2), "\tPoprawność algorytmu dla grupy: ", round(len(algorithm_55_64)/len(diff_55_64)*100,2),"%")
    print("Liczebność grupy 65+: ", len(diff_65), "\tŚrednia różnica wieku w grupie: ", round(numpy.mean(diff_65),2), \
          "\tOdchylenie standardowe różnic wieku w grupie: ", round(numpy.std(diff_65),2), "\tPoprawność algorytmu dla grupy: ", round(len(algorithm_65)/len(diff_65)*100,2),"%")
    print("Łączna liczba klientów: ", len(age_stat), "\tPoprawność algorytmu dla wszystkich klientów: ", round(len(algorithm_all)/len(diff_all)*100,2),"%")

def gender(gender_list):
    """statystyki pod analizę płci"""
    global_correct_male, global_correct_female, global_correct_90, global_correct_75, global_correct_50, global_correct_25 = [], [], [], [], [], []
    for i in range(0,len(gender_list)):
        if gender_list[i][0] < 0 and gender_list[i][1] < 0:
            global_correct_male.append(gender_list[i][0])
        elif gender_list[i][0] > 0 and gender_list[i][1] > 0:
            global_correct_female.append(gender_list[i][0])
    print("\nProcent prawidłowo rozpoznanej płci: ", round(((len(global_correct_male)+len(global_correct_female))/len(gender_list)*100),2), "%")
    for i in range(0, len(gender_list)):
        if gender_list[i][0] <= -0.9 and gender_list[i][1] < 0:
            global_correct_90.append(gender_list[i][0])
        elif gender_list[i][0] >= 0.9 and gender_list[i][1] > 0:
            global_correct_90.append(gender_list[i][0])
        elif -0.9 < gender_list[i][0] <= -0.75 and gender_list[i][1] < 0:
            global_correct_75.append(gender_list[i][0])
        elif 0.9 > gender_list[i][0] >= 0.75 and gender_list[i][1] > 0:
            global_correct_75.append(gender_list[i][0])
        elif -0.75 < gender_list[i][0] <= -0.5 and gender_list[i][1] < 0:
            global_correct_50.append(gender_list[i][0])
        elif 0.75 > gender_list[i][0] >= 0.5 and gender_list[i][1] > 0:
            global_correct_50.append(gender_list[i][0])
        elif -0.5 < gender_list[i][0] <= -0.25 and gender_list[i][1] < 0:
            global_correct_25.append(gender_list[i][0])
        elif 0.5 > gender_list[i][0] >= 0.25 and gender_list[i][1] > 0:
            global_correct_25.append(gender_list[i][0])
    print("Algorytm określił prawidłowo płeć z przwdopodobieństwem większym niż 90% dla: ", round((len(global_correct_90)/len(gender_list))*100,2), "%")
    print("Algorytm określił prawidłowo płeć z przwdopodobieństwem większym niż 75% dla: ", round(((len(global_correct_90)+len(global_correct_75))/len(gender_list))*100,2), "%")
    print("Algorytm określił prawidłowo płeć z przwdopodobieństwem większym niż 50% dla: ", round(((len(global_correct_90)+len(global_correct_75)+len(global_correct_50))/len(gender_list))*100,2), "%")
    print("Algorytm określił prawidłowo płeć z przwdopodobieństwem większym niż 25% dla: ", round(((len(global_correct_90)+len(global_correct_75)+len(global_correct_50)+len(global_correct_25))/len(gender_list))*100,2), "%")

def main():
    company_name = str(input("Podaj nazwę firmy do analizy: ")).lower()
    full_data = import_data(company_name) 
    age_stat = diff(full_data)
    global_stat(age_stat)   
    group_stat(age_stat)
    gender_list = gender_tab(full_data)
    gender(gender_list)

main()

