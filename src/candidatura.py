import json
import sqlite3
import datetime

# Estas listas guardam as habilidades encontradas ou nao encontradas na vaga.
habilidades_compativeis = []
habilidades_incompativeis = []
minhas_habilidades = [] 

# Comandos SQL usados para criar as tabelas do banco de dados.
sql_vagas = "CREATE TABLE IF NOT EXISTS vagas ( id_vaga INTEGER PRIMARY KEY AUTOINCREMENT, nome_vaga TEXT, nome_empresa TEXT, data_vaga_criada TEXT, data_vaga_encerra TEXT, tipo_vaga TEXT, modalidade_trabalho TEXT, local_trabalho TEXT, beneficios TEXT, salario REAL, sobre_vaga TEXT, sobre_empresa TEXT );"
sql_requisitos = "CREATE TABLE IF NOT EXISTS requisitos ( id_requisito INTEGER PRIMARY KEY AUTOINCREMENT, requisito TEXT );" 
sql_requisito_vaga = "CREATE TABLE IF NOT EXISTS requisito_vaga ( fk_vaga INTEGER, fk_requisito INTEGER, prioridade TEXT, FOREIGN KEY(fk_vaga) REFERENCES vagas(id_vaga), FOREIGN KEY(fk_requisito) REFERENCES requisitos(id_requisito) );"
sql_candidatura = "CREATE TABLE IF NOT EXISTS candidaturas ( id_candidatura INTEGER PRIMARY KEY AUTOINCREMENT, fk_vaga INTEGER, data_candidatura TEXT, aderencia INTEGER, FOREIGN KEY(fk_vaga) REFERENCES vagas(id_vaga) );"
sql_requisitos_candidatura  = "CREATE TABLE IF NOT EXISTS requisitos_candidatura ( fk_candidatura INTEGER, fk_requisito INTEGER, requisito_cumprido INTEGER, FOREIGN KEY(fk_candidatura) REFERENCES candidaturas(id_candidatura), FOREIGN KEY(fk_requisito) REFERENCES requisitos(id_requisito) );"

# Comandos SQL usados depois para inserir os dados coletados.
sql_insere_vaga = "INSERT INTO vagas (nome_vaga, nome_empresa, data_vaga_criada, data_vaga_encerra, tipo_vaga, modalidade_trabalho, local_trabalho, beneficios, salario, sobre_vaga, sobre_empresa) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"
sql_insere_requisito = "INSERT INTO requisitos (requisito) VALUES (?);"
sql_insere_requisito_vaga  = "INSERT INTO requisito_vaga(fk_vaga, fk_requisito, prioridade) VALUES (?, ?, ?);"
sql_insere_candidatura = "INSERT INTO candidaturas(fk_vaga, data_candidatura, aderencia) VALUES (?, ?, ?);"
sql_insere_requisito_candidatura = "INSERT INTO requisitos_candidatura(fk_candidatura, fk_requisito, requisito_cumprido) VALUES (?, ?, ?)"

# Aqui sao pedidos os dados principais da vaga.
nome_vaga = input("Digite o nome da vaga: ")
nome_vaga = nome_vaga.strip()
# O nome da vaga nao pode ficar vazio.
while(nome_vaga == ""):  
    nome_vaga = input("Digite o nome da vaga: ")
    nome_vaga = nome_vaga.strip()

nome_empresa = input("Digite o nome da empresa: ")
data_vaga_criada = input("Digite a data de inicio do processo da vaga: ")
data_vaga_encerra = input("Digite a data de fim do processo da vaga: ")
tipo_vaga = input("Digite o tipo da vaga: ")
modalidade_trabalho = input("Digite a modalidade de trabalho da vaga:: ")
local_trabalho = input("Digite o local de trabalho da vaga? ")
beneficios = input("Digite os beneficios da vaga: ")
salario = input("Digite o salario da vaga: ")

sobre_vaga = input("Digite  sobre a vaga: ")
sobre_vaga = sobre_vaga.strip()
while(sobre_vaga == ""):  
    sobre_vaga = input("Digite  sobre a vaga: ")
    sobre_vaga = sobre_vaga.strip()

sobre_empresa = input("Digite sobre a empresa: ") 
 
# Este dicionario relaciona cada requisito com sua prioridade.
mais_requisito = 0
requisito_prioridade = {}
while(mais_requisito == 0):
    novo_requisito = ""
    while(novo_requisito == ""):
        novo_requisito = input("Digite o requisito da vaga: ")
        novo_requisito = novo_requisito.strip()
    prioridade_requisito = ""
    while(prioridade_requisito != "obrigatório") and (prioridade_requisito != "desejável"):
        prioridade_requisito = int(input("Digite 1 para obrigatório ou 2 - desejável! Qual a prioridade do seu requisito: "))
        if(prioridade_requisito == 1):
            prioridade_requisito = "obrigatório"
        elif(prioridade_requisito == 2):
            prioridade_requisito = "desejável"
        else:
            print("Numerão incorreta")
            prioridade_requisito = ""
    requisito_prioridade[novo_requisito] = prioridade_requisito

    # Pergunta se o usuario quer cadastrar outro requisito.
    valida_requisito = 0
    while(valida_requisito == 0):
        mais_requisito = int(input("Digite 0 caso tenha mais requisitos ou 1 para finalizar: "))
        valida_requisito = 1
        if(mais_requisito != 0) and (mais_requisito !=1):
            print("Numerão incorreta")
            valida_requisito = 0

