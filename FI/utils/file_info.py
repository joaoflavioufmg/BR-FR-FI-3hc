#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# print(f'importado! Módulo: {__name__}\tPacote: {__package__}')

import sys # Importa modulos do sistema
import os # Local (path) do sistema
import pathlib  # Local do diretório (pasta)
import time     # Para informações sobre o arquivo

def file_info():
    linha = 95*'='
    print("Informações do arquivo:")
    print(linha)
    nome = sys.argv[0]
    print("Nome: %s" % nome)
    print("Tamanho: %d" % os.path.getsize(nome))
    print("Criado: %s" % time.ctime(os.path.getctime(nome)))
    print("Modificado: %s" % time.ctime(os.path.getmtime(nome)))
    print("Acessado: %s" % time.ctime(os.path.getatime(nome)))
    print(linha)
