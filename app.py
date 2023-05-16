import sqlite3
from flask import Flask, render_template,request, url_for ,flash , redirect ,abort

app = Flask(__name__)
app.config['SECRET_KEY'] = 'abc'

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM MANAGERS WHERE MANAGERID = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post
    
def get_venue(venue_id):
	conn = get_db_connection()
	post = conn.execute('SELECT * FROM VENUES WHERE VENUEID = ?',(venue_id,)).fetchone()
	conn.close()
	return post

def get_ref(ref_id):
	conn = get_db_connection()
	post = conn.execute('SELECT * FROM REFEREES WHERE REFEREEID = ?',(ref_id,)).fetchone()
	conn.close()
	return post

def get_team(team_id):
	if (team_id == 1):
		conn = get_db_connection()
		post = conn.execute('SELECT * FROM TEAMS WHERE TEAMID = ?',(team_id,)).fetchone()
		conn.close()
		return post

	if (team_id == 2):
		conn = get_db_connection()
		post = conn.execute('SELECT * FROM TEAMS WHERE TEAMID = ?',(team_id,)).fetchone()
		conn.close()
		return post
    
	if (team_id == 3):
		conn = get_db_connection()
		post = conn.execute('SELECT * FROM TEAMS WHERE TEAMID = ?',(team_id,)).fetchone()
		conn.close()
		return post
    
    
def populate_points():
	conn = get_db_connection()
	temp1 = conn.execute('SELECT * FROM RESULTS WHERE RESULTID = 1').fetchone()
	temp2 = conn.execute('SELECT * FROM RESULTS WHERE RESULTID = 2').fetchone()
	temp3 = conn.execute('SELECT * FROM RESULTS WHERE RESULTID = 3').fetchone()


	conn.execute('INSERT INTO POINTSTABLE VALUES (?,?,?,?,?,?)',(1,1,0,0,0,0))
	conn.execute('INSERT INTO POINTSTABLE VALUES (?,?,?,?,?,?)',(2,1,0,0,0,0))
	conn.execute('INSERT INTO POINTSTABLE VALUES (?,?,?,?,?,?)',(3,1,0,0,0,0))
		
	conn.commit()
	if ( temp1[3] > temp1[4] ):
		conn.execute('UPDATE POINTSTABLE SET MATCHPLAYED = MATCHPLAYED + 1 , WINCOUNT = WINCOUNT + 1 , POINTS = POINTS + 3 WHERE TEAMID == 1')
		conn.execute('UPDATE POINTSTABLE SET MATCHPLAYED = MATCHPLAYED + 1 , LOSSCOUNT = LOSSCOUNT + 1  WHERE TEAMID == 2')
		conn.commit()
	else:
		conn.execute('UPDATE POINTSTABLE SET MATCHPLAYED = MATCHPLAYED + 1 , WINCOUNT = WINCOUNT + 1 , POINTS = POINTS + 3 WHERE TEAMID == 2')
		conn.execute('UPDATE POINTSTABLE SET MATCHPLAYED = MATCHPLAYED + 1 , LOSSCOUNT = LOSSCOUNT + 1  WHERE TEAMID == 1')
		conn.commit()
		
	if ( temp2[3] > temp2[4] ):
		conn.execute('UPDATE POINTSTABLE SET MATCHPLAYED = MATCHPLAYED + 1 , WINCOUNT = WINCOUNT + 1 , POINTS = POINTS + 3 WHERE TEAMID == 1')
		conn.execute('UPDATE POINTSTABLE SET MATCHPLAYED = MATCHPLAYED + 1 , LOSSCOUNT = LOSSCOUNT + 1  WHERE TEAMID == 3')
		conn.commit()
		
	else:
		conn.execute('UPDATE POINTSTABLE SET MATCHPLAYED = MATCHPLAYED + 1 , WINCOUNT = WINCOUNT + 1 , POINTS = POINTS + 3 WHERE TEAMID == 3')
		conn.execute('UPDATE POINTSTABLE SET MATCHPLAYED = MATCHPLAYED + 1 , LOSSCOUNT = LOSSCOUNT + 1  WHERE TEAMID == 1')
		conn.commit()
		
	if ( temp3[3] > temp3[4] ):
		conn.execute('UPDATE POINTSTABLE SET MATCHPLAYED = MATCHPLAYED + 1 , WINCOUNT = WINCOUNT + 1 , POINTS = POINTS + 3 WHERE TEAMID == 3')
		conn.execute('UPDATE POINTSTABLE SET MATCHPLAYED = MATCHPLAYED + 1 , LOSSCOUNT = LOSSCOUNT + 1  WHERE TEAMID == 2')
		conn.commit()
		
	else:
		conn.execute('UPDATE POINTSTABLE SET MATCHPLAYED = MATCHPLAYED + 1 , WINCOUNT = WINCOUNT + 1 , POINTS = POINTS + 3 WHERE TEAMID == 2')
		conn.execute('UPDATE POINTSTABLE SET MATCHPLAYED = MATCHPLAYED + 1 , LOSSCOUNT = LOSSCOUNT + 1  WHERE TEAMID == 3')
		conn.commit()

	conn.commit()

