import sqlite3

def create_table():
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    
    # Create table if not exists with genre column
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            year INTEGER,
            genre TEXT,
            read_status TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

def add_book(title, author, year, genre, read_status):
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO books (title, author, year, genre, read_status) 
        VALUES (?, ?, ?, ?, ?)
    """, (title, author, year, genre, read_status))
    
    conn.commit()
    conn.close()

def main():
    create_table()  # Ensure table is created
    
    title = input("Enter book title: ")
    author = input("Enter author name: ")
    year = int(input("Enter publication year: "))
    genre = input("Enter genre: ")
    read_status = input("Enter read status (Read/Unread): ")
    
    add_book(title, author, year, genre, read_status)
    print("Book added successfully!")

if __name__ == "__main__":
    main()
