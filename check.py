import pandas as pd
from sqlalchemy import create_engine

# Zastąp 'sqlite:///path/to/your/database.db' odpowiednią ścieżką do swojej bazy danych SQLite
engine = create_engine('sqlite:///instance/database.db')

# Wykonaj zapytanie SQL
query = "SELECT * FROM Used_Keyword;"
df = pd.read_sql_query(query, engine)

# Zapisz wyniki do pliku Excel
df.to_excel('used_keywords.xlsx', index=False)
