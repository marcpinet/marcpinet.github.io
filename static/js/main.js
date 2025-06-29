var themeSwitcher = document.querySelector('.theme-switcher input');
var currentTheme = localStorage.getItem('theme');

// check if there is a theme saved in local storage
if (currentTheme) {
    document.documentElement.setAttribute('data-theme', currentTheme);

    if (currentTheme === 'light') {
        themeSwitcher.checked = true;
    }
} else {
    // If no theme is saved in local storage, use the user's system theme
    if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
        // User prefers dark theme
        document.documentElement.setAttribute('data-theme', 'dark');
        localStorage.setItem('theme', 'dark');
    } else {
        // User prefers light theme or the preference is not set, default to light theme
        document.documentElement.setAttribute('data-theme', 'light');
        localStorage.setItem('theme', 'light');
        themeSwitcher.checked = true;
    }
}

// switch between themes
function switchTheme(e) {
    if (e.target.checked) {
        document.documentElement.setAttribute('data-theme', 'light');
        localStorage.setItem('theme', 'light');
    } else {        
        document.documentElement.setAttribute('data-theme', 'dark');
        localStorage.setItem('theme', 'dark');
    }    
}

// event listener on checkbox change
themeSwitcher.addEventListener('change', switchTheme, false);

// easter egg
let bannerImg = document.querySelectorAll('.banner-home-img');
let clickCount = 0;

bannerImg.forEach(function(img) {
    img.addEventListener('click', function() {
        clickCount++;

        // Remove any existing click classes
        img.classList.remove('click-1', 'click-2', 'click-3', 'click-4', 'click-5');
        
        // Add the appropriate click class
        img.classList.add(`click-${clickCount}`);
        
        // Remove the class after animation completes
        setTimeout(() => {
            img.classList.remove(`click-${clickCount}`);
        }, clickCount === 5 ? 800 : 300 + (clickCount * 100));

        if (clickCount === 5) {
            let pageContent = document.querySelector('.content');
            pageContent.classList.toggle('upside-down');
            
            // Reset click count and remove all click classes after a delay
            setTimeout(() => {
                clickCount = 0;
                img.classList.remove('click-1', 'click-2', 'click-3', 'click-4', 'click-5');
            }, 1000);
        }
    });
});
