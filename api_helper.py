import db_util
from core_objects import Show, State,Territory,District,Movie
from view_objects import MoviePerformanceAnalytics
import json
from datetime import datetime
from flask import jsonify, make_response

MOVIE_ANALYTICS_CRITERIA_BY_DAY='day'
MOVIE_ANALYTICS_CRITERIA_BY_THEATRE='theatre'
MOVIE_ANALYTICS_CRITERIA_BY_TERRITORY='territory'
MOVIE_ANALYTICS_CRITERIA_BY_DISTRICT='district'

def get_states():
    connection=db_util.get_connection()
    cursor=connection.cursor(dictionary=True)
    query="select * from states"
    cursor.execute(query)
    result_set=cursor.fetchall()
    state_list=[]

    for row in result_set:
        state=State()
        state.load(row)
        state_list.append(state.to_json())
    connection.close()
    return json.dumps(state_list)


def get_territories(state_id):
    state_territory_map={}
    connection=db_util.get_connection()
    cursor=connection.cursor(dictionary=True)
    query="select * from territories t inner join states s on t.state_id=s.state_id"
    if(state_id>0):
        query=query+' where s.state_id={};'.format(state_id)
    cursor.execute(query)
    result_set=cursor.fetchall()

    for row in result_set:
        territory=Territory()
        territory.load(row)
        t_list=state_territory_map.get(territory.state)
        if t_list is None:
            t_list=[]
        t_list.append(territory.to_json())
        state_territory_map[territory.state]=t_list
    connection.close()
    return json.dumps(state_territory_map)

def get_districts(territory_id):
    query="select d.district_id,d.dist_name,d.territory_id,t.territory,t.state_id,s.state from districts d inner join territories t on d.territory_id=t.territory_id inner join states s on s.state_id=t.state_id"
    if(territory_id>0):
        query=query+" where t.territory_id={}".format(territory_id)
    connection=db_util.get_connection()
    cursor=connection.cursor(dictionary=True)
    cursor.execute(query)
    resultset=cursor.fetchall()   
    territory_district_map={}

    for row in resultset:
        district= District()
        district.load(row)
        dist_list=territory_district_map.get(district.territory)
        if dist_list is None:
            dist_list=[]
            dist_list.append(district.to_json())
            territory_district_map[district.territory]=dist_list
    connection.close()
    return json.dumps(territory_district_map)

def get_movie_analytics(filters,criteria):
    int_filter_map={}
    str_filter_map={}
    state_id=int(filters[State.COL_ID])
    int_filter_map['s.state_id']=state_id
    territory_id=int(filters[Territory.COL_TERRITORY_ID])
    int_filter_map['t.territory_id']=territory_id
    district_id=int(filters[District.COL_DISTRICT_ID])
    int_filter_map['d.district_id']=district_id
    movie_id=filters[Movie.COL_MOVIE_ID]
    str_filter_map['shows.movie_id']=movie_id
    from_date=filters['from_date']
    to_date=filters['to_date']

    query="select s.state_id,s.state,t.territory_id,t.territory,d.district_id,d.dist_name,shows.movie_id,shows.theatre_id,shows.show_id,"
    query+=' shows.cut_off_time,shows.json_data,IFNULL(theatres.theatre_name,\' \') as theatre_name'
    query+=' from shows inner join districts d on shows.dist_id=d.district_id'
    query+=' inner join territories t on t.territory_id=d.territory_id'
    query+=' inner join states s on s.state_id=t.state_id'
    query+=' left join theatres on theatres.theatre_id=shows.theatre_id'
    query+=' where (1=1)'
    query=add_filters(query,int_filter_map,True)
    query=add_filters(query,str_filter_map,False)
    if from_date is not None:
        query+= ' and shows.cut_off_time>'+'\'{}\''.format(from_date+'0000')
    if to_date is not None:
        query+= ' and shows.cut_off_time<'+'\'{}\''.format(to_date+'2359')

    connection=db_util.get_connection()
    cursor=connection.cursor(dictionary=True)
    cursor.execute(query)
    resultset=cursor.fetchall()
    connection.close()

    show_map_extended={}

    for row in resultset:
        show=Show()
        show.load(row)
        key=''
        if(criteria==MOVIE_ANALYTICS_CRITERIA_BY_DAY):
            key=str(show.cut_off_time)
        elif(criteria==MOVIE_ANALYTICS_CRITERIA_BY_THEATRE):
            key=str(show.theatre_id)
        elif(criteria==MOVIE_ANALYTICS_CRITERIA_BY_TERRITORY):
            key=str(show.territory)
        elif(criteria==MOVIE_ANALYTICS_CRITERIA_BY_DISTRICT):
            key=str(show.dist_name)
        else:
            return make_response(jsonify({'FAILURE REASON':'PROVIDE A VALID OPTION(1,2,3,4)'}), 400)
        show_list=show_map_extended.get(key)
        if show_list is None:
            show_list=[]
        show_list.append(show)
        show_map_extended[key]=show_list

    
    show_map_condensed={}

    for key in show_map_extended.keys():
        show_list=show_map_extended[key]
        shows=0
        movie_total_tickets=0
        movie_tickets_sold=0
        housefulls=0
        movie_revenue=0
        for show in show_list:
            show_details=json.loads(show.json_data)
            ticket_categories=show_details['BookMyShow']['arrShowInfo']
            show_total_tickets=0
            show_available_tickets=0
            show_revenue=0
            for ticket_category in ticket_categories:
                show_total_tickets+=int(ticket_category['TotalSeats'])
                show_available_tickets+=int(ticket_category['AvailableSeats'])
                show_revenue+=int(ticket_category['Price'])*(show_total_tickets-show_available_tickets)
            shows+=1
            movie_total_tickets+=show_total_tickets
            movie_tickets_sold+=(show_total_tickets-show_available_tickets)
            housefulls = housefulls+1 if show_available_tickets==0 else housefulls
            movie_revenue+=show_revenue    
        movie_perf_analytics=MoviePerformanceAnalytics(shows,movie_total_tickets,movie_tickets_sold,housefulls,movie_revenue)
        if(criteria==MOVIE_ANALYTICS_CRITERIA_BY_DAY):
            final_key=date = datetime.strptime(key, '%Y%m%d').strftime('%d/%m/%Y')
        elif(criteria==MOVIE_ANALYTICS_CRITERIA_BY_THEATRE):
            final_key=str(show.theatre_id)+'|'+str(show.theatre_name)
        elif(criteria==MOVIE_ANALYTICS_CRITERIA_BY_TERRITORY):
            final_key=str(show.territory)
        elif(criteria==MOVIE_ANALYTICS_CRITERIA_BY_DISTRICT):
            final_key=str(show.dist_name)
        show_map_condensed[final_key]=movie_perf_analytics.to_json()
    return show_map_condensed
        




def add_filters(query,filter_map,filter_type_is_int):
    for key in filter_map.keys():
        if filter_map[key] is not None and (int(filter_map[key])>0 if filter_type_is_int else len(filter_map[key])>0):
            query+=' and '+key+' = '
            if filter_type_is_int:
                query+=str(filter_map[key])
            else:
                query+='\'' + str(filter_map[key]) + '\''
    return query





