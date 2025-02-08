---
layout: archive
title: "Publications"
permalink: /publications/
---

{% include base_path %}

<style>
.filter-container {
  margin: 20px 0;
  display: flex;
  gap: 20px;
  flex-wrap: wrap;
}

.filter-section {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.filter-title {
  font-weight: bold;
  margin-bottom: 5px;
}

.filter-buttons {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.filter-btn {
  padding: 6px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  background: white;
  cursor: pointer;
  transition: all 0.2s;
}

.filter-btn:hover {
  background: #f0f0f0;
}

.filter-btn.active {
  background: #2a6496;
  color: white;
  border-color: #2a6496;
}

.publication {
  margin-bottom: 20px;
  padding: 15px;
  border: 1px solid #eee;
  border-radius: 4px;
  transition: all 0.2s;
}

.publication:hover {
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.publication-title {
  color: #2a6496;
  text-decoration: none;
  font-weight: bold;
}

.publication-title:hover {
  text-decoration: underline;
}

.hidden {
  display: none;
}
</style>

<div class="filter-container">
  <div class="filter-section">
    <div class="filter-title">Filter by Year</div>
    <div class="filter-buttons" id="year-filters">
      <button class="filter-btn active" data-year="all">All Years</button>
      {% assign years = site.data.publications | map: "year" | uniq | sort | reverse %}
      {% for year in years %}
        <button class="filter-btn" data-year="{{ year }}">{{ year }}</button>
      {% endfor %}
    </div>
  </div>

  <div class="filter-section">
    <div class="filter-title">Show Only</div>
    <div class="filter-buttons">
      <button class="filter-btn active" data-note="all">All Publications</button>
      <button class="filter-btn" data-note="true">Awarded Papers</button>
    </div>
  </div>
</div>

<div id="publication-list">
  {% for publication in site.data.publications %}
    <div class="publication" 
         data-year="{{ publication.year }}" 
         data-has-note="{% if publication.note %}true{% else %}false{% endif %}">
      <a href="{{ publication.paperurl }}" class="publication-title">{{ publication.title }}</a>
      <div>{{ publication.authors }}.</div>
      <div><i>{{ publication.venue }} {{ publication.year }}</i>.</div>
      {% if publication.note %}
        <div><b>{{ publication.note }}</b></div>
      {% endif %}
    </div>
  {% endfor %}
</div>

<script>
document.addEventListener('DOMContentLoaded', function() {
  const yearBtns = document.querySelectorAll('[data-year]');
  const noteBtns = document.querySelectorAll('[data-note]');
  const publications = document.querySelectorAll('.publication');
  
  let activeYear = 'all';
  let activeNote = 'all';

  function updateFilters() {
    publications.forEach(pub => {
      const yearMatch = activeYear === 'all' || pub.dataset.year === activeYear;
      const noteMatch = activeNote === 'all' || 
                       (activeNote === 'true' && pub.dataset.hasNote === 'true');
      
      if (yearMatch && noteMatch) {
        pub.classList.remove('hidden');
      } else {
        pub.classList.add('hidden');
      }
    });
  }

  yearBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      yearBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      activeYear = btn.dataset.year;
      updateFilters();
    });
  });

  noteBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      noteBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      activeNote = btn.dataset.note;
      updateFilters();
    });
  });
});
</script>