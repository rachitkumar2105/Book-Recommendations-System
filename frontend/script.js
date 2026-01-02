const API_BASE = '/api';

// DOM Elements
const bookSearch = document.getElementById('bookSearch');
const suggestionsBox = document.getElementById('suggestions');

// Views
const homeView = document.getElementById('home-view');
const recommendView = document.getElementById('recommend-view');

// Nav Items
const navHome = document.getElementById('nav-home');
const navRecommend = document.getElementById('nav-recommend');

// Grids & Loaders
const trendingGrid = document.getElementById('trendingGrid');
const recommendGrid = document.getElementById('recommendGrid');
const loaderTrending = document.getElementById('loader-trending');
const loaderRecommend = document.getElementById('loader-recommend');
const recommendTitle = document.getElementById('recommendTitle');

let allBooks = []; // Cache for autocomplete

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    fetchBooksList();
    loadTrending(); // Load once on start
});

// View Switching Logic
function showHome() {
    // Toggle Views
    homeView.style.display = 'block';
    recommendView.style.display = 'none';

    // Update Nav
    navHome.classList.add('active');
    navRecommend.classList.remove('active');

    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function showRecommend() {
    // Toggle Views
    homeView.style.display = 'none';
    recommendView.style.display = 'block';

    // Update Nav
    navHome.classList.remove('active');
    navRecommend.classList.add('active');

    // Smooth scroll
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Fetch all book titles for autocomplete
async function fetchBooksList() {
    try {
        const response = await fetch(`${API_BASE}/books`);
        allBooks = await response.json();
    } catch (error) {
        console.error('Failed to fetch book list:', error);
    }
}

// Load Trending Books
async function loadTrending() {
    loaderTrending.style.display = 'block';

    try {
        const response = await fetch(`${API_BASE}/trending`);
        const books = await response.json();
        renderBooks(books, trendingGrid);
    } catch (error) {
        console.error('Error loading trending:', error);
        trendingGrid.innerHTML = '<p class="error">Failed to load trending books.</p>';
    } finally {
        loaderTrending.style.display = 'none';
    }
}

// Get Recommendations
async function getRecommendations(titleOverride = null) {
    const title = titleOverride || bookSearch.value;
    if (!title) return;

    // Ensure we are in recommend view if triggered from elsewhere
    showRecommend();

    loaderRecommend.style.display = 'block';
    recommendTitle.innerHTML = `Because you liked <span style="color: var(--primary)">"${title}"</span>`;
    suggestionsBox.style.display = 'none';
    recommendGrid.innerHTML = ''; // Clear previous

    try {
        const response = await fetch(`${API_BASE}/recommend`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ title: title })
        });

        if (!response.ok) throw new Error('Book not found');

        const books = await response.json();
        renderBooks(books, recommendGrid);
    } catch (error) {
        console.error('Error getting recommendations:', error);
        recommendGrid.innerHTML = `
            <div style="grid-column: 1/-1; text-align: center; padding: 40px;">
                <h3>😕 Oops! Book not found.</h3>
                <p style="color: var(--text-muted)">Please start typing to select a book from the list.</p>
            </div>
        `;
    } finally {
        loaderRecommend.style.display = 'none';
    }
}

// Render Books to Grid
function renderBooks(books, gridElement) {
    gridElement.innerHTML = '';

    books.forEach((book, index) => {
        const card = document.createElement('div');
        card.className = 'book-card';
        card.style.animationDelay = `${index * 50}ms`; // Staggered animation

        card.innerHTML = `
            <div style="flex: 1; cursor: pointer;" onclick="selectBook('${book.title.replace(/'/g, "\\'")}')">
                <div class="book-title" title="${book.title}">${book.title}</div>
                <div class="book-author">by ${book.author}</div>
            </div>
            <div class="book-footer">
                <div class="rating">
                    <i class="fas fa-star"></i> ${parseFloat(book.avg_rating).toFixed(1)}
                    <span>(${parseInt(book.rating_count)})</span>
                </div>
                <button class="btn-icon" onclick="selectBook('${book.title.replace(/'/g, "\\'")}')" title="Find similar to this">
                    <i class="fas fa-magic"></i>
                </button>
            </div>
        `;

        // Add mouse move effect for glow
        card.addEventListener('mousemove', e => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            card.style.setProperty('--mouse-x', `${x}px`);
            card.style.setProperty('--mouse-y', `${y}px`);
        });

        gridElement.appendChild(card);
    });
}

// Trigger recommendation from card button
function selectBook(title) {
    bookSearch.value = title;
    // If we are on Home, this switches to Recommend view automatically
    getRecommendations(title);
    // showRecommend() is called inside getRecommendations
}

// Search Autocomplete Logic
bookSearch.addEventListener('input', (e) => {
    const input = e.target.value.toLowerCase();
    suggestionsBox.innerHTML = '';

    if (input.length < 2) {
        suggestionsBox.style.display = 'none';
        return;
    }

    const filtered = allBooks.filter(title => title.toLowerCase().includes(input)).slice(0, 10);

    if (filtered.length > 0) {
        filtered.forEach(title => {
            const div = document.createElement('div');
            div.className = 'suggestion-item';
            div.textContent = title;
            div.onclick = () => {
                bookSearch.value = title;
                suggestionsBox.style.display = 'none';
                getRecommendations(title);
            };
            suggestionsBox.appendChild(div);
        });
        suggestionsBox.style.display = 'block';
    } else {
        suggestionsBox.style.display = 'none';
    }
});

// Close suggestions on outside click
document.addEventListener('click', (e) => {
    if (!bookSearch.contains(e.target) && !suggestionsBox.contains(e.target)) {
        suggestionsBox.style.display = 'none';
    }
});
