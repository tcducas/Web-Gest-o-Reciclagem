import sqlite3
connection = sqlite3.connect('database.db')
with open('schema.sql') as f:
   
    connection.executescript(f.read())

    print("Tabelas criadas com sucesso!")
    connection.commit()
    connection.close() 