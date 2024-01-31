
from flask import Flask, jsonify, render_template, request , redirect , url_for, abort
import pymysql
import funcionalidades as func
import json
import os
import pandas as pd

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

tipos = ['PLACA ',
        'CHASSI ',
        'EQUIPAMENTO',
        'CLIENTE',
        'MODELO',
        'ENDERECO',
        'COD_RASTREIO',
        'STATUS_ENVIO',
        'STATUS_AGENDAMENTO',
        'STATUS_INSTALACAO',
        'ID ']


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
    try:
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
                'STATUS_ENVIO':resultado[7],
                'STATUS_AGENDAMENTO':resultado[8],
                'STATUS_INSTALACAO':resultado[9],
                'ID':resultado[10]
            })
        return jsonify({'dados': dados})
    except:
        print('OCORREU UM ERRO DE PAGINA INEXISTENTE')


@app.route('/api/dados/remoção', methods=['GET'])
def obter_remoções():
    try:
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
    except:
        print('OCORREU UM ERRO DE PAGINA INEXISTENTE')

@app.route('/api/dados/manutenção', methods=['GET'])
def obter_manutenções():
    try:
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
    except ValueError:
        print('OCORREU UM ERRO DE PAGINA INEXISTENTE')

@app.route('/search', methods=['GET','POST'])
def search():
    return render_template('search.html')

@app.route('/search_response', methods=['GET','POST'])#NÃO ESTA RECEBENDO OS DADOS DO FORMULARIO
def search_response():
    dados = []  # Inicialize a lista fora do loop

    if request.method == 'POST':
        chassi = request.form.get('chassi')
        id_ = request.form.get('id')
        cursor = db.cursor()
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        for table in tables:
            table_name = table[0]
            query = f"SELECT * FROM {table_name} WHERE CHASSI = %s AND ID = %s"
            cursor.execute(query, (chassi, id_))
            row = cursor.fetchone()
            if row:
                print(f"Resultado na tabela {table_name}:")
                print("-" * 50)
                for column, value in zip(tipos, row):
                    dados.append({column: value})
                    print(f"{column}: {value}")
                print('-' * 50)
        cursor.close()
 # Close the database connection outside the 'if' block to ensure it's always closed.

    # Return an empty list if no data was found in any table
    return jsonify(dados) # ESTA MOSTRANDO ALEM DO QUE EU QUERO..............................

@app.route('/index/pre_extração',methods=['GET','POST'])
def pre_extração():
    if request.method == 'GET' or 'POST':
        return render_template('pre_extração.html')

@app.route('/index/extração',methods=['GET','POST'])
def extração():
    # Verifique se o arquivo foi enviado na solicitação
    if 'arquivo' not in request.files:
        print("Nenhum arquivo enviado")
        return "Nenhum arquivo enviado"
    # Obtenha o arquivo da solicitação
    arquivo = request.files['arquivo']
    # Leia o arquivo Excel para um DataFrame pandas
    df = pd.read_excel(arquivo)
    # Obtenha o nome do arquivo JSON da solicitação
    nome_do_json = request.form.get('valor3')
    # Adicione a extensão .json ao nome do arquivo
    jsonn = nome_do_json + '.json'
    # Salve o DataFrame como um arquivo JSON
    df.to_json(jsonn, orient='index', indent=2)
    print(f"dados salvos no arquivo {jsonn}")
    # Leia o arquivo JSON
    with open(jsonn, 'r') as json_:
        dados = json.load(json_)
    
    # O restante do seu código vai aqui

    tipos = ['PLACA ',
            'CHASSI ',
            'EQUIPAMENTO',
            'CLIENTE',
            'MODELO',
            'ENDERECO',
            'COD_RASTREIO',
            'STATUS_ENVIO',
            'STATUS_AGENDAMENTO',
            'STATUS_INSTALACAO',
            'ID ']
    
    cursor = db.cursor()
    cursor.execute('''create table instalacao(
        PLACA varchar(60),
        CHASSI varchar(60),
        EQUIPAMENTO varchar(60),
        CLIENTE varchar(60),
        MODELO varchar(60),
        ENDERECO varchar(60),
        COD_RASTREIO varchar(60),
        STATUS_ENVIO varchar(60),
        STATUS_AGENDAMENTO varchar(60),
        STATUS_INSTALACAO varchar(60),
        ID varchar(30));''')
        
    cursor.execute('''create table manutencao(
        PLACA varchar(60),
        CHASSI varchar(60),
        EQUIPAMENTO varchar(60),
        CLIENTE varchar(60),
        MODELO varchar(60),
        ENDERECO varchar(60),
        COD_RASTREIO varchar(60),
        STATUS_ENVIO varchar(60),
        STATUS_AGENDAMENTO varchar(60),
        STATUS_INSTALACAO varchar(60),
        ID varchar(30));''')
    
    cursor.execute('''create table remocao(
        PLACA varchar(60),
        CHASSI varchar(60),
        EQUIPAMENTO varchar(60),
        CLIENTE varchar(60),
        MODELO varchar(60),
        ENDERECO varchar(60),
        COD_RASTREIO varchar(60),
        STATUS_ENVIO varchar(60),
        STATUS_AGENDAMENTO varchar(60),
        STATUS_INSTALACAO varchar(60),
        ID varchar(30));''')
    
    onde = 'geral'
    cursor.execute(f'''create table {onde}(
        PLACA varchar(60),
        CHASSI varchar(60),
        EQUIPAMENTO varchar(60),
        CLIENTE varchar(60),
        MODELO varchar(60),
        ENDERECO varchar(60),
        COD_RASTREIO varchar(60),
        STATUS_ENVIO varchar(60),
        STATUS_AGENDAMENTO varchar(60),
        STATUS_INSTALACAO varchar(60),
        ID varchar(30));''')
    
    lista = []
    
    for i in dados:
        for j in range(len(tipos)):
            nome = dados[str(i)][str(tipos[j])]
            lista.append(nome)

        inserir_dados = f"INSERT INTO {onde} ({','.join(tipos)}) VALUES ({','.join(['%s'] * len(tipos))})"
        while len(lista) > 0:
            cursor.execute(inserir_dados, lista)
            db.commit()
            lista = []

    cursor.close()
    print("ENVIADO")
    return render_template("sucesso.html")
