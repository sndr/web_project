from flask import Flask, jsonify, render_template, request , redirect , url_for, abort
import pymysql
import funcionalidades as func

app = Flask(__name__)
app.config['API_SORT_KEYS'] = False

# Configurações do banco de dados
db = pymysql.connect(
    host="localhost",
    port=3306,  # Endereço do servidor MySQL
    user="root",  # Nome de usuário do MySQL
    password="sndr",  # Senha do MySQL
    db="dados"  # Nome do banco de dados
)

@app.route('/api/dados/geral', methods=['GET'])
def obter_dados():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM geral")
    resultados = cursor.fetchall()
    cursor.close()
    dados = []
    for resultado in resultados:
        dados.append({
            'PLACA': resultado[0],
            'CHASSI': resultado[1],
            'EQUIPAMENTO': resultado[2],
            'CLIENTE': resultado[3],
            'MODELO': resultado[4],
            'ENDERECO': resultado[5],
            'COD_RASTREIO': resultado[6],
            'STATUS_ENVIO':resultado[7],
            'STATUS_AGENDAMENTO':resultado[8],
            'STATUS_INSTALACAO':resultado[9],
            'ID':resultado[10]
        })
    return jsonify({'dados': dados})

@app.route('/api/dados/instalação', methods=['GET'])
def obter_instalações():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM instalacao")
    resultados = cursor.fetchall()
    cursor.close()
    dados = []
    for resultado in resultados:
        dados.append({
            'PLACA': resultado[0],
            'CHASSI': resultado[1],
            'EQUIPAMENTO': resultado[2],
            'CLIENTE': resultado[3],
            'MODELO': resultado[4],
            'ENDERECO': resultado[5],
            'COD_RASTREIO': resultado[6],
            'STATUS_ENVIO':resultado[7],
            'STATUS_AGENDAMENTO':resultado[8],
            'STATUS_INSTALACAO':resultado[9],
            'ID':resultado[10]
        })
    return jsonify({'dados': dados})

@app.route('/api/dados/remoção', methods=['GET'])
def obter_remoções():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM remocao")
    resultados = cursor.fetchall()
    cursor.close()
    dados = []
    for resultado in resultados:
        dados.append({
            'PLACA': resultado[0],
            'CHASSI': resultado[1],
            'EQUIPAMENTO': resultado[2],
            'CLIENTE': resultado[3],
            'MODELO': resultado[4],
            'ENDERECO': resultado[5],
            'COD_RASTREIO': resultado[6],
            'STATUS_ENVIO':resultado[7],
            'STATUS_AGENDAMENTO':resultado[8],
            'STATUS_INSTALACAO':resultado[9],
            'ID':resultado[10]
        })
    return jsonify({'dados': dados})

@app.route('/api/dados/manutenção', methods=['GET'])
def obter_manutenções():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM manutencao")
    resultados = cursor.fetchall()
    cursor.close()
    dados = []
    for resultado in resultados:
        dados.append({
            'PLACA': resultado[0],
            'CHASSI': resultado[1],
            'EQUIPAMENTO': resultado[2],
            'CLIENTE': resultado[3],
            'MODELO': resultado[4],
            'ENDERECO': resultado[5],
            'COD_RASTREIO': resultado[6],
            'STATUS_ENVIO':resultado[7],
            'STATUS_AGENDAMENTO':resultado[8],
            'STATUS_INSTALACAO':resultado[9],
            'ID':resultado[10]
        })
    return jsonify({'dados': dados})

@app.route('/search', methods=['GET','POST'])
def search():
    return render_template('search.html')

@app.route('/search_response', methods=['GET','POST'])#NÃO ESTA RECEBENDO OS DADOS DO FORMULARIO
def search_response(chassi,id_):
    if request.method == 'POST':
        chassi = request.form.get('chassi') 
        id_ = request.form.get('id')  
        results = func.search(chassi,id_)
        return jsonify(results)
    

@app.route('/index',methods=['GET','POST'])
def index():
    if request.form.get('username') == 'admin' and request.form.get('password') == 'admin': # EXEMPLO FUNCIONAL
        return render_template("index.html")
    else:
        abort(401)

@app.route("/", methods=['GET','POST']) # EXEMPLO FUNCIONAL
def login():
    return render_template('login.html')

@app.route("/manutenção",methods=['GET','POST'])# OS POSTS SO RECEBEM SE ESTIVEREM NO REDIRECT TAMBEM
def manutenção():
    return render_template("manutencao.html")

@app.route("/manutenção/done", methods=['GET','POST'])
def cad_manutenções():
    if request.method == 'POST':
        ... # BASICAMENTE TIVE A IDEIA PERFEITA, SUBSTITUIR OS INPUTS PELOS GETTER DO FORM E FAZER O PROGRAMA RODAR SOZINHO NO MAIN, TIPO VAI SER MUITO CODIGO POREM VAI SER FUNCIONAL

@app.route("/remoção")
def remoção():
    return render_template("remocao.html")

@app.route("/instalação")
def instalação():
    return render_template("instalacao.html")

''' BETA PARA PUXAR OS DADOS DO MYSQL
@app.route("/manutenção")
def manutenção():
    with db.cursor() as cur:
        cur.execute("SELECT * FROM manutencao")
        data = cur.fetchall()
    return render_template("manutencao.html",data=data)
'''

if __name__ == '__main__':
    app.run(debug=True)
