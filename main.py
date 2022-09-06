import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect

app = Flask(__name__)
app.config['SECRET_KEY'] = 'eu sou o douglas'


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def index():
    #exec(open("init_db.py").read())
    conn = get_db_connection()
    players = conn.execute('SELECT * FROM players').fetchall()
    conn.close()
    return render_template('index.html', players=players)


@app.route('/create', methods=('GET', 'POST'))
def create():
  if request.method == 'POST':
    player = request.form['player']

    if not player:
      flash('Nome do Jogador vazio!')
    else:
      conn = get_db_connection()
      conn.execute('INSERT INTO players (player, score) VALUES (?, ?)',
                   (player, 0))
      conn.commit()
      conn.close()
      return redirect(url_for('index'))
          
  return render_template('create.html')


app.run(host='0.0.0.0', port=81)
