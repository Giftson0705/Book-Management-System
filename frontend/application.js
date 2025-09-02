// app.js - Book Management System JavaScript

// Configuration
const API_BASE = "http://127.0.0.1:60619/api/v1";
let authToken = localStorage.getItem('authToken');
let currentUser = JSON.parse(localStorage.getItem('currentUser')) || {};
let currentEditingBookId = null;

// DOM Content Loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
    setupEventListeners();
});

// Initialize Application
function initializeApp() {
    hideLoading();
    
    if (authToken && currentUser.username) {
        showMainContent();
        setupUserInterface();
        loadDashboardData();
    } else {
        showAuthSection();
    }
}

// Setup Event Listeners
function setupEventListeners() {
    // Auth forms
    document.getElementById('loginForm').addEventListener('submit', handleLogin);
    document.getElementById('registerForm').addEventListener('submit', handleRegister);
    
    // Book form
    document.getElementById('bookForm').addEventListener('submit', handleBookSubmit);
    
    // Search
    document.getElementById('searchInput').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            searchBooks();
        }
    });
    
    // Modal close events
    window.addEventListener('click', function(event) {
        const modals = document.querySelectorAll('.modal');
        modals.forEach(modal => {
            if (event.target === modal) {
                closeModal(modal.id);
            }
        });
    });
}

