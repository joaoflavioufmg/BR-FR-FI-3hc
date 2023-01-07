#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# print(f'importado! Módulo: {__name__}\tPacote: {__package__}')

# Importando o módulo 'config' tem-se variáveis globais
# podendo serem usadas entre os módulos que as necessitam
import sys  # Importa modulos do sistema
import os  # Local (path) do sistema
import time  # para sair do sistema
import pathlib  # Local do diretório (pasta)
from negocio import config
from negocio.folders import cd, del_previous_files
from utils.states_info import states_codes

# Bom material (https://realpython.com/python-exceptions/)
# https://docs.python.org/3/faq/programming.html#how-do-i-
# share-global-variables-across-modules

def run_Glpk():
    # GLPK - Gnu Linear Programming Kit

    # global state
    cod = states_codes(config.state)

    solver = 'glpsol'
    model = '-m hc_glpk.mod'
    data = '-d hc.dat -d ' + str(cod) + '_dados.dat -d '\
            + str(cod) + '_dist_dur.txt'
    options = '--cuts --mipgap 0.01 --tmlim 7200 --log hc_log.log'
    call_Glpk = solver + ' ' + model + ' ' + data + ' ' + options
    # print(call_Glpk)
    return call_Glpk
# print(run_Glpk())

def run_Glpk2():
    # GLPK - Gnu Linear Programming Kit

    # global state
    cod = states_codes(config.state)

    solver = 'glpsol'
    model = '-m hc_glpk2.mod'
    data = '-d hc.dat -d pop_res.dat -d ' + str(cod) + '_dados.dat -d '\
            + str(cod) + '_dist_dur.txt'
    options = '--cuts --mipgap 0.01 --tmlim 7200 --log hc_log.log'
    call_Glpk = solver + ' ' + model + ' ' + data + ' ' + options
    # print(call_Glpk)
    return call_Glpk

def run_Ampl():
    # AMPL - Algebraic Mathematical Programming Language

    # global state
    cod = states_codes(config.state)

    solver = 'ampl'
    model = 'hc_ampl.mod'
    data = 'hc.dat ' + str(cod) + '_dados.dat ' \
            + str(cod) + '_dist_dur.txt'
    script = 'hc.run'
    call_Ampl = solver + ' ' + model + ' ' + data + ' ' + script    
    # print(call_Ampl)
    return call_Ampl
# print(run_Ampl())

def run_solver(solver):

    # Elimina os arquivos de rodadas anteriores, se houver.
    del_previous_files('./Resultado/')
    del_previous_files('./Mapas/')

    if solver == "AMPL":
        try:
            call_solver = run_Ampl()
            run(call_solver, solver)
        except Exception as e:
            raise
    else:
        solver = "GLPK"
        try:
            call_solver = run_Glpk()
            call_solver2 = run_Glpk2()
            run(call_solver, solver)
            run(call_solver2, solver)
        except Exception as e:
            raise


def run(call_the_solver, the_solver, folder='./Resultado/'):
    # Se houver erro, a variável global 'Erro_de_otimizacao'
    # deverá ser alterada no escopo global (por isso 'global')
    # para True

    # global Erro_de_otimizacao # <<< Alterar variável de escopo global

    try:
        print(f'chamando o {the_solver}...')
        os.system(call_the_solver)
    except:
        config.Erro_de_otimizacao = True
        print(f'Erro na execução do {the_solver}.')
    else:
        if os.path.isfile(folder + '06-Atend-Demanda-Nivel-3.csv'):
            print("Arquivos de resultado gerados.")
        else:
            config.Erro_de_otimizacao = True
            print(f'Erro interno no {the_solver}.', end=' ')
            print('Não gerou arquivos de resultado.')


def run_optimizer(optimizer):
    # global result_folder
    # global Erro_de_otimizacao
    # print('optimizer: ', optimizer)
    # print('run_optimizer / Erro_de_otimizacao: ', config.Erro_de_otimizacao)
    #####################################################################
    if    optimizer == "AMPL": solver = "AMPL"
    elif  optimizer == "GLPK": solver = "GLPK"
    else:
        print("Erro! Defina um solver (AMPL ou GLPK)")
        sys.exit(1)

    try:
        run_solver(solver)
    except Exception as e:
        print(f'Erro na execução do {solver}.')
        print(f'Motivo: {e}')
    # except:
        # print(f'Erro na execução do {solver}.')
    finally:
        # print("Erro_de_otimizacao:", Erro_de_otimizacao)
        if config.Erro_de_otimizacao:
            if optimizer == "AMPL": solver = "GLPK"
            else: solver = "AMPL"
            try:
                run_solver(solver)
                config.Erro_de_otimizacao = False
                if config.Erro_de_otimizacao is False:
                    print("Calculando estatísticas do resultado...")
                else:
                    print(f'Erro na execução do {solver} também.')
                    sys.exit(1)
            except Exception as e:
                print(f'Erro na execução do {solver} também.')
                print(f'Motivo: {e}')
                sys.exit(1)
        elif config.Erro_de_otimizacao:
            sys.exit(1)
        else:
            # sys.exit(1)
            print(">>> Calculando estatísticas do resultado...")
    #####################################################################

    #######################################################################
    # Aguarda todos os arquivos serem gerados para calcular as estatísticas
    t = 4 # seconds
    while True:
        # if os.path.exists(path) # Se existe a pasta 'ou' arquivo
        if os.path.isfile(config.result_folder + '06-Atend-Demanda-Nivel-3.csv'):
            break
        else:
            time.sleep(t)
            t -= 1
            print(f"Saindo em {t} segundos...")
            if t == 1:
                print("Fim.")
                sys.exit(1)
