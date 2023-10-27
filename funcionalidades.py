
import json
import mysql.connector
import pandas as pd
from datetime import datetime
import os


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

def menu():
    return print(''' FUNCIONALIDADES
1 - ESTRAÇÃO SALVAR_DB
2 - REMOÇÃO DADO ESPECIFICO
3 - UPADATE DADO ESPECIFICO
4 - STATUS INSTALAÇÃO
5 - VISUALIZAR TODOS OS SERVIÇOS
6 - CADASTRAR NOVA INSTALAÇÃO
7 - CADASTRAR NOVA MANUNTENÇÃO
8 - CADASTRAR NOVA REMOÇÃO
9 - EXISTE UM SERVIÇO
10 - VER LEN DE TODAS AS COLUNAS
11 - SAIR
''')
    
def mes_instalação():
    try:
        conexao = mysql.connector.connect(
            host="localhost",
            port=3306,
            user="root",
            password="sndr",
            database="dados"
        )
        cursor = conexao.cursor()
        
        data_atual = datetime.now()
        
        data_formatada = data_atual.strftime("%Y-%m-%d")
        
        valores = (dados, data_formatada)
        
        
        sql_query = """
        SELECT DATE_FORMAT(instalacao, '%Y-%m') AS mes, COUNT(*) AS quantidade
        FROM sua_tabela
        GROUP BY mes
        ORDER BY mes;
        """
        cursor.execute(sql_query)
        resultados = cursor.fetchall()
        cursor.close()
        conexao.close()
        for resultado in resultados:
            mes, quantidade = resultado
            mes_formatado = datetime.strptime(mes, '%Y-%m').strftime('%B %Y')
            print(f'Mês {mes_formatado}: {quantidade} registros de instalações')
    except Exception as e:
        print(f"Não conseguiu se conectar, {e}")
        
def count_():
    try:
        conexao = mysql.connector.connect(
            host="localhost",
            port=3306,
            user="root",
            password="sndr",
            database="dados"
        )
        cursor = conexao.cursor()
        sql_query = f"SELECT COUNT(*) FROM instalacao"
        cursor.execute(sql_query)
        resultado = cursor.fetchone()
        total_registros1 = resultado[0]
        sql_query2 = f"SELECT COUNT(*) FROM remocao"
        cursor.execute(sql_query2)
        resultado = cursor.fetchone()
        total_registros2 = resultado[0]
        sql_query3 = f"SELECT COUNT(*) FROM manutencao"
        cursor.execute(sql_query3)
        resultado = cursor.fetchone()
        total_registros3 = resultado[0]
        cursor.close()
        conexao.close()
        return print(f'''Total de registros na tabela INSTALAÇÃO: {total_registros1}
Total de registros na tabela REMOÇÃO: {total_registros2}
Total de registros na tabela MANUTENÇÃO: {total_registros3}''')
    except Exception as e:
        print(f"Não conseguiu se conectar, {e}")
        
def exist():
    try:
        conexao = mysql.connector.connect(
            host="localhost",
            port=3306,
            user="root",
            password="sndr",
            database="dados"
        )
        nome_arquivo = input("Digite o nome do DADO que deseja verificar: ")
        tabela = input("DIGITE A TABELA PARA PROCURAR: ")
        coluna = input("DIGITE O O NOME DA COLUNA: ")
        cursor = conexao.cursor()
        select_query = f"SELECT * FROM {tabela} WHERE {coluna} = %s"
        data = (nome_arquivo,)
        cursor.execute(select_query, data)
        if cursor.fetchone():
            print(f"O arquivo '{nome_arquivo}' existe no banco de dados.")
            print("-"* 120)
        else:
            print(f"O arquivo '{nome_arquivo}' não foi encontrado no banco de dados.")
            print("-"* 120)
        cursor.close()
        conexao.close()
    except Exception as e:
        print(f"Não conseguiu se conectar, {e}")


