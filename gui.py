import tkinter as tk
from tkinter import messagebox
from database import create_table, register_user, login_user, get_balance, deposit, withdraw, transfer, get_transaction_history, delete_user

create_table()

root = tk.Tk()
root.title("Aplikacja Bankowa")
root.geometry("400x300")
root.configure(bg="#f0f0f0")

def register_account():
    user_id = entry_user_id.get()
    name = entry_name.get()
    pin = entry_pin.get()

    if user_id and name and pin:
        register_user(user_id, name, pin)
        messagebox.showinfo("Rejestracja", "Konto zostało zarejestrowane.")
    else:
        messagebox.showwarning("Błąd", "Wypełnij wszystkie pola.")

def login():
    user_id = entry_user_id.get()
    pin = entry_pin.get()

    account = login_user(user_id, pin)
    if account:
        messagebox.showinfo("Logowanie", f"Zalogowano jako {account[1]}")
        main_menu(user_id)
    else:
        messagebox.showwarning("Błąd", "Nieprawidłowy identyfikator lub PIN.")

def delete_account():
    user_id = entry_user_id.get()
    name = entry_name.get()
    pin=entry_pin.get()

    if user_id and name and pin:
        delete_user(user_id, name, pin)
        messagebox.showinfo("Usuwanie", "Konto zostało usunięte.")
    else:
        messagebox.showwarning("Błąd", "Wypełnij wszytskie pola.")



def main_menu(user_id):
    main_window = tk.Toplevel()
    main_window.title("Menu Główne")
    main_window.geometry("400x400")
    main_window.configure(bg="#e0e0e0")

    def show_balance():
        balance = get_balance(user_id)
        messagebox.showinfo("Saldo", f"Twoje saldo: {balance}")

    def deposit_amount():
        amount = float(entry_amount.get())
        deposit(user_id, amount)
        messagebox.showinfo("Wpłata", "Wpłata została zrealizowana.")

    def withdraw_amount():
        amount = float(entry_amount.get())
        withdraw(user_id, amount)
        messagebox.showinfo("Wypłata", "Wypłata została zrealizowana.")

    def transfer_amount():
        user_id_to = entry_user_id_to.get()
        amount = float(entry_amount.get())
        transfer(user_id, user_id_to, amount)
        messagebox.showinfo("Transfer", "Transfer został zrealizowany.")

    def show_transactions():
        transactions = get_transaction_history(user_id)
        trans_str = '\n'.join([f"Typ: {t[0]}, Kwota: {t[1]}, Data: {t[2]}" for t in transactions])
        messagebox.showinfo("Historia Transakcji", trans_str if transactions else "Brak historii transakcji.")

    def logout():
        main_window.destroy()

    frame_inputs = tk.Frame(main_window, bg="#e0e0e0", pady=10)
    frame_inputs.pack(fill=tk.BOTH, expand=True)

    frame_buttons = tk.Frame(main_window, bg="#e0e0e0", pady=10)
    frame_buttons.pack(fill=tk.BOTH, expand=True)

    tk.Label(frame_inputs, text="Kwota:", bg="#e0e0e0").grid(row=0, column=0, padx=10, pady=5)
    entry_amount = tk.Entry(frame_inputs)
    entry_amount.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(frame_inputs, text="Identyfikator konta docelowego:", bg="#e0e0e0").grid(row=1, column=0, padx=10, pady=5)
    entry_user_id_to = tk.Entry(frame_inputs)
    entry_user_id_to.grid(row=1, column=1, padx=10, pady=5)

    tk.Button(frame_buttons, text="Sprawdzenie Salda", command=show_balance, bg="#4CAF50", fg="white").pack(pady=5, fill=tk.X)
    tk.Button(frame_buttons, text="Wpłata", command=deposit_amount, bg="#2196F3", fg="white").pack(pady=5, fill=tk.X)
    tk.Button(frame_buttons, text="Wypłata", command=withdraw_amount, bg="#FF9800", fg="white").pack(pady=5, fill=tk.X)
    tk.Button(frame_buttons, text="Transfer", command=transfer_amount, bg="#9C27B0", fg="white").pack(pady=5, fill=tk.X)
    tk.Button(frame_buttons, text="Historia Transakcji", command=show_transactions, bg="#607D8B", fg="white").pack(pady=5, fill=tk.X)
    tk.Button(frame_buttons, text="Wyloguj", command=logout, bg="#f44336", fg="white").pack(pady=5, fill=tk.X)

frame_main = tk.Frame(root, bg="#f0f0f0", pady=10)
frame_main.pack(fill=tk.BOTH, expand=True)

tk.Label(frame_main, text="Identyfikator użytkownika:", bg="#f0f0f0").grid(row=0, column=0, padx=10, pady=5)
entry_user_id = tk.Entry(frame_main)
entry_user_id.grid(row=0, column=1, padx=10, pady=5)

tk.Label(frame_main, text="Imię:", bg="#f0f0f0").grid(row=1, column=0, padx=10, pady=5)
entry_name = tk.Entry(frame_main)
entry_name.grid(row=1, column=1, padx=10, pady=5)

tk.Label(frame_main, text="PIN:", bg="#f0f0f0").grid(row=2, column=0, padx=10, pady=5)
entry_pin = tk.Entry(frame_main, show="*")
entry_pin.grid(row=2, column=1, padx=10, pady=5)

frame_buttons = tk.Frame(root, bg="#f0f0f0", pady=10)
frame_buttons.pack(fill=tk.BOTH, expand=True)

tk.Button(frame_buttons, text="Rejestracja", command=register_account, bg="green", fg="white").grid(row=0, column=0, padx=10, pady=5)
tk.Button(frame_buttons, text="Logowanie", command=login, bg="blue", fg="white").grid(row=0, column=1, padx=10, pady=5)
tk.Button(frame_buttons, text="Usuń konto", command=delete_account, bg="red", fg="white").grid(row=0, column=2, padx=10, pady=5)

root.mainloop()
