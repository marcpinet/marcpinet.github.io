+++
title = "WebsemOG24"
description = "🌐 A semantic web project enriching Olympics data through spaCy's deep learning models and knowledge graphs. Features enrichments through APIs, SPARQL inference rules, and SHACL constraints. Expanded from 355 to 15,000+ triples with DBpedia/Wikidata linking."
date = "2025-01-31"
weight = 1

[extra]
remote_image = "/websem-og24/img.gif"
link_to = "https://github.com/marcpinet/websem-og24"
+++

<style>
/* GitHub Alert Styles */
.github-alert {
    border-radius: 6px;
    margin: 16px 0;
    padding: 12px 16px;
    border-left: 4px solid;
}

.github-alert-note {
    background-color: #ddf4ff;
    border-color: #0969da;
}

.github-alert-tip {
    background-color: #dcfce7;
    border-color: #1a7f37;
}

.github-alert-important {
    background-color: #f3e8ff;
    border-color: #8250df;
}

.github-alert-warning {
    background-color: #fff8dc;
    border-color: #d1242f;
}

.github-alert-caution {
    background-color: #ffebee;
    border-color: #d1242f;
}

/* Table Wrapper */
.table-wrapper {
    overflow-x: auto;
    margin: 16px 0;
}

.table-wrapper table {
    width: 100%;
    border-collapse: collapse;
}

.table-wrapper th,
.table-wrapper td {
    border: 1px solid #d1d5da;
    padding: 8px 12px;
    text-align: left;
}

.table-wrapper th {
    font-weight: 600;
}

/* Video Styles */
video {
    max-width: 100%;
    height: auto;
    border-radius: 6px;
    margin: 16px 0;
}

/* Code Block Styles */
pre {
    background-color: #f6f8fa;
    border-radius: 6px;
    padding: 16px;
    overflow-x: auto;
    margin: 16px 0;
}

code {
    background-color: #f6f8fa;
    padding: 2px 4px;
    border-radius: 3px;
    font-family: 'SFMono-Regular', 'Monaco', 'Inconsolata', 'Liberation Mono', 'Consolas', monospace;
    font-size: 85%;
    color: #24292f;
}

pre code {
    background-color: transparent;
    padding: 0;
}

/* Dark mode support for inline code */
@media (prefers-color-scheme: dark) {
    pre {
        background-color: #161b22;
        color: #f0f6fc;
    }
    
    code {
        background-color: #21262d;
        color: #f0f6fc;
    }
    
    pre code {
        background-color: transparent;
        color: inherit;
    }
}
</style>

# Paris 2024 Olympics - Semantic Web Project

A comprehensive knowledge graph project for the Paris 2024 Olympic Games, combining semantic web technologies with advanced NLP for data enrichment.

## 📋 Overview

This project builds an enriched semantic model of Olympic Games data through:
- Custom RDF/OWL ontology for Olympic domain modeling
- Deep learning-based information extraction using spaCy's fr_core_news_lg
- SKOS-based sport classification system
- SPARQL inference rules and SHACL constraints
- External knowledge integration (DBpedia/Wikidata)
- Real-time weather data integration

## 🧠 Deep Learning & NLP

The project leverages [spaCy's fr_core_news_lg](https://spacy.io/models/fr) model (1.7GB) for advanced text analysis:
- Named Entity Recognition optimized for athlete identification
- Sport-specific term classification
- Performance metric extraction
- Contextual relationship mapping

Model Performance:
- 89% accuracy on athlete name recognition
- 97% accuracy on sports terminology classification
- 2,500+ athlete mentions processed
- 1,800+ performance records extracted

## 🏗️ Architecture

### Semantic Layer
- Modular ontology with Person, SportingEvent, and Location hierarchies
- SKOS taxonomy for sports classification
- SHACL constraints for data validation
- Custom SPARQL rules for knowledge inference

### Data Integration Layer
- DBpedia and Wikidata entity linking
- Real-time weather data integration
- Unstructured text processing pipeline
- CSV data transformation system

### Visualization Layer
- Interactive knowledge graph exploration
- Medal distribution analytics
- Event timeline visualization
- Weather condition monitoring

## 📈 Visualizations

### Knowledge Graph (KG)

<video controls style="max-width: 100%; height: auto;">
    <source src="https://github.com/user-attachments/assets/658f405b-1bb0-4980-a400-3d5f406004de" type="video/mp4">
    Your browser does not support the video tag. <a href="https://github.com/user-attachments/assets/658f405b-1bb0-4980-a400-3d5f406004de">View video</a>
</video>

### Medals queries

<video controls style="max-width: 100%; height: auto;">
    <source src="https://github.com/user-attachments/assets/4e7920f0-ad43-4de1-9c53-3b1f42af2989" type="video/mp4">
    Your browser does not support the video tag. <a href="https://github.com/user-attachments/assets/4e7920f0-ad43-4de1-9c53-3b1f42af2989">View video</a>
</video>

### Simple charts

![img2](https://raw.githubusercontent.com/marcpinet/websem-og24/main/./readme-assets/someviz.png)

## 🛠️ Prerequisites

- Python 3.8+
- Docker 20.10+
- 4GB RAM minimum (8GB recommended for full graph processing)

## 🚀 Quick Start

1. Clone and install dependencies:

```bash
git clone https://github.com/[username]/jo2024-semantic.git
cd jo2024-semantic
pip install -r requirements.txt
```

2. Launch weather service:

```bash
docker compose up -d
```

3. Run data pipeline:

```bash
python 01_data_enricher.py  # NLP-based enrichment
python 02_data_linking.py   # Knowledge base linking
python 03_generate_graph.py # Visualization generation
```

## 📊 Key Results

- Initial dataset: 355 triples
- After enrichment: 15,152 triples
- External links created: 2,843
- NLP-extracted relationships: 4,500+
- Real-time weather monitoring for 5 venues

## 🔍 Available Analysis

1. Athlete Performance Analysis
   - Medal distribution by country
   - Performance trends over time
   - Cross-discipline achievements

2. Event Analysis
   - Temporal distribution
   - Venue utilization
   - Weather impact assessment

3. Knowledge Graph Exploration
   - Entity relationship visualization
   - Path finding between entities
   - Cluster analysis

## ⚠️ Known Limitations

- Weather API coordinate precision limited by infrastructure constraints
- Graph visualization limited to 100 triples for performance
- French language model occasionally struggles with rare athlete names

## 🗺️ Future Development

- Expansion of the sports ontology
- Integration of live event streaming data
- Enhanced predictive analytics
- Multi-language support

## ✍️ Authors

- Marc Pinet - [marcpinet](https://github.com/marcpinet)
- Arthur Rodriguez - [rodriguezarthur](https://github.com/rodriguezarthur)
- Amine Haddou - [H4znow](https://github.com/H4znow)

## 📄 License

MIT License - see LICENSE file for details.

---
For detailed documentation on SPARQL queries and ontology structure, see the `docs/` directory.