def cad_instalação():
    try:
        conexao = mysql.connector.connect(
            host="localhost",
            port=3306,
            user="root",
            password="sndr",
            database="dados"
        )
        if conexao.is_connected():
            print("Conexão bem sucedida")
            print("VOCE ESTA DENTRO DA TABELA DE INSTALAÇÃO")
            escolha = int(input("VOCE QUER CADASTRAR MANUALMENTE OU IMPORTAR DA PLANILHA EXCEL? \n 1 - MANUAL \n 2 - IMPORTAR EXCEL \n -->"))
            if escolha == 1:
                placa = int(input("POSSUI PLACA: 1-SIM/2-NÃO"))
                if placa == 1:
                    info_1 = input("DIGITE A PLACA: ")
                    info_2 = input("DIGITE O CHASSI: ")
                    info_3 = input("INSIRA O ENDEREÇO QUE O VEICULO ESTÁ: ")
                    info_4 = input("INSIRA O TIPO DO DISPOSITIVO: ")
                    info_5 = input("INSIRA O STATUS: ")
                    data_atual = datetime.now()
                    data_formatada = data_atual.strftime("%Y-%m-%d")
                    sql_query = f"SELECT COUNT(*) FROM instalacao"
                    cursor = conexao.cursor()
                    cursor.execute(sql_query)
                    resultado = cursor.fetchone()
                    total_registros1 = resultado[0]
                    info_6 = total_registros1 + 1
                    result = cursor.fetchone()
                    if result:
                        print(f"ID {info_6} já existe. Não é permitido criar um novo com o mesmo valor.")
                    else:
                        print(f"Inserindo o ID {info_6} na tabela INSTALAÇÃO.")
                        inserir_id_query = "INSERT INTO instalacao (ID) VALUES (%s)"
                        cursor.execute(inserir_id_query, (info_6,))
                        conexao.commit()
                        att = "UPDATE instalacao SET PLACA = %s, CHASSI = %s, ENDERECO = %s, MODELO = %s, STATUS_INSTALACAO = %s WHERE ID = %s"
                        data = (info_1, info_2, info_3, info_4, info_5, info_6)
                        cursor.execute(att, data)
                        conexao.commit()
                        cursor.close()
                        conexao.close()
                        print("Linhas afetadas:", cursor.rowcount)          
                elif placa == 2:
                    info_2 = input("DIGITE O CHASSI: ")
                    info_3 = input("INSIRA O ENDEREÇO QUE O VEICULO ESTÁ: ")
                    info_4 = input("INSIRA O TIPO DO DISPOSITIVO: ")
                    info_5 = input("INSIRA O STATUS: ")
                    sql_query = f"SELECT COUNT(*) FROM instalacao"
                    cursor = conexao.cursor()
                    cursor.execute(sql_query)
                    resultado = cursor.fetchone()
                    total_registros1 = resultado[0]
                    info_6 = total_registros1 + 1
                    result = cursor.fetchone()
                    if result:
                        print(f"ID {info_6} já existe. Não é permitido criar um novo com o mesmo valor.")
                    else:
                        print(f"Inserindo o ID {info_6} na tabela INSTALAÇÃO.")
                        inserir_id_query = "INSERT INTO instalacao (ID) VALUES (%s)"
                        cursor.execute(inserir_id_query, (info_6,))
                        conexao.commit()
                        att = "UPDATE instalacao SET CHASSI = %s, ENDERECO = %s, MODELO = %s, STATUS_INSTALACAO = %s WHERE ID = %s"
                        data = (info_2, info_3, info_4, info_5, info_6)
                        cursor.execute(att, data)
                        conexao.commit()
                        cursor.close()
                        conexao.close()
                        print("Linhas afetadas:", cursor.rowcount)
            elif escolha == 2:
                pasta = input("DIGITE O NOME DO ARQUIVO EXCEL: ")
                diretorio_atual = os.getcwd()
                caminho_completo = None
                for root, dirs, files in os.walk(diretorio_atual):
                    if pasta in files:
                        caminho_completo = os.path.join(root, pasta)
                        if caminho_completo == None:
                            print("Arquivo não encontrado.")
                        else:
                            planilha = pd.read_excel(caminho_completo)
                            dados_instalacao = planilha[planilha['STATUS_INSTALACAO'].str.strip() == 'instalado']
                            cursor = conexao.cursor()
                            if not dados_instalacao.empty:
                                for indice, linha in dados_instalacao.iterrows():
                                    query = f"INSERT INTO instalacao ({','.join(tipos)}) VALUES ({','.join(['%s'] * len(tipos))})"
                                    valores_a_inserir = [tuple(linha) for _, linha in dados_instalacao.iterrows()]
                                    cursor.executemany(query, valores_a_inserir)
                                    conexao.commit()
                                    print("ENVIADOS com sucesso")
                            cursor.close()
                            conexao.close()
    except Exception as e:
            print(f"Não conseguiu se conectar, {e}")
            

