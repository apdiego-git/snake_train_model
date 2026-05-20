import sqlite3
connection = sqlite3.connect('snake_info.db')

cursor = connection.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS snake_info (
               attempt integer,
               length integer,
               input integer,
               steps integer,
               death text
               )""")


def insert_attempt(snake):
    cursor.execute("INSERT INTO snake_info VALUES (:attempt, :length, :input, :steps, :death)"
                   , {"attempt": snake.attempt, "length": snake.length, "input": snake.input, 
                      "steps": snake.steps, "death": snake.death})
    connection.commit()
    
def get_max_attempt():
    cursor.execute("SELECT MAX(attempt) FROM snake_info")
    result = cursor.fetchone()

    if result[0] is not None:
        return result[0] + 1
    else:
        return 0

    
