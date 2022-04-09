from flask import Flask, request
import api_helper
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/get_states',methods=['POST'])
def get_states():
    return api_helper.get_states()
    
@app.route('/get_territories/<state_id>',methods=['POST'])
def get_territories(state_id):
    state_id=int(state_id)
    return api_helper.get_territories(state_id)

@app.route('/get_districts/<territory_id>',methods=['POST'])
def get_districts(territory_id):
    territory_id=int(territory_id)
    return api_helper.get_districts(territory_id)

@app.route('/get_movies',methods=['POST'])
def get_movies():
    filters=request.get_json()
    movies_from=filters['from_date']+'0000'
    return api_helper.get_movies(movies_from)

@app.route('/movieanalytics',methods=['POST'])
def get_movie_analytics_by_option():
    filters=request.get_json()
    criteria=request.args.get('criteria')
    return api_helper.get_movie_analytics(filters,criteria)


if __name__ == "__main__":
    app.run()
