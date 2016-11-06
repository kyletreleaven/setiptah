from flask import Flask
from flask import render_template_string
from flask import request

import json

#import mathgene
import mathgene_cache


app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

page_template = """
<p>Hello, {{ person.name }} [{{ person.id }}]!</p>
<div id="degree">
	<p>
		{{ person.degree }},
		{{ person.year }},
		{{ person.institution }}
	</p>
</div>
<p>Thesis: {{ person.thesis }}</p>

<br>
<p>Advisers</p>
<ul>
	{% for a in person.advisers %}
	<li>
		{{ a.name }}
		[<a href="math?id={{ a.id }}">{{a.id}}</a>]
	</li>
	{% endfor %}
</ul>

<br>
<p>Students</p>
<ul>
	{% for a in person.students %}
	<li>
		{{ a.name }}
		[<a href="math?id={{ a.id }}">{{a.id}}</a>]
	</li>
	{% endfor %}
</ul>
"""

@app.route("/math")
def math():
	id = request.args.get('id', None)
	id = int(id)

	person = CACHE.get_mathematician(id)
	return render_template_string(page_template, person = person)


"""
with open('Emilio.json','r') as f:
	PERSON = json.load(f)
"""

if __name__ == "__main__":
	import argparse
	import pickle

	parser = argparse.ArgumentParser()
	#parser.add_argument('--reset',type=bool,action='store_true')
	parser.add_argument('--cache', type=str, default='cache.pickle')
	
	args = parser.parse_args()

	#CACHE = mathgene_cache.MiniCache()
	CACHE = mathgene_cache.SQLiteCache(args.cache)
	
	app.run()