import unittest
import urllib.request
import json

URL_LIKES = "http://localhost:5003/likes"
URL_CURTIR = "http://localhost:5003/curtir"
URL_DESCURTIR = "http://localhost:5003/descurtir"
URL_LIKES_POR_FEED = "http://localhost:5003/likes_por_feed"
URL_CURTIU = "http://localhost:5003/curtiu"

class TesteLikes(unittest.TestCase):

    def acessar(self, url):
        resposta = urllib.request.urlopen(url)
        dados = resposta.read()

        return dados.decode("utf-8")

    def enviar(self, url, metodo):
        requisicao = urllib.request.Request(url, method=metodo)
        resposta = urllib.request.urlopen(requisicao)
        dados = resposta.read()

        return dados.decode("utf-8")

    def testar_01_likes_por_feed(self):
        dados = self.acessar(f"{URL_LIKES_POR_FEED}/1")
        resultado = json.loads(dados)

        self.assertEqual(resultado["curtidas"], 1)

    def testar_02_curtir_e_verificar_curtida(self):
        resposta_curtir = self.enviar(f"{URL_CURTIR}/iagobotelhoyt@gmail.com/2", "POST")
        resultado_curtir = json.loads(resposta_curtir)

        self.assertEqual(resultado_curtir["situacao"], "ok")

        dados = self.acessar(f"{URL_LIKES_POR_FEED}/2")
        resultado = json.loads(dados)

        self.assertEqual(resultado["curtidas"], 1)

        resposta_curtiu = self.enviar(f"{URL_CURTIU}/iagobotelhoyt@gmail.com/2", "GET")
        resultado_curtiu = json.loads(resposta_curtiu)

        self.assertEqual(resultado_curtiu["curtiu"], True)

    def testar_03_descurtir_e_verificar_curtida(self):
        resposta_descurtir = self.enviar(f"{URL_DESCURTIR}/iagobotelhoyt@gmail.com/1", "POST")
        resultado_descurtir = json.loads(resposta_descurtir)

        self.assertEqual(resultado_descurtir["situacao"], "ok")

        dados = self.acessar(f"{URL_LIKES_POR_FEED}/1")
        resultado = json.loads(dados)

        self.assertEqual(resultado["curtidas"], 0)

        resposta_curtiu = self.enviar(f"{URL_CURTIU}/iagobotelhoyt@gmail.com/1", "GET")
        resultado_curtiu = json.loads(resposta_curtiu)

        self.assertEqual(resultado_curtiu["curtiu"], False)