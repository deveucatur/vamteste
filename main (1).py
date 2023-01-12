import json


def limpaCidades(cidade):
    limpa = cidade[:-3]
    return limpa


origem = ['brasília df','São Paulo sp','brasília df', 'Taguantinga df','Teresina PI', 'goiânia go','juazeiro do norte CE']
destino = ['goiânia GO','Salvador BA','montes claros mg','goiânia GO','brasília go','aracaju se', 'são paulo sp']


origemBusc = [limpaCidades(x).upper() for x in origem]
destinBusc = [limpaCidades(x).upper() for x in destino]
origemClick = [x.upper() for x in origem]
destinClick = [x.upper() for x in destino]

dicBusc = {'Origem': origemBusc,
           'Destino': destinBusc}

dicClick = {'Origem':origemClick,
            'Destino':destinClick}

with open('RotasJobBuscaO.json','w') as info:
    json.dump(dicBusc, info, indent=4)
    
with open('RotasJobClickB.json','w') as info1:
    json.dump(dicClick, info1, indent=4)
