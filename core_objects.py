class State:
    COL_ID='state_id'
    COL_STATE='state'

    def to_json(self):
        return{'id':self.id,'state':self.state}

    def load(self,row):
        self.id=row[State.COL_ID]
        self.state=row[State.COL_STATE]

class Territory:
    COL_TERRITORY_ID='territory_id'
    COL_STATE_ID='state_id'
    COL_STATE='state'
    COL_TERRITORY='territory'
    
    def load(self,row):
        self.territory_id=row[Territory.COL_TERRITORY_ID]
        self.state_id=row[Territory.COL_STATE_ID]
        self.state=row[Territory.COL_STATE]
        self.territory=row[Territory.COL_TERRITORY]

    def to_json(self):
        return{'territory_id':self.territory_id,'territory':self.territory}

class District:
    COL_DISTRICT_ID='district_id'
    COL_DIST_NAME='dist_name'


    def load(self,row):
        self.district_id=row[District.COL_DISTRICT_ID]
        self.dist_name=row[District.COL_DIST_NAME]
        self.territory_id=row[Territory.COL_TERRITORY_ID]
        self.territory=row[Territory.COL_TERRITORY]
        self.state_id=row[State.COL_ID]
        self.state=row[State.COL_STATE]

    def to_json(self):
        return{'district_id':self.district_id,'district':self.dist_name}

class Movie:
    COL_MOVIE_ID='movie_id'

class Theatre:
    COL_THEATRE_ID='theatre_id'
    COL_THEATRE_NAME='theatre_name'

class Show(District):
    COL_SHOW_ID='show_id'
    COL_CUT_OFF_TIME='cut_off_time'
    COL_JSON_DATA='json_data'

    def load(self,row):
        District.load(self,row)
        self.movie_id=row[Movie.COL_MOVIE_ID]
        self.theatre_id=row[Theatre.COL_THEATRE_ID]
        self.theatre_name=row[Theatre.COL_THEATRE_NAME]
        self.show_id=row[self.COL_SHOW_ID]
        cut_off_time=row[self.COL_CUT_OFF_TIME]
        self.cut_off_time=cut_off_time[0:8]
        self.json_data=row[self.COL_JSON_DATA]

    def to_json(self):
        return super().to_json()


