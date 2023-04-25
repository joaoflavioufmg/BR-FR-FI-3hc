#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# print(f'importado! Módulo: {__name__}\tPacote: {__package__}')

import json # Dados json para Dicionários python

# Retorna o código dos estados brasileiros selecionado por sigla.
def states_codes(state):
    states_cod = {# Estado : Cód
                "BR" : 10,
                "AC" : 12,
                "AL" : 27,
                "AM" : 13,
                "AP" : 16,
                "BA" : 29,
                "CE" : 23,
                "ES" : 32,
                "GO" : 52,
                "MA" : 21,
                "MG" : 31,
                "MS" : 50,
                "MT" : 51,
                "PA" : 15,
                "PB" : 25,
                "PE" : 26,
                "PI" : 22,
                "PR" : 41,
                "RJ" : 33,
                "RN" : 24,
                "RO" : 11,
                "RR" : 14,
                "RS" : 43,
                "SC" : 42,
                "SE" : 28,
                "SP" : 35,
                "TO" : 17,
                }
    return states_cod.get(state, '** Estado inválido **')

# Retorna o número de municípios por estado selecionado por sigla.
def states_mun(state_mun):
    states_mun = {
                "BR" : 5570,
                "AC" : 22,
                "AL" : 102,
                "AM" : 62,
                "AP" : 16,
                "BA" : 417,
                "CE" : 184,
                "ES" : 78,
                "GO" : 247,
                "MA" : 217,
                "MG" : 853,
                "MS" : 79,
                "MT" : 141,
                "PA" : 144,
                "PB" : 223,
                "PE" : 184,
                "PI" : 224,
                "PR" : 399,
                "RJ" : 92,
                "RN" : 167,
                "RO" : 52,
                "RR" : 15,
                "RS" : 497,
                "SC" : 295,
                "SE" : 75,
                "SP" : 645,
                "TO" : 139,
                }
    return states_mun.get(state_mun, '** Estado inválido **')

# Retorna dicionário c/ dados dos múnicípio do Brasil: "codigo_ibge",
# "nome", "latitude", "longitude", "eh capital?", "codigo_uf"
def load_municipalities():
    # Carrega a lista de municípios do Brasil
    with open('municipios.json', 'r', encoding='utf-8-sig') as m:
        mun_list_dic = json.load(m)
    return mun_list_dic

# Retorna a população (em 2018) de cada estado selecionado por sigla.
def states_pop(state_pop):
    states_pop = {# Estado : Pop    : Cód
                "BR" 	:	223852116, # 10
                "AC" 	:	937545	, #	12
                "AL" 	:	3583821	, #	27
                "AM" 	:	4401133	, #	13
                "AP" 	:	894649	, #	16
                "BA" 	:	15976118, #	29
                "CE" 	:	9788522	, #	23
                "ES" 	:	4284409	, #	32
                "GO" 	:	10673164, #	52
                "MA" 	:	7587639	, #	21
                "MG" 	:	22693346, #	31
                "MS" 	:	2963874	, #	50
                "MT" 	:	3712359	, #	51
                "PA" 	:	9182212	, #	15
                "PB" 	:	4310413	, #	25
                "PE" 	:	10238940, #	26
                "PI" 	:	3520952	, #	22
                "PR" 	:	12240362, #	41
                "RJ" 	:	18507837, #	33
                "RN" 	:	3752280	, #	24
                "RO" 	:	1895642	, #	11
                "RR" 	:	621857	, #	14
                "RS" 	:	12219514, #	43
                "SC" 	:	7631251	, #	42
                "SE" 	:	2457262	, #	28
                "SP" 	:	49115904, #	35
                "TO" 	:	1677386	, #	17
                }
    return states_pop.get(state_pop, '** Estado inválido **')