def cad_manutenção():
    try:
        conexao = mysql.connector.connect(
            host="localhost",
            port=3306,
            user="root",
            password="sndr",
            database="dados"
        )
        if conexao.is_connected():
            print("Conexão bem sucedida")
            print("VOCE ESTA DENTRO DA TABELA DE MANUTENÇÃO")
            escolha = int(input("VOCE QUER CADASTRAR MANUAL OU IMPORTAR DO EXCEL? \n 1 - MANUAL \n 2 - EXPORTAR EXCEL \n --> "))
            if escolha == 1:
                placa = int(input("POSSUI PLACA: \n 1 - SIM \n 2 - NÃO \n --> "))
                if placa == 1:
                    info_1 = input("DIGITE A PLACA: ")
                    info_2 = input("DIGITE O CHASSI: ")
                    info_3 = input("INSIRA O ENDEREÇO QUE O VEICULO ESTÁ: ")
                    info_4 = input("INSIRA O TIPO DO DISPOSITIVO: ")
                    info_5 = input("INSIRA O STATUS: ")
                    sql_query = f"SELECT COUNT(*) FROM manutencao"
                    cursor = conexao.cursor()
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
                        conexao.commit()
                        att = "UPDATE manutencao SET PLACA = %s, CHASSI = %s, ENDERECO = %s, MODELO = %s, STATUS_INSTALACAO = %s WHERE ID = %s"
                        data = (info_1, info_2, info_3, info_4, info_5, info_6)
                        cursor.execute(att, data)
                        conexao.commit()
                        cursor.close()
                        conexao.close()
                        print("Linhas afetadas:", cursor.rowcount)
                    
                elif placa == 2:
                    info_2 = input("DIGITE O CHASSI: ")
                    info_3 = input("INSIRA O ENDEREÇO QUE O VEICULO ESTÁ: ")
                    info_4 = input("INSIRA O TIPO DO DISPOSITIVO: ")
                    info_5 = input("INSIRA O STATUS: ")
                    sql_query = f"SELECT COUNT(*) FROM manutencao"
                    cursor = conexao.cursor()
                    cursor.execute(sql_query)
                    resultado = cursor.fetchone()
                    total_registros1 = resultado[0]
                    info_6 = total_registros1 + 1
                    result = cursor.fetchone()
                    if result:
                        print(f"ID {info_6} já existe. Não é permitido criar um novo com o mesmo valor.")
                    else:
                        print(f"Inserindo o ID {info_6} na tabela MANUTENÇÃO.")
                        inserir_id_query = "INSERT INTO manutencao (ID) VALUES (%s)"
                        cursor.execute(inserir_id_query, (info_6,))
                        conexao.commit()
                        att = "UPDATE manutencao SET CHASSI = %s, ENDERECO = %s, MODELO = %s, STATUS_INSTALACAO = %s WHERE ID = %s"
                        data = (info_2, info_3, info_4, info_5, info_6)
                        cursor.execute(att, data)
                        conexao.commit()
                        cursor.close()
                        conexao.close()
                        print("Linhas afetadas:", cursor.rowcount)
            elif escolha == 2:
                pasta = input("DIGITE O NOME DO ARQUIVO EXCEL: ")
                diretorio_atual = os.getcwd()
                caminho_completo = None
                for root, dirs, files in os.walk(diretorio_atual):
                    if pasta in files:
                        caminho_completo = os.path.join(root, pasta)
                        if caminho_completo == None:
                            print("Arquivo não encontrado.")
                        else:
                            planilha = pd.read_excel(caminho_completo)
                            dados_instalacao = planilha[planilha['STATUS_INSTALACAO'].str.strip() == 'manutenção']
                            cursor = conexao.cursor()
                            if not dados_instalacao.empty:
                                for indice, linha in dados_instalacao.iterrows():
                                    query = f"INSERT INTO manutencao ({','.join(tipos)}) VALUES ({','.join(['%s'] * len(tipos))})"
                                    valores_a_inserir = [tuple(linha) for _, linha in dados_instalacao.iterrows()]
                                    cursor.executemany(query, valores_a_inserir)
                                    conexao.commit()
                                    print("ENVIADOS com sucesso")
                            cursor.close()
                            conexao.close()  
    except Exception as e:
        print(f"Não conseguiu se conectar, {e}")
            
