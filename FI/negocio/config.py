#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Escolha do otimizador (Highs, AMPL ou GLPK)
############################################################
optimizer = "Highs"
# optimizer = "GLPK"
# optimizer = "AMPL"
############################################################
state = "FI" # Regions
############################################################
# "01", "02", "03", "04", "05", "06", "07", 
# "08", "09", "10", "11", "12", "13", "14",
# "15", "16", "17", "18", "19", "FI"
############################################################

# Variáveis globais precisam ser importadas no módulo main
# para serem usadas nos outros módulos em seguida
# print(f'importado! Módulo: {__name__}\tPacote: {__package__}')

# Não deve ser alterado (pois este nome está
# implementado até nos modelos de otimização)

result_folder = './Resultado/'    # <<< Não alterar!!!
maps_folder = './Mapas/'
map_br_folder = './MapaFi/'

# Variável 'Erro_de_otimizacao' tem escopo global
# Para ser alterada dentro de funções, as variáveis precisam
# ter o mesmo nome 'Erro_de_otimizacao' com a declaração
# 'global Erro_de_otimizacao'

Erro_de_otimizacao = False
