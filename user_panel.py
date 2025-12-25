import tkinter as tk
import sys
from tkinter import messagebox, ttk
from db_connection import connect_to_database

def open_user_panel(user_id):
    conn = connect_to_database()
    username = ""
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT username FROM Users WHERE user_id = %s", (user_id,))
        result = cursor.fetchone()
        if result:
            username = result[0]
        conn.close()

    window = tk.Toplevel()
    window.title("Kullanıcı Paneli")
    window.geometry("1250x750")
    window.configure(bg="#ff8f4f")

    panel = tk.Frame(window, bg="#ffe7d9")
    panel.place(relx=0.5, rely=0.5, anchor="center", width=800, height=800)

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TButton", font=("Arial", 14), padding=6, background="#993902", foreground="white")
    style.map("TButton", background=[("active", "#6b2802")], foreground=[("active", "white")])
    style.configure("Treeview.Heading", background="#993902", foreground="white", font=("Arial", 13, "bold"))
    style.configure("Treeview", font=("Arial", 12))
    style.map("Treeview", background=[("selected", "#ffe7d9")], foreground=[("selected", "black")])

    # Scrollable canvas for content
    canvas = tk.Canvas(panel, bg="#ffe7d9", highlightthickness=0)
    scrollbar = tk.Scrollbar(panel, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    scrollable_frame = tk.Frame(canvas, bg="#ffe7d9")
    canvas.create_window((0, 0), window=scrollable_frame, anchor="n")

    def on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))
    scrollable_frame.bind("<Configure>", on_frame_configure)

    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    canvas.bind_all("<MouseWheel>", _on_mousewheel)

    # Header
    label = tk.Label(scrollable_frame, text=f"\U0001F464 Hoşgeldiniz, {username}", font=("Arial", 22, "bold"), bg="#ffe7d9", fg="#993902", anchor="center")
    label.pack(pady=(20, 10))
    # Araçlar Bölümü
    section1 = tk.LabelFrame(scrollable_frame, text="\U0001F697 Kayıtlı Araçlar", font=("Arial", 15, "bold"),
                             bg="#ffe7d9", fg="#993902", bd=2, relief="groove", labelanchor="n")
    section1.pack(pady=10)
    section1.pack_configure(anchor="center")

    vehicle_tree = ttk.Treeview(section1, columns=("ID", "Plaka", "Marka", "Model", "Motor", "KM"), show="headings", height=4)
    for col in vehicle_tree["columns"]:
        vehicle_tree.heading(col, text=col, anchor="center")
        vehicle_tree.column(col, width=120, anchor="center")
    vehicle_tree.pack(pady=5, fill="x")
    vehicle_tree.pack_configure(anchor="center")
    ttk.Button(section1, text="Araçları Listele", command=lambda: list_user_vehicles(vehicle_tree, user_id)).pack(pady=5)

    # Yeni Araç Ekle
    section2 = tk.LabelFrame(scrollable_frame, text="\U0001F698 Yeni Araç Ekle", font=("Arial", 15, "bold"),
                             bg="#ffe7d9", fg="#993902", bd=2, relief="groove", labelanchor="n")
    section2.pack(pady=10)
    section2.pack_configure(anchor="center")

    frame_vehicle = tk.Frame(section2, bg="#ffe7d9")
    frame_vehicle.pack(pady=5)
    frame_vehicle.pack_configure(anchor="center")
    labels = ["Plaka", "Marka", "Model", "Motor Tipi", "Kilometre"]
    entries = []
    for i, label in enumerate(labels):
        tk.Label(frame_vehicle, text=label + ":", font=("Arial", 12), bg="#ffe7d9", fg="#993902").grid(row=i, column=0, sticky="e", padx=5, pady=2)
        entry = ttk.Entry(frame_vehicle, width=25)
        entry.grid(row=i, column=1, padx=5, pady=2)
        entries.append(entry)
    ttk.Button(section2, text="➕ Araç Ekle", command=lambda: insert_vehicle(user_id, *[e.get() for e in entries])).pack(pady=5)

    # Arıza bildirimi
    section3 = tk.LabelFrame(scrollable_frame, text="\U0001F4DD Yeni Arıza Bildirimi", font=("Arial", 15, "bold"),
                             bg="#ffe7d9", fg="#993902", bd=2, relief="groove", labelanchor="n")
    section3.pack(pady=10)
    section3.pack_configure(anchor="center")

    frame_fault = tk.Frame(section3, bg="#ffe7d9")
    frame_fault.pack(pady=5)
    frame_fault.pack_configure(anchor="center")
    tk.Label(frame_fault, text="Araç ID:", font=("Arial", 12), bg="#ffe7d9", fg="#993902").grid(row=0, column=0, sticky="e", padx=5, pady=2)
    vehicle_entry = ttk.Entry(frame_fault, width=25)
    vehicle_entry.grid(row=0, column=1, padx=5, pady=2)
    tk.Label(frame_fault, text="Açıklama:", font=("Arial", 12), bg="#ffe7d9", fg="#993902").grid(row=1, column=0, sticky="e", padx=5, pady=2)
    fault_entry = ttk.Entry(frame_fault, width=40)
    fault_entry.grid(row=1, column=1, padx=5, pady=2)
    tk.Label(frame_fault, text="Arıza Kodu:", font=("Arial", 12), bg="#ffe7d9", fg="#993902").grid(row=2, column=0, sticky="e", padx=5, pady=2)
    fault_code_entry = ttk.Entry(frame_fault, width=25)
    fault_code_entry.grid(row=2, column=1, padx=5, pady=2)
    ttk.Button(section3, text="➕ Arıza Ekle", command=lambda: insert_fault(vehicle_entry.get(), fault_entry.get(), fault_code_entry.get())).pack(pady=5)

    # Tanımlı Arıza Kodları
    section4 = tk.LabelFrame(scrollable_frame, text="📋 Tanımlı Arıza Kodları", font=("Arial", 15, "bold"),
                             bg="#ffe7d9", fg="#993902", bd=2, relief="groove", labelanchor="n")
    section4.pack(pady=10)
    section4.pack_configure(anchor="center")

    frame_faultcodes = tk.Frame(section4, bg="#ffe7d9")
    frame_faultcodes.pack(fill="x")
    frame_faultcodes.pack_configure(anchor="center")
    faultcode_tree = ttk.Treeview(frame_faultcodes, columns=("Kod", "Açıklama"), show="headings", height=4)
    faultcode_tree.heading("Kod", text="Kod", anchor="center")
    faultcode_tree.heading("Açıklama", text="Açıklama", anchor="center")
    faultcode_tree.column("Kod", width=100, anchor="center")
    faultcode_tree.column("Açıklama", width=400, anchor="center")
    faultcode_tree.pack(side="left", fill="both", expand=True)
    faultcode_tree.pack_configure(anchor="center")
    scrollbar_faultcodes = tk.Scrollbar(frame_faultcodes, orient="vertical", command=faultcode_tree.yview)
    faultcode_tree.configure(yscrollcommand=scrollbar_faultcodes.set)
    scrollbar_faultcodes.pack(side="right", fill="y")
    ttk.Button(section4, text="🔄 Kodları Yükle", command=lambda: list_fault_codes(faultcode_tree)).pack(pady=5)

    # AI Önerileri
    section5 = tk.LabelFrame(scrollable_frame, text="\U0001F9E0 AI Önerileri", font=("Arial", 15, "bold"),
                             bg="#ffe7d9", fg="#993902", bd=2, relief="groove", labelanchor="n")
    section5.pack(pady=10)
    section5.pack_configure(anchor="center")

    suggestion_tree = ttk.Treeview(section5, columns=("ID", "Plaka", "Kod", "Öneri", "Durum"), show="headings", height=4)
    for col in suggestion_tree["columns"]:
        suggestion_tree.heading(col, text=col,anchor="center")
        suggestion_tree.column(col, width=150, anchor="center")
    suggestion_tree.pack(pady=5, fill="x")
    suggestion_tree.pack_configure(anchor="center")
    ttk.Button(section5, text="AI Önerilerini Göster", command=lambda: list_suggestions(suggestion_tree, user_id)).pack(pady=5)

    # Technician Suggestions
    section6 = tk.LabelFrame(scrollable_frame, text="🛠️ Teknisyen Tavsiyeleri", font=("Arial", 15, "bold"),
                             bg="#ffe7d9", fg="#993902", bd=2, relief="groove", labelanchor="n")
    section6.pack(pady=10)
    section6.pack_configure(anchor="center")

    tech_suggestion_tree = ttk.Treeview(section6, columns=("Plaka", "Arıza Kodu", "Öneri", "Durum"), show="headings", height=4)
    for col in tech_suggestion_tree["columns"]:
        tech_suggestion_tree.heading(col, text=col, anchor="center")
        tech_suggestion_tree.column(col, width=150, anchor="center")
    tech_suggestion_tree.pack(pady=5, fill="x")
    tech_suggestion_tree.pack_configure(anchor="center")
    ttk.Button(section6, text="🔄 Teknisyen Tavsiyelerini Yükle", command=lambda: list_technician_suggestions(tech_suggestion_tree, user_id)).pack(pady=5)

    # Bakım Kayıtları
    section7 = tk.LabelFrame(scrollable_frame, text="\U0001F4D2 Geçmiş Bakım Kayıtları", font=("Arial", 15, "bold"),
                             bg="#ffe7d9", fg="#993902", bd=2, relief="groove", labelanchor="n")
    section7.pack(pady=10)
    section7.pack_configure(anchor="center")

    maintenance_tree = ttk.Treeview(section7, columns=("ID", "Plaka", "Tarih", "Tip", "KM", "Maliyet"), show="headings", height=4)
    for col in maintenance_tree["columns"]:
        maintenance_tree.heading(col, text=col, anchor="center")
        maintenance_tree.column(col, width=130, anchor="center")
    maintenance_tree.pack(pady=5, fill="x")
    maintenance_tree.pack_configure(anchor="center")
    ttk.Button(section7, text="Bakım Geçmişini Göster", command=lambda: list_maintenances(maintenance_tree, user_id)).pack(pady=5)

    def on_closing():
        window.destroy()
        sys.exit()
    window.protocol("WM_DELETE_WINDOW", on_closing)

