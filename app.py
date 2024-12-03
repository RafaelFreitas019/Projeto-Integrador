from flask import Flask, render_template, request, redirect, url_for, session
import pymysql


app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'

DB_CONFIG = {
    'MYSQL_HOST': 'BD-ACD',
    'MYSQL_USER': 'BD070324142',
    'MYSQL_PASSWORD': 'Zvgxr5',
    'MYSQL_DB': 'BD070324142'
}

def get_db_connection():
    return pymysql.connect(
        host=DB_CONFIG['MYSQL_HOST'],
        user=DB_CONFIG['MYSQL_USER'],
        password=DB_CONFIG['MYSQL_PASSWORD'],
        database=DB_CONFIG['MYSQL_DB'],
        cursorclass=pymysql.cursors.DictCursor
    )

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute('SELECT id_usuario, nome, email, senha FROM Usuarios WHERE email=%s AND senha=%s', (email, senha))
            user = cursor.fetchone()
        conn.close()
        
        if user:
            session['user_id'] = user['id_usuario'] 
            return redirect(url_for('dashboard'))  
        else:
            return render_template('login.html', error='Credenciais inválidas.')
    
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nome = request.form['nome']
        senha = request.form['senha']
        escolaridade = request.form['escolaridade']
        idade = request.form['idade']
        email = request.form['email']
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute('INSERT INTO Usuarios (nome, idade, escolaridade, email, senha) VALUES (%s, %s, %s, %s, %s)', (nome, idade, escolaridade, email, senha))
            conn.commit()
        conn.close()
        return redirect(url_for('login'))  
    return render_template('register.html')

@app.route('/recuperacao', methods=['GET', 'POST'])
def recuperacao():
    if request.method == 'POST':
        email = request.form['email']

        return render_template('recuperacao.html', success='Instruções de recuperação enviadas.')
    return render_template('recuperacao.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
 
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM atividades')
        atividades = cursor.fetchall()
    conn.close()
    return render_template('dashboard.html', atividades=atividades)

# Rota para atividades (opcional)
@app.route('/atividades', methods=['GET', 'POST'])
def atividades():
    if 'user_id' not in session:
        return redirect(url_for('login'))  
    if request.method == 'POST':
        atividade = request.form['atividade']
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute('INSERT INTO atividades (descricao, user_id) VALUES (%s, %s)', (atividade, session['user_id']))
            conn.commit()
        conn.close()
        return redirect(url_for('dashboard'))  
    return render_template('atividades.html')


@app.route('/logout')
def logout():
    session.pop('user_id', None)  
    return redirect(url_for('index'))  


@app.route('/matematica')
def matematica():
    return render_template('matematica.html')

@app.route('/portugues')
def portugues():
    return render_template('portugues.html')

@app.route('/quimica')
def quimica():
    return render_template('quimica.html')

@app.route('/biologia')
def biologia():
    return render_template('biologia.html')

@app.route('/libras')
def libras():
    return render_template('libras.html')

@app.route('/ciencias')
def ciencias():
    return render_template('ciencias.html')

@app.route('/historia')
def historia():
    return render_template('historia.html')

@app.route('/geografia')
def geografia():
    return render_template('geografia.html')

@app.route('/fisica')
def fisica():
    return render_template('fisica.html')

@app.route('/ativ_mat')
def ativ_mat():
    return render_template('ativ_mat.html')

@app.route('/ativ_port')
def ativ_port():
    return render_template('ativ_port.html')

@app.route('/ativ_quim')
def ativ_quim():
    return render_template('ativ_quim.html')

@app.route('/ativ_bio')
def ativ_bio():
    return render_template('ativ_bio.html')

@app.route('/ativ_lib')
def ativ_lib():
    return render_template('ativ_lib.html')

@app.route('/ativ_cien')
def ativ_cien():
    return render_template('ativ_cien.html')

@app.route('/ativ_hist')
def ativ_hist():
    return render_template('ativ_his.html')

@app.route('/ativ_geo')
def ativ_geo():
    return render_template('ativ_geo.html')

@app.route('/ativ_fis')
def ativ_fis():
    return render_template('ativ_fis.html')

if __name__ == '__main__':
    app.run(debug=True)