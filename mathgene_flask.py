from flask import Flask
from flask import render_template_string
from flask import request

import json

import mathgene

app = Flask(__name__)

@app.route("/")
def hello():
	return render_template_string(page_template,person = PERSON)
	#return json.dumps(PERSON)
    #return "Hello World!"

"""
{"name": "Emilio Frazzoli", 
"degree": "Ph.D.",
"id": 114748, 
"location": "UnitedStates",
"thesis": "Robust Hybrid Control for Autonomous Vehicle Motion Planning",
"year": 2001,
"institution": "Massachusetts Institute of Technology"}
"students": [{"id": 173538, "name": "Amit Bhatia"}, {"id": 168010, "name": "Sertac Karaman"}, {"id": 167876, "name": "Jerome Le Ny"}, {"id": 190986, "name": "Marco Pavone"}, {"id": 133492, "name": "Ketan Savla"}, {"id": 130959, "name": "Vikrant Sharma"}, {"id": 188052, "name": "Kyle Treleaven"}],
"advisers": [{"id": 68471, "name": "Eric Marie Feron"}, {"id": 86014, "name": "Munther Abdullah Dahleh"}],
"""

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

def get_math(id):
	return mathgene.download_mathematician(id)

@app.route("/math")
def math():
	id = request.args.get('id', None)
	id = int(id)

	person = get_math(id)
	return render_template_string(page_template, person = person)




with open('Emilio.json','r') as f:
	PERSON = json.load(f)


if __name__ == "__main__":
	#person = get_math(mathgene.EMILIO)

	app.run()