''' 
    lista = []
    
    for i in dados:
        for j in range(len(tipos)):
            nome = dados[str(i)].get(str(tipos[j]), 'Valor padrão')  # Se a chave não existir, 'Valor padrão' será usado
            lista.append(nome)

        inserir_dados = f"INSERT INTO {onde} ({','.join(tipos)}) VALUES ({','.join(['%s'] * len(tipos))})"
        while len(lista) > 0:
            cursor.execute(inserir_dados, lista)
            db.commit()
            lista = []

    cursor.close()
    db.close()
    print("ENVIADO")
    return render_template("sucesso.html")
'''


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
    if 'arquivo' not in request.files:
        info_1 = request.form.get('placa')
        info_2 = request.form.get('chassi')
        info_3 = request.form.get('equipamento')
        info_4 = request.form.get('cliente')
        info_5 = request.form.get('modelo')
        info_7 = request.form.get('endereco')
        sql_query = f"SELECT COUNT(*) FROM manutencao"
        cursor = db.cursor()
        cursor.execute(sql_query)
        resultado = cursor.fetchone()
        total_registros1 = resultado[0]
        info_6 = total_registros1 + 1
        result = cursor.fetchone()
        if result:
            print(f"ID {info_6} já existe. Não é permitido criar um novo com o mesmo valor.")
        else:
            print(f"Inserindo o ID {info_6} na tabela MANUTENÇÃO.")
            add = "INSERT INTO manutencao (ID) VALUES (%s)"
            cursor.execute(add, (info_6,))
            db.commit()
            att = "UPDATE manutencao SET PLACA = %s, CHASSI = %s, EQUIPAMENTO = %s, CLIENTE = %s, MODELO = %s, ENDERECO = %s WHERE ID = %s"
            data = (info_1, info_2, info_3, info_4, info_5,info_7, info_6)
            cursor.execute(att, data)
            db.commit()
            cursor.close()
            print("Linhas afetadas:", cursor.rowcount)
            if cursor.rowcount == 1:
                return render_template('sucesso.html')
            else:
                print("ERRO")
    if 'arquivo' in request.files:
        arquivo = request.files['arquivo']
        # Leia o arquivo Excel para um DataFrame pandas
        df = pd.read_excel(arquivo)
        # Filtrar os dados que envolvem manutenção
        df_manutencao = df[df['STATUS_INSTALACAO'].str.contains('manutencao')]
        print(len(df_manutencao))
        cursor = db.cursor()
        cont = 0
        if len(df_manutencao) < 2:
            try:
                while len(df_manutencao) != cont:
                    cont = cont + 1
                    cursor = db.cursor()
                    for index, row in df_manutencao.iterrows():
                        info_1 = row['PLACA ']
                        info_2 = row['CHASSI ']
                        info_3 = row['EQUIPAMENTO']
                        info_4 = row['CLIENTE']
                        info_5 = row['MODELO']
                        info_7 = row['ENDERECO']

                        sql_query = f"SELECT COUNT(*) FROM manutencao"
                        cursor.execute(sql_query)
                        resultado = cursor.fetchone()
                        total_registros1 = resultado[0]
                        info_6 = total_registros1 + 1
                        result = cursor.fetchone()
                        if result:
                            print(f"ID {info_6} já existe. Não é permitido criar um novo com o mesmo valor.")
                        else:
                            print(f"Inserindo o ID {info_6} na tabela MANUTENÇÃO.")
                            add = "INSERT INTO manutencao (ID, PLACA, CHASSI, EQUIPAMENTO, CLIENTE, MODELO, ENDERECO) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                            data = (info_6, info_1, info_2, info_3, info_4, info_5, info_7)
                            cursor.execute(add, data)
                            db.commit()
            
                print("Linhas afetadas:", cursor.rowcount)
                if cursor.rowcount <= 0:
                    print("ACONTECEU NADA")
                if cursor.rowcount == 1:
                    return render_template('sucesso.html')

                cursor.close()
            except Exception as e:
                print(f"OCORREU UM ERRO {e}")
        
        count = 1
        if len(df_manutencao) > 1:
            try:
                while len(df_manutencao) != count:
                    count = count + 1
                    cursor = db.cursor()
                    for index, row in df_manutencao.iterrows():
                        info_1 = row['PLACA ']
                        info_2 = row['CHASSI ']
                        info_3 = row['EQUIPAMENTO']
                        info_4 = row['CLIENTE']
                        info_5 = row['MODELO']
                        info_7 = row['ENDERECO']

                        sql_query = f"SELECT COUNT(*) FROM manutencao"
                        cursor.execute(sql_query)
                        resultado = cursor.fetchone()
                        total_registros1 = resultado[0]
                        info_6 = total_registros1 + 1
                        result = cursor.fetchone()
                        if result:
                            print(f"ID {info_6} já existe. Não é permitido criar um novo com o mesmo valor.")
                        else:
                            print(f"Inserindo o ID {info_6} na tabela MANUTENÇÃO.")
                            add = "INSERT INTO manutencao (ID, PLACA, CHASSI, EQUIPAMENTO, CLIENTE, MODELO, ENDERECO) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                            data = (info_6, info_1, info_2, info_3, info_4, info_5, info_7)
                            cursor.execute(add, data)
                            db.commit()
            
                print("Linhas afetadas:", cursor.rowcount)
                if cursor.rowcount <= 0:
                    print("ACONTECEU NADA")
                if cursor.rowcount == 1:
                    return render_template('sucesso.html')

                cursor.close()
            except Exception as e:
                print(f"OCORREU UM ERRO {e}")
