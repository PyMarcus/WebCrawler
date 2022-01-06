import os
import time
from getpass import getuser
from shutil import move
from urllib.request import urlretrieve
import requests
from bs4 import BeautifulSoup
import re


class Crawler:
    def __init__(self, site):
        self.__site = site

    @property
    def site(self):
        return self.__site

    def scraping(self):
        print("Iniciando...    OK")
        time.sleep(1)
        print("Mapeando o site...    OK")
        time.sleep(1)
        print("Identificando tags alvo...   OK")
        time.sleep(1)
        print("Aguarde...")
        regex = re.compile("<p><strong>Codigo Ref.:</strong> (.+?)<\/p>")  # para filtrar da tag
        url_req = requests.get(self.__site)
        bs = BeautifulSoup(url_req.content, 'html.parser')
        abas_produtos = bs.find_all("li", {"id": "produtos"})
        mini_links = []
        for semi_links in abas_produtos:
            lista_semi_links = semi_links.find_all_next("a", {"class": "subMenuItem"})
            for tags in lista_semi_links:
                valores = str(tags).split()
                if valores[2].split("=")[1] not in mini_links:
                    mini_links.append(valores[2].split("=")[1])
        codigos: list = []
        imagens: list = []
        contador = 0
        f = set()
        for i in mini_links:
            site = "https://www.zapgrafica.com.br/" + i.replace('"', "")
            new_req = requests.get(site)
            bs1 = BeautifulSoup(new_req.content, 'html.parser')
            time.sleep(1)
            valor1 = bs1.find_all("div", {"class": "box-info-servico"})
            valor2 = bs1.find_all("img", {"data-src": "holder.js/160x180"})
            for lista in valor1:
                t = str(lista)
                l = regex.search(t)
                valor = l
                codigos.append(valor.group(1))  # valor.group(1)

            for lista in valor2:
                contador += 1
                item = str(str(lista).split()[5]).split("=")[1].replace('"', "")
                if item:
                    imagens.append(item)
            print("Baixando itens-----OK")

        dicionario_img_cod: dict = dict(zip(codigos, imagens))
        usuario: str = getuser()
        if "ImagesZap" not in os.listdir(f"C:\\Users\\{usuario}\\"):
            os.mkdir(f"C:\\Users\\{usuario}\\ImagesZap\\")
            time.sleep(1)
            for k, v in dicionario_img_cod.items():
                if v not in os.listdir(f"C:\\Users\\{usuario}\\ImagesZap\\"):
                    urlretrieve(v, f"{str(k)}.jpg")
                    move(f"{str(k)}.jpg", f"C:\\Users\\{usuario}\\ImagesZap\\")
        else:
            for k, v in dicionario_img_cod.items():
                if v not in os.listdir(f"C:\\Users\\{usuario}\\ImagesZap\\"):
                    urlretrieve(v, f"{str(k)}.jpg")
                    move(f"{str(k)}.jpg", f"C:\\Users\\{usuario}\\ImagesZap\\")

        print("Concluido identificação de imagens e códigos....")
        print(f"Itens encontrados: {len(codigos)}")
        time.sleep(1)

        print("Terminado!")


if __name__ == '__main__':
    webcrawler = Crawler('https://www.zapgrafica.com.br/loja/home')
    webcrawler.scraping()
