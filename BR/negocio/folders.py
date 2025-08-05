#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# print(f'importado! Módulo: {__name__}\tPacote: {__package__}')

import sys # Importa modulos do sistema
import os # Local (path) do sistema
import pathlib  # Local do diretório (pasta)
from contextlib import contextmanager

import shutil   # Endereços para apagar todos os arquivos da pasta


@contextmanager
def cd(newdir):
    # Mudar de diretório e retornar ao diretório original
    prevdir = os.getcwd()
    os.chdir(os.path.expanduser(newdir))
    # Diretório atual: Retorna ao diretório atual
    # print('>>> Local atual:', pathlib.Path().absolute())
    try:
        yield
    finally:
        os.chdir(prevdir)
        # Diretório atual: Retorna ao diretório atual
        # print('>>> Local atual:', pathlib.Path().absolute())


def del_previous_files(the_folder):
    folder = os.getcwd()+the_folder
    # print('folder:', folder)

    if not os.path.exists(folder):
        print(f'A pasta \"{folder}\" não existe!')
        # sys.exit(1)
        os.mkdir(folder)   # Cria diretorio
        print(f'A pasta \"{folder}\" foi criada!')
    else:
        with cd(folder):
            # Verifica se não há arquivo na pasta. Nem arquivo oculto
            if [f for f in os.listdir(folder) if not f.startswith('.')] == []:
                print('Ok. Sem arquivos na pasta {0:s}.'.format(the_folder))
            else:
                # dir = os.getcwd()
                for filename in os.listdir(folder):
                    file_path = os.path.join(folder, filename)
                    try:
                        if os.path.isfile(file_path) or os.path.islink(file_path):
                            os.unlink(file_path)
                        elif os.path.isdir(file_path):
                            shutil.rmtree(file_path)
                    except Exception as e:
                        print(f'Falha em deletar {filename}.')
                        print(f'Motivo: {e}.')
                # else:
                print('Todos os arquivos da pasta {0:s} foram eliminados.'
                      .format(str(the_folder)), end=' ')
                print("A pasta está limpa.")
