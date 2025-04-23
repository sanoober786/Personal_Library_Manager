import streamlit as st
import json
import os

st.set_page_config(page_title="📚 Personal Library Manager", layout="wide")

DATA_FILE = "library.json"

# Load and Save Function
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return[]

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def add_book(book, library):
    library.append(book)
    save_data(library)

def delete_book(index, library):
    del library[index]
    save_data(library)

# Title & Intro 
st.title("📚 Personal Library Manager")
st.write("Welcome! 👋 This app helps you keep track of the books you own, want to read, or already finished. You can:")
st.markdown("""
- ➕ Add new books
- 🔍 Search by title or author
- ✅ Mark books as read/unread
- ❌ Delete books
"""
     )
# Load library
library = load_data()

# --- Sidebar : Add Book ---
st.sidebar.title("➕ Add a New Book")
st.sidebar.write("Fill out the form below to add a book to your personal library.")

with st.sidebar.form("add_book_form"):
    title = st.text_input("📖 Book Title")
    author = st.text_input("✍️ Author")
    genre = st.text_input("🎨 Genre")
    year = st.number_input("📅 Year Published", min_value=0, max_value=2100, step=1)
    read = st.checkbox("✅ I've read this")
    submitted = st.form_submit_button("📥 Add Book")
    if submitted and title and author:
        new_book = {
            "title": title,
            "author": author,
            "genre": genre,
            "year": year,
            "read": read
        }
        add_book(new_book, library)
        st.success(f"🎉 Book added: '{title}' by {author}")
        st.experimental_rerun()
    elif submitted:
        st.warning("⚠️ Please enter at least the title and author.")

           # --- Search & List View ---
st.header("📚 Your Book Collection")

search = st.text_input("🔍 Search for a book by title or author")
filtered_books = [
        book for book in library
        if search.lower() in book["title"].lower() or search.lower() in book["author"].lower()
    ]

if filtered_books:
        for i, book in enumerate(filtered_books):
            with st.expander(f"📖 {book['title']} by {book['author']}"):
                cols = st.columns([3, 2, 2, 1])
                cols[0].markdown(f"**Genre:** {book['genre'] or 'Not specified'} \n**Year:** {book['year']}")
                status = "✅ Read" if book["read"] else "📖 Not read yet"
                cols[1].markdown(f"**Status:** {status}")
                if cols[2].button("🔁 Toggle Read", key = f"toggle_{i}"):
                    book["read"] = not book["read"]
                    save_data(library)
                    st.experimental_rerun()
                if cols[3].button("🗑️ Delete", key= f"delete_{i}"):
                    delete_book(i, library)
                    st.warning(f"🗑️ Deleted '{book['title']}'")
                    st.experimental_rerun()

else: 
     st.info("No books match your search. Try changing the title or author name.") 

# Footer
st.markdown("---")
st.caption("📘 Build with ❤️ using Streamlit")


