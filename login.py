import tkinter as tk
from tkinter import messagebox, ttk
from db_connection import connect_to_database
from admin_panel import open_admin_panel
from technician_panel import open_technician_panel
from user_panel import open_user_panel

def login(event=None):
    email = entry_email.get().strip()   
    password = entry_password.get().strip()

    conn = connect_to_database()
    if conn:
        cursor = conn.cursor()
        query = "SELECT user_id, role FROM Users WHERE email = %s AND password = %s"
        cursor.execute(query, (email, password))
        result = cursor.fetchone()

        if result:
            user_id, role = result
            messagebox.showinfo("Login successful", f"Logged in. Your role: {role}")

            if role == "admin":
                open_admin_panel()
            elif role == "technician":
                open_technician_panel(user_id)
            elif role == "user":
                open_user_panel(user_id)
        else:
            messagebox.showerror("Error", "Invalid e-mail or password.")
        conn.close()

def register_user(entries, window):
    full_name, username, email, password = [e.get().strip() for e in entries]
    role = "user"

    if not all([full_name, username, email, password]):
        messagebox.showerror("Hata", "Tüm alanları doldurmalısınız.")
        return

    conn = connect_to_database()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Users WHERE email = %s OR username = %s", (email, username))
        if cursor.fetchone():
            messagebox.showerror("Hata", "Bu e-posta veya kullanıcı adı zaten kayıtlı.")
        else:
            cursor.execute("""
                INSERT INTO Users (full_name, username, email, password, role, created_at)
                VALUES (%s, %s, %s, %s, %s, CURDATE())
            """, (full_name, username, email, password, role))
            conn.commit()
            messagebox.showinfo("Başarılı", "Kayıt başarıyla oluşturuldu.")
            window.destroy()
        conn.close()

def open_register():
    register_window = tk.Toplevel()
    register_window.title("Register")
    register_window.geometry("1250x750")
    register_window.configure(bg="#ff8f4f")

    panel = tk.Frame(register_window, bg="#ffe7d9")
    panel.place(relx=0.5, rely=0.5, anchor="center", width=1000, height=800)

    style = ttk.Style()

    frame = tk.Frame(register_window, bg="#ffe7d9")
    frame.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(frame, text="📝 Register", font=("Arial", 45, "bold"), bg="#ffe7d9", fg="#993902").pack(pady=30)

    labels = ["Name&Surname:", "User Name:", "E-mail:", "Password:"]
    entries = []

    for label_text in labels:
        tk.Label(frame, text=label_text, font=("Arial", 20), bg="#ffe7d9", fg="#993902").pack(pady=(10,5))
        entry = ttk.Entry(frame, width=30, font=("Arial", 16), style="Custom.TEntry")
        entry.pack(pady=10, ipady=5)
        entries.append(entry)

    button_frame = tk.Frame(frame, bg="#ffe7d9")
    button_frame.pack(pady=30)

    register_btn = ttk.Button(button_frame, text="➕ Register", width=20,
                              command=lambda: register_user(entries, register_window))
    register_btn.pack(side="left", padx=20, pady=30)

    cancel_btn = ttk.Button(button_frame, text="❌ Cancel", width=20, command=register_window.destroy)
    cancel_btn.pack(side="left", padx=20, pady=30)


# Ana pencere
root = tk.Tk()
root.title("Ustalar Duymasın Login")
root.geometry("1250x750")
root.configure(bg="#ff8f4f")
root.resizable(True, True)

panel = tk.Frame(root, bg="#ffe7d9", bd=0, highlightthickness=0)
panel.place(relx=0.5, rely=0.5, anchor="center", width=1000, height=800)

# Stil ayarları
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

frame = tk.Frame(panel, bg="#ffe7d9")
frame.place(relx=0.5, rely=0.5, anchor="center")

tk.Label(frame, text="WELCOME", font=("Arial", 70, "bold"), bg="#ffe7d9", fg="#993902").pack(pady=20)
tk.Label(frame, text="🚗 Ustalar Duymasın Login Panel", font=("Arial", 30, "bold"), bg="#ffe7d9", fg="#993902").pack(pady=10)

email_label = tk.Label(frame, text="E-mail:", font=("Arial", 20), bg="#ffe7d9", fg="#993902")
email_label.pack(pady=(30, 10))
entry_email = ttk.Entry(frame, width=45, font=("Arial", 15), style="Custom.TEntry")
entry_email.pack(ipady=5)

password_label = tk.Label(frame, text="Password:", font=("Arial", 20), bg="#ffe7d9", fg="#993902")
password_label.pack(pady=(30, 10))
entry_password = ttk.Entry(frame, show="*", width=45, font=("Arial", 15), style="Custom.TEntry")
entry_password.pack(ipady=5)

button_frame = tk.Frame(frame, bg="#ffe7d9")
button_frame.pack(pady=30)

giris_button = ttk.Button(button_frame, text="🔐 Login", command=login, width=15)
giris_button.pack(side="left", padx=(0, 40), pady=30)

register_button = ttk.Button(button_frame, text="➕ Register", command=open_register, width=15)
register_button.pack(side="left", padx=(40, 0), pady=30)

root.bind('<Return>', login)
root.mainloop()
