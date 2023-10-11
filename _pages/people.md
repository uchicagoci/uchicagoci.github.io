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
      <div class="faculty-profile-left">
        <img src="{{ person.imageurl }}" class="faculty-image"/>
      </div>
      <div class="faculty-profile-right">
        <a href="{{ person.website }}" class="faculty-name">
          {{ person.name }}
        </a>
        <div class="faculty-email">
          {{ person.email }}
        </div>
        <div class="faculty-interest">
          {% for interest in person.interests %}
            <span class="faculty-interest-item">
              {{ interest }}
            </span>
          {% endfor %}
        </div>
      </div>
    </div>
  {% endfor %}
</div>

<h2 class="page__content page__content-people-title">Postdocs, Students, and Researchers</h2>