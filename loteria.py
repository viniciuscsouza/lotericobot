import re, requests
from bs4 import BeautifulSoup

def baixadados():
    """
    Baixa código-fonte da página da Mega-Sena e retorna texto do bloco id="resultados"
    """
    try:
        # Baixa página da CEF com resultado da Mega-Sena
        r =  requests.get("http://loterias.caixa.gov.br/wps/portal/loterias/landing/megasena/")
        # Cria instância da classe BeautifulSoup passando a página baixada
        soup = BeautifulSoup(r.content, 'html.parser')
        # Filtra tags do bloco id "resultados"
        soup = soup.find(id="resultados")
        resposta = soup.text
        resposta = resposta.replace("\t","").replace("\r","").replace("\n","|")
    except Exception as e:
        print("Ocorreu um erro: " + str(e))
    return resposta

def concursoatual():
    """
    Retorna uma lista com o número do último concurso, data da realização do último concurso,
    cidade onde foi realizado o sorteio e lista com as dezenas sorteadas
    """
    # Recebe bloco id="resultados"
    texto = baixadados()
    # Extrai número do concurso realizado
    concurso = re.search(r'\d{4}', texto)
    concurso = concurso.group()
    # Extrai data do concurso
    data = re.findall(r'\w+/\w+/\w+', texto)
    data = data[0]
    # Extrai cidade onde ocorreu o sorteio
    cidade = re.search(r'([A-Z]+), ([\w]+)', texto)
    cidade = cidade.group()
    # Extrai e lista dezenas sorteadas
    dezenas = re.search(r'[0-9]{12}', texto)
    dezenas = dezenas.group()
    listadezenas = [d.group() for d in re.finditer(r'\d{2}', dezenas)]
    return [concurso, data, cidade, listadezenas]

dados = concursoatual()
print(dados)


"""
    montante = re.findall(r'R\$[ .]+[\w.]+[,\w]+', texto)
    dataproximoconcurso = datas[1]
    premioestimado = montante[0]
    premioacumulado = montante[1]
    acumulado_megavirada = montante[2]
    arrecadacaototal = montante[-1]

    return [concurso.group(),
            dataconcursoatual,
            dataproximoconcurso,
            cidadesorteio.group(),
            dezenassorteadas.group(),
            premioestimado,
            premioacumulado,
            acumulado_megavirada,
            arrecadacaototal]
"""
