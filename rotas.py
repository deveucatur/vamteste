import json

def limpaCidades(cidade):
    limpa = cidade[:-3]
    return limpa


origem = ['brasília df', 'São Paulo sp', 'brasília df', 'Taguantinga df', 'Teresina PI', 'goiânia go', 'juazeiro do norte CE']
destino = ['goiânia GO', 'Salvador BA', 'montes claros mg', 'goiânia GO', 'brasília go', 'aracaju se', 'são paulo sp']

origemBusc = []
destinoBusc = []
origemClick = []
destinoClick = []

for a in range(len(origem)):
    orig = origem[a].upper()
    dest = destino[a].upper()
    origemClick.append(orig)
    destinoClick.append(dest)
    origemBusc.append(limpaCidades(orig))
    destinoBusc.append(limpaCidades(dest))

dicClick = {'ORIGEM':origemClick,
        'DESTINO':destinoClick}

dicBusca = {'ORIGEM':origemBusc,
        'DESTINO':destinoBusc}

with open('RotasJobBuscaO.json','w') as info:
    json.dump(dicClick, info, indent=4)
    
with open('RotasJobClick.json','w') as info:
    json.dump(dicClick, info, indent=4)
