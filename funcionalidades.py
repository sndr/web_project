

import json
import mysql.connector
import pandas as pd


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
10 - SAIR
''')

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
            placa = int(input("POSSUI PLACA: 1-SIM/2-NÃO"))
            if placa == 1:
                info_1 = input("DIGITE A PLACA: ")
                info_2 = input("DIGITE O CHASSI: ")
                info_3 = input("INSIRA O ENDEREÇO QUE O VEICULO ESTÁ: ")
                info_4 = input("INSIRA O TIPO DO DISPOSITIVO: ")
                info_5 = input("INSIRA O STATUS: ")
                info_6 = input("INSIRA O ID: ")
                cursor = conexao.cursor()
                verificar_id_query = "SELECT ID FROM instalacao WHERE ID = %s"
                cursor.execute(verificar_id_query, (info_6,))
                result = cursor.fetchone()
                if result:
                    print(f"ID {info_6} já existe. Não é permitido criar um novo com o mesmo valor.")
                else:
                    print(f"Inserindo o ID {info_6} na tabela INSTALAÇÃO.")
                    inserir_id_query = "INSERT INTO instalacao (ID) VALUES (%s)"
                    cursor.execute(inserir_id_query, (info_6,))
                    conexao.commit()
                    add = "INSERT INTO instalacao (ID) VALUES (%s)"
                    cursor.execute(add, (info_6,))
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
                info_6 = input("INSIRA O ID: ")
                add = "INSERT INTO instalacao (ID) VALUES (%s)"
                cursor = conexao.cursor()
                verificar_id_query = "SELECT ID FROM instalacao WHERE ID = %s"
                cursor.execute(verificar_id_query, (info_6,))
                result = cursor.fetchone()
                if result:
                    print(f"ID {info_6} já existe. Não é permitido criar um novo com o mesmo valor.")
                else:
                    print(f"Inserindo o ID {info_6} na tabela INSTALAÇÃO.")
                    inserir_id_query = "INSERT INTO instalacao (ID) VALUES (%s)"
                    cursor.execute(inserir_id_query, (info_6,))
                    conexao.commit()
                    cursor.execute(add, (info_6,))
                    att = "UPDATE instalacao SET CHASSI = %s, ENDERECO = %s, MODELO = %s, STATUS_INSTALACAO = %s WHERE ID = %s"
                    data = (info_2, info_3, info_4, info_5, info_6)
                    cursor.execute(att, data)
                    conexao.commit()
                    cursor.close()
                    conexao.close()
                    print("Linhas afetadas:", cursor.rowcount)
                
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
            placa = int(input("POSSUI PLACA: 1-SIM/2-NÃO"))
            if placa == 1:
                info_1 = input("DIGITE A PLACA: ")
                info_2 = input("DIGITE O CHASSI: ")
                info_3 = input("INSIRA O ENDEREÇO QUE O VEICULO ESTÁ: ")
                info_4 = input("INSIRA O TIPO DO DISPOSITIVO: ")
                info_5 = input("INSIRA O STATUS: ")
                info_6 = input("INSIRA O ID: ")
                cursor = conexao.cursor()
                verificar_id_query = "SELECT ID FROM manutencao WHERE ID = %s"
                cursor.execute(verificar_id_query, (info_6,))
                result = cursor.fetchone()
                if result:
                    print(f"ID {info_6} já existe. Não é permitido criar um novo com o mesmo valor.")
                else:
                    print(f"Inserindo o ID {info_6} na tabela MANUTENÇÃO.")
                    inserir_id_query = "INSERT INTO manutencao (ID) VALUES (%s)"
                    cursor.execute(inserir_id_query, (info_6,))
                    conexao.commit()
                    add = "INSERT INTO manutencao (ID) VALUES (%s)"
                    cursor = conexao.cursor()
                    cursor.execute(add, (info_6,))
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
                info_6 = input("INSIRA O ID: ")
                add = "INSERT INTO manutencao (ID) VALUES (%s)"
                cursor = conexao.cursor()
                verificar_id_query = "SELECT ID FROM manutencao WHERE ID = %s"
                cursor.execute(verificar_id_query, (info_6,))
                result = cursor.fetchone()
                if result:
                    print(f"ID {info_6} já existe. Não é permitido criar um novo com o mesmo valor.")
                else:
                    print(f"Inserindo o ID {info_6} na tabela MANUTENÇÃO.")
                    inserir_id_query = "INSERT INTO manutencao (ID) VALUES (%s)"
                    cursor.execute(inserir_id_query, (info_6,))
                    conexao.commit()
                    cursor.execute(add, (info_6,))
                    att = "UPDATE manutencao SET CHASSI = %s, ENDERECO = %s, MODELO = %s, STATUS_INSTALACAO = %s WHERE ID = %s"
                    data = (info_2, info_3, info_4, info_5, info_6)
                    cursor.execute(att, data)
                    conexao.commit()
                    cursor.close()
                    conexao.close()
                    print("Linhas afetadas:", cursor.rowcount)
                
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
            placa = int(input("POSSUI PLACA: 1-SIM/2-NÃO"))
            if placa == 1:
                info_1 = input("DIGITE A PLACA: ")
                info_2 = input("DIGITE O CHASSI: ")
                info_3 = input("INSIRA O ENDEREÇO QUE O VEICULO ESTÁ: ")
                info_4 = input("INSIRA O TIPO DO DISPOSITIVO: ")
                info_5 = input("INSIRA O STATUS: ")
                info_6 = input("INSIRA O ID: ")
                cursor = conexao.cursor()
                verificar_id_query = "SELECT ID FROM remocao WHERE ID = %s"
                cursor.execute(verificar_id_query, (info_6,))
                result = cursor.fetchone()
                if result:
                    print(f"ID {info_6} já existe. Não é permitido criar um novo com o mesmo valor.")
                else:
                    print(f"Inserindo o ID {info_6} na tabela REMOÇÃO.")
                    inserir_id_query = "INSERT INTO remocao (ID) VALUES (%s)"
                    cursor.execute(inserir_id_query, (info_6,))
                    conexao.commit()
                    add = "INSERT INTO remocao (ID) VALUES (%s)"
                    cursor.execute(add, (info_6,))
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
                info_6 = input("INSIRA O ID: ")
                cursor = conexao.cursor()
                verificar_id_query = "SELECT ID FROM remocao WHERE ID = %s"
                cursor.execute(verificar_id_query, (info_6,))
                result = cursor.fetchone()
                if result:
                    print(f"ID {info_6} já existe. Não é permitido criar um novo com o mesmo valor.")
                else:
                    print(f"Inserindo o ID {info_6} na tabela REMOÇÃO.")
                    inserir_id_query = "INSERT INTO remocao (ID) VALUES (%s)"
                    cursor.execute(inserir_id_query, (info_6,))
                    conexao.commit()
                add = "INSERT INTO remocao (ID) VALUES (%s)"
                cursor.execute(add, (info_6,))
                att = "UPDATE remocao SET CHASSI = %s, ENDERECO = %s, MODELO = %s, STATUS_INSTALACAO = %s WHERE ID = %s"
                data = (info_2, info_3, info_4, info_5, info_6)
                cursor.execute(att, data)
                conexao.commit()
                cursor.close()
                conexao.close()
                print("Linhas afetadas:", cursor.rowcount)
                
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
    pasta = str(input("DIGITE O NOME DA PASTA EXCEL PARA SALVAR EM JSON: "))
    nome_do_json = str(input("DIGITE O NOME DA PASTA JSON PARA SER CRIADA: "))
    df = pd.read_excel(pasta)
    jsonn = (nome_do_json)
    teste = df.iterrows()
    for item in teste:
        dado = {f'{item[0]}{item[1]}'}
    dado_salvo = pd.DataFrame(dado)
    df.to_json(jsonn,orient='index',indent=2)
    return print(f"dados salvos no arquivo {jsonn}")

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
            cursor.execute(remo)# ELE SO NÃO ESTA CONSEGUINDO APAGAR POR ID
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
            resposta = int(input("-> "))
            print()
        except Exception as e:
            print("VALOR INVÁLIDO\n---------------------")
            continue
        if resposta == 1:
            while True:
                salvar()
                terminou = input("DESEJA VOLTAR AO MENU OU CONTINUAR COM O ENVIO? \n1-CONTINUAR\n2-MENU\n-->")
                if terminou == 2:
                    break
                arquivo = str(input("DIGITE O NOME DA PASTA JSON PARA FAZER O ENVIO PARA O MYSQL: \n(OU 'S' PARA SAIR) "))
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
                    PLACA varchar(30),
                    CHASSI varchar(30),
                    EQUIPAMENTO varchar(30),
                    CLIENTE varchar(30),
                    MODELO varchar(30),
                    ENDERECO varchar(30),
                    COD_RASTREIO varchar(30),
                    STATUS_ENVIO varchar(30),
                    STATUS_AGENDAMENTO varchar(30),
                    STATUS_INSTALACAO varchar(30),
                    ID varchar(30));''')
                    
                cursor.execute('''create table manutencao(
                    PLACA varchar(30),
                    CHASSI varchar(30),
                    EQUIPAMENTO varchar(30),
                    CLIENTE varchar(30),
                    MODELO varchar(30),
                    ENDERECO varchar(30),
                    COD_RASTREIO varchar(30),
                    STATUS_ENVIO varchar(30),
                    STATUS_AGENDAMENTO varchar(30),
                    STATUS_INSTALACAO varchar(30),
                    ID varchar(30));''')
                
                cursor.execute('''create table remocao(
                    PLACA varchar(30),
                    CHASSI varchar(30),
                    EQUIPAMENTO varchar(30),
                    CLIENTE varchar(30),
                    MODELO varchar(30),
                    ENDERECO varchar(30),
                    COD_RASTREIO varchar(30),
                    STATUS_ENVIO varchar(30),
                    STATUS_AGENDAMENTO varchar(30),
                    STATUS_INSTALACAO varchar(30),
                    ID varchar(30));''')
                
                onde = input("NOME DA PASTA QUE VAI SALVAR OS DADOS: ")
                cursor.execute(f'''create table {onde}(
                    PLACA varchar(30),
                    CHASSI varchar(30),
                    EQUIPAMENTO varchar(30),
                    CLIENTE varchar(30),
                    MODELO varchar(30),
                    ENDERECO varchar(30),
                    COD_RASTREIO varchar(30),
                    STATUS_ENVIO varchar(30),
                    STATUS_AGENDAMENTO varchar(30),
                    STATUS_INSTALACAO varchar(30),
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
            exit()
            
            
