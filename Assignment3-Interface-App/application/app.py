# ----- CONFIGURE YOUR EDITOR TO USE 4 SPACES PER TAB ----- #
import settings
import sys,os
sys.path.append(os.path.join(os.path.split(os.path.abspath(__file__))[0], 'lib'))
import pymysql as db
import random
def connection():
    ''' User this function to create your connections '''
    con = db.connect(
        settings.mysql_host, 
        settings.mysql_user, 
        settings.mysql_passwd, 
        settings.mysql_schema)
    
    return con



def findAirlinebyAge(x,y):
    
    # Create a new connection
    # Create a new connection
    con=connection()
    # Create a cursor on the connection
    cur=con.cursor()
    xint = int(x)
    yint = int(y)

   #######
   #(Implementation details)
   # In case, x > y => y < AgeGroup < x , where AgeGroup is the wanted result we use the 'and' operator for the sql query 
   # In case, x < y => AgeGroup < x && AgeGroup > y  where AgeGroup is the wanted result we use the 'or' operator for the sql query
   ########
   
    if xint > yint :
        find_airline = """
            Select distinct airlines.name, count(distinct passengers.id)
            from airlines, flights, flights_has_passengers, passengers, routes
            where (flights.id = flights_has_passengers.flights_id and passengers.id = flights_has_passengers.passengers_id) and 
            flights.routes_id = routes.id and routes.airlines_id = airlines.id and 
            ((2022 - passengers.year_of_birth) < '%d' and (2022 - passengers.year_of_birth) > '%d')
            group by airlines.id
            order by count(distinct passengers.id) desc
            """ %(xint,yint)
    else :
        find_airline = """Select distinct airlines.name, count(distinct passengers.id)
            from airlines, flights, flights_has_passengers, passengers, routes
            where (flights.id = flights_has_passengers.flights_id and passengers.id = flights_has_passengers.passengers_id) and 
            flights.routes_id = routes.id and routes.airlines_id = airlines.id and 
            ((2022 - passengers.year_of_birth) < '%d' or (2022 - passengers.year_of_birth) > '%d')
            group by airlines.id
            order by count(distinct passengers.id) desc
            """ %(xint,yint)
        
    cur.execute(find_airline)
    
    airline = cur.fetchone()
    
    find_airplanes = """    
                    select count(distinct airplanes.id)
                    from airlines, airlines_has_airplanes, airplanes
                    where airlines.name = '%s' and airlines.id = airlines_has_airplanes.airlines_id 
                    and airlines_has_airplanes.airplanes_id = airplanes.id
                    """ %(airline[0])

    cur.execute(find_airplanes)

    airplanes = cur.fetchone()

    return [("Airline's name: %s" %(airline[0]),"Passenger count: %s" %(airline[1]),"Airplanes' count: %s" %(airplanes[0])),]




def findAirportVisitors(x,a,b):
    
   # Create a new connection
    con=connection()
    
    # Create a cursor on the connection
    cur=con.cursor()

    sql = """select airports.name, count(flights_has_passengers.passengers_id)
            from airlines, routes, airports, flights, flights_has_passengers
            where airlines.id = routes.airlines_id and routes.destination_id = airports.id and routes.id = flights.routes_id and  flights.id = flights_has_passengers.flights_id
	        and airlines.name = '%s' and (flights.date > '%s' and flights.date < '%s')
            group by airports.id
            order by count(flights_has_passengers.passengers_id) desc""" %(x,a,b)

    cur.execute(sql)

    results = cur.fetchall()

    return [("aiport_name", "number_of_visitors"),] + list(results)




def findFlights(x,a,b):

    # Create a new connection
    con=connection()
    # Create a cursor on the connection
    cur=con.cursor()

    sql = """ 
        select flights.id, airlines.alias, airportdestination.name, airplanes.model
        from  airplanes, flights, routes, airports airportdestination, airports airportsource, airlines
        where airplanes.id = flights.airplanes_id and flights.routes_id = routes.id and routes.source_id = airportsource.id and routes.destination_id = airportdestination.id and routes.airlines_id = airlines.id
	    and airlines.active = 'Y' and (flights.date = '%s') and (airportsource.city = '%s') and (airportdestination.city = '%s')
        group by flights.id
        """ %(x,a,b)
    
    cur.execute(sql)

    results=cur.fetchall()
    
    return [("flight_id", "alt_name", "dest_name", "aircraft_model",),] + list(results)
    


def findLargestAirlines(N):
    # Create a new connection
    con=connection()

    # Create a cursor on the connection
    cur=con.cursor()

    find_airlines = """
                select airlines.name, airlines.code, count(distinct airplanes.id), count(distinct flights.id)
                from airlines, flights, routes, airlines_has_airplanes, airplanes
                where flights.routes_id = routes.id and routes.airlines_id = airlines.id and airlines.id = airlines_has_airplanes.airlines_id 
                and airlines_has_airplanes.airplanes_id = airplanes.id
                group by airlines.id
                order by count(distinct flights.id) desc
            """ 

    cur.execute(find_airlines)

    airlines = cur.fetchall()

    results = []
    
    i = 0 
    while i < int(N):
        results.insert(i,airlines[i])
        i += 1

    return [("name", "id", "num_of_aircrafts", "num_of_flights",),] + list(results)






def insertNewRoute(x,y):
    # Create a new connection
    con=connection()

    # Create a cursor on the connection
    cur=con.cursor()
    
   #check if airline has alias
    search_alias = """
                   select airlines.alias
                   from airlines
                   where airlines.alias = '%s'
                   """ %(x)

    cur.execute(search_alias)
    
    search_res = cur.fetchall()

    if not search_res:
        return [("Try another alias",),]


    #find not active destination for the given source airport
    sql = """
            select dest.id 
            from airports dest
            where dest.id not in 
                (select  dest2.id
                from airports source, airports dest2, routes, airlines
                where routes.airlines_id = airlines.id and routes.destination_id = dest2.id and
                routes.source_id = source.id and airlines.alias = '%s'  and source.name = '%s'); 
        """ %(x,y)
    cur.execute(sql)
    new_destination = cur.fetchone()

    if not new_destination:
        return [("airline capacity full",),]

    sql_airlines =  """
                    select airlines.id
                    from airlines
                    where airlines.alias = '%s'
                    """ %(x)
    cur.execute(sql_airlines)
    airline_id = cur.fetchone()


    sql_source = """ 
                    select airports.id
                    from airports
                    where airports.name = '%s'
                """ %(y)
    cur.execute(sql_source)    
    source_id = cur.fetchone()


    route_id = random.randint(0,80000)

    check_route_id = """
                    select routes.id
                    from routes
                    where routes.id = '%d'
                    """ %(route_id)
    
    cur.execute(check_route_id)
    new_route = cur.fetchone()
    
    i = 0
    
    while i < 1:
        if not new_route:
            break

        route_id = random.randint(0,80000)
        check_route_id = """
                    select routes.id
                    from routes
                    where routes.id = '%d'
                    """ %(route_id)
    
        cur.execute(check_route_id)
        new_route = cur.fetchone()

    sql_insert = """
                insert into routes
                values(%d, %d, %d, %d)
                """ %(route_id,airline_id[0],source_id[0],new_destination[0])

    cur.execute(sql_insert)
    con.commit()

    return [("OK",),]
