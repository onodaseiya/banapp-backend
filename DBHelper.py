from fastapi import HTTPException
from mysql.connector import Error

from repositories.InitDB import create_db_connection, close_db_connection


def execute_query(query: str, values: tuple = None, fetch: bool = True, return_id: bool = False):
    try:
        connection = create_db_connection()
        cursor = connection.cursor(dictionary=True)

        if values:
            cursor.execute(query, values)
        else:
            cursor.execute(query)

        if fetch:
            result = cursor.fetchall()
        elif return_id:
            connection.commit()
            result = {"id": cursor.lastrowid}
        else:
            connection.commit()
            result = {"message": "Query executed successfully"}
            
        cursor.close()
        return result
    except Error as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if connection.is_connected():
            close_db_connection(connection)
