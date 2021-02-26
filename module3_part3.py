import requests

url = 'https://raw.githubusercontent.com/datasets/co2-ppm-daily/master/data/co2-ppm-daily.csv'
res = requests.get(url, allow_redirects=True)
with open('co2_ed.csv','wb') as file:
    file.write(res.content)


def get_data(filename):
    res = []
    f = open(filename, 'r')
    for line in f:
        point = [x for x in line.split(",")]
        res.append(point)

    f.close()

    return res

co2_by_date = get_data('co2_ed.csv')

number = 0
for value in co2_by_date:
    date = value[0]
    c02 = (value[1])
    co2 = (c02[:-1])
    number = float(co2)










