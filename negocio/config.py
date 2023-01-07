#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Escolha do otimizador (AMPL ou GLPK)
############################################################
optimizer = "GLPK"
# optimizer = "AMPL"
############################################################
state = "BA"
############################################################
# "AC", "AL", "AM", "AP", "BA", "CE", "ES", "GO", "MA",
# "MG", "MS", "MT", "PA", "PB", "PE", "PI", "PR", "RJ",
# "RN", "RO", "RR", "RS", "SC", "SE", "SP", "TO", "BR"
############################################################

# Variáveis globais precisam ser importadas no módulo main
# para serem usadas nos outros módulos em seguida
# print(f'importado! Módulo: {__name__}\tPacote: {__package__}')

# Não deve ser alterado (pois este nome está
# implementado até nos modelos de otimização)

result_folder = './Resultado/'    # <<< Não alterar!!!
maps_folder = './Mapas/'
map_br_folder = './MapaBr/'

# Variável 'Erro_de_otimizacao' tem escopo global
# Para ser alterada dentro de funções, as variáveis precisam
# ter o mesmo nome 'Erro_de_otimizacao' com a declaração
# 'global Erro_de_otimizacao'

Erro_de_otimizacao = False
