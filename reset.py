import os
import shutil

# Usunięcie pliku bazy danych
if os.path.exists('instance\database.db'):
    os.remove('instance\database.db')

# Usunięcie folderu migracji
if os.path.exists('migrations'):
    shutil.rmtree('migrations')

# Inicjalizacja nowej bazy danych i migracji
os.system('flask db init')
os.system('flask db migrate -m "Initial migration"')
os.system('flask db upgrade')