@app.route('/')
def index():
    conn = get_db_connection()
    conn.execute('DROP VIEW IF EXISTS temp1')
    conn.execute('DROP VIEW IF EXISTS temp2')
    conn.execute('CREATE VIEW temp1 AS SELECT MANAGERNAME,MANAGERID,TEAMNAME FROM MANAGERS NATURAL JOIN TEAMS ')
    conn.execute('CREATE VIEW temp2 AS SELECT MEMBERID , MEMBERNAME , TEAMNAME FROM TEAMMEMBERS JOIN TEAMS ON TEAMMEMBERS.TEAMID = TEAMS.TEAMID ')
    MANAGERS = conn.execute ('SELECT * FROM temp1').fetchall()
    PLAYERS = conn.execute ('SELECT * FROM temp2').fetchall()
    
    conn.close()
    return render_template('index.html', MANAGERS=MANAGERS , PLAYERS=PLAYERS)
    
@app.route('/view/' , methods=('GET','POST'))
def view():
	conn = get_db_connection()
	populate_points()
	conn.execute('DROP VIEW IF EXISTS points')
	conn.execute(('CREATE VIEW POINTS AS SELECT TEAMNAME , POINTS , MANAGERNAME FROM TEAMS NATURAL JOIN POINTSTABLE NATURAL JOIN MANAGERS ORDER BY POINTS DESC')) 
	POINTS = conn.execute ('SELECT * FROM POINTS').fetchall()	
	
	conn.close()
	return render_template('view.html' , POINTS=POINTS)
    
@app.route('/create/', methods=('GET', 'POST'))

def create():
    
    if request.method == 'POST':
       
        manager = request.form['Manager']
     
        email = request.form['EMAIL']
        team = request.form['Team']
        sponsor = request.form['Sponsor']
      
        player1= request.form['Player1'] 
        position1= request.form['Position1']
        player2= request.form['Player2'] 
        position2= request.form['Position2']
        player3= request.form['Player3'] 
        position3= request.form['Position3']
        player4= request.form['Player4'] 
        position4= request.form['Position4']
        player5= request.form['Player5'] 
        position5= request.form['Position5']
        
        
        conn = get_db_connection()
        conn.execute('INSERT INTO MANAGERS (MANAGERNAME,AGE,EMAIL) VALUES (?,?,?)',(manager,30,email))
        conn.commit()
        mid = conn.execute (' SELECT MAX(MANAGERID) FROM MANAGERS ').fetchone() 
        conn.execute('INSERT INTO TEAMS (TEAMNAME,SPONSOREDBY,MANAGERID) VALUES (?,?,?)',(team,sponsor,mid[0]))
        conn.commit()
        tid = conn.execute (' SELECT MAX(TEAMID) FROM TEAMS ').fetchone() 
        conn.execute ('BEGIN TRANSACTION')
        conn.execute('INSERT INTO TEAMMEMBERS (MEMBERNAME,POSITION,TEAMID) VALUES (?,?,?)',(player1,position1,tid[0]))
        conn.execute('INSERT INTO TEAMMEMBERS (MEMBERNAME,POSITION,TEAMID) VALUES (?,?,?)',(player2,position2,tid[0]))
        conn.execute('INSERT INTO TEAMMEMBERS (MEMBERNAME,POSITION,TEAMID) VALUES (?,?,?)',(player3,position3,tid[0]))
        conn.execute('INSERT INTO TEAMMEMBERS (MEMBERNAME,POSITION,TEAMID) VALUES (?,?,?)',(player4,position4,tid[0]))
        conn.execute('INSERT INTO TEAMMEMBERS (MEMBERNAME,POSITION,TEAMID) VALUES (?,?,?)',(player5,position5,tid[0]))
        conn.commit()
        
        conn.close()
        return redirect(url_for('index'))

    return render_template('create.html')


