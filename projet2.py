import mysql.connector
from tkinter import *
from tkinter import ttk

def connect_to_db():
    # Récupérer les infos depuis l'interface utilisateur
    server = server_entry.get()
    username = username_entry.get()
    password = password_entry.get()
    port = port_entry.get()

    # Connexion à la base de données
    try:
        conn = mysql.connector.connect(
            host=server,
            user=username,
            password=password,
            port=port
        )
        if conn.is_connected():
            print("Connecté à la base de données")

            # Obtenez la liste des bases de données
            cursor = conn.cursor()
            cursor.execute("SHOW DATABASES")
            databases = [db[0] for db in cursor.fetchall()]

            # Mettez à jour la liste déroulante
            database_combobox['values'] = databases
            database_combobox.set(databases[0])  # Sélectionnez la première base de données par défaut

            # Fermez le curseur
            cursor.close()

    except mysql.connector.Error as err:
        print(f"Erreur de connexion à la base de données : {err}")

# Interface utilisateur
root = Tk()
root.title("Interface de connexion MySQL")

server_label = Label(root, text="Serveur :")
server_label.pack()
server_entry = Entry(root)
server_entry.pack()

username_label = Label(root, text="Login :")
username_label.pack()
username_entry = Entry(root)
username_entry.pack()

password_label = Label(root, text="Mot de passe :")
password_label.pack()
password_entry = Entry(root, show="*")
password_entry.pack()

port_label = Label(root, text="Port :")
port_label.pack()
port_entry = Entry(root)
port_entry.pack()

connect_button = Button(root, text="Se connecter", command=connect_to_db)
connect_button.pack()

# Ajouter une liste déroulante pour afficher les bases de données
database_label = Label(root, text="Base de données :")
database_label.pack()
database_combobox = ttk.Combobox(root, state="readonly")
database_combobox.pack()

root.mainloop()
