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


