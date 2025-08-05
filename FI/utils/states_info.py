#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# print(f'importado! Módulo: {__name__}\tPacote: {__package__}')

import json # Dados json para Dicionários python

# Retorna o código dos estados brasileiros selecionado por sigla.
def states_codes(state):
    states_cod = {# Estado : Cód
                "FI"  : 0, 
                "01"  : 1,
                "02"  : 2,
                "03"  : 3,
                "04"  : 4,
                "05"  : 5,
                "06"  : 6,
                "07" : 7,
                "08"  : 8,
                "09"  : 9,
                "10"  : 10,
                "11"  : 11,
                "12"  : 12,
                "13"  : 13,
                "14"  : 14,
                "15"  : 15,
                "16"  : 16,
                "17"  : 17,
                "18"  : 18,
                "19"  : 19,
                }
    return states_cod.get(state, '** Invalid Region **')

# Retorna o número de municípios por estado selecionado por sigla.
def states_mun(state_mun):
    states_mun = {
                "FI"  : 309,
                "01" : 16,
                "02" : 9,
                "03" : 17,
                "04" : 14,
                "05" : 9,
                "06" : 11,
                "07" : 8,
                "08" : 23,
                "09" : 6,
                "10" : 21,
                "11" : 22,
                "12" : 15,
                "13" : 12,
                "14" : 29,
                "15" : 18,
                "16" : 10,
                "17" : 16,
                "18" : 26,
                "19" : 27,
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
                "FI"  : 5598821,
                "01" : 32197,
                "02" : 119591,
                "03" : 178914,
                "04" : 124860,
                "05" : 67751,
                "06" : 164397,
                "07" : 65348,
                "08" : 271186,
                "09" : 148033,
                "10" : 169391,
                "11" : 544900,
                "12" : 177701,
                "13" : 152697,
                "14" : 416050,
                "15" : 235851,
                "16" : 199927,
                "17" : 201574,
                "18" : 1836816,
                "19" : 491637,
                }
    return states_pop.get(state_pop, '** Invalid Region **')
