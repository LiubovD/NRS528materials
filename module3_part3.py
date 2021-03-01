import csv
import requests

url = 'https://raw.githubusercontent.com/datasets/co2-ppm-daily/master/data/co2-ppm-daily.csv'
res = requests.get(url, allow_redirects=True)
with open('co2_ed.csv','wb') as file:
    file.write(res.content)

number = 0
year_list = list()
value_list = list()
year_co2 = dict()

spring = ["03", "04", "05", 0, 0]
summer = ["06", "07", "08", 0, 0]
autumn = ["09", "10", "11", 0, 0]
winter = ["12", "01", "02", 0, 0]


with open('co2_ed.csv') as table_co2:
    next(table_co2)
    for row in table_co2:
        date,value = row.split(sep = ',')
        co2 = float(str(value[:-1]))
        year, month, day = date.split("-")
        year_list.append(year)
        value_list.append(co2)
        if year not in year_co2:
            year_co2[year] = co2
        if year in year_co2:
            year_co2[year] += co2

        if month in spring:
            spring[3] += co2
            spring[4] += 1
        if month in summer:
            summer[3] += co2
            summer[4] += 1
        if month in autumn:
            autumn[3] += co2
            autumn[4] += 1
        if month in winter:
            winter[3] += co2
            winter[4] += 1

year_freq = dict()

for year, co2 in year_co2.items():
    with open('co2_ed.csv') as table_co2:
        next(table_co2)
        counter = 1
        for row in table_co2:
            year_table, month_table, everything_else = row.split("-")
            if year_table == year:
                counter += 1
                year_freq[year] = counter

for year, co2 in year_co2.items():
    for years, freq in year_freq.items():
        if year == years:
            year_co2[year] = co2/freq

for year, co2 in year_co2.items():
    print(str(year) + " annual average " + str("{:.2f}".format(co2)))

print("Minimum for entire dataset " + str(min(value_list)))
print("Maximum for entire dataset " + str(max(value_list)))
print("Average for entire dataset " + str("{:.2f}".format(sum(value_list)/len(value_list))))

print("Spring average " + str("{:.2f}".format(spring[3]/spring[4])))
print("Summer average " + str("{:.2f}".format(summer[3]/summer[4])))
print("Autumn average " + str("{:.2f}".format(autumn[3]/autumn[4])))
print("Winter average " + str("{:.2f}".format(winter[3]/winter[4])))


anomaly_list = list()
average = sum(value_list)/len(value_list)
x = 0
for item in value_list:
    x = item - average
    anomaly_list.append(x)
print("Anomaly list:")
print(anomaly_list)








