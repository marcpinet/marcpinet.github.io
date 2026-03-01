document.addEventListener('DOMContentLoaded', function() {
    const hamburgerButton = document.querySelector('.hamburger-button');
    const mobileMenu = document.querySelector('.mobile-menu');
    const mobileMenuOverlay = document.querySelector('.mobile-menu-overlay');
    const mobileMenuClose = document.querySelector('.mobile-menu-close');
    const homeTitleMobile = document.querySelector('.home-title-mobile');

    function openMenu() {
        mobileMenu.classList.add('active');
        mobileMenuOverlay.classList.add('active');
        document.body.style.overflow = 'hidden';
    }

    function closeMenu() {
        mobileMenu.classList.remove('active');
        mobileMenuOverlay.classList.remove('active');
        document.body.style.overflow = '';
    }

    if (hamburgerButton) {
        hamburgerButton.addEventListener('click', openMenu);
    }

    if (mobileMenuClose) {
        mobileMenuClose.addEventListener('click', closeMenu);
    }

    if (mobileMenuOverlay) {
        mobileMenuOverlay.addEventListener('click', closeMenu);
    }

    if (homeTitleMobile) {
        homeTitleMobile.addEventListener('click', closeMenu);
    }

    const mobileMenuLinks = document.querySelectorAll('.mobile-menu-item');
    mobileMenuLinks.forEach(link => {
        link.addEventListener('click', closeMenu);
    });

    const desktopThemeSwitch = document.getElementById('themeswitch');
    const mobileThemeSwitch = document.getElementById('mobile-themeswitch');

    if (desktopThemeSwitch && mobileThemeSwitch) {
        mobileThemeSwitch.checked = desktopThemeSwitch.checked;
        
        desktopThemeSwitch.addEventListener('change', function() {
            mobileThemeSwitch.checked = this.checked;
        });

        mobileThemeSwitch.addEventListener('change', function() {
            desktopThemeSwitch.checked = this.checked;
            desktopThemeSwitch.dispatchEvent(new Event('change'));
        });
    }

    function formatSearchResultItem(item, terms) {
        var teaser = "";
        if (item.doc.description) {
            teaser = item.doc.description;
        } else if (item.doc.body) {
            teaser = makeTeaser(item.doc.body, terms);
        }

        return `
            <a href="${item.ref}" class="search-results__item">
                <div class="search-results__title">${item.doc.title}</div>
                <div class="search-results__description">${teaser}</div>
            </a>
        `;
    }

    function makeTeaser(body, terms) {
        var TERM_WEIGHT = 40;
        var NORMAL_WORD_WEIGHT = 2;
        var FIRST_WORD_WEIGHT = 8;
        var TEASER_MAX_WORDS = 20;

        var stemmedTerms = terms.map(function (w) {
            return elasticlunr.stemmer(w.toLowerCase());
        });

        var words = body.split(/\s+/);
        var weighted = [];

        for (var i = 0; i < words.length; i++) {
            var word = words[i];
            var weight = NORMAL_WORD_WEIGHT;
            if (i === 0 || words[i - 1].endsWith(".")) {
                weight = FIRST_WORD_WEIGHT;
            }
            for (var k in stemmedTerms) {
                if (elasticlunr.stemmer(word.toLowerCase()).startsWith(stemmedTerms[k])) {
                    weight = TERM_WEIGHT;
                }
            }
            weighted.push([word, weight]);
        }

        if (weighted.length === 0) {
            return body.substring(0, 100) + "…";
        }

        var firstMatchIndex = weighted.findIndex(w => w[1] === TERM_WEIGHT);
        if (firstMatchIndex === -1) {
            firstMatchIndex = 0;
        }

        var halfWindow = Math.floor(TEASER_MAX_WORDS / 2);
        var start = Math.max(0, firstMatchIndex - halfWindow);
        var end = Math.min(weighted.length, start + TEASER_MAX_WORDS);

        if (end - start < TEASER_MAX_WORDS && start > 0) {
            start = Math.max(0, end - TEASER_MAX_WORDS);
        }

        var teaser = [];
        if (start > 0) {
            teaser.push("… ");
        }
        for (var i = start; i < end; i++) {
            var word = weighted[i][0];
            if (weighted[i][1] === TERM_WEIGHT) {
                teaser.push("<b>" + word + "</b>");
            } else {
                teaser.push(word);
            }
        }
        if (end < weighted.length) {
            teaser.push(" …");
        }

        return teaser.join(" ");
    }

    const mobileSearchInput = document.getElementById('mobile-search');
    const mobileSearchResultsItems = document.querySelector('.mobile-search-results__items');

    if (mobileSearchInput && typeof elasticlunr !== 'undefined' && window.searchIndex) {
        var initIndex = elasticlunr.Index.load(window.searchIndex);
        var options = {
            bool: "AND",
            fields: { title: {boost: 2}, body: {boost: 1} }
        };

        mobileSearchInput.addEventListener('input', function(e) {
            const term = e.target.value.trim();
            
            if (!mobileSearchResultsItems) return;

            if (term === "" || term.length < 2) {
                mobileSearchResultsItems.innerHTML = '';
                return;
            }

            var results = initIndex.search(term, options);
            
            if (results.length === 0) {
                mobileSearchResultsItems.innerHTML = '<div class="search-results__item" style="padding: 14px 16px; color: var(--meta-color); cursor: default;">No results found</div>';
                return;
            }

            var MAX_ITEMS = 10;
            var html = '';
            for (var i = 0; i < Math.min(results.length, MAX_ITEMS); i++) {
                html += formatSearchResultItem(results[i], term.split(" "));
            }
            mobileSearchResultsItems.innerHTML = html;

            const resultLinks = mobileSearchResultsItems.querySelectorAll('a');
            resultLinks.forEach(link => {
                link.addEventListener('click', closeMenu);
            });
        });
    }
});
