import json
import sqlite3

habilidades_compativeis = []
habilidades_incompativeis = []
requisitos = [] 

sql_vagas = "CREATE TABLE IF NOT EXISTS vagas ( id_vaga INTEGER PRIMARY KEY AUTOINCREMENT, nome_vaga TEXT, nome_empresa TEXT, data_vaga_criada TEXT, data_vaga_encerra TEXT, tipo_vaga TEXT, modalidade_trabalho TEXT, local_trabalho TEXT, beneficios TEXT, salario REAL, sobre_vaga TEXT, sobre_empresa TEXT );"
sql_requisitos = "CREATE TABLE IF NOT EXISTS requisitos ( id_requisito INTEGER PRIMARY KEY AUTOINCREMENT, requisito TEXT );" 
sql_requisito_vaga = "CREATE TABLE IF NOT EXISTS requisito_vaga ( fk_vaga INTEGER, fk_requisito INTEGER, prioridade TEXT, FOREIGN KEY(fk_vaga) REFERENCES vagas(id_vaga), FOREIGN KEY(fk_requisito) REFERENCES requisitos(id_requisito) );"
sql_candidatura = "CREATE TABLE IF NOT EXISTS candidaturas ( id_candidatura INTEGER PRIMARY KEY AUTOINCREMENT, fk_vaga INTEGER, data_candidatura TEXT, aderencia INTEGER, FOREIGN KEY(fk_vaga) REFERENCES vagas(id_vaga) );"
sql_requisitos_candidatura  = "CREATE TABLE IF NOT EXISTS requisitos_candidatura ( fk_candidatura INTEGER, fk_requisito INTEGER, requisito_cumprido INTEGER, FOREIGN KEY(fk_candidatura) REFERENCES candidaturas(id_candidatura), FOREIGN KEY(fk_requisito) REFERENCES requisitos(id_requisito) );"

sql_insere_vaga = "INSERT INTO vagas (nome_vaga, nome_empresa, data_vaga_criada, data_vaga_encerra, tipo_vaga, modalidade_trabalho, local_trabalho, beneficios, salario, sobre_vaga, sobre_empresa) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"
sql_insere_requisito = "INSERT INTO requisitos (requisito) VALUES (?)"

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
while(maisRequisito == 0):                                                                                                                                                                      
    novo_requisito = input("Digite o requisito da vaga: ")
    requisitos.append(novo_requisito)                                                                                                                          
    maisRequisito = int(input("Digite 0 caso tanha mais requisitos ou 1 para finalizar"))                                                                  

vaga = {'nome_vaga' : nome_vaga, 'nome_empresa' : nome_empresa, 'data_vaga_criada' : data_vaga_criada, 'data_vaga_encerra' : data_vaga_encerra, 'tipo_vaga' : tipo_vaga, 'modalidade_trabalho' : modalidade_trabalho, 'local_trabalho' : local_trabalho,
         'beneficios' : beneficios,'salario' : salario,'sobre_vaga' : sobre_vaga,'sobre_empresa' : sobre_empresa}

for x in vaga:
    if(vaga[x] == ""):
        vaga[x] = None

valores_vaga = tuple(vaga.values())

conexao = sqlite3.connect("candidatoIA.db")
cursor = conexao.cursor()

cursor.execute(sql_vagas)
cursor.execute(sql_requisitos)
cursor.execute(sql_requisito_vaga)
cursor.execute(sql_candidatura)
cursor.execute(sql_requisitos_candidatura)

cursor.execute(sql_insere_vaga, valores_vaga)

for x in requisitos:
    requisito_atual = (x, )
    cursor.execute(sql_insere_requisito, requisito_atual)


res = cursor.execute("SELECT * FROM requisitos;")
resultado = res.fetchall()

print(resultado)


conexao.commit()
conexao.close()


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
        
porcentagem_compativel = len(habilidades_compativeis) * 100 / len(perfil_candidato_habilidades)
porcentagem_compativel = int(round(porcentagem_compativel, 0))

if(porcentagem_compativel >= 70):
    print("Grande aderência das habilidades na vaga!")
elif((porcentagem_compativel <= 69) and (porcentagem_compativel >= 50)):
    print("Boa aderência das habilidades na vaga!")
else:
    print("Pouca aderência das habilidades na vaga")

print(f"Essas habilidades batem com a vaga: {habilidades}!")

print(f"Porcentagem de aderência de habilidades na vaga: {porcentagem_compativel}%")