def cad_remoção():
    try:
        conexao = mysql.connector.connect(
            host="localhost",
            port=3306,
            user="root",
            password="sndr",
            database="dados"
        )
        if conexao.is_connected():
            print("Conexão bem sucedida")
            print("VOCE ESTA DENTRO DA TABELA DE REMOÇÃO")
            escolha = int(input("QUER CADASTRAR MANUAL OU IMPORTAR DO ESCEL? \n 1 - MANUAL \n 2 - IMPORTAR EXCEL \n --> "))
            if escolha == 1: 
                placa = int(input("POSSUI PLACA: \n 1 - SIM \n 2 - NÃO \n --> "))
                if placa == 1:
                    info_1 = input("DIGITE A PLACA: ")
                    info_2 = input("DIGITE O CHASSI: ")
                    info_3 = input("INSIRA O ENDEREÇO QUE O VEICULO ESTÁ: ")
                    info_4 = input("INSIRA O TIPO DO DISPOSITIVO: ")
                    info_5 = input("INSIRA O STATUS: ")
                    sql_query = f"SELECT COUNT(*) FROM remocao"
                    cursor = conexao.cursor()
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
                        conexao.commit()
                        att = "UPDATE remocao SET PLACA = %s, CHASSI = %s, ENDERECO = %s, MODELO = %s, STATUS_INSTALACAO = %s WHERE ID = %s"
                        data = (info_1, info_2, info_3, info_4, info_5, info_6)
                        cursor.execute(att, data)
                        conexao.commit()
                        cursor.close()
                        conexao.close()
                        print("Linhas afetadas:", cursor.rowcount)
                    
                elif placa == 2:
                    info_2 = input("DIGITE O CHASSI: ")
                    info_3 = input("INSIRA O ENDEREÇO QUE O VEICULO ESTÁ: ")
                    info_4 = input("INSIRA O TIPO DO DISPOSITIVO: ")
                    info_5 = input("INSIRA O STATUS: ")
                    sql_query = f"SELECT COUNT(*) FROM remocao"
                    cursor = conexao.cursor()
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
                        conexao.commit()
                        att = "UPDATE remocao SET CHASSI = %s, ENDERECO = %s, MODELO = %s, STATUS_INSTALACAO = %s WHERE ID = %s"
                        data = (info_2, info_3, info_4, info_5, info_6)
                        cursor.execute(att, data)
                        conexao.commit()
                        cursor.close()
                        conexao.close()
                        print("Linhas afetadas:", cursor.rowcount)
            elif escolha == 2:
                pasta = input("DIGITE O NOME DO ARQUIVO EXCEL: ")
                diretorio_atual = os.getcwd()
                caminho_completo = None
                for root, dirs, files in os.walk(diretorio_atual):
                    if pasta in files:
                        caminho_completo = os.path.join(root, pasta)
                        if caminho_completo == None:
                            print("Arquivo não encontrado.")
                        else:
                            planilha = pd.read_excel(caminho_completo)
                            dados_instalacao = planilha[planilha['STATUS_INSTALACAO'].str.strip() == 'removido']
                            cursor = conexao.cursor()
                            if not dados_instalacao.empty:
                                for indice, linha in dados_instalacao.iterrows():
                                    query = f"INSERT INTO remocao ({','.join(tipos)}) VALUES ({','.join(['%s'] * len(tipos))})"
                                    valores_a_inserir = [tuple(linha) for _, linha in dados_instalacao.iterrows()]
                                    cursor.executemany(query, valores_a_inserir)
                                    conexao.commit()
                                    print("ENVIADOS com sucesso")
                            cursor.close()
                            conexao.close()        
    except Exception as e:
        print(f"Não conseguiu se conectar, {e}")
            
    
