function debounce(func, wait) {
  var timeout;
  return function () {
    var context = this;
    var args = arguments;
    clearTimeout(timeout);
    timeout = setTimeout(function () {
      timeout = null;
      func.apply(context, args);
    }, wait);
  };
}

// Taken from mdbook
// The strategy is as follows:
// First, assign a value to each word in the document:
//  Words that correspond to search terms (stemmer aware): 40
//  Normal words: 2
//  First word in a sentence: 8
// Then use a sliding window with a constant number of words and count the
// sum of the values of the words within the window. Then use the window that got the
// maximum sum. If there are multiple maximas, then get the last one.
// Enclose the terms in <b>.
function makeTeaser(body, terms) {
  var TERM_WEIGHT = 40;
  var NORMAL_WORD_WEIGHT = 2;
  var FIRST_WORD_WEIGHT = 8;
  var TEASER_MAX_WORDS = 20;

  var stemmedTerms = terms.map(function (w) {
    return elasticlunr.stemmer(w.toLowerCase());
  });

  var words = body.split(/\s+/); // split tout le texte
  var weighted = [];

  // Associe un poids à chaque mot
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

  // Trouver l'index du premier mot correspondant
  var firstMatchIndex = weighted.findIndex(w => w[1] === TERM_WEIGHT);
  if (firstMatchIndex === -1) {
    firstMatchIndex = 0; // fallback : pas trouvé
  }

  // Calcule une fenêtre centrée autour du mot trouvé
  var halfWindow = Math.floor(TEASER_MAX_WORDS / 2);
  var start = Math.max(0, firstMatchIndex - halfWindow);
  var end = Math.min(weighted.length, start + TEASER_MAX_WORDS);

  // Ajuster si on est trop près de la fin
  if (end - start < TEASER_MAX_WORDS && start > 0) {
    start = Math.max(0, end - TEASER_MAX_WORDS);
  }

  // Construire le teaser
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


function formatSearchResultItem(item, terms) {
  // Titre + petit extrait max
  var teaser = "";
  if (item.doc.description) {
    teaser = item.doc.description;
  } else if (item.doc.body) {
    teaser = makeTeaser(item.doc.body, terms);
  }

  return `
    <div class="search-results__item">
      <a href="${item.ref}">${item.doc.title}</a>
      <p>${teaser}</p>
    </div>
  `;
}

function initSearch() {
  var $searchInput = document.getElementById("search");
  var $searchResults = document.querySelector(".search-results");
  var $searchResultsItems = document.querySelector(".search-results__items");
  var MAX_ITEMS = 10;

  var options = {
    bool: "AND",
    fields: { title: {boost: 2}, body: {boost: 1} }
  };
  var currentTerm = "";
  var initIndex = elasticlunr.Index.load(window.searchIndex);

  $searchInput.addEventListener("keyup", debounce(async function() {
    var term = $searchInput.value.trim();
    if (term === currentTerm) return;

    $searchResults.style.display = term === "" ? "none" : "block";
    $searchResultsItems.innerHTML = "";
    currentTerm = term;
    if (term === "") return;

    var results = initIndex.search(term, options);
    if (results.length === 0) {
      $searchResults.style.display = "none";
      return;
    }

    for (var i = 0; i < Math.min(results.length, MAX_ITEMS); i++) {
      var item = document.createElement("li");
      item.innerHTML = formatSearchResultItem(results[i], term.split(" "));
      $searchResultsItems.appendChild(item);
    }
  }, 150));

  window.addEventListener('click', function(e) {
    if ($searchResults.style.display === "block" && !$searchResults.contains(e.target)) {
      $searchResults.style.display = "none";
    }
  });
}

if (document.readyState === "complete" ||
    (document.readyState !== "loading" && !document.documentElement.doScroll)
) {
  initSearch();
} else {
  document.addEventListener("DOMContentLoaded", initSearch);
}