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
      {{ publication.authors }} ({{ publication.venue }} {{ publication.year }})
    </div>
  {% endfor %}
</div>