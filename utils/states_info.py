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
                "BR" : 214000000,   # 10
                "AC" : 869265,      # 12
                "AL" : 3322820,     # 27
                "AM" : 4080610,     # 13
                "AP" : 829494,      # 16
                "BA" : 14812600,    # 29
                "CE" : 9075650,     # 23
                "ES" : 3972390,     # 32
                "GO" : 9895860,     # 52
                "MA" : 7035060,     # 21
                "MG" : 21040700,    # 31
                "MS" : 2748020,     # 50
                "MT" : 3442000,     # 51
                "PA" : 8513500,     # 15
                "PB" : 3996500,     # 25
                "PE" : 9493270,     # 26
                "PI" : 3264530,     # 22
                "PR" : 11348900,    # 41
                "RJ" : 17160000,    # 33
                "RN" : 3479010,     # 24
                "RO" : 1757590,     # 11
                "RR" : 576568,      # 14
                "RS" : 11329600,    # 43
                "SC" : 7075490,     # 42
                "SE" : 2278310,     # 28
                "SP" : 45538900,    # 35
                "TO" : 1555230,     # 17
                }
    return states_pop.get(state_pop, '** Estado inválido **')
