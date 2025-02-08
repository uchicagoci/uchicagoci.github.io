---
layout: archive
title: "Publications"
permalink: /publications/
---

{% include base_path %}

<div id="publication-list">
  {% for publication in site.data.publications %}
    <div class="publication">
      <a href="{{ publication.paperurl }}" class="publication-title">{{ publication.title }}</a>
      {{ publication.authors }}.
      <i>{{ publication.venue }} {{ publication.year }}</i>. 
      {% if publication.note %}
        <b>{{ publication.note }}</b>.
      {% endif %}
    </div>
  {% endfor %}
</div>