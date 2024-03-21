import csv

with open('oscar_age_male.csv') as csvfile:
    reader = csv.reader(csvfile, skipinitialspace=True)
    data = []
    for i, row in enumerate(reader):
        if i == 0:
            headers = row
        else:
            data.append(row)

print(headers, data[:3])

with open('oscar_age_male.csv') as csvfile:
    reader = csv.DictReader(csvfile, skipinitialspace=True)


with open("some_winners.csv", "w") as outfile:
    writer = csv.writer(outfile)
    writer.writerow(headers)
    writer.writerows(data[-5:])
