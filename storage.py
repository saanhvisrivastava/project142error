import csv

all_articles = []

with open('final.csv',encoding="utf-8") as f:
    reader = csv.reader(f)
    data = list(reader)
    all_articles = data[1:]

liked_article = []
not_liked_article = []
did_not_read = []