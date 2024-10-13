from database import create_table, create_connection
from gui import root

def main():
    conn = create_connection()
    create_table(conn)
    root.mainloop()

if __name__ == "__main__":
    main()