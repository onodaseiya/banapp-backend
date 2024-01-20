import os

from mysql.connector import Error
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, TIMESTAMP, text, func
from sqlalchemy.orm import declarative_base
from dotenv import load_dotenv

from InitDB import create_db_connection, close_db_connection, insert_test_data_into_users, \
    insert_test_data_into_pets, insert_test_data_into_histories, insert_test_data_into_achievements, \
    insert_test_data_into_items, insert_test_data_into_baitlogs

# 環境変数を読み込む
load_dotenv()
db_host = os.getenv("DB_HOST")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_name = os.getenv("DB_NAME")

# DBエンジン作成
database = create_engine(f"mysql+mysqlconnector://{db_user}:{db_password}@{db_host}/{db_name}")
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column('id', Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String(500), nullable=False)
    coin = Column(Integer, default=0, nullable=False)
    cigarette_price = Column(Integer, nullable=False)
    cigarette_per_day = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, default=func.now())


class Pet(Base):
    __tablename__ = 'pets'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column('user_id', Integer, ForeignKey('users.id'), nullable=False)
    name = Column(String(500), nullable=False)
    hunger = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime(timezone=True), nullable=False, default=func.now())
    death_at = Column(DateTime(timezone=True))
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True, default=func.now())


class History(Base):
    __tablename__ = 'histories'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column('user_id', Integer, ForeignKey('users.id'), nullable=False)
    pet_id = Column(Integer, ForeignKey('pets.id'), nullable=False)
    more_money = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), nullable=False, default=func.now())


class Achievement(Base):
    __tablename__ = 'achievements'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    title = Column(String(500), nullable=False)
    description = Column(String(500), nullable=False)
    reward_coin = Column(Integer, nullable=False)


class GetAchievement(Base):
    __tablename__ = 'get_achievements'

    user_id = Column('user_id', Integer, ForeignKey('users.id'), nullable=False, primary_key=True)
    achievement_id = Column('achievement_id', Integer, ForeignKey('achievements.id'), primary_key=True)


class Item(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String(500), nullable=False)
    price = Column(Integer, nullable=False)
    energy = Column(Integer, nullable=False)

class BaitLog(Base):
    __tablename__ = 'baitlogs'

    user_id = Column('user_id', Integer, ForeignKey('users.id'), nullable=False, primary_key=True)
    continueday = Column(Integer, nullable=False)
    totalcount = Column(Integer, nullable=False)
    log_date = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), nullable=False)


def update_created_at_default(table_name, column_name):
    load_dotenv()
    db_name = os.getenv('DB_NAME')
    try:
        connection = create_db_connection()
        if connection is not None:
            cursor = connection.cursor()
            cursor.execute(f"USE {db_name}")

            # カラム変更
            alter_table_query = f"""
            ALTER TABLE {table_name} MODIFY {column_name} TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
            """
            cursor.execute(alter_table_query)
            print(f"Column {column_name} update successfully")
    except Error as error:
        print(f"Failed to update {column_name}' column {error}")
    finally:
        if connection is not None:
            cursor.close()
            close_db_connection(connection)

def update_column_at_pets_death_at():
    load_dotenv()
    db_name = os.getenv('DB_NAME')
    try:
        connection = create_db_connection()
        if connection is not None:
            cursor = connection.cursor()
            cursor.execute(f"USE {db_name}")

            # カラムを変更
            aleter_table_query = """
            ALTER TABLE pets MODIFY death_at TIMESTAMP NULL;
            """
            cursor.execute(aleter_table_query)
            print(f"Column death_at in table pets updated successfully")
    except Error as error:
            print(f"Failed to update death_at column in table pets {error}")

    finally:
        if connection.is_connected():
            cursor.close()
            close_db_connection(connection)

def update_updated_at_column(table_name, column_name):
    load_dotenv()
    db_name = os.getenv('DB_NAME')
    try:
        connection = create_db_connection()
        if connection is not None:
            cursor = connection.cursor()
            cursor.execute(f"USE {db_name}")

            # カラム変更
            alter_table_query = f"""
            ALTER TABLE {table_name} MODIFY {column_name} TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP;
            """
            cursor.execute(alter_table_query)
            print(f"Column '{column_name}' in table '{table_name}' updated successfully")
    except Error as error:
        print(f"Failed to update '{column_name}' column in table '{table_name}' {error}")
    finally:
        if connection.is_connected():
            cursor.close()
            close_db_connection(connection)


Base.metadata.create_all(database)

update_created_at_default('users', 'created_at')
update_created_at_default('pets', 'created_at')
update_created_at_default('pets', 'updated_at')
update_updated_at_column('pets', 'updated_at')
update_created_at_default('Histories', 'created_at')
update_column_at_pets_death_at()

insert_test_data_into_users()
insert_test_data_into_pets()
insert_test_data_into_histories()
insert_test_data_into_achievements()
insert_test_data_into_items()
insert_test_data_into_baitlogs()
