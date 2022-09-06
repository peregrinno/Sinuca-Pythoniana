import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort

app = Flask(__name__)
app.config['SECRET_KEY'] = 'eu sou o douglas'


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_player(player_id):
    conn = get_db_connection()
    player = conn.execute('SELECT * FROM players WHERE id = ?',
                        (player_id,)).fetchone()
    conn.close()
    if player is None:
        abort(404)
    return player


@app.route('/')
def index():
    #exec(open("init_db.py").read())
    conn = get_db_connection()
    players = conn.execute('SELECT * FROM players').fetchall()
    conn.close()
    return render_template('index.html', players=players)

@app.route('/<int:player_id>')
def player(player_id):
    player = get_player(player_id)
    return render_template('player.html', player=player)


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

@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
  player = get_player(id)
  if request.method == 'POST':
    player = request.form['player']
    score = request.form['score']

    if not player:
      flash('Nome do Jogador vazio!')
    else:
      conn = get_db_connection()
      conn.execute('UPDATE players SET player = ?, score = ?'
                   ' WHERE id = ?',
                   (player, score, id))
      conn.commit()
      conn.close()
      return redirect(url_for('index'))

  return render_template('edit.html', player=player)

app.run(host='0.0.0.0', port=81)
