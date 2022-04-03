from crypt import methods
from flask import Flask, request
import api_helper

app = Flask(__name__)

@app.route('/get_states',methods=['GET'])
def get_states():
    return api_helper.get_states()
    
@app.route('/get_territories/<state_id>',methods=['GET'])
def get_territories(state_id):
    state_id=int(state_id)
    return api_helper.get_territories(state_id)

@app.route('/get_districts/<territory_id>',methods=['GET'])
def get_districts(territory_id):
    territory_id=int(territory_id)
    return api_helper.get_districts(territory_id)

@app.route('/movieanalyticsbyday',methods=['GET'])
def get_movie_analytics_by_day():
    filters=request.get_json()
    return api_helper.get_movie_analytics_by_day(filters)
    

if __name__ == "__main__":
    app.run()