// Authentication Functions
async function handleLogin(e) {
    e.preventDefault();
    
    const username = document.getElementById('loginUsername').value;
    const password = document.getElementById('loginPassword').value;
    
    if (!username || !password) {
        showAlert('Please fill in all fields', 'error');
        return;
    }
    
    showLoading();
    
    try {
        const response = await fetch(`${API_BASE}/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, password })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            authToken = data.access_token;
            localStorage.setItem('authToken', authToken);
            
            // Get user info from token
            const tokenPayload = JSON.parse(atob(authToken.split('.')[1]));
            currentUser = {
                username: tokenPayload.sub,
                role: tokenPayload.role
            };
            localStorage.setItem('currentUser', JSON.stringify(currentUser));
            
            showAlert('Login successful!', 'success');
            showMainContent();
            setupUserInterface();
            loadDashboardData();
        } else {
            showAlert(data.detail || 'Login failed', 'error');
        }
    } catch (error) {
        console.error('Login error:', error);
        showAlert('Network error. Please try again.', 'error');
    } finally {
        hideLoading();
    }
}

async function handleRegister(e) {
    e.preventDefault();
    
    const username = document.getElementById('regUsername').value;
    const email = document.getElementById('regEmail').value;
    const fullName = document.getElementById('regFullName').value;
    const password = document.getElementById('regPassword').value;
    
    if (!username || !email || !fullName || !password) {
        showAlert('Please fill in all fields', 'error');
        return;
    }
    
    if (password.length < 6) {
        showAlert('Password must be at least 6 characters long', 'error');
        return;
    }
    
    showLoading();
    
    try {
        const response = await fetch(`${API_BASE}/auth/signup`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                username,
                email,
                full_name: fullName,
                password
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showAlert('Registration successful! Please login.', 'success');
            toggleAuth();
            // Clear form
            document.getElementById('registerForm').reset();
        } else {
            showAlert(data.detail || 'Registration failed', 'error');
        }
    } catch (error) {
        console.error('Registration error:', error);
        showAlert('Network error. Please try again.', 'error');
    } finally {
        hideLoading();
    }
}

function logout() {
    localStorage.removeItem('authToken');
    localStorage.removeItem('currentUser');
    authToken = null;
    currentUser = {};
    
    showAlert('Logged out successfully', 'info');
    showAuthSection();
}

// UI Functions
function showAuthSection() {
    document.getElementById('auth').style.display = 'flex';
    document.getElementById('mainContent').style.display = 'none';
    document.getElementById('navbar').style.display = 'none';
}

function showMainContent() {
    document.getElementById('auth').style.display = 'none';
    document.getElementById('mainContent').style.display = 'block';
    document.getElementById('navbar').style.display = 'block';
}

function setupUserInterface() {
    // Update user greeting
    document.getElementById('userGreeting').textContent = `Welcome, ${currentUser.username}!`;
    
    // Show/hide admin features
    if (currentUser.role === 'admin') {
        document.getElementById('adminLink').style.display = 'block';
        document.getElementById('adminStats').style.display = 'block';
        document.getElementById('addBookBtn').style.display = 'block';
    } else {
        document.getElementById('adminLink').style.display = 'none';
        document.getElementById('adminStats').style.display = 'none';
        document.getElementById('addBookBtn').style.display = 'none';
    }
}

function showSection(sectionName) {
    // Update navigation
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
    });
    
    event.target.closest('.nav-link')?.classList.add('active');
    
    // Update content sections
    document.querySelectorAll('.content-section').forEach(section => {
        section.classList.remove('active');
    });
    
    document.getElementById(sectionName).classList.add('active');
    
    // Load section-specific data
    switch(sectionName) {
        case 'books':
            loadAllBooks();
            break;
        case 'mybooks':
            loadMyBooks();
            break;
        case 'admin':
            if (currentUser.role === 'admin') {
                loadAdminBooks();
            }
            break;
        case 'dashboard':
            loadDashboardData();
            break;
    }
}

function toggleAuth() {
    const loginForm = document.getElementById('loginForm');
    const registerForm = document.getElementById('registerForm');
    
    if (loginForm.style.display === 'none') {
        loginForm.style.display = 'flex';
        registerForm.style.display = 'none';
    } else {
        loginForm.style.display = 'none';
        registerForm.style.display = 'flex';
    }
}

// API Helper Functions
async function apiCall(endpoint, options = {}) {
    const url = `${API_BASE}${endpoint}`;
    const headers = {
        'Content-Type': 'application/json',
        ...options.headers
    };
    
    if (authToken) {
        headers['Authorization'] = `Bearer ${authToken}`;
    }
    
    try {
        const response = await fetch(url, {
            ...options,
            headers
        });
        
        if (response.status === 401) {
            logout();
            throw new Error('Authentication required');
        }
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.detail || 'API call failed');
        }
        
        return data;
    } catch (error) {
        console.error('API call error:', error);
        throw error;
    }
}

// Dashboard Functions
async function loadDashboardData() {
    try {
        showLoading();
        
        // Load books data
        const books = await apiCall('/books');
        const myBooks = await apiCall('/mybooks');
        
        // Update stats
        document.getElementById('totalBooks').textContent = books.length;
        document.getElementById('borrowedBooks').textContent = myBooks.length;
        
        const availableCount = books.reduce((count, book) => count + book.available_copies, 0);
        document.getElementById('availableBooks').textContent = availableCount;
        
        // Load admin stats if admin
        if (currentUser.role === 'admin') {
            try {
                const users = await apiCall('/admin/users');
                document.getElementById('totalUsers').textContent = users.length;
            } catch (error) {
                console.error('Failed to load admin stats:', error);
            }
        }
        
    } catch (error) {
        showAlert('Failed to load dashboard data', 'error');
    } finally {
        hideLoading();
    }
}

// Books Functions
async function loadAllBooks() {
    try {
        showLoading();
        const books = await apiCall('/books');
        displayBooks(books, 'booksGrid');
    } catch (error) {
        showAlert('Failed to load books', 'error');
        displayEmptyState('booksGrid', 'No books available');
    } finally {
        hideLoading();
    }
}

async function loadMyBooks() {
    try {
        showLoading();
        const books = await apiCall('/mybooks');
        displayBooks(books, 'myBooksGrid', true);
    } catch (error) {
        showAlert('Failed to load your books', 'error');
        displayEmptyState('myBooksGrid', 'No borrowed books');
    } finally {
        hideLoading();
    }
}

async function searchBooks() {
    const query = document.getElementById('searchInput').value.trim();
    
    if (!query) {
        loadAllBooks();
        return;
    }
    
    try {
        showLoading();
        const books = await apiCall(`/books/search?query=${encodeURIComponent(query)}`);
        displayBooks(books, 'booksGrid');
        
        if (books.length === 0) {
            showAlert(`No books found for "${query}"`, 'info');
        }
    } catch (error) {
        showAlert('Search failed', 'error');
    } finally {
        hideLoading();
    }
}

function displayBooks(books, containerId, isMyBooks = false) {
    const container = document.getElementById(containerId);
    
    if (books.length === 0) {
        displayEmptyState(containerId, isMyBooks ? 'No borrowed books' : 'No books found');
        return;
    }
    
    container.innerHTML = books.map(book => createBookCard(book, isMyBooks)).join('');
}

function createBookCard(book, isMyBooks = false) {
    const isAvailable = book.available_copies > 0;
    const isAdmin = currentUser.role === 'admin';
    
    return `
        <div class="book-card">
            <div class="book-header">
                <h3>${book.title}</h3>
                <p>by ${book.author}</p>
            </div>
            <div class="book-body">
                <div class="book-info">
                    <div class="info-row">
                        <span class="info-label">Genre:</span>
                        <span class="info-value">${book.genre}</span>
                    </div>
                    <div class="info-row">
                        <span class="info-label">ISBN:</span>
                        <span class="info-value">${book.isbn}</span>
                    </div>
                    <div class="info-row">
                        <span class="info-label">Copies:</span>
                        <span class="info-value">${book.available_copies}/${book.total_copies} available</span>
                    </div>
                    <div class="info-row">
                        <span class="info-label">Status:</span>
                        <span class="availability ${isAvailable ? 'available' : 'unavailable'}">
                            <i class="fas ${isAvailable ? 'fa-check-circle' : 'fa-times-circle'}"></i>
                            ${isAvailable ? 'Available' : 'Unavailable'}
                        </span>
                    </div>
                    ${book.description ? `
                    <div class="info-row">
                        <span class="info-label">Description:</span>
                        <span class="info-value">${book.description}</span>
                    </div>` : ''}
                </div>
                <div class="book-actions">
                    ${!isMyBooks && isAvailable ? `
                        <button onclick="borrowBook('${book.id}')" class="btn btn-primary">
                            <i class="fas fa-bookmark"></i> Borrow
                        </button>
                    ` : ''}
                    ${isMyBooks ? `
                        <button onclick="returnBook('${book.id}')" class="btn btn-warning">
                            <i class="fas fa-undo"></i> Return
                        </button>
                    ` : ''}
                    ${isAdmin ? `
                        <button onclick="editBook('${book.id}')" class="btn btn-secondary">
                            <i class="fas fa-edit"></i> Edit
                        </button>
                        <button onclick="deleteBook('${book.id}')" class="btn btn-danger">
                            <i class="fas fa-trash"></i> Delete
                        </button>
                    ` : ''}
                </div>
            </div>
        </div>
    `;
}

async function borrowBook(bookId) {
    try {
        showLoading();
        await apiCall(`/books/${bookId}/borrow`, { method: 'POST' });
        showAlert('Book borrowed successfully!', 'success');
        
        // Refresh current view
        if (document.getElementById('books').classList.contains('active')) {
            loadAllBooks();
        }
        loadDashboardData();
    } catch (error) {
        showAlert(error.message || 'Failed to borrow book', 'error');
    } finally {
        hideLoading();
    }
}

async function returnBook(bookId) {
    try {
        showLoading();
        await apiCall(`/books/${bookId}/return`, { method: 'POST' });
        showAlert('Book returned successfully!', 'success');
        
        // Refresh current view
        if (document.getElementById('mybooks').classList.contains('active')) {
            loadMyBooks();
        }
        loadDashboardData();
    } catch (error) {
        showAlert(error.message || 'Failed to return book', 'error');
    } finally {
        hideLoading();
    }
}

// Admin Functions
async function loadAdminBooks() {
    try {
        showLoading();
        const books = await apiCall('/books');
        displayAdminBooks(books);
    } catch (error) {
        showAlert('Failed to load admin books', 'error');
    } finally {
        hideLoading();
    }
}

function displayAdminBooks(books) {
    const container = document.getElementById('adminBooksGrid');
    
    if (books.length === 0) {
        displayEmptyState('adminBooksGrid', 'No books in the system');
        return;
    }
    
    container.innerHTML = books.map(book => createBookCard(book, false)).join('');
}

async function loadUsers() {
    try {
        showLoading();
        const users = await apiCall('/admin/users');
        displayUsers(users);
        showAdminTab('users');
    } catch (error) {
        showAlert('Failed to load users', 'error');
    } finally {
        hideLoading();
    }
}

function displayUsers(users) {
    const tbody = document.getElementById('usersTableBody');
    
    if (users.length === 0) {
        tbody.innerHTML = '<tr><td colspan="6" class="text-center">No users found</td></tr>';
        return;
    }
    
    tbody.innerHTML = users.map(user => `
        <tr>
            <td>${user.username}</td>
            <td>${user.email}</td>
            <td>${user.full_name}</td>
            <td>
                <span class="role-badge role-${user.role}">${user.role}</span>
            </td>
            <td>${user.borrowed_books.length}</td>
            <td>
                <select onchange="changeUserRole('${user.id}', this.value)" 
                        ${user.username === currentUser.username ? 'disabled' : ''}>
                    <option value="user" ${user.role === 'user' ? 'selected' : ''}>User</option>
                    <option value="admin" ${user.role === 'admin' ? 'selected' : ''}>Admin</option>
                </select>
                ${user.username !== currentUser.username ? `
                    <button onclick="deleteUser('${user.id}')" class="btn btn-danger btn-sm">
                        <i class="fas fa-trash"></i>
                    </button>
                ` : ''}
            </td>
        </tr>
    `).join('');
}

async function changeUserRole(userId, newRole) {
    try {
        showLoading();
        await apiCall(`/admin/users/${userId}`, {
            method: 'PUT',
            body: JSON.stringify({ role: newRole })
        });
        showAlert('User role updated successfully!', 'success');
        loadUsers();
    } catch (error) {
        showAlert(error.message || 'Failed to update user role', 'error');
        loadUsers(); // Reload to reset the select
    } finally {
        hideLoading();
    }
}

async function deleteUser(userId) {
    if (!confirm('Are you sure you want to delete this user? This action cannot be undone.')) {
        return;
    }
    
    try {
        showLoading();
        await apiCall(`/admin/users/${userId}`, { method: 'DELETE' });
        showAlert('User deleted successfully!', 'success');
        loadUsers();
        loadDashboardData(); // Update stats
    } catch (error) {
        showAlert(error.message || 'Failed to delete user', 'error');
    } finally {
        hideLoading();
    }
}

function showAdminTab(tabName) {
    // Update tab buttons
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    document.querySelector(`[onclick="showAdminTab('${tabName}')"]`).classList.add('active');
    
    // Update tab content
    document.querySelectorAll('.tab-content').forEach(content => {
        content.classList.remove('active');
    });
    document.getElementById(`admin${tabName.charAt(0).toUpperCase() + tabName.slice(1)}Tab`).classList.add('active');
}

// Book Management Functions
function showAddBookModal() {
    currentEditingBookId = null;
    document.getElementById('modalTitle').textContent = 'Add New Book';
    document.getElementById('bookForm').reset();
    document.getElementById('bookModal').style.display = 'block';
}

async function editBook(bookId) {
    try {
        showLoading();
        const book = await apiCall(`/books/${bookId}`);
        
        currentEditingBookId = bookId;
        document.getElementById('modalTitle').textContent = 'Edit Book';
        
        // Populate form
        document.getElementById('bookTitle').value = book.title;
        document.getElementById('bookAuthor').value = book.author;
        document.getElementById('bookGenre').value = book.genre;
        document.getElementById('bookISBN').value = book.isbn;
        document.getElementById('bookDescription').value = book.description || '';
        document.getElementById('totalCopies').value = book.total_copies;
        
        document.getElementById('bookModal').style.display = 'block';
    } catch (error) {
        showAlert('Failed to load book details', 'error');
    } finally {
        hideLoading();
    }
}

async function handleBookSubmit(e) {
    e.preventDefault();
    
    const bookData = {
        title: document.getElementById('bookTitle').value,
        author: document.getElementById('bookAuthor').value,
        genre: document.getElementById('bookGenre').value,
        isbn: document.getElementById('bookISBN').value,
        description: document.getElementById('bookDescription').value,
        total_copies: parseInt(document.getElementById('totalCopies').value)
    };
    
    try {
        showLoading();
        
        if (currentEditingBookId) {
            // Update existing book
            await apiCall(`/admin/books/${currentEditingBookId}`, {
                method: 'PUT',
                body: JSON.stringify(bookData)
            });
            showAlert('Book updated successfully!', 'success');
        } else {
            // Create new book
            await apiCall('/admin/books', {
                method: 'POST',
                body: JSON.stringify(bookData)
            });
            showAlert('Book added successfully!', 'success');
        }
        
        closeModal('bookModal');
        
        // Refresh current view
        if (document.getElementById('admin').classList.contains('active')) {
            loadAdminBooks();
        }
        if (document.getElementById('books').classList.contains('active')) {
            loadAllBooks();
        }
        loadDashboardData();
        
    } catch (error) {
        showAlert(error.message || 'Failed to save book', 'error');
    } finally {
        hideLoading();
    }
}

async function deleteBook(bookId) {
    if (!confirm('Are you sure you want to delete this book? This action cannot be undone.')) {
        return;
    }
    
    try {
        showLoading();
        await apiCall(`/admin/books/${bookId}`, { method: 'DELETE' });
        showAlert('Book deleted successfully!', 'success');
        
        // Refresh current view
        if (document.getElementById('admin').classList.contains('active')) {
            loadAdminBooks();
        }
        if (document.getElementById('books').classList.contains('active')) {
            loadAllBooks();
        }
        loadDashboardData();
        
    } catch (error) {
        showAlert(error.message || 'Failed to delete book', 'error');
    } finally {
        hideLoading();
    }
}

// Modal Functions
function closeModal(modalId) {
    document.getElementById(modalId).style.display = 'none';
    currentEditingBookId = null;
}

// Utility Functions
function showLoading() {
    document.getElementById('loading').style.display = 'flex';
}

function hideLoading() {
    document.getElementById('loading').style.display = 'none';
}

function showAlert(message, type = 'info') {
    const alertContainer = document.getElementById('alertContainer');
    const alertId = 'alert-' + Date.now();
    
    const alertElement = document.createElement('div');
    alertElement.id = alertId;
    alertElement.className = `alert alert-${type}`;
    
    const icon = getAlertIcon(type);
    alertElement.innerHTML = `
        <i class="${icon}"></i>
        <span>${message}</span>
    `;
    
    alertContainer.appendChild(alertElement);
    
    // Auto remove after 4 seconds
    setTimeout(() => {
        const element = document.getElementById(alertId);
        if (element) {
            element.remove();
        }
    }, 4000);
    
    // Remove on click
    alertElement.addEventListener('click', () => {
        alertElement.remove();
    });
}

function getAlertIcon(type) {
    switch (type) {
        case 'success':
            return 'fas fa-check-circle';
        case 'error':
            return 'fas fa-exclamation-circle';
        case 'warning':
            return 'fas fa-exclamation-triangle';
        case 'info':
        default:
            return 'fas fa-info-circle';
    }
}

function displayEmptyState(containerId, message) {
    const container = document.getElementById(containerId);
    container.innerHTML = `
        <div class="empty-state">
            <i class="fas fa-book-open"></i>
            <h3>No Items Found</h3>
            <p>${message}</p>
            ${containerId === 'booksGrid' ? `
                <button onclick="showSection('dashboard')" class="btn btn-primary">
                    <i class="fas fa-home"></i> Go to Dashboard
                </button>
            ` : ''}
        </div>
    `;
}

// Keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Escape key to close modals
    if (e.key === 'Escape') {
        const modals = document.querySelectorAll('.modal');
        modals.forEach(modal => {
            if (modal.style.display === 'block') {
                closeModal(modal.id);
            }
        });
    }
    
    // Ctrl/Cmd + K for search focus
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        const searchInput = document.getElementById('searchInput');
        if (searchInput && document.getElementById('books').classList.contains('active')) {
            searchInput.focus();
        }
    }
    
    // Admin shortcuts (only for admins)
    if (currentUser.role === 'admin') {
        // Ctrl/Cmd + N for new book
        if ((e.ctrlKey || e.metaKey) && e.key === 'n') {
            e.preventDefault();
            showAddBookModal();
        }
        
        // Ctrl/Cmd + U for users
        if ((e.ctrlKey || e.metaKey) && e.key === 'u') {
            e.preventDefault();
            showSection('admin');
            loadUsers();
        }
    }
});

// Form validation helpers
function validateBookForm() {
    const title = document.getElementById('bookTitle').value.trim();
    const author = document.getElementById('bookAuthor').value.trim();
    const genre = document.getElementById('bookGenre').value.trim();
    const isbn = document.getElementById('bookISBN').value.trim();
    const totalCopies = document.getElementById('totalCopies').value;
    
    if (!title) {
        showAlert('Book title is required', 'error');
        return false;
    }
    
    if (!author) {
        showAlert('Author name is required', 'error');
        return false;
    }
    
    if (!genre) {
        showAlert('Genre is required', 'error');
        return false;
    }
    
    if (!isbn || isbn.length < 10) {
        showAlert('Valid ISBN is required (at least 10 characters)', 'error');
        return false;
    }
    
    if (!totalCopies || totalCopies < 1) {
        showAlert('Total copies must be at least 1', 'error');
        return false;
    }
    
    return true;
}

// Add validation to book form
document.getElementById('bookForm').addEventListener('submit', function(e) {
    if (!validateBookForm()) {
        e.preventDefault();
        return false;
    }
});

// Auto-refresh functionality
let autoRefreshInterval;

function startAutoRefresh() {
    // Refresh dashboard stats every 5 minutes
    autoRefreshInterval = setInterval(() => {
        if (document.getElementById('dashboard').classList.contains('active')) {
            loadDashboardData();
        }
    }, 300000); // 5 minutes
}

function stopAutoRefresh() {
    if (autoRefreshInterval) {
        clearInterval(autoRefreshInterval);
    }
}

// Start auto-refresh when logged in
if (authToken) {
    startAutoRefresh();
}

// Stop auto-refresh on logout
const originalLogout = logout;
logout = function() {
    stopAutoRefresh();
    originalLogout();
};

// Handle network errors gracefully
window.addEventListener('online', function() {
    showAlert('Connection restored', 'success');
    if (authToken) {
        loadDashboardData();
    }
});

window.addEventListener('offline', function() {
    showAlert('You are offline. Some features may not work.', 'warning');
});

// Progressive Web App support
if ('serviceWorker' in navigator) {
    window.addEventListener('load', function() {
        navigator.serviceWorker.register('/sw.js')
            .then(function(registration) {
                console.log('ServiceWorker registration successful');
            })
            .catch(function(err) {
                console.log('ServiceWorker registration failed');
            });
    });
}

// Theme handling
function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
}

// Load saved theme
const savedTheme = localStorage.getItem('theme');
if (savedTheme) {
    document.documentElement.setAttribute('data-theme', savedTheme);
}

// Export/Import functionality for admin
async function exportBooks() {
    if (currentUser.role !== 'admin') return;
    
    try {
        const books = await apiCall('/books');
        const dataStr = JSON.stringify(books, null, 2);
        const dataBlob = new Blob([dataStr], {type: 'application/json'});
        
        const link = document.createElement('a');
        link.href = URL.createObjectURL(dataBlob);
        link.download = `books_export_${new Date().toISOString().split('T')[0]}.json`;
        link.click();
        
        showAlert('Books exported successfully!', 'success');
    } catch (error) {
        showAlert('Failed to export books', 'error');
    }
}

// Accessibility improvements
function setupAccessibility() {
    // Add ARIA labels
    document.querySelectorAll('button').forEach(button => {
        if (!button.getAttribute('aria-label') && button.textContent.trim()) {
            button.setAttribute('aria-label', button.textContent.trim());
        }
    });
    
    // Add focus management for modals
    const modals = document.querySelectorAll('.modal');
    modals.forEach(modal => {
        modal.addEventListener('shown', function() {
            const firstInput = modal.querySelector('input, button, textarea, select');
            if (firstInput) {
                firstInput.focus();
            }
        });
    });
}

// Initialize accessibility features
document.addEventListener('DOMContentLoaded', setupAccessibility);

// Error boundary for unhandled errors
window.addEventListener('error', function(e) {
    console.error('Unhandled error:', e.error);
    showAlert('An unexpected error occurred. Please refresh the page.', 'error');
});

window.addEventListener('unhandledrejection', function(e) {
    console.error('Unhandled promise rejection:', e.reason);
    showAlert('An unexpected error occurred. Please try again.', 'error');
});

// Performance monitoring
const performanceObserver = new PerformanceObserver((list) => {
    list.getEntries().forEach((entry) => {
        if (entry.entryType === 'navigation') {
            console.log('Page load time:', entry.loadEventEnd - entry.loadEventStart, 'ms');
        }
    });
});

if ('PerformanceObserver' in window) {
    performanceObserver.observe({entryTypes: ['navigation']});
}

// Analytics helper (if needed)
function trackEvent(eventName, properties = {}) {
    // Placeholder for analytics tracking
    console.log('Event:', eventName, properties);
}

// Track page views
function trackPageView(page) {
    trackEvent('page_view', { page });
}

// Add tracking to section changes
const originalShowSection = showSection;
showSection = function(sectionName) {
    originalShowSection(sectionName);
    trackPageView(sectionName);
};

// Initialize the app
console.log('Book Management System initialized');
trackEvent('app_initialized', { 
    user_role: currentUser.role || 'anonymous',
    timestamp: new Date().toISOString()
});