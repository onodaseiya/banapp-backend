import os
import mysql.connector
from dotenv import load_dotenv
from mysql.connector import Error


# MySQL接続関数
def create_db_connection():
    try:
        load_dotenv()
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
        print("MySQL DB connection successful")
        return connection
    except Error as erorr:
        print(f"Error while connecting to MySQL {erorr}")


# データベースとの接続を切る
def close_db_connection(connection):
    if connection.is_connected():
        connection.close()
        print("MySQL DB connection is closed")


# データベース作成
def create_database():
    load_dotenv()
    db_name: str = os.getenv("DB_NAME")
    try:
        connection = create_db_connection()
        if connection is not None:
            cursor = connection.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
            print(f"{db_name} Database created successfully")
    except Error as error:
        print(f"Failed to create database {db_name} {error}")
    finally:
        if connection.is_connected():
            cursor.close()
            close_db_connection(connection)


def drop_database():
    load_dotenv()
    db_name: str = os.getenv("DB_NAME")
    try:
        connection = create_db_connection()
        if connection is not None:
            cursor = connection.cursor()

            cursor.execute(f"DROP DATABASE IF EXISTS {db_name}")
            print(f"{db_name} Database dropped successfully")
    except Error as error:
        print(f"Failed to drop database {db_name} {error}")
    finally:
        if connection.is_connected():
            cursor.close()
            close_db_connection(connection)


def insert_test_data_into_users():
    load_dotenv()
    db_name: str = os.getenv("DB_NAME")
    try:
        connection = create_db_connection()
        if connection is not None:
            cursor = connection.cursor()
            # DBの選択
            cursor.execute(f"USE {db_name}")

            # 挿入
            insert_users_query = """
            INSERT INTO users (name, coin, cigarette_price, cigarette_per_day) VALUES
            ('ユーザ1', 30, 500, 12),
            ('ユーザ2', 30, 550, 30),
            ('ユーザ3', 30, 400, 21)
            """

            cursor.execute(insert_users_query)
            connection.commit()
            print("Test users data inserted successfully")
    except Error as error:
        print(f"Failed to create test data {error}")
    finally:
        if connection.is_connected():
            cursor.close()
            close_db_connection(connection)


def insert_test_data_into_pets():
    load_dotenv()
    db_name: str = os.getenv("DB_NAME")
    try:
        connection = create_db_connection()
        if connection is not None:
            cursor = connection.cursor()
            cursor.execute(f"USE {db_name}")
            insert_pets_query = """
            INSERT INTO pets (user_id, name, hunger) VALUES (%s, %s, %s)
            """
            test_data = [
                (3, 'ペット1', 20),
                (1, 'ペット2', 30),
                (2, 'ペット3', 40)
            ]
            cursor.executemany(insert_pets_query, test_data)
            connection.commit()
            print("Test pets data inserted successfully")
    except Error as error:
        print(f"Failed to insert test data {error}")
    finally:
        if connection.is_connected:
            cursor.close()
            close_db_connection(connection)


def insert_test_data_into_histories():
    load_dotenv()
    db_name: str = os.getenv("DB_NAME")
    try:
        connection = create_db_connection()
        if connection is not None:
            cursor = connection.cursor()
            cursor.execute(f"USE {db_name}")
            insert_query = """
            INSERT INTO histories (user_id, pet_id, more_money)
            VALUES (%s, %s, %s)
            """
            test_data = [
                (1, 1, 100),
                (1, 2, 200),
                (2, 3, 300)
            ]
            cursor.executemany(insert_query, test_data)
            connection.commit()
            print("Test data inserted into histories successfully")
    except Error as error:
        print(f"Failed to insert test data into histories {error}")
    finally:
        if connection.is_connected():
            cursor.close()
            close_db_connection(connection)


def insert_test_data_into_achievements():
    load_dotenv()
    db_name: str = os.getenv("DB_NAME")
    try:
        connection = create_db_connection()
        if connection is not None:
            cursor = connection.cursor()
            cursor.execute(f"USE {db_name}")
            insert_query = """
            INSERT INTO achievements (title, description, reward_coin)
            VALUES (%s, %s, %s)
            """
            test_data = [
                ('餌やりをしてみよう', "Let's feed them!", 50),
                ('3日連続餌やりをしよう', "Let's feed them 3days in a row!", 100),
                ('5日連続餌やりをしよう', "Let's feed them three 5days in a row!", 150),
                ('1週間餌やりをしよう', "Let's feed them for a week.", 200)
            ]
            cursor.executemany(insert_query, test_data)
            connection.commit()
            print("Test data inserted into achievements successfully")
    except Error as error:
        print(f"Failed to insert test data into achievements {error}")
    finally:
        if connection.is_connected():
            cursor.close()
            close_db_connection(connection)


def insert_test_data_into_items():
    load_dotenv()
    db_name: str = os.getenv("DB_NAME")
    try:
        connection = create_db_connection()
        if connection is not None:
            cursor = connection.cursor()
            cursor.execute(f"USE {db_name}")
            insert_query = """
            INSERT INTO items (name, price, energy)
            VALUES (%s, %s, %s)
            """
            test_data = [
                ('クロワッサン', 30, 30),
                ('アイスクリーム', 40, 40),
                ('ハンバーガー', 60, 80),
                ('ラーメン', 80, 80),
                ('ケーキ', 100, 100)
            ]
            cursor.executemany(insert_query, test_data)
            connection.commit()
            print("Test data inserted into items successfully")
    except Error as error:
        print(f"Failed to insert test data into items {error}")
    finally:
        if connection.is_connected():
            cursor.close()
            close_db_connection(connection)

def insert_test_data_into_baitlogs():
    load_dotenv()
    db_name: str = os.getenv("DB_NAME")
    try:
        connection = create_db_connection()
        if connection is not None:
            cursor = connection.cursor()
            cursor.execute(f"USE {db_name}")
            insert_query = """
            INSERT INTO baitlogs (user_id, continueday, totalcount) VALUES (%s, %s, %s)
            """
            test_data = [
                (1, 3, 1),
                (2, 9, 19),
                (3, 0, 0)
            ]
            cursor.executemany(insert_query, test_data)
            connection.commit()
            print("Test baitlogs data inserted successfully")
    except Error as error:
        print(f"Failed to insert test data {error}")
    finally:
        if connection.is_connected:
            cursor.close()
            close_db_connection(connection)


#drop_database()
#create_database()