@app.route('/<int:id>/edit/', methods=('GET', 'POST'))
def edit(id):
    MANAGER = get_post(id)

    if request.method == 'POST':
        Manager = request.form['Manager']
        managerage = request.form['Manager_Age']
        email = request.form['EMAIL']
        

        if not Manager:
            flash('Name is required!')

        elif not email:
            flash('Email is required!')

        else:
            conn = get_db_connection()
            conn.execute('UPDATE MANAGERS SET MANAGERNAME = ?, EMAIL = ? , AGE = ? '
                         ' WHERE MANAGERID = ?',
                         (Manager, email ,managerage, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('edit.html', MANAGER=MANAGER)
    

@app.route('/<int:id>/delete/', methods=('POST',))
def delete(id):
    MANAGER = get_post(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM MANAGERS WHERE MANAGERID = ?', (id,))
    conn.commit()
    conn.close()
    
    return redirect(url_for('index'))
    
    
    
    
@app.route('/tournament/', methods=('GET', 'POST'))
def tournament():
	if request.method == 'POST':
		tournament = request.form['Tournament']
		organizer = request.form['Organizer']
		entry = request.form['Entry']
		winning = request.form['Winning']
		 
		conn = get_db_connection()
		conn.execute('INSERT INTO TOURNAMENTS(TOURNAMENTNAME,ORGANIZER,REGISTRATIONFEES,WINNINGPRIZE) VALUES (?,?,?,?)',(tournament,organizer,entry,winning))
         
		conn.commit()
		conn.close()
		return redirect(url_for('index'))

	return render_template('tournament.html')
	
@app.route('/fixtures/',methods=('GET', 'POST'))
def fixtures():
	VENUE = get_venue(1)
	REFEREE = get_ref(1)
	OppA = get_team(1)
	OppB = get_team(2)
	OppC = get_team(3)
	
	if request.method == 'POST':
		score1= request.form['Score1']
		score2= request.form['Score2']
		score3= request.form['Score3']
		score4= request.form['Score4']
		score5= request.form['Score5']
		score6= request.form['Score6']
	
		conn = get_db_connection()
		tournament = conn.execute('SELECT MAX(TOURNAMENTID) FROM TOURNAMENTS').fetchone()
		conn.execute('INSERT INTO RESULTS(RESULTID ,OPPONENTA,OPPONENTB,SCOREA,SCOREB,VENUEID,REFEREEID,TOURNAMENTID) VALUES (?,?,?,?,?,?,?,?)', (1,OppA['TEAMID'],OppB['TEAMID'],score1,score2,1,1,tournament[0]))
		conn.execute('INSERT INTO RESULTS(RESULTID ,OPPONENTA,OPPONENTB,SCOREA,SCOREB,VENUEID,REFEREEID,TOURNAMENTID) VALUES (?,?,?,?,?,?,?,?)', (2,OppA['TEAMID'],OppC['TEAMID'],score3,score4,1,1,tournament[0]))
		conn.execute('INSERT INTO RESULTS(RESULTID ,OPPONENTA,OPPONENTB,SCOREA,SCOREB,VENUEID,REFEREEID,TOURNAMENTID) VALUES (?,?,?,?,?,?,?,?)', (3,OppC['TEAMID'],OppB['TEAMID'],score5,score6,1,1,tournament[0]))
		conn.commit()
		conn.close()
		return redirect(url_for('index'))
	return render_template('fixtures.html' , VENUE=VENUE , REFEREE=REFEREE , OppA=OppA , OppB=OppB , OppC=OppC)
