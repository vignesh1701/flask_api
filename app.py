from flask import Flask,make_response,jsonify
from flask_cors import cross_origin

app=Flask(__name__)



@app.route('/api')
@cross_origin()
def cors():
    return make_response(jsonify({'message':'wow its working'}))

app.run(debug=True)