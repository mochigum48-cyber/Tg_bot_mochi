// Telegram WebApp init
const tg = window.Telegram.WebApp;
tg.ready();
tg.expand();

let books = [];
let currentCategory = 'all';

// Load books from JSON
async function loadBooks() {
    try {
        const response = await fetch('books.json');
        books = await response.json();
        renderBooks(books);
    } catch (error) {
        console.error('Error loading books:', error);
        // Demo data if JSON fails
        books = [
            {
                id: "1",
                title: "Python Programming",
                author: "John Doe",
                category: "technology",
                cover: "https://via.placeholder.com/150x200?text=Python",
                description: "Learn Python programming from basics to advanced."
            },
            {
                id: "2",
                title: "Myanmar History",
                author: "Dr. Smith",
                category: "education",
                cover: "https://via.placeholder.com/150x200?text=History",
                description: "Complete history of Myanmar."
            },
            {
                id: "3",
                title: "Love Story",
                author: "Jane Doe",
                category: "fiction",
                cover: "https://via.placeholder.com/150x200?text=Novel",
                description: "A beautiful love story."
            }
        ];
        renderBooks(books);
    }
}

// Render books to grid
function renderBooks(bookList) {
    const grid = document.getElementById('bookGrid');
    grid.innerHTML = '';
    
    bookList.forEach(book => {
        const card = document.createElement('div');
        card.className = 'book-card';
        card.innerHTML = `
            <img src="${book.cover}" alt="${book.title}" class="book-cover">
            <div class="book-title">${book.title}</div>
            <div class="book-author">${book.author}</div>
        `;
        card.addEventListener('click', () => showBookDetail(book));
        grid.appendChild(card);
    });
}

// Filter by category
function filterBooks(category) {
    currentCategory = category;
    const filtered = category === 'all' 
        ? books 
        : books.filter(book => book.category === category);
    renderBooks(filtered);
}

// Search books
function searchBooks(query) {
    const filtered = books.filter(book => 
        book.title.toLowerCase().includes(query.toLowerCase()) ||
        book.author.toLowerCase().includes(query.toLowerCase())
    );
    renderBooks(filtered);
}

// Show book detail modal
function showBookDetail(book) {
    const modal = document.getElementById('bookModal');
    document.getElementById('modalTitle').textContent = book.title;
    document.getElementById('modalAuthor').textContent = `by ${book.author}`;
    document.getElementById('modalDesc').textContent = book.description;
    document.getElementById('modalCover').src = book.cover;
    
    const openBtn = document.getElementById('openInBot');
    openBtn.onclick = () => {
        // Send data to bot
        tg.sendData(JSON.stringify({ action: 'open_book', book_id: book.id }));
        // Close modal and mini app
        setTimeout(() => {
            tg.close();
        }, 500);
    };
    
    modal.style.display = 'flex';
}

// Close modal
document.querySelector('.close').onclick = () => {
    document.getElementById('bookModal').style.display = 'none';
};

// Category buttons
document.querySelectorAll('.category-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
        document.querySelectorAll('.category-btn').forEach(b => b.classList.remove('active'));
        e.target.classList.add('active');
        filterBooks(e.target.dataset.category);
    });
});

// Search input
document.getElementById('searchInput').addEventListener('input', (e) => {
    searchBooks(e.target.value);
});

// Initialize
loadBooks();
