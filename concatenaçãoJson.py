import json

with open('OfertasBuscaO.json', 'r') as dades:
    former = json.load(dades)

with open('OfertasClickBuss1 (3).json', 'r') as dado:
    new = json.load(dado)


#CONCATENAR OS DADOS
def concatenac(dados_novos, dados_antigos, NewRotas):
    for x in dados_antigos:
        for z in dados_novos:
            if z == x:
                dados_antigos[x].extend(dados_novos[z])

    for a in NewRotas:
        dados_antigos[a] = NewRotas[a]

    return dados_antigos


AntigEmpres = []

#FUNÇÃO PARA IDENTIFICAR AS NOVAS ROTAS SOLICITADAS
NewRotas = [x for x in new if x not in former.keys()]

NovasOfertas = {}
for x in NewRotas:
    NovasOfertas[f'{x}'] = new[x]

for a in former:
    for b in former[a]:
        AntigEmpres.append(f'{b[1]}'.upper())

#FUNÇÃO PARA INSERIR NOVAS EMPRESAS DE ROTAS ANTIGAS
NewEmpres = []
listaTempo = []
EmpreRotNew = {}
for rotas in new:
    for lista in new[rotas]:
        empresas = f'{lista[1]}'.upper()
        if empresas == 'MATRIZ':
            empresas = 'Matriz Transportes'.upper()
        if empresas not in AntigEmpres:
            print(lista)
            listaTempo.append(lista)
    NewEmpres = listaTempo.copy()
    EmpreRotNew[rotas] = NewEmpres
    listaTempo.clear()


#EXCLUINDO ROTAS VAZIAS
todasrotas = concatenac(EmpreRotNew, former, NovasOfertas)

cont_lista = 0
rotas_vazias = []
for r in todasrotas:
    for l in todasrotas[r]:
        cont_lista += 1
    if cont_lista < 1:
        rotas_vazias.append(f'{r}')
    cont_lista = 0

for a in rotas_vazias:
    todasrotas.pop(a, None)

#SALVANDO OS DADOS
with open('OfertasConcatenadas.json', 'w') as myjson:
    json.dump(todasrotas, myjson, indent=4)
