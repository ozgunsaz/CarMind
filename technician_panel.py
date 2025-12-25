import tkinter as tk
import sys
from tkinter import messagebox, ttk
from db_connection import connect_to_database
from report_panel import open_report_panel

def open_technician_panel(technician_id):

    root = tk.Toplevel()
    root.title("Teknisyen Paneli")
    root.geometry("1250x750")
    root.configure(bg="#ff8f4f")

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TButton", font=("Arial", 15), padding=6, background="#993902", foreground="white")
    style.map("TButton", background=[("active", "#6b2802")], foreground=[("active", "white")])

    style.configure("Custom.TEntry",
        fieldbackground="#fff",
        bordercolor="#878787",
        borderwidth=2,
        relief="flat",
        foreground="#000"
    )
    style.map("Custom.TEntry",
        bordercolor=[("focus", "#993902"), ("!focus", "#878787")],
        lightcolor=[("focus", "#993902"), ("!focus", "#878787")],
        highlightcolor=[("focus", "#993902"), ("!focus", "#878787")]
    )

    style.configure("Treeview.Heading",
        background="#993902",
        foreground="white",
        font=("Arial", 14, "bold")
    )
    style.configure("Treeview",
        font=("Arial", 13)
    )
    style.map("Treeview",
        background=[("selected", "#ffe7d9")],
        foreground=[("selected", "black")]
    )
    style.configure("TCombobox",
        font=("Arial", 14),
        padding=5
    )
    style.map("TCombobox",
        fieldbackground=[("readonly", "white")],
        bordercolor=[("focus", "#993902"), ("!focus", "#878787")],
        foreground=[("readonly", "black")]
    )


    panel = tk.Frame(root, bg="#ffe7d9", bd=0, highlightthickness=0)
    panel.place(relx=0.5, rely=0.5, anchor="center", width=1000, height=800)

    canvas = tk.Canvas(panel, bg="#ffe7d9", highlightthickness=0)
    scrollbar = tk.Scrollbar(panel, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    frame = tk.Frame(canvas, bg="#ffe7d9")
    frame_id = canvas.create_window((500, 0), window=frame, anchor="n")
    canvas.bind("<Configure>", lambda e: canvas.coords(frame_id, e.width / 2, 0))

    def on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    frame.bind("<Configure>", on_frame_configure)

    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    canvas.bind_all("<MouseWheel>", _on_mousewheel)

    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("SELECT full_name FROM Users WHERE user_id = %s", (technician_id,))
    result = cursor.fetchone()
    full_name = result[0] if result else "Teknisyen"
    conn.close()

    tk.Label(frame, text="🔧 Teknisyen Paneli", font=("Arial", 40, "bold"), bg="#ffe7d9", fg="#993902").pack(pady=20)
    tk.Label(frame, text=f"Hoş geldiniz, {full_name}!", font=("Arial", 20, "bold"), bg="#ffe7d9", fg="#993902").pack(pady=10)


    section1 = tk.LabelFrame(frame, text="🔧 Bekleyen Öneriler", font=("Arial", 18, "bold"), bg="#ffe7d9", fg="#993902", bd=2, relief="groove", labelanchor="n")
    section1.pack(pady=10, fill="x")
    pending_tree = ttk.Treeview(section1, columns=("ID", "Araç", "Model", "Plaka", "Arıza", "Kod", "Öneri", "Durum"), show="headings", height=6)
    for col in pending_tree["columns"]:
        pending_tree.heading(col, text=col, anchor="center")
        pending_tree.column(col, anchor="center", stretch=True, minwidth=0, width=1)
    pending_tree.pack(pady=5, fill="x")

    btn_frame1 = tk.Frame(section1, bg="#ffe7d9")
    btn_frame1.pack(pady=5)
    ttk.Button(btn_frame1, text="📋 Bekleyenleri Listele", command=lambda: list_pending_suggestions(pending_tree), width=18).pack(side="left", padx=10)
    ttk.Button(btn_frame1, text="✅ Onayla", command=lambda: update_suggestion_status(pending_tree, 'approved', technician_id), width=12).pack(side="left", padx=10)
    ttk.Button(btn_frame1, text="❌ Reddet", command=lambda: update_suggestion_status(pending_tree, 'declined', technician_id), width=12).pack(side="left", padx=10)

    section2 = tk.LabelFrame(frame, text="🛠️ Kuralsız Arızalar için Öneri (AUTO101)", font=("Arial", 18, "bold"), bg="#ffe7d9", fg="#993902", bd=2, relief="groove", labelanchor="n")
    section2.pack(pady=10, fill="x")
    auto_tree = ttk.Treeview(section2, columns=("Fault ID", "Plate", "Description"), show="headings", height=4)
    for col in auto_tree["columns"]:
        auto_tree.heading(col, text=col, anchor="center")
        auto_tree.column(col, anchor="center", stretch=True, minwidth=0, width=1)
    auto_tree.pack(pady=5, fill="x")

    btn_frame2 = tk.Frame(section2, bg="#ffe7d9")
    btn_frame2.pack(pady=5)
    ttk.Button(btn_frame2, text="🔄 AUTO101 Arızaları Yükle", command=lambda: list_auto101_faults(auto_tree), width=25).pack(side="left", padx=10)

    manual_frame = tk.Frame(section2, bg="#ffe7d9")
    manual_frame.pack(pady=5)
    tk.Label(manual_frame, text="Öneri Metni:", font=("Arial", 14), bg="#ffe7d9", fg="#993902").grid(row=0, column=0, padx=5, pady=5)
    auto_suggestion_entry = ttk.Entry(manual_frame, width=50, font=("Arial", 13), style="Custom.TEntry")
    auto_suggestion_entry.grid(row=0, column=1, padx=5, pady=5, ipady=4)
    ttk.Button(manual_frame, text="➕ Öneri Ekle", command=lambda: insert_auto101_suggestion(auto_tree, auto_suggestion_entry.get(), technician_id), width=18).grid(row=0, column=2, padx=10)

    section3 = tk.LabelFrame(frame, text="🛠️ Bakım Kaydı Ekle", font=("Arial", 18, "bold"), bg="#ffe7d9", fg="#993902", bd=2, relief="groove", labelanchor="n")
    section3.pack(pady=10, fill="x")
    maint_frame = tk.Frame(section3, bg="#ffe7d9")
    maint_frame.pack(pady=5)
    tk.Label(maint_frame, text="Onaylı Öneri:", font=("Arial", 14), bg="#ffe7d9", fg="#993902").grid(row=0, column=0, padx=5, pady=5)
    approved_combo = ttk.Combobox(maint_frame, width=45, font=("Arial", 13), state="readonly")
    approved_combo.grid(row=0, column=1, padx=5, pady=5, ipady=4)
    populate_approved_suggestions(approved_combo)

    tk.Label(maint_frame, text="Tarih (YYYY-MM-DD):", font=("Arial", 14), bg="#ffe7d9", fg="#993902").grid(row=1, column=0, padx=5, pady=5)
    date_entry = ttk.Entry(maint_frame, width=20, font=("Arial", 13), style="Custom.TEntry")
    date_entry.grid(row=1, column=1, padx=5, pady=5, ipady=4)

    tk.Label(maint_frame, text="Bakım Türü:", font=("Arial", 14), bg="#ffe7d9", fg="#993902").grid(row=2, column=0, padx=5, pady=5)
    type_entry = ttk.Entry(maint_frame, width=20, font=("Arial", 13), style="Custom.TEntry")
    type_entry.grid(row=2, column=1, padx=5, pady=5, ipady=4)

    tk.Label(maint_frame, text="Kilometre:", font=("Arial", 14), bg="#ffe7d9", fg="#993902").grid(row=3, column=0, padx=5, pady=5)
    km_entry = ttk.Entry(maint_frame, width=20, font=("Arial", 13), style="Custom.TEntry")
    km_entry.grid(row=3, column=1, padx=5, pady=5, ipady=4)

    tk.Label(maint_frame, text="Maliyet:", font=("Arial", 14), bg="#ffe7d9", fg="#993902").grid(row=4, column=0, padx=5, pady=5)
    cost_entry = ttk.Entry(maint_frame, width=20, font=("Arial", 13), style="Custom.TEntry")
    cost_entry.grid(row=4, column=1, padx=5, pady=5, ipady=4)

    ttk.Button(section3, text="➕ Bakım Kaydı Ekle", command=lambda: insert_maintenance_from_suggestion(
        approved_combo.get(), date_entry.get(), type_entry.get(), km_entry.get(), cost_entry.get()
    ), width=25).pack(pady=10)

    # --- Geçmiş Öneriler ---
    section4 = tk.LabelFrame(frame, text="📜 Onaylanmış / Reddedilmiş Öneriler", font=("Arial", 18, "bold"), bg="#ffe7d9", fg="#993902", bd=2, relief="groove", labelanchor="n")
    section4.pack(pady=10, fill="x")
    history_tree = ttk.Treeview(section4, columns=("ID", "Araç", "Kod", "Öneri", "Durum"), show="headings", height=5)
    for col in history_tree["columns"]:
        history_tree.heading(col, text=col, anchor="center")
        history_tree.column(col, anchor="center", stretch=True, minwidth=0, width=1)
    history_tree.pack(pady=5, fill="x")
    ttk.Button(section4, text="📁 Geçmişi Listele", command=lambda: list_old_suggestions(history_tree, technician_id), width=22).pack(pady=5)

    ttk.Button(frame, text="📊 Raporları Görüntüle", command=open_report_panel, width=25).pack(pady=15)

    def on_closing():
        root.destroy()
        sys.exit()

    root.protocol("WM_DELETE_WINDOW", on_closing)


def list_pending_suggestions(tree):
    tree.delete(*tree.get_children())
    conn = connect_to_database()
    if conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT s.suggestion_id, v.brand, v.model, v.plate, f.description, f.fault_code, s.suggestion_text, s.status
            FROM MaintenanceSuggestions s
            JOIN Vehicles v ON s.vehicle_id = v.vehicle_id
            JOIN VehicleFaults f ON s.fault_id = f.fault_id
            WHERE s.status = 'pending'
        """)
        for row in cursor.fetchall():
            tree.insert("", "end", values=row)
        conn.close()

def update_suggestion_status(tree, new_status, user_id):
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Uyarı", "Lütfen bir öneri seçin.")
        return
    suggestion_id = tree.item(selected)["values"][0]
    conn = connect_to_database()
    if conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE MaintenanceSuggestions SET status = %s WHERE suggestion_id = %s", (new_status, suggestion_id))
        conn.commit()
        conn.close()
        messagebox.showinfo("Başarılı", f"Öneri {new_status} olarak güncellendi.")
        list_pending_suggestions(tree)


def list_old_suggestions(tree, user_id):
    tree.delete(*tree.get_children())
    conn = connect_to_database()
    if conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT s.suggestion_id, v.plate, f.fault_code, s.suggestion_text, s.status
            FROM MaintenanceSuggestions s
            JOIN Vehicles v ON s.vehicle_id = v.vehicle_id
            JOIN VehicleFaults f ON s.fault_id = f.fault_id
            WHERE s.status IN ('approved', 'declined')
""")

        for row in cursor.fetchall():
            tree.insert("", "end", values=row)
        conn.close()

