import os
import shutil
import sqlite3

# Usunięcie pliku bazy danych
if os.path.exists('instance\\database.db'):
    os.remove('instance\\database.db')

# Usunięcie folderu migracji
if os.path.exists('migrations'):
    shutil.rmtree('migrations')

# Inicjalizacja nowej bazy danych i migracji
os.system('flask db init')
os.system('flask db migrate -m "Initial migration"')
os.system('flask db upgrade')

# Ścieżka do pliku bazy danych
db_path = 'instance\\database.db'

# Funkcja do wykonywania plików SQL
def execute_sql_file(db_path, sql_file):
    with sqlite3.connect(db_path) as conn:
        with open(sql_file, 'r', encoding='utf-8') as f:
            sql = f.read()
        conn.executescript(sql)

# Lista plików SQL do wykonania
sql_files = [
    'sql\\insert_family.sql',
    'sql\\insert_patrol.sql',
    'sql\\insert_family_task.sql'
]

# Wykonaj pliki SQL
for sql_file in sql_files:
    execute_sql_file(db_path, sql_file)

print("Baza danych została zresetowana i zainicjalizowana na nowo.")
