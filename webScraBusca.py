import datetime
import requests
from bs4 import BeautifulSoup
import json


## FUNÇOES ##
def limpa_str(info_pag):
    valo_limpo = ''
    for values in info_pag:
        if values.isdigit():
            valo_limpo = f'{valo_limpo}' + f'{values}'
    return valo_limpo


def limpa_str_valor(valor):
    valor_limpo = limpa_str(valor)
    qntd_dig = len(valor_limpo) - 2
    cont = 0
    valor_menor = ''
    valor_maior = ''
    for splitad in valor_limpo:
        cont += 1
        if cont <= qntd_dig:
            valor_menor = f'{valor_menor}' + splitad
        else:
            valor_maior = f'{valor_maior}' + splitad
    valor_final = f'{valor_menor}' + '.' + f'{valor_maior}'
    return valor_final


def limpa_str_horas(valor):
    valor_limpo = limpa_str(valor)
    qntd_dig = len(valor_limpo) - 2
    cont = 0
    valor_menor = ''
    valor_maior = ''
    for splitad in valor_limpo:
        cont += 1
        if cont <= qntd_dig:
            valor_menor = f'{valor_menor}' + splitad
        else:
            valor_maior = f'{valor_maior}' + splitad
    valor_final = f'{valor_menor}' + ':' + f'{valor_maior}'
    return valor_final


def rotas_concorrentes(saida, destino, ano, mes, dia):
    ender = requests.get(f'https://www.buscaonibus.com.br/horario/{saida}/{destino}?dt={dia}/{mes}/{ano}')
    ender_get = ender.content
    bea = BeautifulSoup(ender_get, 'html.parser')

    # HTML DA PAGINA
    feed = bea.findAll('div', attrs={'class': 'bo-timetable-info'})

    empresas = []
    lista_paramet = []
    lista_tempo = []

    cont = 0
    for info in feed:
        cont += 1

        preco = info.find('div', attrs={'class': 'bo-timetable-price'})
        empresa = info.find('div', attrs={'class': 'bo-timetable-company-name'})
        tipo_leito = info.find('div', attrs={'class': 'bo-timetable-type'})
        hr_saida = info.find('span', attrs={'class': 'bo-timetable-departure'})
        hr_chedada = info.find('span', attrs={'class': 'bo-timetable-arrival'})
        qtd_leito = info.find('div', attrs={'class': 'bo-timetable-seats'})


        preco_limpo = limpa_str_valor(preco.text)
        hr_saida_limpo = limpa_str_horas(hr_saida.text)
        hr_chedada_limpo = limpa_str_horas(hr_chedada.text)
        qtd_leito_limpo = limpa_str(qtd_leito.text)

        lista_tempo.append(str(datetime.date(ano, mes, dia)))
        lista_tempo.append(empresa.text)
        lista_tempo.append(preco_limpo)
        lista_tempo.append(hr_saida_limpo)
        lista_tempo.append(hr_chedada_limpo)
        lista_tempo.append(tipo_leito.text)
        lista_tempo.append(qtd_leito_limpo)

        if empresa.text == "Skyscanner":
            lista_tempo.append("Aviao")
        elif empresa.text == "BlaBlaCar":
            lista_tempo.append("Carro")
        else:
            lista_tempo.append("Onibus")

        lista_tempo.append(saida)
        lista_tempo.append(destino)
        lista_tempo.append(saida + " - " + destino)
        lista_tempo.append(str(datetime.date.today()))

        lista_paramet = lista_tempo.copy()
        empresas.append(lista_paramet)
        lista_tempo.clear()

    return empresas


#ABRINDO ARQUIVO JSON DE ROTAS
with open('RotasJobBuscaO.json', 'r') as info:
    rotas = json.load(info)

Lorigem = rotas['Origem']
Ldestino = rotas['Destino']

dados = {}
cont = 0

for i in range(len(Lorigem)):
    print(f'{i}° ROTA')
    origem = Lorigem[i]
    destino = Ldestino[i]
    hoje = datetime.date(2023, 1, 12)

    for j in range(10): #QUANTIDADE DE DIAS QUE VAI RODAR
        cont += 1
        data1 = str(hoje)
        ano = int(data1[0:4])
        mes = int(data1[5:7])
        dia = int(data1[8:10])

        if cont == 1:
            r1 = rotas = rotas_concorrentes(origem, destino, ano, mes, dia)
        elif cont >= 2:
            r2 = rotas = rotas_concorrentes(origem, destino, ano, mes, dia)
            r1.extend(r2)
        hoje += datetime.timedelta(days=1)

    cont = 0

    dados[f"{Lorigem[i]} - {Ldestino[i]}"] = r1


with open("OfertasBuscaO.json", "w") as json_file:
    json.dump(dados, json_file, indent=4)


