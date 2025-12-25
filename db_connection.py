import mysql.connector

def connect_to_database():
    try:
        connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Ozgun2003.",          
    database="carmind_db"
)

        if connection.is_connected():
            print("✅ Veritabanına başarıyla bağlanıldı.")
            return connection
    except Exception as err:
        print("❌ Bağlantı hatası:", err)
        return None


