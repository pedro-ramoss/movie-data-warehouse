from movie_dw.db import get_connection

connection = get_connection()
print("Conexão com PostgreSQL funcionando!")
connection.close()