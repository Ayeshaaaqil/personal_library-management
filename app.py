import sqlite3
import streamlit as st

# Function to create the books table
def create_table():
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    
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

# Function to add a book
def add_book(title, author, year, genre, read_status):
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO books (title, author, year, genre, read_status) 
        VALUES (?, ?, ?, ?, ?)
    """, (title, author, year, genre, read_status))
    
    conn.commit()
    conn.close()

# Function to retrieve all books
def get_books():
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    
    conn.close()
    return books

# Function to search books
def search_books(query):
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM books WHERE title LIKE ? OR author LIKE ? OR genre LIKE ?", 
                   ('%' + query + '%', '%' + query + '%', '%' + query + '%'))
    books = cursor.fetchall()
    
    conn.close()
    return books

# Function to delete a book
def remove_book(book_id):
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
    conn.commit()
    conn.close()

# Function to get statistics
def get_statistics():
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM books")
    total_books = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM books WHERE read_status = 'Read'")
    read_books = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM books WHERE read_status = 'Unread'")
    unread_books = cursor.fetchone()[0]

    conn.close()
    
    return total_books, read_books, unread_books

# Streamlit UI
def main():
    st.title("📚 Personal Library Management System")
    
    # Sidebar for navigation
    menu = ["Add Book", "View All Books", "Search Books", "Remove Books", "Book Statistics"]
    choice = st.sidebar.selectbox("Menu", menu)
    
    create_table()

    if choice == "Add Book":
        st.subheader("➕ Add a New Book")
        
        title = st.text_input("Book Title")
        author = st.text_input("Author Name")
        year = st.number_input("Publication Year", min_value=1000, max_value=2100, step=1)
        genre = st.text_input("Genre")
        read_status = st.selectbox("Read Status", ["Read", "Unread"])
        
        if st.button("Add Book"):
            add_book(title, author, year, genre, read_status)
            st.success(f"Book '{title}' added successfully! 📖")

    elif choice == "View All Books":
        st.subheader("📖 Book Collection")
        books = get_books()
        
        if books:
            for book in books:
                st.write(f"**{book[1]}** by {book[2]} ({book[3]})")
                st.write(f"📚 Genre: {book[4]} | 📖 Status: {book[5]}")
                st.markdown("---")
        else:
            st.warning("No books found in the database.")

    elif choice == "Search Books":
        st.subheader("🔍 Search for Books")
        query = st.text_input("Enter book title, author, or genre:")
        
        if st.button("Search"):
            results = search_books(query)
            if results:
                for book in results:
                    st.write(f"**{book[1]}** by {book[2]} ({book[3]})")
                    st.write(f"📚 Genre: {book[4]} | 📖 Status: {book[5]}")
                    st.markdown("---")
            else:
                st.warning("No matching books found.")

    elif choice == "Remove Books":
        st.subheader("❌ Remove a Book")
        books = get_books()
        
        if books:
            book_options = {f"{book[1]} by {book[2]}": book[0] for book in books}
            selected_book = st.selectbox("Select a book to remove", list(book_options.keys()))
            
            if st.button("Remove Book"):
                remove_book(book_options[selected_book])
                st.success(f"Book '{selected_book}' removed successfully!")
                st.experimental_rerun()
        else:
            st.warning("No books available to remove.")

    elif choice == "Book Statistics":
        st.subheader("📊 Library Statistics")
        total, read, unread = get_statistics()
        
        st.write(f"📚 Total Books: **{total}**")
        st.write(f"📖 Read Books: **{read}**")
        st.write(f"📕 Unread Books: **{unread}**")

if __name__ == "__main__":
    main()