# BASICAMENTE TIVE A IDEIA PERFEITA, SUBSTITUIR OS INPUTS PELOS GETTER DO FORM E FAZER O PROGRAMA RODAR SOZINHO NO MAIN, TIPO VAI SER MUITO CODIGO POREM VAI SER FUNCIONAL

@app.route("/remoção", methods=['GET','POST'])
def remoção():
    return render_template("remocao.html")

@app.route("/remoção/done" , methods=['GET', 'POST'])
def cad_remoção():
    if 'arquivo' not in request.files:
        info_1 = request.form.get('placa')
        info_2 = request.form.get('chassi')
        info_3 = request.form.get('equipamento')
        info_4 = request.form.get('cliente')
        info_5 = request.form.get('modelo')
        info_7 = request.form.get('endereco')
        
        sql_query = f"SELECT COUNT(*) FROM remocao"
        cursor = db.cursor()
        cursor.execute(sql_query)
        resultado = cursor.fetchone()
        total_registros1 = resultado[0]
        info_6 = total_registros1 + 1
        result = cursor.fetchone()
        if result:
            print(f"ID {info_6} já existe. Não é permitido criar um novo com o mesmo valor.")
        else:
            print(f"Inserindo o ID {info_6} na tabela REMOÇÃO.")
            add = "INSERT INTO remocao (ID) VALUES (%s)"
            cursor.execute(add, (info_6,))
            db.commit()
            att = "UPDATE remocao SET PLACA = %s, CHASSI = %s, EQUIPAMENTO = %s, CLIENTE = %s, MODELO = %s, ENDERECO = %s WHERE ID = %s"
            data = (info_1, info_2, info_3, info_4, info_5,info_7, info_6)
            cursor.execute(att, data)
            db.commit()
            cursor.close()
            print("Linhas afetadas:", cursor.rowcount)
            if cursor.rowcount == 1:
                return render_template('sucesso.html')
            else:
                print("DEU PROBLEMA")
    if 'arquivo' in request.files:
        arquivo = request.files['arquivo']
        # Leia o arquivo Excel para um DataFrame pandas
        df = pd.read_excel(arquivo)
        # Filtrar os dados que envolvem manutenção
        df_remocao = df[df['STATUS_INSTALACAO'].str.contains('remocao')]
        print(len(df_remocao))
        cursor = db.cursor()
        cont = 0
        if len(df_remocao) < 2:
            try:
                while len(df_remocao) != cont:
                    cont = cont + 1
                    cursor = db.cursor()
                    for index, row in df_remocao.iterrows():
                        info_1 = row['PLACA ']
                        info_2 = row['CHASSI ']
                        info_3 = row['EQUIPAMENTO']
                        info_4 = row['CLIENTE']
                        info_5 = row['MODELO']
                        info_7 = row['ENDERECO']

                        sql_query = f"SELECT COUNT(*) FROM remocao"
                        cursor.execute(sql_query)
                        resultado = cursor.fetchone()
                        total_registros1 = resultado[0]
                        info_6 = total_registros1 + 1
                        result = cursor.fetchone()
                        if result:
                            print(f"ID {info_6} já existe. Não é permitido criar um novo com o mesmo valor.")
                        else:
                            print(f"Inserindo o ID {info_6} na tabela REMOÇÃO.")
                            add = "INSERT INTO remocao (ID, PLACA, CHASSI, EQUIPAMENTO, CLIENTE, MODELO, ENDERECO) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                            data = (info_6, info_1, info_2, info_3, info_4, info_5, info_7)
                            cursor.execute(add, data)
                            db.commit()
            
                print("Linhas afetadas:", cursor.rowcount)
                if cursor.rowcount <= 0:
                    print("ACONTECEU NADA")
                if cursor.rowcount >= 1:
                    return render_template('sucesso.html')

                cursor.close()
            except Exception as e:
                print(f"OCORREU UM ERRO {e}")
        count = 1
        if len(df_remocao) > 1:
            try:
                while len(df_remocao) != count:
                    count = count + 1
                    cursor = db.cursor()
                    for index, row in df_remocao.iterrows():
                        info_1 = row['PLACA ']
                        info_2 = row['CHASSI ']
                        info_3 = row['EQUIPAMENTO']
                        info_4 = row['CLIENTE']
                        info_5 = row['MODELO']
                        info_7 = row['ENDERECO']

                        sql_query = f"SELECT COUNT(*) FROM remocao"
                        cursor.execute(sql_query)
                        resultado = cursor.fetchone()
                        total_registros1 = resultado[0]
                        info_6 = total_registros1 + 1
                        result = cursor.fetchone()
                        if result:
                            print(f"ID {info_6} já existe. Não é permitido criar um novo com o mesmo valor.")
                        else:
                            print(f"Inserindo o ID {info_6} na tabela REMOÇÃO.")
                            add = "INSERT INTO remocao (ID, PLACA, CHASSI, EQUIPAMENTO, CLIENTE, MODELO, ENDERECO) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                            data = (info_6, info_1, info_2, info_3, info_4, info_5, info_7)
                            cursor.execute(add, data)
                            db.commit()
            
                print("Linhas afetadas:", cursor.rowcount)
                if cursor.rowcount <= 0:
                    print("ACONTECEU NADA")
                if cursor.rowcount >= 1:
                    return render_template('sucesso.html')

                cursor.close()
            except Exception as e:
                print(f"OCORREU UM ERRO {e}")
            

    
