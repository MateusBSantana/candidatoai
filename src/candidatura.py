import json
import sqlite3
import datetime

habilidades_compativeis = []
habilidades_incompativeis = []
minhas_habilidades = [] 

sql_vagas = "CREATE TABLE IF NOT EXISTS vagas ( id_vaga INTEGER PRIMARY KEY AUTOINCREMENT, nome_vaga TEXT, nome_empresa TEXT, data_vaga_criada TEXT, data_vaga_encerra TEXT, tipo_vaga TEXT, modalidade_trabalho TEXT, local_trabalho TEXT, beneficios TEXT, salario REAL, sobre_vaga TEXT, sobre_empresa TEXT );"
sql_requisitos = "CREATE TABLE IF NOT EXISTS requisitos ( id_requisito INTEGER PRIMARY KEY AUTOINCREMENT, requisito TEXT );" 
sql_requisito_vaga = "CREATE TABLE IF NOT EXISTS requisito_vaga ( fk_vaga INTEGER, fk_requisito INTEGER, prioridade TEXT, FOREIGN KEY(fk_vaga) REFERENCES vagas(id_vaga), FOREIGN KEY(fk_requisito) REFERENCES requisitos(id_requisito) );"
sql_candidatura = "CREATE TABLE IF NOT EXISTS candidaturas ( id_candidatura INTEGER PRIMARY KEY AUTOINCREMENT, fk_vaga INTEGER, data_candidatura TEXT, aderencia INTEGER, FOREIGN KEY(fk_vaga) REFERENCES vagas(id_vaga) );"
sql_requisitos_candidatura  = "CREATE TABLE IF NOT EXISTS requisitos_candidatura ( fk_candidatura INTEGER, fk_requisito INTEGER, requisito_cumprido INTEGER, FOREIGN KEY(fk_candidatura) REFERENCES candidaturas(id_candidatura), FOREIGN KEY(fk_requisito) REFERENCES requisitos(id_requisito) );"

sql_insere_vaga = "INSERT INTO vagas (nome_vaga, nome_empresa, data_vaga_criada, data_vaga_encerra, tipo_vaga, modalidade_trabalho, local_trabalho, beneficios, salario, sobre_vaga, sobre_empresa) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"
sql_insere_requisito = "INSERT INTO requisitos (requisito) VALUES (?);"
sql_insere_requisito_vaga  = "INSERT INTO requisito_vaga(fk_vaga, fk_requisito, prioridade) VALUES (?, ?, ?);"
sql_insere_candidatura = "INSERT INTO candidaturas(fk_vaga, data_candidatura, aderencia) VALUES (?, ?, ?);"
sql_insere_requisito_candidatura = "INSERT INTO requisitos_candidatura(fk_candidatura, fk_requisito, requisito_cumprido) VALUES (?, ?, ?)"

nome_vaga = input("Digite o nome da vaga: ")
while(nome_vaga == ""):  
    nome_vaga = input("Digite o nome da vaga: ")
nome_empresa = input("Digite o nome da empresa: ")
data_vaga_criada = input("Digite a data de inicio do processo da vaga: ")
data_vaga_encerra = input("Digite a data de fim do processo da vaga: ")
tipo_vaga = input("Digite o tipo da vaga: ")
modalidade_trabalho = input("Digite a modalidade de trabalho da vaga:: ")
local_trabalho = input("Digite o local de trabalho da vaga? ")
beneficios = input("Digite os beneficios da vaga: ")
salario = input("Digite o salario da vaga: ")
sobre_vaga = input("Digite  sobre a vaga: ")
while(sobre_vaga == ""):  
    sobre_vaga = input("Digite  sobre a vaga: ")
sobre_empresa = input("Digite sobre a empresa: ") 
 
maisRequisito = 0
requisito_prioridade = {}
while(maisRequisito == 0):
    novo_requisito = input("Digite o requisito da vaga: ")
    prioridade_requisito = int(input("Digite 1 para obrigatório ou 2 - desejável! Qual a prioridade do seu requisito: "))
    if(prioridade_requisito == 1):
        prioridade_requisito = "obrigatório"
    else:
        prioridade_requisito = "desejável"
    requisito_prioridade[novo_requisito] = prioridade_requisito
    maisRequisito = int(input("Digite 0 caso tenha mais requisitos ou 1 para finalizar: "))   

