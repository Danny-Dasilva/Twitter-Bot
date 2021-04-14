from csv import DictReader
import csv

with open('file.csv', 'r') as read:
    csv_reader = DictReader(read, delimiter='\t', quoting=csv.QUOTE_NONE)
    # Iterate over each row in the csv using reader object
    lst = []
    for row in csv_reader:
        print(row['tweet'])
        lst.append(row['tweet'])


with open('output.txt', 'a') as writer:
    for val in lst:
        writer.write(val)
        writer.write('\n')
        writer.write('<|endoftext|>')
        writer.write('\n')

