#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# print(f'importado! Módulo: {__name__}\tPacote: {__package__}')

import json # Dados json para Dicionários python

# Retorna o código dos estados brasileiros selecionado por sigla.
def states_codes(state):
    states_cod = {# Estado : Cód 
                "GE"  : 1,
                "NA"  : 2,
                "AR"  : 3,
                "BF"  : 4,
                "BR"  : 5,
                "VL"  : 6,
                "CO" : 7,
                "IF"  : 8,
                "OC"  : 9,
                "NO"  : 10,
                "HF"  : 11,
                "PL"  : 12,
                "CD"  : 13,
                }
    return states_cod.get(state, '** Invalid Region **')

# Retorna o número de municípios por estado selecionado por sigla.
def states_mun(state_mun):
    states_mun = {
                "GE"  : 935,
                "NA"  : 1075,
                "AR"  : 1408,
                "BF"  : 472,
                "BR"  : 737,
                "VL"  : 490,
                "CO"  : 48,
                "IF"  : 689,
                "OC"  : 907,
                "NO"  : 579,
                "HF"  : 950,
                "PL"  : 748,
                "CD"  : 436,
                }
    return states_mun.get(state_mun, '** Invalid Region **')

# Retorna dicionário c/ dados dos múnicípio do Brasil: "codigo_ibge",
# "nome", "latitude", "longitude", "eh capital?", "codigo_uf"
def load_municipalities():
    # Carrega a lista de municípios do Brasil
    with open('municipios.json', 'r', encoding='utf-8-sig') as m:
        mun_list_dic = json.load(m)
    # print("mun_list_dic: ", mun_list_dic)
    return mun_list_dic


# Retorna a população (em 2018) de cada estado selecionado por sigla.
def states_pop(state_pop):
    states_pop = {# Estado : Pop    : Cód
                "GE" : 4212491,
                "NA" : 4592959,
                "AR" : 6766166,
                "BF" : 1798735,
                "BR" : 3005819,
                "VL" : 1953179,
                "CO" : 255891,
                "IF" : 11406876,
                "OC" : 4745472,
                "NO" : 2328831,
                "HF" : 4905571,
                "PL" : 3389089,
                "CD" : 4837426,
                }
    return states_pop.get(state_pop, '** Invalid Region **')
