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

            # Définir une fonction pour récupérer et afficher les tables d'une base de données sélectionnée
            def show_tables(event):
                selected_db = database_combobox.get()
                conn.database = selected_db

                table_cursor = conn.cursor()
                table_cursor.execute("SHOW TABLES")
                tables = [table[0] for table in table_cursor.fetchall()]
                table_cursor.close()

                # Mettre à jour la liste déroulante des tables
                table_combobox['values'] = tables
                table_combobox.set(tables[0])  # Sélectionner la première table par défaut

            # Définir une fonction pour afficher le contenu de la table sélectionnée
            def show_table_content():
                selected_table = table_combobox.get()
                content_cursor = conn.cursor()
                content_cursor.execute(f"SELECT * FROM {selected_table}")
                table_content = content_cursor.fetchall()
                content_cursor.close()

                # Afficher le contenu dans une nouvelle fenêtre
                table_window = Toplevel(root)
                table_window.title(f"Contenu de la table {selected_table}")
                for row_idx, row in enumerate(table_content):
                    for col_idx, value in enumerate(row):
                        Label(table_window, text=value).grid(row=row_idx, column=col_idx)

            # Définir une fonction pour exécuter une requête SQL
            def execute_sql():
                query = sql_entry.get()
                if query:
                    try:
                        sql_cursor = conn.cursor()
                        sql_cursor.execute(query)
                        result = sql_cursor.fetchall()
                        sql_cursor.close()

                        # Afficher le résultat dans une nouvelle fenêtre
                        result_window = Toplevel(root)
                        result_window.title("Résultat de la requête SQL")
                        for row_idx, row in enumerate(result):
                            for col_idx, value in enumerate(row):
                                Label(result_window, text=value).grid(row=row_idx, column=col_idx)
                    except mysql.connector.Error as err:
                        print(f"Erreur d'exécution de la requête SQL : {err}")

            # Créer la liste déroulante pour afficher les tables
            table_label = Label(root, text="Table :")
            table_label.pack()
            table_combobox = ttk.Combobox(root, state="readonly")
            table_combobox.pack()

            # Associer la fonction show_tables à l'événement de changement de sélection de la base de données
            database_combobox.bind("<<ComboboxSelected>>", show_tables)

            # Bouton pour afficher le contenu de la table sélectionnée
            show_table_button = Button(root, text="Afficher le contenu de la table sélectionnée", command=show_table_content)
            show_table_button.pack()

            # Champ texte pour la requête SQL
            sql_label = Label(root, text="Requête SQL :")
            sql_label.pack()
            sql_entry = Entry(root, width=50)
            sql_entry.pack()

            # Bouton pour exécuter la requête SQL
            execute_sql_button = Button(root, text="Exécuter la requête SQL", command=execute_sql)
            execute_sql_button.pack()

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
