from bs4 import BeautifulSoup
import requests
import datetime
import json
import pyautogui
from datetime import date
import unidecode


with open('RotasJobClickB.json', 'r') as info:
    rotas = json.load(info)


def limpaValor(valor):
    cont = 0
    digit = ''
    PosVirg = ''
    for a in valor:
        qnt = len(valor) - 3
        cont += 1
        if cont <= qnt:
            digit += a
        elif cont > qnt + 1:
            PosVirg += a
    numFinal = f'{digit}.{PosVirg}'
    return(numFinal)


def isdigit(texto):
    numero = ''
    for a in str(texto.strip()):
        if a.isdigit():
            numero = numero + a
    return numero


def limpaCidades(cidade):
    limpa = cidade[:-3]
    return limpa


def rotasClickBuss(origem, destino, ano, mes, dia):
    origem_tratada = unidecode.unidecode(origem).lower().strip()
    destino_tratado = unidecode.unidecode(destino).lower().strip()

    origem_final = origem_tratada.replace(' ', '-')
    destino_final = destino_tratado.replace(' ', '-')

    print(origem_final)
    print(destino_final)

    origemLimpa = limpaCidades(origem_final)
    destinoLimpa = limpaCidades(destino_final)

    city_todos = ['sao-paulo-sp', 'rio-de-janeiro-rj', 'belo-horizonte-mg', 'recife-pe', 'maceio-al', 'brasilia-df', 'fortaleza-ce',
                  'vitoria-es', 'campinas-ms', 'sao-jose-do-rio-preto-sp', 'juiz-de-fora-mg ', 'sao-jose-dos-campos-sp',
                  'campos-dos-goytacazes-rj', 'joao-pessoa-pb', 'curitiba-pr', 'natal-rn', 'nova-friburgo-rj',
                  'porto-alegre-rs', 'aracaju']

    SemiLeitos = ['Semileito - C/ AR', 'Semileito - DD', 'Semileito - Space']
    Execut = ['Executivo - DD', 'Convencional -  DD', 'Convencional']
    Cama = ['Cama - Cabine']
    Leito = ['Leito - Total']

    if origem_final in city_todos:
        url = requests.get(f'https://www.clickbus.com.br/onibus/{origem_final}-todos/{destino_final}?departureDate={ano}-{mes}-{dia}')
        if destino_final in city_todos:
            url = requests.get(f'https://www.clickbus.com.br/onibus/{origem_final}-todos/{destino_final}-todos?departureDate={ano}-{mes}-{dia}')
    elif destino_final in city_todos:
        url = requests.get(f'https://www.clickbus.com.br/onibus/{origem_final}/{destino_final}-todos?departureDate={ano}-{mes}-{dia}')
    else:
        url = requests.get(f'https://www.clickbus.com.br/onibus/{origem_final}/{destino_final}?departureDate={ano}-{mes}-{dia}')

    print(url)

    ender = url.content
    bea = BeautifulSoup(ender, 'html.parser')

    fedd = bea.findAll('div', attrs={'class': 'search-result-item valign-wrapper'})

    lista_ofestas = []
    listDelist = []
    listacopy = []
    for info in fedd:
        preco = info.find('span', attrs={'class': 'price-value'})
        empresas = info.find('div', attrs={'class': 'company'})
        tipo_leito = info.find('div', attrs={'class': 'service-class'})
        hr_saida = info.find('time', attrs={'class': 'departure-time'})
        hr_chegada = info.find('time', attrs={'class': 'return-time'})
        qtd_leito = info.find('small', attrs={'class': 'available-seats'})
        data = hr_saida['data-date']

        leitotexto = str(qtd_leito.text)
        var = isdigit(leitotexto)

        leito = str(tipo_leito['content'])
        if leito in SemiLeitos:
            leito = 'SEMI-LEITO'
        elif leito in Execut:
            leito = 'EXECUTIVO'
        elif leito in Cama:
            leito = 'CAMA'
        elif leito in Leito:
            leito = 'LEITO'

        valor = str(preco.text)[2:]
        valorlimpo = limpaValor(valor)

        lista_ofestas.append(data)
        lista_ofestas.append(empresas['data-name'])
        lista_ofestas.append(valorlimpo)
        lista_ofestas.append(hr_saida.text)
        lista_ofestas.append(hr_chegada.text)
        lista_ofestas.append(leito.upper())
        lista_ofestas.append(var)
        lista_ofestas.append('Onibus')
        lista_ofestas.append(f'{origemLimpa.replace("-"," ")}'.upper())
        lista_ofestas.append(f'{destinoLimpa.replace("-"," ")}'.upper())
        lista_ofestas.append(f'{origemLimpa.replace("-"," ")} - {destinoLimpa.replace("-"," ")}'.upper())
        lista_ofestas.append(str(date.today()))

        listacopy = lista_ofestas.copy()
        listDelist.append(listacopy)
        lista_ofestas.clear()

    return listDelist


Lorigem = rotas['Origem']
Ldestino = rotas['Destino']

dados = {}
rotaRaiz = {}

data = date.today()
cont = 0
for i in range(len(Lorigem)):
    print(f'{i}° ROTA')
    origem = Lorigem[i]
    destino = Ldestino[i]
    hoje = date(2023, 1, 12)
    for j in range(10): #QUANTIDADE DE DIAS QUE VAI RODAR
        cont += 1
        data1 = str(hoje)
        ano = int(data1[0:4])
        mes = int(data1[5:7])
        dia = int(data1[8:10])

        #pyautogui.press("win")

        if cont == 1:
            rot1 = rotasClickBuss(origem, destino, ano, mes, dia)
        elif cont >= 2:
            rot2 = rotasClickBuss(origem, destino, ano, mes, dia)
            rot1.extend(rot2)

        hoje += datetime.timedelta(days=1)

    cont = 0

    dados[f"{limpaCidades(Lorigem[i]).replace('-',' ')} - {limpaCidades(Ldestino[i]).replace('-',' ')}".upper()] = rot1


with open('OfertasClickBuss1.json', 'w') as mijson:
    json.dump(dados, mijson, indent=4)