# Le o arquivo com a descricao da vaga e transforma o texto em minusculo.
with open("./dados/vagas.txt", "r", encoding="utf-8") as arquivo:
    conteudo = arquivo.read()
    conteudo = conteudo.lower()
    
# Le o perfil do candidato para comparar suas habilidades com a vaga.
with open("./dados/curriculo.json", "r", encoding="utf-8") as arquivo:
    curriculo = json.load(arquivo)
    habilidades_para_comparar = curriculo["competencias"]["linguagens"] + curriculo["competencias"]["ferramentas"] + curriculo["competencias"]["sistemas_operacionais"]

    # Compara cada habilidade do candidato com o texto da vaga.
    for habilidade in habilidades_para_comparar:
        habilidade  = habilidade.lower()
        if(habilidade in conteudo):
            habilidades_compativeis.append(habilidade)
        else:
            # Esta lista pode ser usada futuramente pelo RF 005.
            habilidades_incompativeis.append(habilidade)

# Junta as habilidades encontradas para mostrar na tela.
habilidades = ', '.join(habilidades_compativeis)

# Calcula a porcentagem de habilidades do candidato que aparecem na vaga.
aderencia = len(habilidades_compativeis) * 100 / len(habilidades_para_comparar)
aderencia = int(round(aderencia, 0))

# Mostra uma mensagem de acordo com o resultado da aderencia.
if(aderencia >= 70):
    print("Grande aderência das habilidades na vaga!")
elif((aderencia <= 69) and (aderencia >= 50)):
    print("Boa aderência das habilidades na vaga!")
else:
    print("Pouca aderência das habilidades na vaga")

print(f"Essas habilidades batem com a vaga: {habilidades}!")

print(f"Porcentagem de aderência de habilidades na vaga: {aderencia}%")                                                              

# Cria um dicionario com os dados preenchidos pelo usuario.
vaga = {'nome_vaga' : nome_vaga, 'nome_empresa' : nome_empresa, 'data_vaga_criada' : data_vaga_criada, 'data_vaga_encerra' : data_vaga_encerra, 'tipo_vaga' : tipo_vaga, 'modalidade_trabalho' : modalidade_trabalho, 'local_trabalho' : local_trabalho,
         'beneficios' : beneficios,'salario' : salario,'sobre_vaga' : sobre_vaga,'sobre_empresa' : sobre_empresa}

# Retira espacos desnecessarios e troca campos vazios por None.
for x in vaga:
    vaga[x] = vaga[x].strip()
    if(vaga[x] == ""):
        vaga[x] = None

valores_vaga = tuple(vaga.values())

data_candidatura = str(datetime.datetime.now())

# Abre o banco de dados e cria um cursor para executar os comandos SQL.

conexao = sqlite3.connect("candidatoIA.db")
cursor = conexao.cursor()

# Garante que todas as tabelas existam antes de inserir os dados.
cursor.execute(sql_vagas)

cursor.execute(sql_requisitos)
cursor.execute(sql_requisito_vaga)
cursor.execute(sql_candidatura)
cursor.execute(sql_requisitos_candidatura)

# Primeiro salva a vaga e pega o ID criado automaticamente.
cursor.execute(sql_insere_vaga, valores_vaga)
id_vaga = cursor.lastrowid

# Salva a candidatura ligada a essa vaga.
candidatura = (id_vaga, data_candidatura, aderencia)
cursor.execute(sql_insere_candidatura, candidatura)
id_candidatura = cursor.lastrowid

# Deixa as habilidades do candidato em minusculo para facilitar a comparacao.
for requisito in habilidades_para_comparar:
    requisito = requisito.lower()
    minhas_habilidades.append(requisito)

# Salva cada requisito e informa se o candidato possui essa habilidade.
for x in requisito_prioridade:
    requisito_atual = (x, )
    cursor.execute(sql_insere_requisito, requisito_atual)

    valores_requisito_vaga = (id_vaga, cursor.lastrowid, requisito_prioridade[x])

    cursor.execute(sql_insere_requisito_vaga, valores_requisito_vaga)

    if(x.lower() in minhas_habilidades):
        # Valor 1 representa requisito cumprido.
        requisito_cumprido = 1
    else:
        # Valor 0 representa requisito que ainda nao foi cumprido.
        requisito_cumprido = 0

    valores_requisito_candidatura = (id_candidatura, cursor.lastrowid, requisito_cumprido)
    cursor.execute(sql_insere_requisito_candidatura, valores_requisito_candidatura)

                                     
# Este trecho pode ser usado para consultar os requisitos salvos.
'''res = cursor.execute("SELECT * FROM requisitos_candidatura")
resultado = res.fetchall()

print(resultado)'''
# Confirma todas as alteracoes e fecha a conexao com o banco.
conexao.commit()
conexao.close()