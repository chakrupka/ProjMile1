import datetime, mysql.connector, re, string
from flask import Flask, render_template, request, url_for, redirect


app = Flask(__name__)

DATABASE_CONFIG = {
    'user': 'username',
    'password': 'password',
    'host': '127.0.0.1',
    'database': 'nbaplayers',
    'raise_on_warnings': True
}


@app.route('/')
def home():
    return render_template('index.html')


def sanitizer(in_str):
    interim_str = in_str.replace(" ", "%").replace("-", "%")
    sanitized_str = re.sub(r'[^a-zA-Z0-9%]', '', interim_str)
    return sanitized_str


def query_playername(player_name):
    conn = mysql.connector.connect(**DATABASE_CONFIG)
    cur = conn.cursor()

    cur.execute("SELECT p.name, di.draft_year, p.id FROM players p JOIN draftinfo di on p.id = di.id WHERE name LIKE %s ORDER BY di.draft_year DESC", ('%' + sanitizer(player_name) + '%',))
    data = cur.fetchall()

    cur.close()
    conn.close()
    return data


def query_playerdata(id):
    conn = mysql.connector.connect(**DATABASE_CONFIG)
    cur = conn.cursor()
    data = []

    # Name
    cur.execute("SELECT id, name FROM players WHERE id = %s", (id,))
    data.append(cur.fetchone())

    # Game-related stats
    cur.execute("SELECT cs.career_g, cs.career_per, cs.career_ws, pg.career_ast, pg.career_pts, pg.career_trb, s.career_fg, s.career_fg3, s.career_ft, s.career_efg FROM careerstats cs JOIN pergame pg ON cs.id = pg.id JOIN splits s ON pg.id = s.id WHERE cs.id = %s", (id,))
    data.append(cur.fetchone())

    # Draft info
    cur.execute("SELECT draft_pick, draft_round, draft_team, draft_year FROM draftinfo WHERE id = %s", (id,))
    data.append(cur.fetchone())

    # Medical info
    cur.execute("SELECT birthdate, height, weight FROM medinfo WHERE id =  %s", (id,))
    data.append(cur.fetchone())

    # Playstyle
    cur.execute("SELECT position, shoots FROM playstyle WHERE id =  %s", (id,))
    data.append(cur.fetchone())

    # Education and Origin
    cur.execute("SELECT CONCAT(o.birthcity, ', ', o.birthloc), e.highschool, CONCAT(e.hscity,', ',e.hsloc), e.college FROM origin o JOIN education e on o.id = e.id  WHERE o.id = %s", (id,))
    data.append(cur.fetchone())

    cur.close()
    conn.close()
    return data


def query_playersalaries(id):
    conn = mysql.connector.connect(**DATABASE_CONFIG)
    cur = conn.cursor()
    
    cur.execute("SELECT s.season, t.team, FORMAT(s.salary,0) FROM salaries s JOIN teams t on s.team_id = t.team_id WHERE id = %s", (id,))
    data = cur.fetchall()

    cur.close()
    conn.close()
    return data


def query_totalsalaries(id):
    conn = mysql.connector.connect(**DATABASE_CONFIG)
    cur = conn.cursor()
    
    cur.execute("SELECT FORMAT(SUM(s.salary),0) FROM salaries s WHERE id = %s GROUP BY s.id", (id,))
    data = cur.fetchone()

    cur.close()
    conn.close()
    return data


@app.route('/playersearch/', methods=['GET', 'POST'])
def psearch():
    players = ""
    if request.method == 'POST':
        req = request.form.get('player_name')
        if req != "" and not bool(re.match('^[^a-zA-Z0-9]*$', req)):
            players = query_playername(req)
    return render_template('playersearch.html', players = players)


