#1
SELECT DISTINCT plane.number number
FROM airplanes plane, airlines line, airlines_has_airplanes aha
WHERE
	plane.manufacturer = "Airbus" 
	AND aha.airplanes_id = plane.id
    AND aha.airlines_id = line.id
    AND line.name = "Lufthansa";

#2
SELECT DISTINCT line.name name
FROM airports port1, airports port2, airlines line, routes r
WHERE
	r.source_id = port1.id 
	AND port1.city = "Athens" 
    AND r.destination_id = port2.id 
    AND port2.city = "Prague" 
    AND r.airlines_id = line.id;
    
#3
SELECT COUNT(fhp.passengers_id) number
FROM flights f, flights_has_passengers fhp, airlines line, routes r
WHERE
	f.date = '2012-02-19' 
	AND fhp.flights_id = f.id 
	AND line.name = "Aegean Airlines" 
	AND f.routes_id = r.id;
    
#4
SELECT DISTINCT "yes" result
WHERE EXISTS
    (SELECT f.id
	FROM flights f, routes r, airlines line, airports port1, airports port2
	WHERE 
		r.source_id = port1.id AND port1.name = "Athens El. Venizelos"
		AND r.destination_id = port2.id AND port2.name = "London Gatwick"
		AND f.date = '2014-12-12' AND f.routes_id = r.id 
		AND line.id = r.airlines_id AND line.name = "Olympic Airways")

UNION

SELECT DISTINCT "no" result
WHERE NOT EXISTS 
    (SELECT f.id
	FROM flights f, routes r, airlines line, airports port1, airports port2
	WHERE
		r.source_id = port1.id AND port1.name = "Athens El. Venizelos"
		AND r.destination_id = port2.id AND port2.name = "London Gatwick"
		AND f.date = '2014-12-12' AND f.routes_id = r.id 
		AND line.id = r.airlines_id AND line.name = "Olympic Airways");
	
#5
SELECT AVG(2022 - p.year_of_birth) age
FROM passengers p, airports port, flights f, routes r, flights_has_passengers fhp
WHERE
	r.destination_id = port.id AND port.city = "Berlin"
	AND r.id = f.routes_id 
    AND f.id = fhp.flights_id AND fhp.passengers_id = p.id;

#6
SELECT DISTINCT p.name name, p.surname surname
FROM flights f1, airplanes plane1, flights_has_passengers fhp1, passengers p
WHERE
	fhp1.flights_id = f1.id AND fhp1.passengers_id = p.id AND plane1.id = f1.airplanes_id 
	AND NOT EXISTS
		(SELECT f2.id
		FROM flights f2, airplanes plane2, flights_has_passengers fhp2
		WHERE 
			f2.id != f1.id AND plane2.id != plane1.id 
			AND fhp2.passengers_id = p.id 
            AND fhp2.flights_id = f2.id 
            AND f2.airplanes_id = plane2.id);
        
#7
SELECT port1.city source_city, port2.city destination_city
FROM flights f, routes r, airports port1, airports port2, flights_has_passengers fhp
WHERE
	port1.id != port2.id 
    AND f.routes_id = r.id AND f.id = fhp.flights_id 
	AND port1.id = r.source_id AND port2.id = r.destination_id
    AND f.date >= '2010-03-01' AND f.date <= '2014-07-17'
GROUP BY f.id
HAVING COUNT(fhp.passengers_id) > 5;

#8
SELECT line.name name, line.code code, COUNT(DISTINCT r.id) num
FROM airlines line, routes r, airlines_has_airplanes aha
WHERE line.id = r.airlines_id AND line.id = aha.airlines_id
GROUP BY line.id
HAVING COUNT(DISTINCT aha.airplanes_id) = 4;

#9
SELECT p.name name, p.surname surname
FROM passengers p
WHERE NOT EXISTS
		(SELECT line.id
        FROM airlines line
        WHERE
            line.active = "Y"
            AND NOT EXISTS
				(SELECT r.id
                FROM flights_has_passengers fhp, flights f, routes r
				WHERE
					p.id = fhp.passengers_id
					AND fhp.flights_id = f.id
					AND f.routes_id = r.id
                    AND r.airlines_id = line.id));
                    
#10
SELECT p.name name, p.surname surname
FROM passengers p, airlines line, flights_has_passengers fhp1, flights f1, routes r1
WHERE
	p.id = fhp1.passengers_id
	AND fhp1.flights_id = f1.id
	AND f1.routes_id = r1.id
	AND r1.airlines_id = line.id
    AND line.name = "Aegean Airlines"
    AND NOT EXISTS 
		(SELECT r2.id
		FROM flights_has_passengers fhp2, flights f2, routes r2
        WHERE 
        	p.id = fhp2.passengers_id
			AND fhp2.flights_id = f2.id
			AND f2.routes_id = r2.id
            AND r2.airlines_id != line.id)

UNION

SELECT p.name name, p.surname surname
FROM passengers p, flights_has_passengers fhp, flights f
where 
	p.id = fhp.passengers_id AND fhp.flights_id = f.id
	AND f.date >= '2011-01-02' AND f.date <= '2013-12-31'
GROUP BY p.id
HAVING COUNT(DISTINCT f.id) > 1;