#codigo que ler um arquivo.txt e também o deixa minusculo
with open("./dados/vagas.txt", "r", encoding="utf-8") as arquivo:
    conteudo = arquivo.read()
    conteudo = conteudo.lower()
    
#codigo que ler um arquivo.json e também o deixa minusculo
with open("./dados/perfil.json", "r", encoding="utf-8") as arquivo:
    perfil_candidato = json.load(arquivo)
    perfil_candidato_habilidades = perfil_candidato["habilidades"]

    #Essa estrutura de for e if pega só as habililades compatives e incompativeis entre habilidades do candidato e descrição davaga
    for habilidade in perfil_candidato_habilidades:
        habilidade  = habilidade.lower()
        if(habilidade in conteudo):
            habilidades_compativeis.append(habilidade)
        else:
            #Guardado para uso futuro no RF 005, quando o LLM estiver integrado
            habilidades_incompativeis.append(habilidade)

habilidades = ', '.join(habilidades_compativeis)
        
aderencia = len(habilidades_compativeis) * 100 / len(perfil_candidato_habilidades)
aderencia = int(round(aderencia, 0))

if(aderencia >= 70):
    print("Grande aderência das habilidades na vaga!")
elif((aderencia <= 69) and (aderencia >= 50)):
    print("Boa aderência das habilidades na vaga!")
else:
    print("Pouca aderência das habilidades na vaga")

print(f"Essas habilidades batem com a vaga: {habilidades}!")

print(f"Porcentagem de aderência de habilidades na vaga: {aderencia}%")                                                              

vaga = {'nome_vaga' : nome_vaga, 'nome_empresa' : nome_empresa, 'data_vaga_criada' : data_vaga_criada, 'data_vaga_encerra' : data_vaga_encerra, 'tipo_vaga' : tipo_vaga, 'modalidade_trabalho' : modalidade_trabalho, 'local_trabalho' : local_trabalho,
         'beneficios' : beneficios,'salario' : salario,'sobre_vaga' : sobre_vaga,'sobre_empresa' : sobre_empresa}

for x in vaga:
    if(vaga[x] == ""):
        vaga[x] = None

valores_vaga = tuple(vaga.values())

data_candidatura = str(datetime.datetime.now())



conexao = sqlite3.connect("candidatoIA.db")
cursor = conexao.cursor()

cursor.execute(sql_vagas)

cursor.execute(sql_requisitos)
cursor.execute(sql_requisito_vaga)
cursor.execute(sql_candidatura)
cursor.execute(sql_requisitos_candidatura)

cursor.execute(sql_insere_vaga, valores_vaga)
id_vaga = cursor.lastrowid

valores_requisito_vaga = []

candidatura = (id_vaga, data_candidatura, aderencia)
cursor.execute(sql_insere_candidatura, candidatura)
id_candidatura = cursor.lastrowid

minhas_habilidades = []

for requisito in perfil_candidato_habilidades:
    requisito = requisito.lower()
    minhas_habilidades.append(requisito)

for x in requisito_prioridade:
    requisito_atual = (x, )
    cursor.execute(sql_insere_requisito, requisito_atual)

    valores_requisito_vaga = (id_vaga, cursor.lastrowid, requisito_prioridade[x])

    cursor.execute(sql_insere_requisito_vaga, valores_requisito_vaga)

    if(x.lower() in minhas_habilidades):
        requisito_cumprido = 1
    else:
        requisito_cumprido = 0

    valores_requisito_candidatura = (id_candidatura, cursor.lastrowid, requisito_cumprido)
    cursor.execute(sql_insere_requisito_candidatura, valores_requisito_candidatura)

                                     
res = cursor.execute("SELECT * FROM requisitos_candidatura")
resultado = res.fetchall()

print(resultado)


conexao.commit()
conexao.close()