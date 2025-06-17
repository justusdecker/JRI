from markdown import markdown

JINJA = """{% extends "default.html" %}

{% block title %}
Create a Lets Play
{% endblock %}

{% block c_content %}
__INSERT__
{% endblock %}
{% block css %}<link rel="stylesheet" href="{{ url_for('static', filename='help_style.css') }}">{% endblock %}
"""
def whelp():
    with open('.GITHUB\\WIKI\\main.md') as f1:
        
        with open('templates\\help.html','w') as f2:
            f2.write(JINJA.replace('__INSERT__',markdown(f1.read())))
