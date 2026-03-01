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

window.addEventListener('load', function() {
    const searchInput = document.querySelector('.search-container input');
    if (searchInput) {
        searchInput.classList.add('loaded');
    }
});

document.addEventListener('DOMContentLoaded', function() {
    const cards = document.querySelectorAll('.card, .bloglist-table-row');
    
    cards.forEach(card => {
        card.addEventListener('mousemove', function(e) {
            const rect = card.getBoundingClientRect();
            const x = ((e.clientX - rect.left) / rect.width) * 100;
            const y = ((e.clientY - rect.top) / rect.height) * 100;
            
            card.style.setProperty('--mouse-x', x + '%');
            card.style.setProperty('--mouse-y', y + '%');
        });
    });
    
    const fieldTags = document.querySelectorAll('.field-tag');
    fieldTags.forEach(tag => {
        const tagText = tag.textContent.trim();
        if (tagText && !tag.querySelector('a')) {
            const cleanedTextForSearch = tagText.replace(/\s*\([^)]*\)\s*/g, '').trim();
            const wikipediaUrl = `https://en.wikipedia.org/wiki/${encodeURIComponent(cleanedTextForSearch)}`;
            const link = document.createElement('a');
            link.href = wikipediaUrl;
            link.target = '_blank';
            link.rel = 'noopener noreferrer';
            link.textContent = tagText;
            
            tag.innerHTML = '';
            tag.appendChild(link);
        }
    });
    
    initTagsCollapse();
    initDescriptionCollapse();
});

function initTagsCollapse() {
    const fieldsContainers = document.querySelectorAll('.fields');
    
    fieldsContainers.forEach(container => {
        const tags = container.querySelectorAll('.field-tag');
        
        if (tags.length > 3) {
            for (let i = 3; i < tags.length; i++) {
                tags[i].classList.add('hidden');
            }
            
            const showMoreBtn = document.createElement('span');
            showMoreBtn.className = 'show-more-tags';
            showMoreBtn.textContent = 'Show more';
            showMoreBtn.style.cursor = 'pointer';
            
            let isExpanded = false;
            
            showMoreBtn.addEventListener('click', function() {
                isExpanded = !isExpanded;
                
                for (let i = 3; i < tags.length; i++) {
                    if (isExpanded) {
                        tags[i].classList.remove('hidden');
                    } else {
                        tags[i].classList.add('hidden');
                    }
                }
                
                showMoreBtn.textContent = isExpanded ? 'Show less' : 'Show more';
            });
            
            container.appendChild(showMoreBtn);
        }
    });
}

function initDescriptionCollapse() {
    if (window.innerWidth <= 768) {
        const descriptions = document.querySelectorAll('.entry-description');
        
        descriptions.forEach(description => {
            const fullText = description.textContent.trim();
            
            if (fullText.length > 80) {
                const truncatedText = fullText.substring(0, 80);
                
                description.innerHTML = truncatedText + '... ';
                
                const showMoreBtn = document.createElement('span');
                showMoreBtn.className = 'show-more-description';
                showMoreBtn.textContent = 'more';
                
                let isExpanded = false;
                
                showMoreBtn.addEventListener('click', function() {
                    isExpanded = !isExpanded;
                    
                    if (isExpanded) {
                        description.innerHTML = fullText + ' ';
                        const showLessBtn = document.createElement('span');
                        showLessBtn.className = 'show-more-description';
                        showLessBtn.textContent = 'less';
                        showLessBtn.addEventListener('click', function() {
                            isExpanded = false;
                            description.innerHTML = truncatedText + '... ';
                            const newShowMoreBtn = document.createElement('span');
                            newShowMoreBtn.className = 'show-more-description';
                            newShowMoreBtn.textContent = 'more';
                            newShowMoreBtn.addEventListener('click', arguments.callee.bind(this));
                            description.appendChild(newShowMoreBtn);
                        });
                        description.appendChild(showLessBtn);
                    }
                });
                
                description.appendChild(showMoreBtn);
            }
        });
    }
}
