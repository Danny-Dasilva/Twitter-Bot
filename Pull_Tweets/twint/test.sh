while read p; do
  twint -u $p -o file.csv --csv
done <file.txt