def populate_approved_suggestions(combo):
    conn = connect_to_database()
    if conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT suggestion_id, suggestion_text FROM MaintenanceSuggestions WHERE status = 'approved'
        """)
        results = cursor.fetchall()
        if results:
            combo['values'] = [f"{sid} - {text}" for sid, text in results]
        conn.close()

def insert_maintenance_from_suggestion(combo_value, date, maint_type, km, cost):
    if not (combo_value and date and maint_type and km and cost):
        messagebox.showerror("Eksik Bilgi", "Tüm alanlar doldurulmalı.")
        return
    try:
        suggestion_id = int(combo_value.split(" - ")[0])
    except:
        messagebox.showerror("Hata", "Öneri ID okunamadı.")
        return
    conn = connect_to_database()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT vehicle_id, user_id FROM MaintenanceSuggestions WHERE suggestion_id = %s", (suggestion_id,))
        result = cursor.fetchone()
        if not result:
            messagebox.showerror("Hata", "Öneri bulunamadı.")
            return
        vehicle_id, user_id = result
        cursor.execute("""
            INSERT INTO Maintenances (service_date, maintenance_type, kilometers_at_service, cost, vehicle_id, user_id)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (date, maint_type, km, cost, vehicle_id, user_id))
        
        cursor.execute("UPDATE MaintenanceSuggestions SET status = 'completed' WHERE suggestion_id = %s", (suggestion_id,))
        
        conn.commit()
        conn.close()
        messagebox.showinfo("Başarılı", "Bakım kaydı başarıyla eklendi.")

