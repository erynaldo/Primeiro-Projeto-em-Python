import os
import mysql.connector
from flask_mysqldb import MySQL
from flask import Flask, render_template, request, redirect, url_for, redirect, jsonify
from datetime import date

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

# Configuração da conexão MySQL quando já se tem o banco de dados criado
config = {
    'user': os.getenv("DB_USER"),
    'password': os.getenv("DB_PASSWORD"),
    'host': os.getenv("DB_HOST"),
    'database': os.getenv("DB_NAME"),
}
# Conecta ao banco de dados MySQL
primeiraConexao = mysql.connector.connect(**config)


app.config['SECRET_KEY'] = 'your secret key'

app.config['MYSQL_HOST'] = os.getenv("DB_HOST")
app.config['MYSQL_USER'] = os.getenv("DB_USER")
app.config['MYSQL_PASSWORD'] = os.getenv("DB_PASSWORD")
app.config['MYSQL_DB'] = os.getenv("DB_NAME")

mysql = MySQL(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/passoDois', methods=['GET', 'POST'])
def passoDois():
    if request.method == 'POST':
        cpf_ra = request.form['cpf_ra'].upper()
    else:
        cpf_ra = ''

    return render_template('passoDois.html', cpf_ra=cpf_ra)


@app.route('/estouChegando', methods=['POST'])
def estouChegando():
    if request.method == 'POST':
        cpf_ra = request.form['cpf_ra'].upper()
    else:
        cpf_ra = ''
    
    return render_template('estouChegando.html', cpf_ra=cpf_ra)



@app.route('/estouSaindo', methods=['POST'])
def estouSaindo():

    connection = mysql.connection.cursor()
       
    if request.method == 'POST':
        cpf_ra = request.form['cpf_ra'].upper()
    else:
        cpf_ra = ''
    
    # data = date.today()
    # dataFormatada = data.strftime('%d-%m-%Y')
    dataFormatada = date.today().strftime('%d/%m/%Y')
    # print (dataFormatada)
 
    connection.execute("SELECT * FROM atividades WHERE data_evento = %s", (dataFormatada,))
    resultados = connection.fetchall()
    connection.close()

    return render_template('estouSaindo.html', cpf_ra=cpf_ra, result=resultados, dataHj=dataFormatada)



@app.route('/respostaChegada', methods=['POST'])
def respostaChegada():
    urlChegada = request.path # pega a Url "respostaChegada" para depois eu criar uma condição, aceitar envio somente uma vez
    cpf_ra = request.form['cpf_ra']
    status_chegada = request.form['status_chegada']
    # skills = request.form.getlist('skills')  # Para campos de checkbox, use getlist()
    # dataHora = datetime.now()
    # dtHrformatada = dataHora.strftime('%d-%m-%Y | %H:%M:%S')
    data = date.today()
    dataFormatada = data.strftime('%d-%m-%Y')

    connection = mysql.connection.cursor()

    connection.execute("SELECT * FROM pesquisa WHERE cpf_ra = %s AND urlChegada = %s AND time_chegada = %s", (cpf_ra, urlChegada, dataFormatada))
    result = connection.fetchall()
    # connection.close()

    if result:
        # return jsonify({'message': 'Vi que você já participou da pesquisa de entrada.'}), 400
        return "Você já respondeu essa pesquisa."
    else:
        try:
            with mysql.connection.cursor() as cursor:
                # Query para inserir os dados no banco de dados
                sql = "INSERT INTO pesquisa (cpf_ra, urlChegada, status_chegada, time_chegada) VALUES (%s, %s, %s, %s)"
                # cursor.execute(sql, (cpf_ra, status_chegada, ', '.join(skills), dtHrformatada))
                cursor.execute(sql, (cpf_ra, urlChegada, status_chegada, dataFormatada))
                mysql.connection.commit()
                connection.close()
                # return "Ultimo: Dados enviados."
                return redirect(url_for('msgSuccess'))
        except Exception as e:
            return str(e)
            # return render_template('msgSuccess.html')



@app.route('/respostaSaida', methods=['POST'])
def respostaSaida():
    urlSaida = request.path # pega a Url "respostaSaida" para depois eu criar uma condição, aceitar envio somente uma vez
    cpf_ra = request.form['cpf_ra']
    status_saida = request.form['status_saida']
    atividades = request.form.getlist('atividades_gostou')  # Para campos de checkbox, use getlist()
    data = date.today()
    dataFormatada = data.strftime('%d-%m-%Y')
   
    connection = mysql.connection.cursor()

    connection.execute("SELECT * FROM pesquisa WHERE cpf_ra = %s AND urlSaida = %s AND time_saida = %s", (cpf_ra, urlSaida, dataFormatada))
    result = connection.fetchall()
    connection.close()

    if result:
        # return jsonify({'message': 'Vi que você já participou da pesquisa de entrada.'}), 400
        return redirect(url_for('msg_entrada_ja_registrada'))
        # return "Você já respondeu essa pesquisa."
    else:
        try:
            with mysql.connection.cursor() as cursor:
                # Query para inserir os dados no banco de dados
                sql = "UPDATE pesquisa SET urlSaida = %s, status_saida = %s, time_saida = %s, atividades_gostou = %s WHERE cpf_ra = %s"
                cursor.execute(sql, (urlSaida, status_saida, dataFormatada, ', '.join(atividades), cpf_ra))
                mysql.connection.commit()
                connection.close()
                # return "Ultimo: Dados enviados."
                return redirect(url_for('msgSuccess'))
        except Exception as e:
            return str(e)


@app.route('/msgSuccess')
def msgSuccess():
    return render_template('msgSuccess.html')


@app.route('/msg_entrada_ja_registrada')
def msg_entrada_ja_registrada():
    return render_template('msg_entrada_ja_registrada.html')



def execute_sql_file(filename, primeiraConexao):
    # Abre o arquivo SQL e lê o conteúdo
    with open(filename, 'r') as file:
        sql_script = file.read()
    
    # Divida o script em comandos SQL individuais
    sql_commands = sql_script.split(';')

    # Remove espaços em branco e linhas em branco dos comandos
    sql_commands = [command.strip() for command in sql_commands if command.strip()]

    # Execute cada comando SQL na conexão fornecida
    for command in sql_commands:
        with primeiraConexao.cursor() as cursor:
            cursor.execute(command)

# Configuração da conexão MySQL quando não se tem o banco de dados
# config = {
#     'user': 'root',
#     'password': '',
#     'host': 'localhost',
# }

# Configuração da conexão MySQL quando já se tem o banco de dados criado
# config = {
#     'user': 'root',
#     'password': '',
#     'host': 'localhost',
#     'database': 'banco_python'
# }

# Chama a função para executar o arquivo SQL
execute_sql_file('script.sql', primeiraConexao) 

# Commit as alterações
primeiraConexao.commit()

# Fecha a conexão
primeiraConexao.close()

if __name__ == "__main__":
	app.run(debug=True)