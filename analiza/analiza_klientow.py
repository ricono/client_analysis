import pymysql, numpy, klient_per_dzien, numpy



#daily_quantity = klient_per_dzien.days_list(company_name)
#weekday_qunatity = klient_per_dzien.weekdays_dict(company_name)

def week_day(company_name):
    """Obliczenie średniej ilości odwiedzić dla poszczegolnych dni tygodnia"""
    weekday_qunatity = klient_per_dzien.weekdays_dict(company_name)
    weekday_qunatity_female = klient_per_dzien.weekdays_dict_female(company_name) #dodane
    weekday_list = [['Monday'], ['Tuesday'], ['Wednesday'], ['Thursday'], ['Friday'], ['Saturday'], ['Sunday']]
    for i in weekday_qunatity:
        avg = int(round(numpy.mean(weekday_qunatity[i]),0))
        for j in range(0, len(weekday_list)):
            if i == weekday_list[j][0]:
                weekday_list[j].append(avg)
    
    print("\nŚrednia ilość odwiedzin w danym dniu tygodnia: ")
    for k in range(0, len(weekday_list)):
        print(weekday_list[k][0], ": \t", weekday_list[k][1])

    for i in weekday_qunatity_female:
        avg = int(round(numpy.mean(weekday_qunatity_female[i]),0))
        for j in range(0, len(weekday_list)):
            if i == weekday_list[j][0]:
                weekday_list[j].append(avg)

    print("\nŚrednia ilość odwiedzin w danym dniu tygodnia z podziałem na płeć: ")
    for k in range(0, len(weekday_list)):
        print(weekday_list[k][0], ": \t", "(kobiety: ",round(weekday_list[k][2]/weekday_list[k][1]*100),"%)", "(mężczyźni: ", round((weekday_list[k][1]-weekday_list[k][2])/weekday_list[k][1]*100),"%)")
    

def min_max(company_name):
    min_quantity = klient_per_dzien.days_min(company_name)
    max_quantity = klient_per_dzien.days_max(company_name)

    print("\nNajmniej ludzi pojawiło się w sklepie w dniach:")
    for i in range(0, len(min_quantity)):
        print(min_quantity[i][0], " (",min_quantity[i][2],"):", min_quantity[i][1], "osób.")

    print("\nNajwięcej ludzi pojawiło się w sklepie w dniach:")
    for i in range(0, len(max_quantity)):
        print(max_quantity[i][0], " (",max_quantity[i][2],"):", max_quantity[i][1], "osób.")

def weather_stat(company_name):
    weather_data = klient_per_dzien.weather_clients(company_name)
    from prettytable import PrettyTable
    x = PrettyTable()
    x.field_names = ["Data", "Ilość klientów", "Temperatura (C)", "Ciśnienie (hPa)", "Opady (mm)"]
    for i in range(0,len(weather_data)):
        x.add_row([weather_data[i][0], weather_data[i][4], weather_data[i][1], weather_data[i][2], weather_data[i][3]])
    print("\nIlość odwiedzin w odnienieniu do pogody")
    print(x.get_string())

def weather_correlation(company_name):
    weather_cor = klient_per_dzien.weather_clients(company_name)
    clients, temperature, preasure, rain = [], [], [], []
    for i in range(0, len(weather_cor)):
        clients.append(weather_cor[i][4])
    for i in range(0, len(weather_cor)):
        temperature.append(weather_cor[i][1])
    for i in range(0, len(weather_cor)):
        preasure.append(weather_cor[i][2])
    for i in range(0, len(weather_cor)):
        rain.append(weather_cor[i][3])
    print("\nWspółzależność między ilością odwiedzin a warunkami atmosferycznymi:")
    print("- współczynnik w okolicach 0 -> słaba korelacja")
    print("- współczynnik w okolicach 1 lub -1 -> silna korelacja")
    print("Współczynnik korelacji pomiędzy ilością klientów, a temperaturą: ", round(numpy.corrcoef(clients, temperature)[0,1],3))
    print("Współczynnik korelacji pomiędzy ilością klientów, a ciśnieniem: ", round(numpy.corrcoef(clients, preasure)[0,1],3))
    print("Współczynnik korelacji pomiędzy ilością klientów, a wysokością opadów: ", round(numpy.corrcoef(clients, rain)[0,1],3))

def main():
    company_name = str(input("Podaj nazwę firmy do analizy: ")).lower()
    week_day(company_name)   
    min_max(company_name)
    weather_correlation(company_name)
    weather_stat(company_name)

main()