# Veritabanı işlemleri
def insert_vehicle(user_id, plate, brand, model, engine_type, kilometers):
    if not all([plate, brand, model, engine_type, kilometers]):
        messagebox.showwarning("Eksik Bilgi", "Tüm alanları doldurun.")
        return

    conn = connect_to_database()
    if conn:
        try:
            cursor = conn.cursor()
            query = """
            INSERT INTO Vehicles (plate, brand, model, engine_type, kilometers, user_id)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (plate, brand, model, engine_type, kilometers, user_id))
            conn.commit()
            messagebox.showinfo("Başarılı", "Araç eklendi.")
        except Exception as e:
            messagebox.showerror("Hata", str(e))
        finally:
            conn.close()

def list_user_vehicles(tree, user_id):
    for i in tree.get_children():
        tree.delete(i)

    conn = connect_to_database()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT vehicle_id, plate, brand, model, engine_type, kilometers FROM Vehicles WHERE user_id = %s", (user_id,))
        for row in cursor.fetchall():
            tree.insert("", "end", values=row)
        conn.close()

def insert_fault(vehicle_id, description, fault_code):
    if not (vehicle_id and description and fault_code):
        messagebox.showwarning("Eksik", "Tüm alanları doldurun.")
        return

    conn = connect_to_database()
    if conn:
        try:
            cursor = conn.cursor()

            # 1. Arızayı ekle
            insert_fault_query = """
                INSERT INTO VehicleFaults (report_date, description, vehicle_id, fault_code)
                VALUES (CURDATE(), %s, %s, %s)
            """
            cursor.execute(insert_fault_query, (description, vehicle_id, fault_code))
            fault_id = cursor.lastrowid

            # 2. Kullanıcı ID’sini aracın sahibinden al
            cursor.execute("SELECT user_id FROM Vehicles WHERE vehicle_id = %s", (vehicle_id,))
            user_id_result = cursor.fetchone()
            if not user_id_result:
                messagebox.showerror("Hata", "Araç bulunamadı.")
                return
            user_id = user_id_result[0]

            # 3. Eğer hata kodu AUTO101 (veya özel kod) ise öneri üretmeden çık
            if fault_code == "AUTO101":
                messagebox.showinfo("Bilgi", "Arıza kaydı eklendi. Bu kod için öneri sistem tarafından oluşturulmayacak.")
                conn.commit()
                return

            # 4. fault_code’a uygun rule_id’yi bul
            rule_mapping = {
                'P0420': 1,
                'P0300': 2,
                'C1234': 3,
                'P0421': 4,
                'P1234': 5,
                'P5678': 6,
                'AUTO101': 99999
                # İsteğe bağlı genişletilebilir
            }

            rule_id = rule_mapping.get(fault_code)
            if not rule_id:
                messagebox.showwarning("Bilgi", f"{fault_code} için eşleşen bir rule_id bulunamadı. Arıza kaydedildi, öneri oluşturulmadı.")
                conn.commit()
                return

            # 5. Rule ID'den öneri metnini al
            cursor.execute("SELECT recommendation_text FROM MaintenanceRules WHERE rule_id = %s AND active = TRUE", (rule_id,))
            rule_result = cursor.fetchone()
            if not rule_result:
                messagebox.showwarning("Kural Eksik", f"Rule ID {rule_id} için aktif kural bulunamadı.")
                conn.commit()
                return

            suggestion_text = rule_result[0]

            # 6. Öneriyi kaydet
            insert_suggestion_query = """
                INSERT INTO MaintenanceSuggestions
                (suggestion_text, suggestion_date, status, vehicle_id, fault_id, rule_id, user_id)
                VALUES (%s, CURDATE(), 'pending', %s, %s, %s, %s)
            """
            cursor.execute(insert_suggestion_query, (suggestion_text, vehicle_id, fault_id, rule_id, user_id))
            conn.commit()

            messagebox.showinfo("Başarılı", "Arıza ve öneri başarıyla eklendi.")
        except Exception as e:
            messagebox.showerror("Hata", str(e))
        finally:
            conn.close()


def list_suggestions(tree, user_id):
    for i in tree.get_children():
        tree.delete(i)

    conn = connect_to_database()
    if conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT s.suggestion_id, v.plate, f.fault_code, s.suggestion_text, s.status
            FROM MaintenanceSuggestions s
            JOIN Vehicles v ON s.vehicle_id = v.vehicle_id
            JOIN VehicleFaults f ON s.fault_id = f.fault_id
            WHERE v.user_id = %s AND s.status = 'approved' AND s.rule_id <> 99999
        """, (user_id,))
        for row in cursor.fetchall():
            tree.insert("", "end", values=row)
        conn.close()

