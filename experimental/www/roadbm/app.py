from flask import Flask
from flask import request

from flask import jsonify


# domain
import roadbm_json
import setiptah.roadbm.bm as bm
import json

app = Flask(__name__)

@app.route('/', methods=['GET'])
def roads_bipartite_match():
	data = { key: value for key, value in request.args.iteritems() }

	query_json = data['query']
	query = json.loads(query_json)

	inst = roadbm_json.RoadMatchInstance.from_json(query)

	S = inst.source_points()
	T = inst.target_points()
	roadmap = inst.get_roadmap()

	match = bm.ROADSBIPARTITEMATCH(S, T, roadmap)

	return jsonify(match)
	

if __name__ == "__main__":
	app.run()