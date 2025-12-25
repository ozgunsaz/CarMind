from db_connection import connect_to_database

conn = connect_to_database()

if conn:
    print("✅ Bağlantı başarılı!")
    conn.close()
else:
    print("❌ Veritabanı bağlantısı başarısız.")
