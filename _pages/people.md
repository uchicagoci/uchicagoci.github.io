---
permalink: /people/
title: "People"
redirect_from: 
  - /people.html
---

{% include base_path %}

<h2 class="page__content page__content-people-title">Faculty Members</h2>

<div id="faculty-list">
  {% for person in site.data.faculty %}
    <div class="faculty-profile">
      <img src="{{ person.imageurl }}" class="faculty-image"/>
      <a href="{{ person.website }}" class="faculty-name">
        {{ person.name }}
      </a>
      <div class="faculty-email">
        {{ person.email }}
      </div>
      <div class="faculty-interest">{{ person.interests }}</div>
    </div>
  {% endfor %}
</div>

<script defer>
  // randomize order
  var faculty = document.querySelector('#faculty-list');
  for (var i = faculty.children.length; i >= 0; i--) {
      faculty.appendChild(faculty.children[Math.random() * i | 0]);
  }
</script>

<h2 class="page__content page__content-people-title">Postdocs, Students, and Researchers</h2>