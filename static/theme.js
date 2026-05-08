const toggleBtn = document.getElementById('theme-toggle');
const html = document.documentElement;

toggleBtn.addEventListener('click', () => {
    if (html.getAttribute('data-bs-theme') === 'dark') {
        html.setAttribute('data-bs-theme', 'light');
        toggleBtn.textContent = '🌙';
        localStorage.setItem('theme', 'light');
    } else {
        html.setAttribute('data-bs-theme', 'dark');
        toggleBtn.textContent = '☀️';
        localStorage.setItem('theme', 'dark');
    }
});

// Загрузка сохранённой темы
if (localStorage.getItem('theme') === 'dark') {
    html.setAttribute('data-bs-theme', 'dark');
    toggleBtn.textContent = '☀️';
}