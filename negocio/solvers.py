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

def run_Highs():
    # Highs Solver

    # global state
    cod = states_codes(config.state)

    def create_highs_options_file(cod, filename="hc_highs.opt"):
        """Create HiGHS options file with correct syntax"""
        options_content = f"""mip_rel_gap=0.01
primal_feasibility_tolerance=1e-9
dual_feasibility_tolerance=1e-9
time_limit=300
write_solution_style=2
solution_file=hc_highs.sol
log_file = Resultado/log_highs_{cod}.log"""
        
        with open(filename, 'w') as f:
            f.write(options_content)
        
        return filename
    
    create_highs_options_file(cod)

    solver1 = 'glpsol'
    model1 = '-m hc_glpk.mod'
    data1 = '-d hc.dat -d ' + str(cod) + '_dados.dat -d '\
            + str(cod) + '_dist_dur.txt'
    options1 = '--wmps hc_glpk.mps --check'
    
    solver2 = 'highs'
    model2 = '--model_file hc_glpk.mps'    
    options2 = '--options_file hc_highs.opt'
    
    solver3 = 'glpsol'
    model3 = '-m hc_glpk.mod'
    data3 = '-d hc.dat -d ' + str(cod) + '_dados.dat -d '\
            + str(cod) + '_dist_dur.txt'
    options3 = '-r hc_highs.sol'

    # Create the .bat file content
    bat_content = f"""@echo off
    REM Batch file for running optimization solvers
    REM State code: {cod}

    echo Running GLPSOL to generate MPS file...
    {solver1} {model1} {data1} {options1}

    echo Running HiGHS solver...
    {solver2} {model2} {options2}

    echo Running GLPSOL with HiGHS solution...
    {solver3} {model3} {data3} {options3}

    echo All solver commands completed.
    pause
    """

    # Write to .bat file
    output_filename="hc_highs.bat"
    try:
        with open(output_filename, 'w', encoding='utf-8') as bat_file:
            bat_file.write(bat_content)
        print(f"Successfully created {output_filename}")
        # return True
        # print(call_Highs)    
        return output_filename
    except Exception as e:
        print(f"Error creating .bat file: {e}")
        return False    
# print(run_Highs())

def run_Glpk():
    # GLPK - Gnu Linear Programming Kit

    # global state
    cod = states_codes(config.state)

    solver = 'glpsol'
    # model = '-m hc_glpk1.mod'
    model = '-m hc_glpk.mod'
    data = '-d hc.dat -d ' + str(cod) + '_dados.dat -d '\
            + str(cod) + '_dist_dur.txt'
    options = '--cuts --mipgap 0.01 --tmlim 7200 --log '\
            './Resultado/' + 'log_glpk_' + str(cod) + '.log'
    # --pcost (para instancias dificeis)
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
    elif solver == "Highs":
        try:
            call_solver = run_Highs()
            run(call_solver, solver)
        except Exception as e:
            raise
    else:
        solver = "GLPK"
        try:
            call_solver = run_Glpk()
            # call_solver2 = run_Glpk2()
            run(call_solver, solver)
            # run(call_solver2, solver)
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
    elif  optimizer == "Highs": solver = "Highs"
    elif  optimizer == "GLPK": solver = "GLPK"
    else:
        print("Erro! Defina um solver (AMPL, Highs ou GLPK)")
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
            if optimizer == "AMPL": solver = "Highs"
            elif optimizer == "Highs": solver = "GLPK"
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