def list_maintenances(tree, user_id):
    for i in tree.get_children():
        tree.delete(i)

    conn = connect_to_database()
    if conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT m.maintenance_id, v.plate, m.service_date, m.maintenance_type,
                   m.kilometers_at_service, m.cost
            FROM Maintenances m
            JOIN Vehicles v ON m.vehicle_id = v.vehicle_id
            WHERE v.user_id = %s
        """, (user_id,))
        for row in cursor.fetchall():
            tree.insert("", "end", values=row)
        conn.close()

def list_fault_codes(tree):
    for i in tree.get_children():
        tree.delete(i)

    conn = connect_to_database()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT fault_code, fault_description
                FROM FaultCodes
                ORDER BY
                    CASE WHEN fault_code = 'AUTO101' THEN 0 ELSE 1 END,
                    fault_code ASC
            """)
            for row in cursor.fetchall():
                tree.insert("", "end", values=row)
        except Exception as e:
            messagebox.showerror("Hata", str(e))
        finally:
            conn.close()

def list_technician_suggestions(tree, user_id):
    tree.delete(*tree.get_children())
    conn = connect_to_database()
    if conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT v.plate, f.fault_code, s.suggestion_text, s.status
            FROM MaintenanceSuggestions s
            JOIN Vehicles v ON s.vehicle_id = v.vehicle_id
            JOIN VehicleFaults f ON s.fault_id = f.fault_id
            WHERE s.user_id = %s AND s.rule_id = 99999
        """, (user_id,))
        for row in cursor.fetchall():
            tree.insert("", "end", values=row)
        conn.close()