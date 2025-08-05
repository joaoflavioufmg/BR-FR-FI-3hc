# -*- coding: utf-8 -*-
#!/usr/bin/env python3
# Diretório atual
import sys # Importa modulos do sistema
print('Vesão do python: ', sys.version) # Versao do python em uso
import pathlib  # Local do diretório (pasta)
# print('Local da pasta: ', pathlib.Path().absolute())
# Onde começa o script
# print('Local da pasta: ',pathlib.Path(__file__).parent.absolute())
import os # Local (path: caminho) do sistema
# print('Local do módulo: ', os.path)
# print('Locais mapeados: ', sys.path) # Local do pyhton e do arquivo

import numpy as np  # Estatísticas (np é um 'alias' para numpy)
import scipy.stats  # Estatísticas

###############################################################
# from pacote (pasta) import modulos (arquivos) # Customizados
from app import file_info
from app import run_optimizer
from app import demand_meet_graphics
from negocio import config
from negocio.oridest import OriDestAssignment
# from negocio.demand import SatisfyDemand
###############################################################

def run_post_optimization():

    assin_n1 = OriDestAssignment
    assin_n2 = OriDestAssignment
    assin_n3 = OriDestAssignment

    assin_n1("01-Atribuicao-Nivel-1.csv", "Nivel_1", config.state)
    assin_n2("02-Atribuicao-Nivel-2.csv", "Nivel_2", config.state)
    assin_n3("03-Atribuicao-Nivel-3.csv", "Nivel_3", config.state)

    
    demand_meet_graphics("04-Atend-Demanda-Nivel-1.csv",
                         "Nivel_1", config.state)

    demand_meet_graphics("05-Atend-Demanda-Nivel-2.csv",
                         "Nivel_2", config.state)

    demand_meet_graphics("06-Atend-Demanda-Nivel-3.csv",
                         "Nivel_3", config.state)

    # file_info()


if __name__ == '__main__':
    # global optimizer
    # global state

    run_optimizer(config.optimizer)
    run_post_optimization()

    