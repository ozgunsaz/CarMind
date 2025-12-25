import tkinter as tk
import sys
from tkinter import ttk, messagebox
from db_connection import connect_to_database

def open_admin_panel():
    admin_window = tk.Toplevel()
    admin_window.title("Admin Paneli")
    admin_window.geometry("1300x800")
    admin_window.configure(bg="#ff8f4f")

    panel = tk.Frame(admin_window, bg="#ffe7d9")
    panel.place(relx=0.5, rely=0.5, anchor="center", width=1000, height=700)

    style = ttk.Style()
    style.theme_use("clam")

    style.configure("TButton", font=("Arial", 14), padding=6, background="#993902", foreground="white")
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
        font=("Arial", 20),
        padding=5
    )
    style.map("TCombobox",
        fieldbackground=[("readonly", "white")],
        bordercolor=[("focus", "#993902"), ("!focus", "#878787")],
        foreground=[("readonly", "black")]
    )

    tk.Label(panel, text="\U0001F451 Admin Paneli", font=("Arial", 35, "bold"), bg="#ffe7d9", fg="#993902").pack(pady=20)

       # Treeview + Dikey Scrollbar kapsayıcı frame
    tree_frame = tk.Frame(panel)
    tree_frame.pack(pady=10, fill="both", expand=True)

    tree_scroll_y = tk.Scrollbar(tree_frame, orient="vertical")
    tree_scroll_y.pack(side="right", fill="y")

    tree = ttk.Treeview(
        tree_frame,
        columns=("ID", "Kullanıcı Adı", "E-posta", "Rol"),
        show="headings",
        yscrollcommand=tree_scroll_y.set
    )

    tree_scroll_y.config(command=tree.yview)

    for col in tree["columns"]:
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=180)

    tree.pack(fill="both", expand=True)


    ttk.Button(panel, text="\U0001F465 Kullanıcıları Listele", command=lambda: list_users(tree)).pack(pady=10)

    form_frame = tk.Frame(panel, bg="#ffe7d9")
    form_frame.pack(pady=10)

    username_entry = ttk.Entry(form_frame, width=30, font=("Arial", 14), style="Custom.TEntry")
    username_entry.insert(0, "Kullanıcı Adı")
    username_entry.grid(row=0, column=0, padx=10, pady=5, ipady=5)

    password_entry = ttk.Entry(form_frame, width=30, font=("Arial", 14), show="*", style="Custom.TEntry")
    password_entry.insert(0, "Şifre")
    password_entry.grid(row=0, column=1, padx=10, pady=5, ipady=5)

    email_entry = ttk.Entry(form_frame, width=30, font=("Arial", 14), style="Custom.TEntry")
    email_entry.insert(0, "E-posta")
    email_entry.grid(row=1, column=0, padx=10, pady=5, ipady=5)

    role_entry = ttk.Combobox(form_frame, values=["user", "technician", "admin"], width=28, font=("Arial", 14), state="readonly")
    role_entry.set("user")
    role_entry.grid(row=1, column=1, padx=10, pady=5)

    ttk.Button(panel, text="➕ Kullanıcı Ekle", command=lambda: add_user(username_entry.get(), password_entry.get(), email_entry.get(), role_entry.get(), tree)).pack(pady=10)
    ttk.Button(panel, text="✏️ Kullanıcı Güncelle", command=lambda: update_selected_user(tree, username_entry, password_entry, email_entry, role_entry)).pack(pady=5)
    ttk.Button(panel, text="❌ Kullanıcı Sil", command=lambda: delete_selected_user(tree)).pack(pady=5)

    def on_closing():
        admin_window.destroy()
        sys.exit()

    admin_window.protocol("WM_DELETE_WINDOW", on_closing)

def add_user(username, password, email, role, tree):
    conn = connect_to_database()
    if conn:
        try:
            cursor = conn.cursor()
            query = "INSERT INTO Users (username, password, email, role, created_at) VALUES (%s, %s, %s, %s, CURDATE())"
            cursor.execute(query, (username, password, email, role))
            conn.commit()
            messagebox.showinfo("Başarılı", "Yeni kullanıcı eklendi.")
            list_users(tree)
        except Exception as e:
            messagebox.showerror("Hata", f"Kullanıcı eklenemedi: {e}")
        finally:
            conn.close()

def update_selected_user(tree, username_entry, password_entry, email_entry, role_entry):
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Uyarı", "Lütfen güncellemek için bir kullanıcı seçin.")
        return

    user_id = tree.item(selected_item)["values"][0]
    username = username_entry.get()
    password = password_entry.get()
    email = email_entry.get()
    role = role_entry.get()

    try:
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Users 
            SET username=%s, password=%s, email=%s, role=%s 
            WHERE user_id=%s
        """, (username, password, email, role, user_id))
        conn.commit()
        conn.close()
        messagebox.showinfo("Başarılı", "Kullanıcı güncellendi.")
        list_users(tree)
    except Exception as e:
        messagebox.showerror("Hata", f"Kullanıcı güncellenemedi: {e}")

def delete_selected_user(tree):
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Uyarı", "Lütfen silmek için bir kullanıcı seçin.")
        return

    user_id = tree.item(selected_item)["values"][0]

    try:
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Users WHERE user_id = %s", (user_id,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Başarılı", "Kullanıcı silindi.")
        list_users(tree)
    except Exception as e:
        messagebox.showerror("Hata", f"Kullanıcı silinemedi: {e}")

def list_users(tree):
    for item in tree.get_children():
        tree.delete(item)

    conn = connect_to_database()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT user_id, username, email, role FROM Users")
            results = cursor.fetchall()
            for row in results:
                tree.insert("", "end", values=row)
        except Exception as e:
            messagebox.showerror("Hata", f"Listeleme hatası: {e}")
        finally:
            conn.close()