def visualização():
    try:
        conexao = mysql.connector.connect(
            host="localhost",
            port=3306,
            user="root",
            password="sndr",
            database="dados"
        )
        if conexao.is_connected():
            print("Conexão bem sucedida")
    except Exception as e:
            print("Não conseguiu se conectar")

    cursor = conexao.cursor()
    onde_ = input("QUAL TABELA VOCE QUER VER: ") 
    cursor.execute(f'SELECT * FROM {onde_}')
    results = cursor.fetchall()
    count = 0
    for row in results:
        count += 1
        print(f"AQUI ESTÁ SEUS DADOS DO MYSQL LINHA {count}:\n")
        print(f"{tipos}\n")
        print(row)
        print("-"*175)
    conexao.close()
    

def remocao():
    try:
        conexao = mysql.connector.connect(
            host="localhost",
            port=3306,
            user="root",
            password="sndr",
            database="dados"
        )
        if conexao.is_connected():
            print("Conexão bem-sucedida")
            pasta = input("PASTA: ")
            print(f"VOCE ESTA DENTRO DA PASTA {pasta}")
            print(tipos)
            coluna = input("Digite o nome da coluna que deseja usar como critério: ")
            print(f"VOCE ESTA DENTRO DA COLUNA {coluna}")
            item = input("Digite o nome do item: ")
            remo = f"UPDATE {pasta} SET {coluna} = NULL WHERE {coluna} = '{item}';"
            cursor = conexao.cursor()
            cursor.execute(remo)
            conexao.commit()
            print("Linhas afetadas:", cursor.rowcount)
            cursor.close()
            conexao.close()
            if cursor.rowcount != 0:
                return print(f'Item {item} removido com sucesso')
    except Exception as e:
        print(f"Não conseguiu se conectar{e}")


def salvar():
    try:
        try:
            pasta = input("DIGITE O NOME DA PASTA EXCEL PARA SALVAR EM JSON: ")
            diretorio_atual = os.getcwd()
            for root, dirs, files in os.walk(diretorio_atual):
                if pasta in files:
                    caminho_completo = os.path.join(root, pasta)
                    print(f'O arquivo {pasta} foi encontrado em: {caminho_completo}')
            df = pd.read_excel(caminho_completo)
        except Exception as e:
            print(f"PASTA NÃO ENCONTRADA: {e}")
        criar = input("QUER CRIAR UM ARQUIVO JSON OU USAR UM EXISTENTE: \n 1 - NOVO \n 2 - EXISTENTE\n -->")
        if criar == 1:
            nome_do_json = str(input("DIGITE O NOME DA PASTA JSON PARA SER CRIADA: "))
            jsonn = (nome_do_json)
            teste = df.iterrows()
            for item in teste:
                dado = {f'{item[0]}{item[1]}'}
            dado_salvo = pd.DataFrame(dado)
            df.to_json(jsonn,orient='index',indent=2)
            return print(f"dados salvos no arquivo {jsonn}")
        elif criar == 2:
            j = input("DIGITE O NOME DO ARQUIVO JSON EXISTENTE: ")
            jsonn = (j)
            teste = df.iterrows()
            for item in teste:
                dado = {f'{item[0]}{item[1]}'}
            dado_salvo = pd.DataFrame(dado)
            df.to_json(jsonn,orient='index',indent=2)
    except Exception as e:
        print(f"OCORREU UM TIPO DE ERRO: {e}")
        
