import os
import shutil
import sqlite3

# Ścieżka do pliku bazy danych
db_path = os.path.join('instance', 'database.db')

# Usunięcie pliku bazy danych
if os.path.exists(db_path):
    os.remove(db_path)

# Usunięcie folderu migracji
if os.path.exists('migrations'):
    shutil.rmtree('migrations')

# Inicjalizacja nowej bazy danych i migracji
os.system('flask db init')
os.system('flask db migrate -m "Initial migration"')
os.system('flask db upgrade')

# Funkcja do wykonywania plików SQL
def execute_sql_file(db_path, sql_file):
    with open(sql_file, 'r', encoding='utf-8') as file:
        sql = file.read()
    conn = sqlite3.connect(db_path)
    conn.executescript(sql)
    conn.close()

# Ścieżka do katalogu z plikami SQL
sql_dir = 'sql'

# Lista plików SQL do wykonania
sql_files = [
    'insert_family.sql',
    'insert_patrol.sql',
    'insert_family_task.sql'
]

# Wykonaj pliki SQL
for sql_file in sql_files:
    sql_path = os.path.join(sql_dir, sql_file)
    if os.path.exists(sql_path):
        execute_sql_file(db_path, sql_path)
    else:
        print(f"Plik {sql_path} nie został znaleziony")

print("Baza danych została zresetowana i zainicjalizowana na nowo.")