def list_auto101_faults(tree):
    tree.delete(*tree.get_children())
    conn = connect_to_database()
    if conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT f.fault_id, v.plate, f.description
            FROM VehicleFaults f
            JOIN Vehicles v ON f.vehicle_id = v.vehicle_id
            WHERE f.fault_code = 'AUTO101'
            AND f.fault_id NOT IN (
                SELECT fault_id FROM MaintenanceSuggestions
            )
        """)
        for row in cursor.fetchall():
            tree.insert("", "end", values=row)
        conn.close()

def insert_auto101_suggestion(tree, suggestion_text, technician_id):
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Warning", "Please select a fault.")
        return
    if not suggestion_text:
        messagebox.showwarning("Warning", "Suggestion text cannot be empty.")
        return

    fault_id = tree.item(selected[0])["values"][0]
    conn = connect_to_database()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT vehicle_id FROM VehicleFaults WHERE fault_id = %s", (fault_id,))
        result = cursor.fetchone()
        if not result:
            messagebox.showerror("Error", "Vehicle not found.")
            return
        vehicle_id = result[0]

        cursor.execute("SELECT user_id FROM Vehicles WHERE vehicle_id = %s", (vehicle_id,))
        user_result = cursor.fetchone()
        if not user_result:
            messagebox.showerror("Error", "User not found.")
            return
        user_id = user_result[0]

        cursor.execute("""
            INSERT INTO MaintenanceSuggestions
            (suggestion_text, suggestion_date, status, vehicle_id, fault_id, rule_id, user_id)
            VALUES (%s, CURDATE(), 'approved', %s, %s, 99999, %s)
        """, (suggestion_text, vehicle_id, fault_id, user_id))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Suggestion added successfully.")
        list_auto101_faults(tree)
