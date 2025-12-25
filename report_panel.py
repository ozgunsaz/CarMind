import tkinter as tk
from tkinter import ttk
import mysql.connector
from db_connection import connect_to_database

def open_report_panel():
    root = tk.Toplevel()
    root.title("📊 Rapor Paneli")
    root.geometry("650x700")

    canvas = tk.Canvas(root)
    scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    canvas.bind_all("<MouseWheel>", _on_mousewheel)

    # Veritabanı bağlantısı
    conn = connect_to_database()
    cursor = conn.cursor()

    queries = [
        {
            "title": "1. En Sık Bildirilen 5 Arıza Kodu",
            "sql": """
                SELECT f.fault_code, f.fault_description, COUNT(vf.fault_id) AS report_count
                FROM VehicleFaults vf
                JOIN FaultCodes f ON vf.fault_code = f.fault_code
                GROUP BY vf.fault_code
                ORDER BY report_count DESC
                LIMIT 5;
            """
        },
        {
            "title": "2. Son 10.000 km’de Yağ Değişimi Yapılmayan Araçlar",
            "sql": """
                SELECT v.plate, MAX(m.kilometers_at_service) AS last_oil_km
                FROM Vehicles v
                LEFT JOIN Maintenances m ON v.vehicle_id = m.vehicle_id
                WHERE m.maintenance_type = 'Yağ değişimi'
                GROUP BY v.vehicle_id
                HAVING MAX(m.kilometers_at_service) < (
                    SELECT MAX(kilometers_at_service) FROM Maintenances
                ) - 10000;
            """
        },
        {
            "title": "3. Aynı Arızayı 3+ Kez Bildiren Araçlar",
            "sql": """
                SELECT v.plate, vf.fault_code, COUNT(*) AS fault_count
                FROM VehicleFaults vf
                JOIN Vehicles v ON vf.vehicle_id = v.vehicle_id
                GROUP BY vf.vehicle_id, vf.fault_code
                HAVING fault_count >= 3;
            """
        },
        {
            "title": "4. Teknisyenlerin Onay Oranı (%)",
            "sql": """
                SELECT u.full_name AS technician_name,
                       COUNT(CASE WHEN ms.status = 'approved' THEN 1 END) AS approved_count,
                       COUNT(ms.suggestion_id) AS total_suggestions,
                       ROUND(100 * COUNT(CASE WHEN ms.status = 'approved' THEN 1 END) / COUNT(ms.suggestion_id), 2) AS approval_rate
                FROM MaintenanceSuggestions ms
                JOIN Users u ON ms.user_id = u.user_id
                WHERE u.role = 'technician'
                GROUP BY u.user_id;
            """
        },
        {
            "title": "5. Ortalama Maliyetle Bakım Türleri (Azalan)",
            "sql": """
                SELECT maintenance_type, 
                       ROUND(AVG(cost), 2) AS avg_cost
                FROM Maintenances
                GROUP BY maintenance_type
                ORDER BY avg_cost DESC;
            """
        },
        {
            "title": "6. En Çok Bakım Yapılmış 5 Araç",
            "sql": """
                SELECT v.plate, COUNT(m.maintenance_id) AS maintenance_count
                FROM Maintenances m
                JOIN Vehicles v ON m.vehicle_id = v.vehicle_id
                GROUP BY m.vehicle_id
                ORDER BY maintenance_count DESC
                LIMIT 5;
            """
        },
        {
            "title": "7. Son 6 Aydaki Aylık Toplam Bakım Maliyeti",
            "sql": """
                SELECT DATE_FORMAT(service_date, '%Y-%m') AS month,
                       ROUND(SUM(cost), 2) AS total_monthly_cost
                FROM Maintenances
                WHERE service_date >= DATE_SUB(CURDATE(), INTERVAL 6 MONTH)
                GROUP BY month
                ORDER BY month DESC;
            """
        }
    ]

    for query in queries:
        label = tk.Label(scrollable_frame, text=query["title"], font=("Helvetica", 12, "bold"))
        label.pack(pady=(20, 5))

        tree = ttk.Treeview(scrollable_frame, show='headings')
        tree.pack(fill="x", padx=10, expand=True)

        try:
            cursor.execute(query["sql"])
            rows = cursor.fetchall()
            columns = [i[0] for i in cursor.description]

            tree["columns"] = columns
            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, anchor="center", width=150)

            for row in rows:
                tree.insert("", "end", values=row)
        except Exception as e:
            tk.Label(scrollable_frame, text=f"Hata: {e}", fg="red").pack()

    conn.close()
