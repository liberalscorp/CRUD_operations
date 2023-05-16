import sqlite3

connection = sqlite3.connect('database.db')


teams = ['Portugal' , 'Argentina']
captains = ['a' , 'f']
players = ['a','b','c','d','e','f','g','h','i','j']
venue = ['Ground-Zero' , 'KU']
location = ['Defence' , 'Gulshan']
matches= [(1,1,1) ,(1,1,2) ,(1,2,1) ,(1,2,2)]


with open('schema.sql') as f:
	connection.executescript(f.read())

cur = connection.cursor()

for i  in range (0,2):
	cur.execute ("INSERT INTO MANAGERS(MANAGERNAME , SALARY , AGE , EMAIL) VALUES (?,?,?,?)" ,('Ahsan' , 12000 , 21 ,'abc@def.com' ) ) 
	cur.execute ("INSERT INTO  TEAMS(TEAMNAME,SPONSOREDBY,MANAGERID) VALUES (?,?,?)" ,(teams[i], 'Nike'  ,i+1 ) ) 
	cur.execute ("INSERT INTO  REFEREES(REFEREENAME) VALUES (?)" ,(players[i] ) )
	cur.execute ("INSERT INTO  VENUES(VENUENAME,LOCATION) VALUES (?,?)" ,(venue[i] , location[i] ) )  
	
	connection.commit()

for i in range (0,2):
	for j in range (0,10):
		if ( i == 0  and j < 5):
		
			cur.execute ("INSERT INTO  TEAMMEMBERS(MEMBERNAME,TEAMID,COACHID,POSITION) VALUES (?,?,?,?)" ,(players[j],i+1,1,'') ) 
			connection.commit()
		
		elif ( i == 1 and j >= 5):
		
			cur.execute ("INSERT INTO  TEAMMEMBERS(MEMBERNAME,TEAMID,COACHID,POSITION) VALUES (?,?,?,?)" ,(players[j],i+1,7,'') ) 
			connection.commit()
		
		
cur.execute ("INSERT INTO TRAININGS(COACHID,DETAILS,DURATION) VALUES(?,?,?)" , (0,'ATTACK',2))
cur.execute ("INSERT INTO TRAININGS(COACHID,DETAILS,DURATION) VALUES(?,?,?)" , (7,'DEFENCE',2))
cur.execute ("INSERT INTO TOURNAMENTS(TOURNAMENTNAME,REGISTRATIONFEES,WINNINGPRIZE,ORGANIZER) VALUES(?,?,?,?)" , ('FUTSAL KARACHI',2000,10000,'MAIDAN') )
cur.execute ("UPDATE TEAMMEMBERS SET COACHID = NULL WHERE MEMBERID = 1 ")
cur.execute ("UPDATE TEAMMEMBERS SET COACHID = NULL WHERE MEMBERID = 7 ")

	

connection.commit()
connection.close()
