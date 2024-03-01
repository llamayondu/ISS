import requests
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import mysql.connector
import sys
import re
import json
import decimal
from dotted_dict import DottedDict


# Run this on windows MySQL CLI to create user
# mysql> CREATE USER 'root'@'172.27.153.109' IDENTIFIED BY 'some_pass';
# Query OK, 0 rows affected (0.48 sec)

# mysql> GRANT ALL PRIVILEGES ON *.* TO 'root'@'172.27.153.109';
# Query OK, 0 rows affected (0.37 sec)

#use this to access mysql on windows from wsl:
# mysql -h 172.27.144.1 -u root -p some_pass
#password is some_pass

db_config = {
    "host": "172.27.144.1",
    "user": "root",
    "password": "some_pass",
    "database": "top-250-shows",
    "port": "3306"
}

connection = mysql.connector.connect(**db_config)

if connection.is_connected():
    print("Connected to the database")


mycursor = connection.cursor()

headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}
url = "https://www.imdb.com/chart/toptv/"
response = requests.get(url,headers=headers)

soup= BeautifulSoup(response.content, 'html.parser')

# title_elements = soup.find_all(class_="ipc-title__text")
# episode_counts_raw = soup.find_all(class_="sc-be6f1408-8 fcCUPU cli-title-metadata-item")
# ratings = soup.find_all(class_="ipc-rating-star ipc-rating-star--base ipc-rating-star--imdb ratingGroup--imdb-rating")
# num_ratings = []
# episode_counts = []
# s_no = []
# titles = []
# ratings_counts = []
# # genres = []

# for elem in soup.find_all(class_="ipc-title__text"):
#     m = re.search("(\d+)\.\s+(.+)", elem.text)
#     if m: 
#         s_no.append(m.group(1))
#         titles.append(m.group(2))

# for elem in soup.find_all(class_="ipc-rating-star ipc-rating-star--base ipc-rating-star--imdb ratingGroup--imdb-rating"):
#     m = re.search("(\S+)\s+\((\S+)\)", elem.text)
#     if m: 
#         ratings_counts.append(decimal.Decimal(m.group(1)))
#         num_ratings.append(m.group(2))

# for elem in soup.find_all(class_="sc-be6f1408-8 fcCUPU cli-title-metadata-item"):
#     m = re.search("(\d+) eps", elem.text)
#     if m: episode_counts.append(int(m.group(1)))

# for st, ep, rc in zip(sno_titles, episode_counts, ratings_counts):
#     print(f"{st[0]}, {st[1]}, {ep}, {rc[0]}, {rc[1]}")


# data_tuples = list(zip(titles, episode_counts, ratings_counts, num_ratings))
# mycursor.executemany(insert_query, data_tuples)
# connection.commit()
# mycursor.execute("SELECT * FROM imdb")

# myresult = mycursor.fetchall()

# for x in myresult:
#     print(', '.join(map(str,x)))

elem = soup.find(id="__NEXT_DATA__")
next_data = json.loads(elem.text)
data = DottedDict(next_data)
# print(json.dumps(next_data, indent=2))
movies = []
for edge in data.props.pageProps.pageData.chartTitles.edges:
    node = edge.node
    # genres = )
    movies.append((
        # edge.currentRank,
        node.titleText.text, 
        ' '.join(g.genre.text for g in node.titleGenres.genres),
        str(node.episodes.episodes.total),
        str(node.ratingsSummary.aggregateRating),
        str(node.ratingsSummary.voteCount),
        ))

insert_query = """
    INSERT INTO imdb (Titles, Genres, Episode_Count, Rating, Num_Ratings)
    VALUES (%s, %s, %s, %s, %s)
"""

mycursor.executemany(insert_query, movies)
connection.commit()
print("\n".join(map(str, movies)))

sys.exit(0)