import streamlit as st
import json
import os
from datetime import datetime
import pandas as pd
import plotly.express as px

# Set page configuration
st.set_page_config(
    page_title="Personal Library Manager",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling with dark theme
st.markdown("""
<style>
    /* Main background and text colors */
    .main {
        background-color: #121212;
        color: #ffffff;
    }
    
    /* Custom container for content */
    .content-container {
        background-color: #1e1e1e;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
    }
    
    /* Headers */
    h1, h2, h3, h4, h5 {
        color: #00b4d8 !important;
        font-weight: bold;
    }
    
    /* Sidebar */
    .css-1d391kg, .css-hxt7ib {
        background-color: #212121;
    }
    
    /* Buttons */
    .stButton button {
        background-color: #00b4d8;
        color: #121212;
        border-radius: 5px;
        font-weight: bold;
        border: none;
    }
    
    .stButton button:hover {
        background-color: #48cae4;
    }
    
    /* Book cards */
    .book-card {
        background-color: #2a2a2a;
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 15px;
        border-left: 4px solid #00b4d8;
    }
    
    .book-title {
        font-size: 18px;
        font-weight: bold;
        color: #ffffff;
        margin-bottom: 5px;
    }
    
    .book-author {
        font-style: italic;
        color: #cccccc;
    }
    
    .book-details {
        margin-top: 8px;
        color: #aaaaaa;
    }
    
    /* Badges */
    .read-badge {
        background-color: #4caf50;
        color: #ffffff;
        padding: 3px 8px;
        border-radius: 4px;
        font-size: 12px;
    }
    
    .unread-badge {
        background-color: #f44336;
        color: #ffffff;
        padding: 3px 8px;
        border-radius: 4px;
        font-size: 12px;
    }
    
    /* Stats cards */
    .stats-card {
        background-color: #2a2a2a;
        border-radius: 8px;
        padding: 15px;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.3);
        text-align: center;
    }
    
    /* Input fields */
    .stTextInput, .stNumberInput, .stSelectbox {
        background-color: #2a2a2a;
    }
    
    .stTextInput input, .stNumberInput input, .stSelectbox select {
        color: #ffffff;
    }
    
    /* Plot background */
    .js-plotly-plot .plotly {
        background-color: #2a2a2a !important;
    }
    
    /* DataFrames */
    .dataframe {
        background-color: #2a2a2a !important;
    }
    
    /* Info messages */
    .stAlert {
        background-color: #2a2a2a;
        color: #ffffff;
    }
</style>
""", unsafe_allow_html=True)

# File path for the library data
LIBRARY_FILE = "library.json"

# Initialize session state
if "library" not in st.session_state:
    st.session_state.library = []
if "current_page" not in st.session_state:
    st.session_state.current_page = "Dashboard"
if "search_results" not in st.session_state:
    st.session_state.search_results = []
if "search_performed" not in st.session_state:
    st.session_state.search_performed = False

# Functions
def load_library():
    """Load the library from a JSON file if it exists."""
    if os.path.exists(LIBRARY_FILE):
        try:
            with open(LIBRARY_FILE, 'r') as file:
                st.session_state.library = json.load(file)
        except Exception as e:
            st.error(f"Error loading library: {e}")
            # Create default library
            create_default_library()
    else:
        # Create default library for first run
        create_default_library()

def create_default_library():
    """Create a default library with Python, JavaScript, Next.js, and motivational books."""
    default_books = [
        {
            "title": "Python Crash Course",
            "author": "Eric Matthes",
            "year": 2019,
            "genre": "Python",
            "read": True
        },
        {
            "title": "Fluent Python",
            "author": "Luciano Ramalho",
            "year": 2021,
            "genre": "Python",
            "read": False
        },
        {
            "title": "Eloquent JavaScript",
            "author": "Marijn Haverbeke",
            "year": 2018,
            "genre": "JavaScript",
            "read": True
        },
        {
            "title": "JavaScript: The Good Parts",
            "author": "Douglas Crockford",
            "year": 2008,
            "genre": "JavaScript",
            "read": False
        },
        {
            "title": "Next.js in Action",
            "author": "Adam Boduch",
            "year": 2021,
            "genre": "Next.js",
            "read": False
        },
        {
            "title": "The Complete Next.js Developer",
            "author": "Reed Barger",
            "year": 2022,
            "genre": "Next.js",
            "read": False
        },
        {
            "title": "Atomic Habits",
            "author": "James Clear",
            "year": 2018,
            "genre": "Motivational",
            "read": True
        },
        {
            "title": "Mindset: The New Psychology of Success",
            "author": "Carol S. Dweck",
            "year": 2006,
            "genre": "Motivational",
            "read": True
        },
        {
            "title": "Deep Work",
            "author": "Cal Newport",
            "year": 2016,
            "genre": "Motivational",
            "read": False
        },
        {
            "title": "The Python Data Science Handbook",
            "author": "Jake VanderPlas",
            "year": 2016,
            "genre": "Python",
            "read": False
        }
    ]
    
    st.session_state.library = default_books
    save_library()

def save_library():
    """Save the library to a JSON file."""
    try:
        with open(LIBRARY_FILE, 'w') as file:
            json.dump(st.session_state.library, file, indent=4)
        return True
    except Exception as e:
        st.error(f"Error saving library: {e}")
        return False

def navigate_to(page):
    """Navigate to a different page in the app."""
    st.session_state.current_page = page
    st.session_state.search_performed = False
    st.session_state.search_results = []

def add_book(title, author, year, genre, read_status):
    """Add a new book to the library."""
    # Check if book already exists
    for book in st.session_state.library:
        if book["title"].lower() == title.lower() and book["author"].lower() == author.lower():
            return False
    
    # Create book dictionary
    book = {
        "title": title,
        "author": author,
        "year": int(year),
        "genre": genre,
        "read": read_status
    }
    
    st.session_state.library.append(book)
    save_library()
    return True

def remove_book(index):
    """Remove a book from the library."""
    st.session_state.library.pop(index)
    save_library()

def toggle_read_status(index):
    """Toggle the read status of a book."""
    st.session_state.library[index]["read"] = not st.session_state.library[index]["read"]
    save_library()

def search_books(search_term, search_field):
    """Search for books in the library."""
    st.session_state.search_results = []
    
    for book in st.session_state.library:
        if search_term.lower() in book[search_field].lower():
            st.session_state.search_results.append(book)
    
    st.session_state.search_performed = True

# Load library data on app start
load_library()

# App header
st.markdown("<h1 style='text-align: center;'>📚 Personal Library Manager</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #aaaaaa;'>Manage your book collection with ease</p>", unsafe_allow_html=True)
st.markdown("---")

# Sidebar
with st.sidebar:
    st.markdown("<h2>📖 Navigation</h2>", unsafe_allow_html=True)
    
    if st.button("📊 Dashboard", use_container_width=True):
        navigate_to("Dashboard")
    
    if st.button("📚 View All Books", use_container_width=True):
        navigate_to("View Library")
    
    if st.button("➕ Add New Book", use_container_width=True):
        navigate_to("Add Book")
    
    if st.button("🔍 Search Books", use_container_width=True):
        navigate_to("Search Books")
    
    st.markdown("---")
    
    # Quick stats
    st.markdown("<h3>📈 Library Stats</h3>", unsafe_allow_html=True)
    
    if st.session_state.library:
        total_books = len(st.session_state.library)
        read_books = sum(1 for book in st.session_state.library if book["read"])
        unread_books = total_books - read_books
        percentage_read = (read_books / total_books) * 100 if total_books > 0 else 0
        
        st.markdown(f"**Total Books:** {total_books}")
        st.markdown(f"**Read:** {read_books} ({percentage_read:.1f}%)")
        st.markdown(f"**Unread:** {unread_books} ({100 - percentage_read:.1f}%)")
        
        # Genre breakdown
        genres = {}
        for book in st.session_state.library:
            if book["genre"] in genres:
                genres[book["genre"]] += 1
            else:
                genres[book["genre"]] = 1
        
        st.markdown("**Genre Breakdown:**")
        for genre, count in genres.items():
            st.markdown(f"- {genre}: {count}")
    else:
        st.markdown("No books in your library yet.")

# Main content
if st.session_state.current_page == "Dashboard":
    st.markdown("<h2>📊 Dashboard</h2>", unsafe_allow_html=True)
    
    if not st.session_state.library:
        st.info("Your library is empty. Add some books to get started!")
    else:
        # Create dataframe for analysis
        df = pd.DataFrame(st.session_state.library)
        
        # Top stats row
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="stats-card">
                <h3>Total Books</h3>
                <p style="font-size: 28px; font-weight: bold; color: #ffffff;">{}</p>
            </div>
            """.format(len(df)), unsafe_allow_html=True)
        
        with col2:
            read_percentage = (df["read"].sum() / len(df) * 100)
            st.markdown("""
            <div class="stats-card">
                <h3>Read Percentage</h3>
                <p style="font-size: 28px; font-weight: bold; color: #ffffff;">{:.1f}%</p>
            </div>
            """.format(read_percentage), unsafe_allow_html=True)
        
        with col3:
            genres_count = len(df["genre"].unique())
            st.markdown("""
            <div class="stats-card">
                <h3>Unique Genres</h3>
                <p style="font-size: 28px; font-weight: bold; color: #ffffff;">{}</p>
            </div>
            """.format(genres_count), unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("<h3>Genre Distribution</h3>", unsafe_allow_html=True)
            genre_counts = df["genre"].value_counts().reset_index()
            genre_counts.columns = ["Genre", "Count"]
            
            fig = px.pie(
                genre_counts, 
                values="Count", 
                names="Genre", 
                hole=0.4,
                color_discrete_sequence=px.colors.sequential.Blues_r
            )
            
            fig.update_layout(
                plot_bgcolor="#2a2a2a",
                paper_bgcolor="#2a2a2a",
                font=dict(color="#ffffff"),
                margin=dict(t=30, b=30, l=30, r=30)
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("<h3>Read vs Unread</h3>", unsafe_allow_html=True)
            read_by_genre = df.groupby(["genre", "read"]).size().reset_index(name="count")
            read_by_genre["read_status"] = read_by_genre["read"].apply(lambda x: "Read" if x else "Unread")
            
            fig = px.bar(
                read_by_genre, 
                x="genre", 
                y="count", 
                color="read_status", 
                barmode="group",
                color_discrete_sequence=["#4caf50", "#f44336"]
            )
            
            fig.update_layout(
                xaxis_title="Genre",
                yaxis_title="Number of Books",
                plot_bgcolor="#2a2a2a",
                paper_bgcolor="#2a2a2a",
                font=dict(color="#ffffff"),
                legend_title="Status",
                margin=dict(t=30, b=30, l=30, r=30)
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Books by year
        st.markdown("<h3>Books by Publication Year</h3>", unsafe_allow_html=True)
        
        year_counts = df.groupby("year").size().reset_index(name="count")
        
        fig = px.line(
            year_counts, 
            x="year", 
            y="count",
            markers=True,
            line_shape="linear",
            color_discrete_sequence=["#00b4d8"]
        )
        
        fig.update_layout(
            xaxis_title="Publication Year",
            yaxis_title="Number of Books",
            plot_bgcolor="#2a2a2a",
            paper_bgcolor="#2a2a2a",
            font=dict(color="#ffffff"),
            margin=dict(t=30, b=30, l=30, r=30)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Recently added books
        st.markdown("<h3>Recently Added Books</h3>", unsafe_allow_html=True)
        
        recent_books = st.session_state.library[-3:]  # Last 3 books
        recent_books.reverse()  # Latest first
        
        for book in recent_books:
            read_status = "Read" if book["read"] else "Unread"
            badge_class = "read-badge" if book["read"] else "unread-badge"
            
            st.markdown(f"""
            <div class="book-card">
                <div class="book-title">{book["title"]}</div>
                <div class="book-author">by {book["author"]}</div>
                <div class="book-details">
                    {book["genre"]} • {book["year"]} • <span class="{badge_class}">{read_status}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

elif st.session_state.current_page == "View Library":
    st.markdown("<h2>📚 Your Library</h2>", unsafe_allow_html=True)
    
    if not st.session_state.library:
        st.info("Your library is empty. Add some books to get started!")
    else:
        # Filter options
        col1, col2, col3 = st.columns(3)
        
        with col1:
            genre_filter = st.selectbox(
                "Filter by Genre", 
                ["All"] + sorted(list(set(book["genre"] for book in st.session_state.library)))
            )
        
        with col2:
            read_filter = st.selectbox("Filter by Read Status", ["All", "Read", "Unread"])
        
        with col3:
            sort_by = st.selectbox("Sort by", ["Title", "Author", "Year (Newest)", "Year (Oldest)"])
        
        # Apply filters
        filtered_books = st.session_state.library.copy()
        
        if genre_filter != "All":
            filtered_books = [book for book in filtered_books if book["genre"] == genre_filter]
        
        if read_filter == "Read":
            filtered_books = [book for book in filtered_books if book["read"]]
        elif read_filter == "Unread":
            filtered_books = [book for book in filtered_books if not book["read"]]
        
        # Apply sorting
        if sort_by == "Title":
            filtered_books.sort(key=lambda x: x["title"])
        elif sort_by == "Author":
            filtered_books.sort(key=lambda x: x["author"])
        elif sort_by == "Year (Newest)":
            filtered_books.sort(key=lambda x: x["year"], reverse=True)
        elif sort_by == "Year (Oldest)":
            filtered_books.sort(key=lambda x: x["year"])
        
        # Display books
        if not filtered_books:
            st.info("No books match your filters.")
        else:
            st.markdown(f"<p>Showing {len(filtered_books)} books</p>", unsafe_allow_html=True)
            st.markdown("---")
            
            for i, book in enumerate(filtered_books):
                col1, col2 = st.columns([4, 1])
                
                with col1:
                    read_status = "Read" if book["read"] else "Unread"
                    badge_class = "read-badge" if book["read"] else "unread-badge"
                    
                    st.markdown(f"""
                    <div class="book-card">
                        <div class="book-title">{book["title"]}</div>
                        <div class="book-author">by {book["author"]}</div>
                        <div class="book-details">
                            {book["genre"]} • {book["year"]} • <span class="{badge_class}">{read_status}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    # Find the index in the original library
                    original_index = next((index for (index, d) in enumerate(st.session_state.library) if d["title"] == book["title"] and d["author"] == book["author"]), None)
                    
                    st.button("Delete", key=f"delete_{i}", on_click=remove_book, args=(original_index,))
                    
                    status_label = "Mark Unread" if book["read"] else "Mark Read"
                    st.button(status_label, key=f"toggle_{i}", on_click=toggle_read_status, args=(original_index,))

elif st.session_state.current_page == "Add Book":
    st.markdown("<h2>➕ Add a New Book</h2>", unsafe_allow_html=True)
    
    with st.form("add_book_form"):
        title = st.text_input("Book Title")
        author = st.text_input("Author")
        
        col1, col2 = st.columns(2)
        
        with col1:
            current_year = datetime.now().year
            year = st.number_input("Publication Year", min_value=1800, max_value=current_year, value=2020)
        
        with col2:
            # Use predefined genres for focus
            genre = st.selectbox(
                "Genre", 
                ["Python", "JavaScript", "Next.js", "Motivational", "Other"]
            )
            
            # Allow custom genre input if "Other" is selected
            if genre == "Other":
                genre = st.text_input("Enter Custom Genre")
        
        read_status = st.checkbox("I have read this book")
        
        submitted = st.form_submit_button("Add Book")
        
        if submitted:
            if not title:
                st.error("Please enter a book title.")
            elif not author:
                st.error("Please enter an author name.")
            elif not genre:
                st.error("Please enter a genre.")
            else:
                success = add_book(title, author, year, genre, read_status)
                if success:
                    st.success(f"'{title}' by {author} has been added to your library!")
                    # Clear form by redirecting
                    st.experimental_rerun()
                else:
                    st.warning("This book already exists in your library.")

elif st.session_state.current_page == "Search Books":
    st.markdown("<h2>🔍 Search Books</h2>", unsafe_allow_html=True)
    
    if not st.session_state.library:
        st.info("Your library is empty. Add some books to search.")
    else:
        col1, col2 = st.columns(2)
        
        with col1:
            search_field = st.selectbox("Search by", ["Title", "Author", "Genre"])
        
        with col2:
            if search_field == "Title":
                search_term = st.text_input("Enter title to search")
            elif search_field == "Author":
                search_term = st.text_input("Enter author to search")
            else:
                search_term = st.text_input("Enter genre to search")
        
        if st.button("Search", use_container_width=True):
            field_map = {"Title": "title", "Author": "author", "Genre": "genre"}
            search_books(search_term, field_map[search_field])
        
        if st.session_state.search_performed:
            st.markdown("---")
            
            if not st.session_state.search_results:
                st.info(f"No books found matching '{search_term}' in {search_field.lower()}.")
            else:
                st.markdown(f"<h3>Found {len(st.session_state.search_results)} books:</h3>", unsafe_allow_html=True)
                
                for i, book in enumerate(st.session_state.search_results):
                    col1, col2 = st.columns([4, 1])
                    
                    with col1:
                        read_status = "Read" if book["read"] else "Unread"
                        badge_class = "read-badge" if book["read"] else "unread-badge"
                        
                        st.markdown(f"""
                        <div class="book-card">
                            <div class="book-title">{book["title"]}</div>
                            <div class="book-author">by {book["author"]}</div>
                            <div class="book-details">
                                {book["genre"]} • {book["year"]} • <span class="{badge_class}">{read_status}</span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col2:
                        # Find the index in the original library
                        original_index = next((index for (index, d) in enumerate(st.session_state.library) if d["title"] == book["title"] and d["author"] == book["author"]), None)
                        
                        st.button("Delete", key=f"search_delete_{i}", on_click=remove_book, args=(original_index,))
                        
                        status_label = "Mark Unread" if book["read"] else "Mark Read"
                        st.button(status_label, key=f"search_toggle_{i}", on_click=toggle_read_status, args=(original_index,))

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: #888888;'>Personal Library Manager - Track your reading journey</p>", unsafe_allow_html=True)
