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
<div id="student-list">
  {% for person in site.data.students %}
    <div class="student-profile">
      <div class="student-profile-top">
        <img src="{{ person.imageurl }}" class="student-image"/>
      </div>
      <div class="student-profile-bottom">
        <a href="{{ person.website }}" class="student-name">
          {{ person.name }}
        </a>
      </div>
        <div> 
        {{ person.note }}
      </div>
    </div>
  {% endfor %}
</div>

<h2 class="page__content page__content-people-title">Past Members</h2>
<div id="student-list">
  {% for person in site.data.past-members %}
    <div class="student-profile">
      <div class="student-profile-top">
        <img src="{{ person.imageurl }}" class="student-image"/>
      </div>
      <div class="student-profile-bottom">
        <a href="{{ person.website }}" class="student-name">
          {{ person.name }}         </a>
      </div>
        <div> 
        {{ person.note }}
      </div>
    </div>
  {% endfor %}
</div>