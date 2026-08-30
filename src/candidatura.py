import json

habilidades_compativeis = []
habilidades_incompativeis = []

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
            habilidades_incompativeis.append(habilidade)

habilidades = ', '.join(habilidades_compativeis)
        
porcentagem_compativel = len(habilidades_compativeis) * 100 / len(perfil_candidato_habilidades)
porcentagem_compativel = int(round(porcentagem_compativel, 0))

if(porcentagem_compativel >= 70):
    print("Grandes chances de ser aprovado!")
elif((porcentagem_compativel <= 69) and (porcentagem_compativel >= 50)):
    print("Boas chances de ser aprovado!")
else:
    print("Pouca chance ser aprovado")

print(f"Essas habilidades batem com a vaga: {habilidades}!")

print(f"Chance de aprovação: {porcentagem_compativel}%")