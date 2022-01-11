
#1 psql -U postgres
#2 CREATE DATABASE project_pythondb;
#3 \c pythondb;
from typing import ValuesView
import psycopg2
from decouple import config

DROP_USERS_TABLE= "DROP TABLE IF EXISTS users"

USERS_TABLE="""CREATE TABLE users(
    id SERIAL,
    username VARCHAR (50) NOT NULL,
    email VARCHAR (50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)"""

# CREAR USUARIO
def create_user(connect, cursor):   
    """ A) Crear Usuario  """  #Docstring
    
    username = input("Ingresa un usuario: ")
    email = input("Ingresa un email: ")
    
    query = "INSERT INTO users (username,email) VALUES (%s, %s)"
    values = (username,email)
    
    cursor.execute(query,values)
    connect.commit()      
    
    print(">>>> Usuario creado")
    
# LISTAR USUARIO
def list_user(connect, cursor):
    """ B) Listar Usuarios  """
    
    query = "SELECT id,username, email FROM users"
    cursor.execute(query)
    
    for id, username, email in cursor.fetchall():
        print(id, '-',username, '-', email)
    
    print(">>>> Usuario listado")
    
# ACTUALIZAR USUARIO   
def update_user(connect, cursor):
    """ C) Actualizar Usuario  """
    
    id = input("Ingresa el id del usuario que desea actualizar: ")
    
    query = "SELECT id FROM users WHERE id = %s"
    cursor.execute(query,(id,))
    
    user = cursor.fetchone() #None
    if user:
        
        username = input("Ingresa un nuevo usuario: ")
        email = input("Ingresa un nuevo email: ")
        
        query = "UPDATE users SET username = %s, email = %s WHERE id = %s"
        values = (username, email, id)
        
        cursor.execute(query,values)
        connect.commit()
    
        print(" >>>> Usuario actualizado exitosamente")
        
    else:
        print("No existe un usuario con ese id, intenta de nuevo")


# ELIMINAR USUARIO   
def delete_user(connect, cursor):
    """ D) Eliminar Usuario  """
    
    id = input("Ingresa el id del usuario que desea eliminar: ")
    
    query = "SELECT id FROM users WHERE id = %s"
    cursor.execute(query,(id,))
    
    user = cursor.fetchone() 
    if user:
        query = "DELETE FROM users WHERE id = %s "
        
        cursor.execute(query, (id,))
        connect.commit()
        
        print(">>>> Usuario aliminado exitosamente")        
    
    else:
        print("No existe un usuario con ese id, intenta de nuevo")
    
    
    

def default(*args):
    print("opcion no valida")

if __name__=='__main__':      
    
    options = {
        'a': create_user,
        'b': list_user,
        'c': update_user,
        'd': delete_user,
    }

    try:
        connect = psycopg2.connect(dbname='project_pythondb',
                                   user = config('USER'),
                                   password= config('SECRET_KEY'),
                                   host='localhost') 
        with connect.cursor() as cursor:
            
            #cursor.execute(DROP_USERS_TABLE)
            #cursor.execute(USERS_TABLE)
            
            connect.commit()
            
            while True:
                for function in options.values():
                    print(function.__doc__)
                    
                print("quit para salir")
                option = input("Selecciona una opcion valida: ").lower()
                
                if option == "quit" or option == "q":
                    break
                
                function = options.get(option, default)
                function(connect,cursor)
                    
                    
        
        connect.close()
        
    except psycopg2.OperationalError as err:
        print("No fue posible realizar la conexion") 
        print(err)
        
    