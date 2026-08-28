import json

habilidades_compativeis = []

#codigo que ler um arquivo.txt e também o deixa minusculo
with open("../dados/vagas.txt", "r", encoding="utf-8") as arquivo:
    conteudo = arquivo.read()
    conteudo = conteudo.lower()

#codigo que ler um arquivo.json e também o deixa minusculo
with open("../dados/perfil.json", "r", encoding="utf-8") as arquivo:
    perfil_candidato = json.load(arquivo)
    perfil_candidato_habilidades = perfil_candidato["habilidades"]

    #também pega só as habililades compatives entre habilidades do candidato e descrição davaga
    for habilidade in perfil_candidato_habilidades:
        habilidade  = habilidade.lower()
        if(habilidade in conteudo):
            habilidades_compativeis.append(habilidade)

print(habilidades_compativeis)