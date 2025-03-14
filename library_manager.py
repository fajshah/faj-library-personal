import streamlit as st
import json

# File to save library data
LIBRARY_FILE = "library.json"

# Load library from file
def load_library():
    try:
        with open(LIBRARY_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Save library to file
def save_library(library):
    with open(LIBRARY_FILE, "w") as file:
        json.dump(library, file, indent=4)

# Initialize library
library = load_library()

# Add background image style with very light, study-themed image and fully pink sidebar
st.markdown(
    """
    <style>
    .stApp {
        background: url('https://images.unsplash.com/photo-1503676260728-1c00da094a0b');
        background-size: cover;
        background-position: center;
        color: #333333;
    }
    
    /* Fully pink sidebar */
    [data-testid="stSidebar"]
    {
        background-color: #D8BFD8 !important;
        border-radius: 10px;
    }
    
    /* Darker text for readability */
    .stMarkdown, .stTextInput, .stNumberInput, .stCheckbox, .stButton {
        color: #333333;
    }
    
    /* Red footer */
    .footer {
        color: red;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Streamlit app
st.title("📚 Personal Library Manager")

menu_option = st.sidebar.selectbox(
    "Menu", [
        "Add a Book",
        "Remove a Book",
        "Search for a Book",
        "Display All Books",
        "Display Statistics",
        "Exit",
    ]
)

if menu_option == "Add a Book":
    st.header("Add a Book")
    title = st.text_input("Enter the book title:")
    author = st.text_input("Enter the author:")
    year = st.number_input("Enter the publication year:", min_value=0, step=1)
    genre = st.text_input("Enter the genre:")
    read_status = st.checkbox("Have you read this book?")

    if st.button("Add Book"):
        library.append({
            "Title": title,
            "Author": author,
            "Year": year,
            "Genre": genre,
            "Read": read_status
        })
        save_library(library)
        st.success("Book added successfully!")

elif menu_option == "Remove a Book":
    st.header("Remove a Book")
    book_titles = [book["Title"] for book in library]
    title_to_remove = st.selectbox("Select a book to remove:", book_titles)
    
    if st.button("Remove Book"):
        library = [book for book in library if book["Title"] != title_to_remove]
        save_library(library)
        st.success(f"'{title_to_remove}' removed successfully!")

elif menu_option == "Search for a Book":
    st.header("Search for a Book")
    search_by = st.radio("Search by:", ["Title", "Author"])
    search_query = st.text_input(f"Enter the {search_by.lower()}:")

    if st.button("Search"):
        results = [
            book for book in library
            if search_query.lower() in book[search_by].lower()
        ]
        
        if results:
            for idx, book in enumerate(results, start=1):
                st.markdown(
                    f"**{idx}. {book['Title']} by {book['Author']} ({book['Year']}) - {book['Genre']} - {'Read' if book['Read'] else 'Unread'}**"
                )
        else:
            st.warning("No matching books found!")

elif menu_option == "Display All Books":
    st.header("Your Library")
    if library:
        for idx, book in enumerate(library, start=1):
            st.markdown(
                f"**{idx}. {book['Title']} by {book['Author']} ({book['Year']}) - {book['Genre']} - {'Read' if book['Read'] else 'Unread'}**"
            )
    else:
        st.info("Your library is empty!")

elif menu_option == "Display Statistics":
    st.header("Library Statistics")
    total_books = len(library)
    read_books = sum(1 for book in library if book['Read'])
    percentage_read = (read_books / total_books * 100) if total_books > 0 else 0

    st.write(f"Total books: {total_books}")
    st.write(f"Books read: {read_books}")
    st.write(f"Percentage read: {percentage_read:.2f}%")

elif menu_option == "Exit":
    st.success("Library saved to file. Goodbye! 👋")
    st.stop()

# Save library on app close
save_library(library)

# Footer
st.markdown("---")
st.markdown("<div class='footer'><b>Syeda Farzana Shah Library</b></div>", unsafe_allow_html=True)