def instalação():
    try:
        conexao = mysql.connector.connect(
            host="localhost",
            port=3306,
            user="root",
            password="sndr",
            database="dados"
        )
        if conexao.is_connected():
            print("Conexão bem-sucedida")
            pasta = input("PASTA do BD: ")
            print(f"VOCE ESTA DENTRO DA COLUNA STATUS_INSTALACAO")
            ID = str(input("DIGITE O ID DA COLUNA ESCOLHIDA: "))
            item = input("Digite o status: ")
            remo = f"UPDATE {pasta} SET STATUS_INSTALACAO = '{item}' WHERE ID = '{ID}';"
            cursor = conexao.cursor()
            cursor.execute(remo)
            conexao.commit()
            print("Linhas afetadas:", cursor.rowcount)
            cursor.close()
            conexao.close()
            if cursor.rowcount != 0:
                return print(f'Item {item} Adicionado com sucesso')
    except Exception as e:
        print(f"Não conseguiu se conectar{e}")
    
    
def manuntenção():
    try:
        conexao = mysql.connector.connect(
            host="localhost",
            port=3306,
            user="root",
            password="sndr",
            database="dados"
        )
        if conexao.is_connected():
            print("Conexão bem-sucedida")
            pasta = input("PASTA: ")
            print(f"VOCE ESTA DENTRO DA PASTA {pasta}")
            print(tipos)
            coluna = input("Digite o nome da coluna que deseja usar como critério: ")
            print(f"VOCE ESTA DENTRO DA COLUNA {coluna}")
            item = input("Digite o nome do item a ser Adicionado: ")
            ID = str(input("DIGITE O ID COMO REFERENCIA: "))
            remo = f"UPDATE {pasta} SET {coluna} = '{item}' WHERE ID = '{ID}';"
            cursor = conexao.cursor()
            cursor.execute(remo)
            conexao.commit()
            print("Linhas afetadas:", cursor.rowcount)
            cursor.close()
            conexao.close()
            if cursor.rowcount != 0:
                return print(f'Item {item} Adicionado com sucesso')
    except Exception as e:
        print(f"Não conseguiu se conectar{e}")


if __name__ == '__main__':
    while True:
        menu()
        try:
            resposta = int(input("--> "))
            print()
        except Exception as e:
            print("VALOR INVÁLIDO\n---------------------")
            continue
        if resposta == 1:
            while True:
                salvar()
                try:
                    terminou = int(input("DESEJA VOLTAR AO MENU OU CONTINUAR COM O ENVIO? \n 1 - CONTINUAR \n 2 - MENU \n -->"))
                except Exception as e:
                    print(f"VALOR INVALIDO: {e}")
                if terminou == 2:
                    break
                try:
                    arquivo = str(input("DIGITE O NOME DA PASTA JSON PARA FAZER O ENVIO PARA O MYSQL: \n 'S' PARA SAIR \n --> "))
                except Exception as e:
                    print(f"VALOR INVALIDO: {e}")
                if arquivo.upper() == 'S':
                    print("SAINDO...")
                    break


                def ler_por_index(arquivo, indice):
                    with open(arquivo, 'r') as arquivo:
                        dados = json.load(arquivo)
                    if indice < len(dados):
                        return dados[indice]
                    else:
                        return None


                with open(arquivo, 'r') as json_:
                    dados = json.load(json_)

                try:
                    conexao = mysql.connector.connect(
                        host="localhost",
                        port=3306,
                        user="root",
                        password="sndr",
                        database="dados"
                    )

                    if conexao.is_connected():
                        print("Conexão bem sucedida")
                except Exception as e:
                    print("Não conseguiu se conectar")

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

                cursor = conexao.cursor()
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
                    DATE varchar(30),
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
                    DATE varchar(30),
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
                    DATE varchar(30),
                    ID varchar(30));''')
                
                onde = input("NOME DA PASTA QUE VAI SALVAR OS DADOS: ")
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
                        conexao.commit()
                        lista = []

                cursor.close()
                conexao.close()
                print("ENVIADO")
                break
        elif resposta == 2:
            remocao()
        elif resposta == 3:
            manuntenção()
        elif resposta == 4:
            instalação()
        elif resposta == 5:
            visualização()
        elif resposta == 6:
            cad_instalação()
        elif resposta == 7:
            cad_manutenção()
        elif resposta == 8:
            cad_remoção()
        elif resposta == 9:
            exist()
        elif resposta == 10:
            count_()
            mes_instalação()
        elif resposta == 11:
            exit()