@app.route("/instalação", methods=['GET','POST'])
def instalação():
    return render_template("instalacao.html")

@app.route("/instalação/done", methods=['GET','POST'])
def cad_instalação():
    if 'arquivo' not in request.files:
        info_1 = request.form.get('placa')
        info_2 = request.form.get('chassi')
        info_3 = request.form.get('equipamento')
        info_4 = request.form.get('cliente')
        info_5 = request.form.get('modelo')
        info_7 = request.form.get('endereco')
        
        sql_query = f"SELECT COUNT(*) FROM instalacao"
        cursor = db.cursor()
        cursor.execute(sql_query)
        resultado = cursor.fetchone()
        total_registros1 = resultado[0]
        info_6 = total_registros1 + 1
        result = cursor.fetchone()
        if result:
            print(f"ID {info_6} já existe. Não é permitido criar um novo com o mesmo valor.")
        else:
            print(f"Inserindo o ID {info_6} na tabela INSTALAÇÃO.")
            add = "INSERT INTO instalacao (ID) VALUES (%s)"
            cursor.execute(add, (info_6,))
            db.commit()
            att = "UPDATE instalacao SET PLACA = %s, CHASSI = %s, EQUIPAMENTO = %s, CLIENTE = %s, MODELO = %s , ENDERECO = %s WHERE ID = %s"
            data = (info_1, info_2, info_3, info_4, info_5, info_7, info_6)
            cursor.execute(att, data)
            db.commit()
            cursor.close()
            print("Linhas afetadas:", cursor.rowcount)
            if cursor.rowcount == 1:
                return render_template('sucesso.html')
            else:
                print("ERRO")
    if 'arquivo' in request.files:
        try:
            arquivo = request.files['arquivo']
            # Leia o arquivo Excel para um DataFrame pandas
            df = pd.read_excel(arquivo)
            # Filtrar os dados que envolvem manutenção
            df_instalacao = df[df['STATUS_INSTALACAO'].str.contains('instalacao')]
            print(len(df_instalacao))
            cursor = db.cursor()
            cont = 0
            if len(df_instalacao) < 2:
                while len(df_instalacao) != cont:
                    cont = cont + 1
                    cursor = db.cursor()
                    for index, row in df_instalacao.iterrows():
                        info_1 = row['PLACA ']
                        info_2 = row['CHASSI ']
                        info_3 = row['EQUIPAMENTO']
                        info_4 = row['CLIENTE']
                        info_5 = row['MODELO']
                        info_7 = row['ENDERECO']

                        sql_query = f"SELECT COUNT(*) FROM instalacao"
                        cursor.execute(sql_query)
                        resultado = cursor.fetchone()
                        total_registros1 = resultado[0]
                        info_6 = total_registros1 + 1
                        result = cursor.fetchone()
                        if result:
                            print(f"ID {info_6} já existe. Não é permitido criar um novo com o mesmo valor.")
                        else:
                            print(f"Inserindo o ID {info_6} na tabela INSTALAÇÃO.")
                            add = "INSERT INTO instalacao (ID, PLACA, CHASSI, EQUIPAMENTO, CLIENTE, MODELO, ENDERECO) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                            data = (info_6, info_1, info_2, info_3, info_4, info_5, info_7)
                            cursor.execute(add, data)
                            db.commit()
            
                print("Linhas afetadas:", cursor.rowcount)
                if cursor.rowcount <= 0:
                    print("ACONTECEU NADA")
                if cursor.rowcount == 1:
                    return render_template('sucesso.html')

                cursor.close()
        except Exception as e:
            print(f"OCORREU UM ERRO {e}")
           
        count = 1
        if len(df_instalacao) > 1:
            try:
                while len(df_instalacao) != count:
                    count = count + 1
                    cursor = db.cursor()
                    for index, row in df_instalacao.iterrows():
                        info_1 = row['PLACA ']
                        info_2 = row['CHASSI ']
                        info_3 = row['EQUIPAMENTO']
                        info_4 = row['CLIENTE']
                        info_5 = row['MODELO']
                        info_7 = row['ENDERECO']

                        sql_query = f"SELECT COUNT(*) FROM instalacao"
                        cursor.execute(sql_query)
                        resultado = cursor.fetchone()
                        total_registros1 = resultado[0]
                        info_6 = total_registros1 + 1
                        result = cursor.fetchone()
                        if result:
                            print(f"ID {info_6} já existe. Não é permitido criar um novo com o mesmo valor.")
                        else:
                            print(f"Inserindo o ID {info_6} na tabela INSTALAÇÃO.")
                            add = "INSERT INTO instalacao (ID, PLACA, CHASSI, EQUIPAMENTO, CLIENTE, MODELO, ENDERECO) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                            data = (info_6, info_1, info_2, info_3, info_4, info_5, info_7)
                            cursor.execute(add, data)
                            db.commit()
            
                print("Linhas afetadas:", cursor.rowcount)
                if cursor.rowcount <= 0:
                    print("ACONTECEU NADA")
                if cursor.rowcount >= 1:
                    return render_template('sucesso.html')

                cursor.close()
            except Exception as e:
                print(f"OCORREU UM ERRO {e}")
if __name__ == '__main__':
    app.run(debug=True)


