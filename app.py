import streamlit as st
from recommender import recommend_by_title, get_trending, get_book_titles

st.set_page_config(
    page_title="Book Recommendation System",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
# Custom CSS for Premium UI
st.markdown("""
    <style>
        /* Import Google Font: Inter */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

        /* Global Theme */
        .stApp {
            background-color: #0F172A; /* Slate 900 */
            color: #F8FAFC; /* Slate 50 */
            font-family: 'Inter', sans-serif;
        }
        
        /* Sidebar customization */
        [data-testid="stSidebar"] {
            background-color: #1E293B; /* Slate 800 */
            border-right: 1px solid #334155;
        }

        /* Typography */
        h1, h2, h3, h4, h5, h6 {
            font-family: 'Inter', sans-serif;
            color: #F8FAFC;
        }
        p, div {
            color: #CBD5E1; /* Slate 300 */
        }
        
        /* Card Design */
        .book-card {
            background-color: #1E293B; /* Slate 800 */
            padding: 24px;
            border-radius: 12px;
            border: 1px solid #334155; /* Slate 700 */
            height: 100%;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            transition: all 0.3s ease;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        }
        
        .book-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3), 0 4px 6px -2px rgba(0, 0, 0, 0.15);
            border-color: #6366F1; /* Indigo 500 */
        }
        
        .book-title {
            font-size: 1.25rem;
            font-weight: 700;
            margin-bottom: 8px;
            color: #F8FAFC;
            line-height: 1.4;
        }
        
        .book-author {
            font-size: 0.95rem;
            color: #94A3B8; /* Slate 400 */
            margin-bottom: 16px;
            font-style: italic;
        }
        
        .book-stats {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: auto;
            font-size: 0.875rem;
            color: #64748B; /* Slate 500 */
            border-top: 1px solid #334155;
            padding-top: 12px;
        }
        
        .rating-badge {
            background-color: #4F46E5; /* Indigo 600 */
            color: white;
            padding: 4px 10px;
            border-radius: 9999px;
            font-weight: 600;
            font-size: 0.8rem;
            box-shadow: 0 2px 5px rgba(79, 70, 229, 0.4);
        }
        
        /* Button Styling override */
        div.stButton > button:first-child {
            background-color: #6366F1;
            color: white;
            border-radius: 8px;
            border: none;
            padding: 10px 24px;
            font-weight: 600;
            transition: background-color 0.2s;
        }
        div.stButton > button:first-child:hover {
            background-color: #4F46E5;
            border-color: #4F46E5;
        }
        div.stButton > button:first-child:active {
            background-color: #4338CA;
            color: white;
        }
        
        /* Input fields */
        div[data-baseweb="select"] > div {
            background-color: #1E293B;
            border-color: #334155;
            color: white;
        }

        /* RESPONSIVE GRID LAYOUT */
        .book-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 24px;
            padding: 10px 0;
        }
        
        /* Mobile adjustments */
        @media (max-width: 640px) {
            .book-grid {
                grid-template-columns: 1fr; /* Stack vertically on small screens */
            }
            .book-card {
                padding: 16px; /* Slightly less padding on mobile */
            }
            .book-title {
                font-size: 1.1rem;
            }
        }
    </style>
    """, unsafe_allow_html=True)

st.title("📚 Book Recommendation System")
st.markdown("### Find your next favorite book")

# Initialize Session State
if 'selected_book' not in st.session_state:
    st.session_state.selected_book = None
if 'mode' not in st.session_state:
    st.session_state.mode = 'Trending Books'

# Sidebar
with st.sidebar:
    st.header("Navigation")
    # specific callback to handle manual mode switch
    def update_mode():
        st.session_state.mode = st.session_state.sidebar_mode
        
    option = st.radio(
        "Select Mode",
        ["Trending Books", "Search by Book"],
        index=0 if st.session_state.mode == "Trending Books" else 1,
        key="sidebar_mode",
        on_change=update_mode
    )
    st.markdown("---")
    st.info("Select 'Trending Books' to see what's popular, or 'Search by Book' to find similar reads based on a book you love.")

def display_books(df):
    """Helper to display books with interactive buttons"""
    # Use standard Streamlit columns for interactivity
    cols = st.columns(4)
    
    for idx, row in df.iterrows():
        with cols[idx % 4]:
            # Card Container
            with st.container():
                st.markdown(f"""
                <div class="book-card">
                    <div class="book-title">{row['title']}</div>
                    <div class="book-author">by {row['author']}</div>
                    <div class="book-stats">
                        <span class="rating-badge">★ {round(row['avg_rating'], 2)}</span>
                        <span>({int(row['rating_count'])} ratings)</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Interactive Button
                if st.button("Show Similar", key=f"btn_{row['title']}_{idx}", use_container_width=True):
                    st.session_state.selected_book = row['title']
                    st.session_state.mode = "Search by Book"
                    st.rerun()
            st.markdown("---") # Spacer

# TRENDING BOOKS
if st.session_state.mode == "Trending Books":
    st.subheader("🔥 Trending & Popular Books")
    trending = get_trending(12) # Fetch top 12
    display_books(trending.reset_index(drop=True))

# SEARCH BY BOOK
else:
    st.subheader("📖 Book-Based Recommendation")
    
    # Selectbox for search
    all_titles = get_book_titles()
    
    # Determine default index
    default_index = None
    if st.session_state.selected_book in all_titles:
        default_index = all_titles.index(st.session_state.selected_book)
        
    selected_book = st.selectbox(
        "Select a book you like:",
        options=all_titles,
        index=default_index,
        placeholder="Type to search..."
    )

    if selected_book:
        if st.button("Get Recommendations", type="primary"):
            with st.spinner("Finding similar books..."):
                recs = recommend_by_title(selected_book)
                
                if recs is None or recs.empty:
                    st.error("Oop! Something went wrong. Book not found.")
                else:
                    st.success(f"Because you liked **{selected_book}**:")
                    display_books(recs.reset_index(drop=True))