@app.route('/nbasalaries/')
def nbasalaries():
    conn = mysql.connector.connect(**DATABASE_CONFIG)
    cur = conn.cursor()
    
    cur.execute("SELECT o.birthloc, SUM(s.salary) AS total_salary_unformatted, FORMAT(SUM(s.salary), 0) AS total_salary_formatted, COUNT(DISTINCT s.id) AS num_of_players, FORMAT(SUM(s.salary) / COUNT(DISTINCT s.id),0) AS avg_salary_per_player FROM salaries s JOIN origin o ON s.id = o.id GROUP BY o.birthloc ORDER BY total_salary_unformatted DESC")
    locsals = cur.fetchall()

    cur.execute("SELECT e.college, SUM(s.salary) AS total_salary_unformatted, FORMAT(SUM(s.salary), 0) AS total_salary_formatted, COUNT(DISTINCT s.id) AS num_of_players, FORMAT(SUM(s.salary) / COUNT(DISTINCT s.id),0) AS avg_salary_per_player FROM salaries s JOIN education e ON s.id = e.id WHERE e.college IS NOT NULL GROUP BY e.college ORDER BY total_salary_unformatted DESC LIMIT 50;")
    colsals = cur.fetchall()

    cur.execute("WITH seasavg AS (SELECT season, AVG(salary) avgsal FROM salaries GROUP BY SEASON) SELECT season, FORMAT(ROUND(avgsal),0), ROUND((avgsal-lag(avgsal) OVER (ORDER BY season)) / LAG(avgsal) OVER (ORDER BY season) * 100, 1) FROM seasavg ORDER BY season DESC")
    avgsals = cur.fetchall()

    cur.execute("SELECT p.name, SUM(s.salary) sal FROM players p JOIN salaries s ON p.id = s.id GROUP BY p.name ORDER BY sal DESC LIMIT 50")
    topearns = cur.fetchall()

    cur.execute("SELECT mi.height, FORMAT(AVG(y.totalyrs),0) yrsfor, AVG(y.totalyrs) yrsunfor FROM medinfo mi JOIN years y ON y.id = mi.id GROUP BY mi.height ORDER BY yrsunfor DESC")
    heights = cur.fetchall()

    cur.close()
    conn.close()

    return render_template('salaries.html', locsalaries = locsals, collegesals = colsals, averages = avgsals, topttls = topearns, yrheight = heights)


@app.route('/playerinfo/<id>/')
def pinfo(id):
    stats = query_playerdata(id)
    salaries = query_playersalaries(id)
    totalsal = query_totalsalaries(id)
    return render_template('playerinfo.html', pstats=stats, psals = salaries, ptotal = totalsal)


@app.route('/team/<teamid>/')
def teaminfo(teamid):
    conn = mysql.connector.connect(**DATABASE_CONFIG)
    cur = conn.cursor()

    cur.execute("SELECT p.id, p.name, SUM(s.salary) AS sal_unformatted, FORMAT(SUM(s.salary), 0) AS sal_formatted FROM salaries s JOIN players p ON p.id = s.id WHERE s.season = \"2017-18\" AND s.team_id = %s GROUP BY p.id, p.name ORDER BY sal_unformatted DESC", (teamid,))
    data = cur.fetchall()

    cur.execute("SELECT team FROM teams WHERE team_id = %s", (teamid,))
    team = cur.fetchone()

    cur.execute("SELECT FORMAT(SUM(salary),0) FROM salaries WHERE season = \"2017-18\" AND team_id = %s GROUP BY team_id", (teamid,))
    payroll = cur.fetchone()

    cur.close()
    conn.close()
    return render_template('team.html', payroll = data, team = team, ptotal = payroll)


@app.route('/teams/')
def teams():
    conn = mysql.connector.connect(**DATABASE_CONFIG)
    cur = conn.cursor()

    cur.execute("SELECT * FROM teams WHERE team_id NOT IN (4, 14, 21, 22, 24, 33, 36, 37)")
    data = cur.fetchall()

    cur.close()
    conn.close()
    return render_template('teams.html', teams=data)


@app.route('/about/')
def about():
    return render_template('about.html')


def handle_all_exceptions(error):
    return render_template("error.html"), 500

app.register_error_handler(Exception, handle_all_exceptions)