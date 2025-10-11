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

function normalizeText(text) {
  return text.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '');
}

function findMatches(text, terms) {
  var normalizedText = normalizeText(text);
  var matches = [];
  
  terms.forEach(function(term) {
    var normalizedTerm = normalizeText(term);
    var index = 0;
    while ((index = normalizedText.indexOf(normalizedTerm, index)) !== -1) {
      matches.push({ start: index, length: term.length, term: term });
      index += normalizedTerm.length;
    }
  });
  
  return matches;
}

function calculateScore(doc, terms) {
  var score = 0;
  var titleLower = normalizeText(doc.title);
  var bodyLower = normalizeText(doc.body || '');
  
  terms.forEach(function(term) {
    var normalizedTerm = normalizeText(term);
    
    var titleExactMatches = (titleLower.match(new RegExp('\\b' + normalizedTerm + '\\b', 'g')) || []).length;
    var titlePartialMatches = (titleLower.match(new RegExp(normalizedTerm, 'g')) || []).length - titleExactMatches;
    
    var bodyExactMatches = (bodyLower.match(new RegExp('\\b' + normalizedTerm + '\\b', 'g')) || []).length;
    var bodyPartialMatches = (bodyLower.match(new RegExp(normalizedTerm, 'g')) || []).length - bodyExactMatches;
    
    score += titleExactMatches * 100;
    score += titlePartialMatches * 50;
    score += bodyExactMatches * 10;
    score += bodyPartialMatches * 5;
  });
  
  return score;
}

function makeTeaser(body, terms) {
  var TEASER_MAX_WORDS = 30;
  var words = body.split(/\s+/);
  
  if (words.length === 0) {
    return '';
  }
  
  var normalizedBody = normalizeText(body);
  var firstMatchIndex = -1;
  var firstMatchWord = -1;
  
  for (var i = 0; i < terms.length; i++) {
    var normalizedTerm = normalizeText(terms[i]);
    var index = normalizedBody.indexOf(normalizedTerm);
    if (index !== -1 && (firstMatchIndex === -1 || index < firstMatchIndex)) {
      firstMatchIndex = index;
      var textBeforeMatch = body.substring(0, index);
      firstMatchWord = textBeforeMatch.split(/\s+/).length - 1;
    }
  }
  
  if (firstMatchWord === -1) {
    firstMatchWord = 0;
  }
  
  var halfWindow = Math.floor(TEASER_MAX_WORDS / 2);
  var start = Math.max(0, firstMatchWord - halfWindow);
  var end = Math.min(words.length, start + TEASER_MAX_WORDS);
  
  if (end - start < TEASER_MAX_WORDS && start > 0) {
    start = Math.max(0, end - TEASER_MAX_WORDS);
  }
  
  var teaserWords = words.slice(start, end);
  var teaserText = teaserWords.join(' ');
  
  terms.forEach(function(term) {
    var normalizedTerm = normalizeText(term);
    var regex = new RegExp('(' + normalizedTerm.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + ')', 'gi');
    teaserText = teaserText.replace(regex, '<b>$1</b>');
  });
  
  var prefix = start > 0 ? '… ' : '';
  var suffix = end < words.length ? ' …' : '';
  
  return prefix + teaserText + suffix;
}

function formatSearchResultItem(item, terms) {
  var teaser = '';
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

function performSearch(docs, searchTerms) {
  var results = [];
  
  docs.forEach(function(doc) {
    var score = calculateScore(doc, searchTerms);
    if (score > 0) {
      results.push({
        ref: doc.ref,
        doc: doc,
        score: score
      });
    }
  });
  
  results.sort(function(a, b) {
    return b.score - a.score;
  });
  
  return results;
}

function initSearch() {
  var $searchInput = document.getElementById('search');
  var $searchResults = document.querySelector('.search-results');
  var $searchResultsItems = document.querySelector('.search-results__items');
  var MAX_ITEMS = 10;

  var currentTerm = '';
  var indexData = elasticlunr.Index.load(window.searchIndex);
  var allDocs = [];
  
  indexData.documentStore.docs = indexData.documentStore.docs || {};
  for (var ref in indexData.documentStore.docs) {
    if (indexData.documentStore.docs.hasOwnProperty(ref)) {
      var doc = indexData.documentStore.docs[ref];
      allDocs.push({
        ref: ref,
        title: doc.title || '',
        body: doc.body || '',
        description: doc.description || ''
      });
    }
  }

  $searchInput.addEventListener('keyup', debounce(function() {
    var term = $searchInput.value.trim();
    if (term === currentTerm) return;

    $searchResults.style.display = term === '' ? 'none' : 'block';
    $searchResultsItems.innerHTML = '';
    currentTerm = term;
    if (term === '') return;

    var searchTerms = term.split(/\s+/).filter(function(t) { return t.length > 0; });
    var results = performSearch(allDocs, searchTerms);
    
    if (results.length === 0) {
      $searchResults.style.display = 'none';
      return;
    }

    for (var i = 0; i < Math.min(results.length, MAX_ITEMS); i++) {
      var item = document.createElement('li');
      item.innerHTML = formatSearchResultItem(results[i], searchTerms);
      $searchResultsItems.appendChild(item);
    }
  }, 150));

  window.addEventListener('click', function(e) {
    if ($searchResults.style.display === 'block' && !$searchResults.contains(e.target)) {
      $searchResults.style.display = 'none';
    }
  });
}

if (document.readyState === 'complete' ||
    (document.readyState !== 'loading' && !document.documentElement.doScroll)
) {
  initSearch();
} else {
  document.addEventListener('DOMContentLoaded', initSearch);
}
