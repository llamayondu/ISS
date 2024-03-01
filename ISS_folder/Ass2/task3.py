import requests
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import mysql.connector
import sys
import re

# Run this on windows MySQL CLI to create user
# mysql> CREATE USER 'root'@'172.27.153.109' IDENTIFIED BY 'some_pass';
# Query OK, 0 rows affected (0.48 sec)

# mysql> GRANT ALL PRIVILEGES ON *.* TO 'root'@'172.27.153.109';
# Query OK, 0 rows affected (0.37 sec)

#use this to access mysql on windows from wsl:
# mysql -h 172.27.144.1 -u wsl_user -p
#password is some_pass

db_config = {
    "host": "172.27.144.1",
    "user": "root",
    "password": "some_pass",
    "database": "imdb",
    "port": "3306"
}

connection = mysql.connector.connect(**db_config)

if connection.is_connected():
    print("Connected to the database")


mycursor = connection.cursor()

mycursor.execute("SELECT * FROM test_table")

myresult = mycursor.fetchall()

# for x in myresult:
#     # for y in x:
#     #     print(y, end=', ')
#     print(', '.join(map(str,x)))

# sys.exit(0)

headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}
url = "https://www.imdb.com/chart/toptv/"
response = requests.get(url,headers=headers)

soup= BeautifulSoup(response.content, 'html.parser')

title_elements = soup.find_all(class_="ipc-title__text")
episode_counts_raw = soup.find_all(class_="sc-be6f1408-8 fcCUPU cli-title-metadata-item")
ratings = soup.find_all(class_="ipc-rating-star ipc-rating-star--base ipc-rating-star--imdb ratingGroup--imdb-rating")
num_ratings = []
episode_counts = []
s_no = []
sno_titles = []
ratings_counts = []
genres = []

for elem in soup.find_all(class_="ipc-title__text"):
    m = re.search("(\d+)\.\s+(.+)", elem.text)
    if m: sno_titles.append(m.group(1, 2))

for elem in soup.find_all(class_="ipc-rating-star ipc-rating-star--base ipc-rating-star--imdb ratingGroup--imdb-rating"):
    m = re.search("(\S+)\s+\((\S+)\)", elem.text)
    if m: ratings_counts.append(m.group(1, 2))

for elem in soup.find_all(class_="sc-be6f1408-8 fcCUPU cli-title-metadata-item"):
    m = re.search("(\d+) eps", elem.text)
    if m: episode_counts.append(m.group(1))

# for st, ep, rc in zip(sno_titles, episode_counts, ratings_counts):
#     print(f"{st[0]}, {st[1]}, {ep}, {rc[0]}, {rc[1]}")

sys.exit(0)

# for num in range(250):
#     s_no.append(title_elements[num+2].text.split('.')[0])
#     s_no[num]=s_no[num].split('.')[0]
#     words = title_elements[num+2].text.split()[1:]
#     title_elements[num] = ' '.join(words)

#     num_ratings.append(ratings[num].text.split()[1])
#     ratings[num] = ratings[num].text.split()[0]

# for raw in episode_counts_raw:
#     # print(raw.text)
#     splitty = raw.text.split()
#     if len(splitty)==2 and splitty[1]=='eps':
#         episode_counts.append(raw.text)

# frequency_count = {}
# for count in episode_counts:
#     frequency_count[count] = frequency_count.get(count, 0) + 1

# x_values = list(frequency_count.keys())
# y_values = list(frequency_count.values())



# for i in range(250):
#     print([i for i in s_no][0:250][i], end=', ')
#     print([i for i in title_elements][0:250][i], end=', ')
#     print([i for i in episode_counts][0:250][i], end=', ')
#     print([i for i in ratings][0:250][i], end=', ')
#     print([i for i in num_ratings][0:250][i])


# for i in range(250):
#     print([i.text for i in ratings][0:250][i])

# plt.plot(x_values, y_values, marker='o', linestyle='-')
# plt.title('Frequency Count of TV Shows by Episode Count')
# plt.xlabel('Number of Episodes')
# plt.ylabel('Frequency Count')
# plt.grid(True)
# plt.show()

db_config = {
    "host": "172.27.153.109",
    "user": "root",
    "password": "",
    "database": "imdb",
    "port": "3306"
}

try:
    connection = mysql.connector.connect(**db_config)

    if connection.is_connected():
        print("Connected to the database")

        cursor = connection.cursor()

        create_table_query = """
        CREATE TABLE IF NOT EXISTS tv_shows (
            serial_no INT PRIMARY KEY,
            title VARCHAR(255),
            episode_count VARCHAR(50),
            rating FLOAT,
            num_ratings INT
        )
        """
        cursor.execute(create_table_query)

        # Insert data into the database
        for num in range(250):
            insert_query = """
            INSERT INTO tv_shows (serial_no, title, episode_count, rating, num_ratings)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (s_no[num], title_elements[num], episode_counts[num], ratings[num], num_ratings[num]))

            # Print the data
            print(f"{s_no[num]}, {title_elements[num]}, {episode_counts[num]}, {ratings[num]}, {num_ratings[num]}")

        connection.commit()

except mysql.connector.Error as e:
    print(f"Error: {e}")

finally:
    if 'connection' in locals():
        connection.close()
        print("Connection closed.")























# Replace the placeholders with your actual database information
db_config = {
    "host": "127.0.0.1",
    "user": "root",
    "password": "Omlet90!omlet90!",
    "database": "imdb",
    "port": "3306"
}
connection = mysql.connector.connect(**db_config)

# try:
#     # Establish a connection to the database
#     connection = mysql.connector.connect(**db_config)

if connection.is_connected():
    print("Connected to the database")

        # Perform database operations here

# except mysql.connector.Error as e:
#     print(f"Error: {e}")

# finally:
#     # Close the connection in the finally block to ensure it always happens
#     if 'connection' in locals():
#         connection.close()
#         print("Connection closed.")