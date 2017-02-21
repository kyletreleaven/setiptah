from flask import Flask, jsonify
app = Flask(__name__)

@app.route('/')
def hello_world():
    if False:
    	return 'Hello, World!'
    else:
    	data = [(0,1)]
    	return jsonify(data)

if __name__ == "__main__":
	app.run()