var themeSwitchers = document.querySelectorAll('.theme-switcher input');
var currentTheme = localStorage.getItem('theme');

if (currentTheme) {
    document.documentElement.setAttribute('data-theme', currentTheme);

    if (currentTheme === 'light') {
        themeSwitchers.forEach(switcher => switcher.checked = true);
    }
} else {
    if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
        document.documentElement.setAttribute('data-theme', 'dark');
        localStorage.setItem('theme', 'dark');
    } else {
        document.documentElement.setAttribute('data-theme', 'light');
        localStorage.setItem('theme', 'light');
        themeSwitchers.forEach(switcher => switcher.checked = true);
    }
}

function switchTheme(e) {
    if (e.target.checked) {
        document.documentElement.setAttribute('data-theme', 'light');
        localStorage.setItem('theme', 'light');
        themeSwitchers.forEach(switcher => switcher.checked = true);
    } else {        
        document.documentElement.setAttribute('data-theme', 'dark');
        localStorage.setItem('theme', 'dark');
        themeSwitchers.forEach(switcher => switcher.checked = false);
    }    
}

themeSwitchers.forEach(switcher => {
    switcher.addEventListener('change', switchTheme, false);
});

// Glassy highlight effect on cards
document.addEventListener('DOMContentLoaded', function() {
    const cards = document.querySelectorAll('.card');
    
    cards.forEach(card => {
        card.addEventListener('mousemove', function(e) {
            const rect = card.getBoundingClientRect();
            const x = ((e.clientX - rect.left) / rect.width) * 100;
            const y = ((e.clientY - rect.top) / rect.height) * 100;
            
            card.style.setProperty('--mouse-x', x + '%');
            card.style.setProperty('--mouse-y', y + '%');
        });
    });
    
    // Make field tags clickable with Wikipedia links
    const fieldTags = document.querySelectorAll('.field-tag');
    fieldTags.forEach(tag => {
        const tagText = tag.textContent.trim();
        if (tagText && !tag.querySelector('a')) {
            // Remove acronyms in parentheses for Wikipedia search only
            const cleanedTextForSearch = tagText.replace(/\s*\([^)]*\)\s*/g, '').trim();
            const wikipediaUrl = `https://en.wikipedia.org/wiki/${encodeURIComponent(cleanedTextForSearch)}`;
            const link = document.createElement('a');
            link.href = wikipediaUrl;
            link.target = '_blank';
            link.rel = 'noopener noreferrer';
            link.textContent = tagText; // Keep original text with acronym for display
            
            tag.innerHTML = '';
            tag.appendChild(link);
        }
    });
});


