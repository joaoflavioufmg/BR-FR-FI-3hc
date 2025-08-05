#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# print(f'importado! Módulo: {__name__}\tPacote: {__package__}')

import sys # Importa modulos do sistema
import os # Local (path) do sistema
import pathlib  # Local do diretório (pasta)

import numpy as np  # Estatísticas (np é um 'alias' para numpy)
import scipy.stats  # Estatísticas

# Importando o módulo 'config' tem-se variáveis globais
# podendo serem usadas entre os módulos que as necessitam
from negocio import config
from negocio.graphics import make_flow_maps
from negocio.graphics import make_all_flow_maps
from negocio.graphics import make_fi_flow_map
from utils.states_info import states_mun,load_municipalities,states_pop

class OriDestAssignment:
    def __init__(self, file_name, level, state_mun):
        # global result_folder
        # global maps_folder
        self.result_folder = config.result_folder
        self.maps_folder = config.maps_folder
        self.map_br_folder = config.map_br_folder
        self.file_name = file_name
        self.level = level
        self.state_mun = states_mun(state_mun)

        # Carrega a lista de municípios do Brasil
        mun_list_dic = load_municipalities()

        # Imprime o dicionário do json filtrado por chaves (keys)
        # for mun_dic in mun_list_dic:
            # print(mun_dic) # Imprime cada dicionário do json
            # print(mun_dic['codigo']) # Filtra pelo código
            # print(str(mun_dic['codigo'])[:-1]) # Filtra pelo código

        # Verifica o nome do arquivo passado no parâmetro do objeto
        if os.path.isfile(self.result_folder + self.file_name) == False:
            raise ValueError("Arquivo não encontrado.")

        os.chdir(self.result_folder)
        # Diretório atual
        # print(pathlib.Path().absolute())

        # Leitura do arquivo excluindo a primeira linha
         # Atribuição de valores csv à variáveis
        with open(self.file_name,"r", encoding = "utf-8") as file:
            next(file)

            patient_dist = []
            patient_orig = []
            patient_dest = []
            patient_flow = []

            for line in file.readlines():
                # line.rstrip()
                # print(line.rstrip())
                items = line.rstrip().split(",")
                orig = {items[0]:items[1]}
                dest = {items[2]:items[3]}
                # dist = int(float(items[4]))
                dist = float(items[4])
                path = [orig, dest, dist]
                patient_dist.append(dist)
                # print(items)
                # print(path)
                # print()
                # print("Distâncias dos pacientes: ", patient_dist)

                # Visualização da estrutura do arquivo a ser gerado
                pat_orig = []
                pat_dest = []
                
                for mun_dic in mun_list_dic:
                    # print("str(mun_dic['codigo'])[:-1]: ", str(mun_dic['codigo'])[:-1])
                    # print("items[0]: ", items[0])
                    # if str(mun_dic['codigo'])[:-1] == items[0]:
                    if str(mun_dic['codigo'])[:] == items[0]:
                        pat_orig = [mun_dic['nome'], mun_dic['latitude'],\
                                        mun_dic['longitude']]
                        # print("pat_orig: ", pat_orig)
                        patient_orig.append(pat_orig)
                    # if str(mun_dic['codigo'])[:-1] == items[2]:
                    if str(mun_dic['codigo'])[:] == items[2]:
                        pat_dest = [mun_dic['nome'], mun_dic['latitude'],\
                                        mun_dic['longitude']] 
                        if pat_dest not in patient_dest: 
                            patient_dest.append(pat_dest)                       
                
                # print(patient_dest)
            # print(patient_orig)
                        # print(mun_dic['nome'],",", \
                        # mun_dic['latitude'], ",",
                        # mun_dic['longitude'])

        #         for mun_dic in mun_list_dic:
        #             if str(mun_dic['codigo'])[:-1] == items[0]:
        #                 patient_orig.append(list(mun_dic['nome'],\
        #                 mun_dic['latitude'], mun_dic['longitude']))
        #
        # print('patient_orig: ', patient_orig)


                # Visualização da estrutura do arquivo de fluxo a ser gerado
                pat_flow = []
                # List Comprehension
                # pat_flow = [(mun_dic['nome'], mun_dic['latitude'],
                #             mun_dic['longitude']) for \
                #             mun_dic in mun_list_dic \
                #             if str(mun_dic['codigo'])[:-1] == items[0]]
                #
                # pat_flow += [(mun_dic['nome'], mun_dic['latitude'],\
                #             mun_dic['longitude']) for \
                #             mun_dic in mun_list_dic \
                #             if str(mun_dic['codigo'])[:-1] == items[2]]

                # Loop For
                # for mun_dic in mun_list_dic:
                #     if str(mun_dic['codigo'])[:-1] == items[0]:
                #         pat_flow = [mun_dic['nome'], mun_dic['latitude'],\
                #                         mun_dic['longitude']]
                # for mun_dic in mun_list_dic:
                #     if str(mun_dic['codigo'])[:-1] == items[2]:
                #         pat_flow += [mun_dic['nome'], mun_dic['latitude'],\
                #                         mun_dic['longitude']]
                # print(pat_flow)
        # print(patient_flow)
        #             # print(mun_dic['nome'],",", \
        #             # mun_dic['latitude'], ",",
        #             # mun_dic['longitude'])

                pat_flow = [[mun_dic['latitude'],mun_dic['longitude']] for \
                            mun_dic in mun_list_dic \
                            # if str(mun_dic['codigo'])[:-1] == items[0]]
                            if str(mun_dic['codigo'])[:] == items[0]]

                pat_flow += [[mun_dic['latitude'],mun_dic['longitude']] for \
                            mun_dic in mun_list_dic \
                            # if str(mun_dic['codigo'])[:-1] == items[2]]
                            if str(mun_dic['codigo'])[:] == items[2]]
                patient_flow.append(pat_flow)

            # Impressão da lista de [Origem(lat/lon),Destino(lat/lon)]
            # print(patient_flow)


        #         for mun_dic in mun_list_dic:
        #             if str(mun_dic['codigo'])[:-1] == items[0]:
        #                 patient_flow.append(list(mun_dic['nome'],\
        #                 mun_dic['latitude'], mun_dic['longitude']))
        #
        # print('patient_flow: ', patient_flow)

        # Muda para Diretorio um nivel superior
        os.chdir('..')
        # Diretório atual: Retorna ao diretório atual
        # print('>>> Local atual:', pathlib.Path().absolute())

        os.chdir(self.maps_folder)
        # Diretório atual: Retorna ao diretório atual
        # print('>>> Local atual:', pathlib.Path().absolute())
        map_file = self.level + '.csv'
        map_flow_file = 'fluxo_' + level + '.csv'
        map_kernel_file = 'kernel_' + level + '.csv'

        # Arquivos de saída: Mapa de pontos de origem dos pacientes
        #################################################################
        # Abrir arquivo para escerver 'w' - write
        with open(map_file, 'w') as file_out:
            print('{0:s},{1:s},{2:s}'
                  .format('name','lat','lon'), end='', file = file_out)

        # Abrir arquivo anterior para adicionar texto 'a' - append
        with open(map_file, 'a') as file_out:
            for lista in range(len(patient_orig)):
                print('',file = file_out)
                for item in patient_orig[lista]:
                    print(item, end = ',', file = file_out)
        
        if self.level == "Nivel_3":
            # Abrir arquivo de destino para escerver 'w' - write
            with open('Nivel_4.csv', 'w') as file_out:
                print('{0:s},{1:s},{2:s}'
                    .format('name','lat','lon'), end='', file = file_out)

            # Abrir arquivo anterior para adicionar texto 'a' - append
            with open('Nivel_4.csv', 'a') as file_out:
                for lista in range(len(patient_dest)):
                    print('',file = file_out)
                    for item in patient_dest[lista]:
                        print(item, end = ',', file = file_out)

            

        # Para teste: Vericação de arquivo (de escrita) fechado
        # if file_out.closed: print('Ok! Arquivo de saída fechado')

        # Para teste: Vericação de arquivo (de leitura) fechado
        # if file.closed: print('Ok! Arquivo de leitura fechado.')

        # Arquivos de saída: Mapa de fluxo (origem, destino) dos pacientes
        #################################################################
        # Abrir arquivo para escerver 'w' - write
        with open(map_flow_file, 'w') as file_out:
            print('{0:s},{1:s},{2:s},{3:s}'
                  .format('lat_departure','lon_departure',
                          'lat_arrival','lon_arrival'),
                  end='', file = file_out)

        # Abrir arquivo anterior para adicionar texto 'a' - append
        # print("patient_flow: ", patient_flow)
        with open(map_flow_file, 'a') as file_out:
            for ind_lista_dupla in range(len(patient_flow)):
                print('',file = file_out)
                for lista in patient_flow[ind_lista_dupla]:
                    for item in lista:
                        print(item, end = ',', file = file_out)

        # Para teste: Vericação de arquivo (de escrita) fechado
        # if file_out.closed: print('Ok! Arquivo de saída fechado')

        # Para teste: Vericação de arquivo (de leitura) fechado
        # if file.closed: print('Ok! Arquivo de leitura fechado.')

        # Posicionamento de elementos nas listas de listas [[][]]
        # print('patient_flow: ', patient_flow)
        # print((len(patient_flow)))
        # print('patient_flow[0]: ', patient_flow[0])
        # print('patient_flow[1]: ', patient_flow[1])
        # print('patient_flow[0][0]: ', patient_flow[0][0])
        # print('patient_flow[0][1]: ', patient_flow[0][1])

        # Arquivos de saída: Mapa de kernel (destino) dos pacientes
        #################################################################
        # Abrir arquivo para escerver 'w' - write
        with open(map_kernel_file, 'w') as file_out:
            print('{0:s},{1:s}'.format('lon','lat'),
                  end='', file = file_out)

        # Abrir arquivo anterior para adicionar texto 'a' - append
        with open(map_kernel_file, 'a') as file_out:
            for ind_lista_dupla in range(len(patient_flow)):
                print('',file = file_out)
                for item in reversed(patient_flow[ind_lista_dupla][1]):
                    print(item, end = ',', file = file_out)

        # Para teste: Vericação de arquivo (de escrita) fechado
        # if file_out.closed: print('Ok! Arquivo de saída fechado')

        # Para teste: Vericação de arquivo (de leitura) fechado
        # if file.closed: print('Ok! Arquivo de leitura fechado.')

        # Calcula estatísticas
        # Calcula o intervalo de confiança (IC)
        confidence = 0.95
        n = len(patient_dist)
        # d_se: Erro Padrão da Mean
        d_se = scipy.stats.sem(patient_dist)
        h = d_se * scipy.stats.t.ppf((1 + confidence) / 2., n-1)
        # Intervalo de confiança: d_mean, d_mean-h, d_mean+h

        print()
        d_n    = n # Número de municípios atendidos
        d_max  = np.amax(patient_dist)
        d_min  = np.amin(patient_dist)
        d_mean = np.mean(patient_dist)
        d_med  = np.median(patient_dist)
        d_std  = np.std(patient_dist)
        d_vc   = np.std(patient_dist)/np.mean(patient_dist) if \
                 np.mean(patient_dist) > 0 else 0
        d_ci   = h

        linha = 78*'='
        print(linha)        
        print('Statistics of travel duration ', end='')
        print(f'by patients to services - {self.level}')
        print(linha)
        if self.level == "Nivel_1":
            print("Coverage (qty):{0:>6d} mun ({1:5.2f}%)."
                  .format(d_n, (d_n/int(self.state_mun))*100))
        else:
            print("Coverage (qty):{0:>6d} mun.".format(d_n))

        print("Maximum:\t{0:>6.2f} h.".format(d_max))
        print("Minimum:\t{0:>6.2f} h.".format(d_min))
        print("Mean:\t\t{0:>6.2f} h.".format(d_mean), end='')
        print(" [Between {0:5.2f} and {1:5.2f}] ({2:d}% conf. interval)".
              format(max(d_mean-h,0), d_mean+h, int(confidence*100)))
        print("Median:\t\t{0:>6.2f} h.".format(d_med))
        print("Std Deviation:\t{0:>6.2f} h.".format(d_std))
        print("Co. Variation:\t{0:>6.2f} h.".format(d_vc))
        print("Conf. Int(95%):\t{0:>6.2f} h.".format(d_ci))
        print(linha)
        print()

        # Arquivos de saída: Relatório de estatísticas de distâncias
        #################################################################
        # Verifica o nome do arquivo passado no parâmetro do objeto
        dist_stat_file = 'Estatisticas_de_deslocamento.txt'

        if os.path.isfile(dist_stat_file) == True:
            with open(dist_stat_file, 'a') as file_out:
                print('\n', file = file_out)
                print('{0:s}'.format(linha), file = file_out)
                print('{0:s}{1:s}'.format('Statistics of travel duration by patients to services - ', self.level), file = file_out)
                print('{0:s}'.format(linha), file = file_out)
                if self.level == "Nivel_1":
                    print("Coverage (qty):{0:>6d} mun ({1:5.2f}%).".format(d_n, (d_n/int(self.state_mun))*100), file = file_out)
                else:
                    print("Coverage (qty):{0:>6d} mun.".format(d_n), file = file_out)
                print("Maximum:\t\t{0:>6.2f} h.".format(d_max), file = file_out)
                print("Minimum:\t\t{0:>6.2f} h.".format(d_min), file = file_out)
                print("Mean:\t\t\t{0:>6.2f} h. [Between {1:5.2f} and {2:5.2f}] ({3:2.0f}% conf. interval)".format(d_mean, max(d_mean-h, 0), d_mean+h, int(confidence*100)), file = file_out)
                print("Median:\t\t\t{0:>6.2f} h.".format(d_med), file = file_out)
                print("Std Deviation:\t{0:>6.2f} h.".format(d_std), file = file_out)
                print("Co. Variation:\t{0:>6.2f} h.".format(d_vc), file = file_out)
                print("Conf. Int(95%):\t{0:>6.2f} h.".format(d_ci), file = file_out)
                print('{0:s}'.format(linha), file = file_out)
        else:
            print(f'>>> Gerando relatório {dist_stat_file}...')
            # Abrir arquivo para escerver 'w' - write
            with open(dist_stat_file, 'w') as file_out:
                print('{0:s}'.format(linha), file = file_out)
                print('{0:s}{1:s}'.format('Statistics of travel duration by patients to services - ', self.level), file = file_out)
                print('{0:s}'.format(linha), file = file_out)
                if self.level == "Nivel_1":
                    print("Coverage (qty):{0:>6d} mun ({1:5.2f}%).".format(d_n, (d_n/int(self.state_mun))*100), file = file_out)
                else:
                    print("Coverage (qty):{0:>6d} mun.".format(d_n), file = file_out)
                print("Maximum:\t\t{0:>6.2f} h.".format(d_max), file = file_out)
                print("Minimum:\t\t{0:>6.2f} h.".format(d_min), file = file_out)
                print("Mean:\t\t\t{0:>6.2f} h. [Between {1:5.2f} and {2:5.2f}] ({3:2.0f}% conf. interval)".format(d_mean, max(d_mean-h, 0), d_mean+h, int(confidence*100)), file = file_out)
                print("Median:\t\t\t{0:>6.2f} h.".format(d_med), file = file_out)
                print("Std Deviation:\t{0:>6.2f} h.".format(d_std), file = file_out)
                print("Co. Variation:\t{0:>6.2f} h.".format(d_vc), file = file_out)
                print("Conf. Int(95%):\t{0:>6.2f} h.".format(d_ci), file = file_out)
                print('{0:s}'.format(linha), file = file_out)


        # COMENTAR PARA GERAR RELATORIOS APENAS
        # ################################################################
        make_flow_maps(self.level)  # Gera o mapa após as estatísticas        
        # ################################################################

        # Muda para Diretorio um nivel superior
        os.chdir("..")

        # Diretório atual: Retorna ao diretório atual
        # print('>>> Local atual:', pathlib.Path().absolute())

        # Verifica o nome do arquivo passado no parâmetro do objeto
        if os.path.isfile(self.maps_folder + 'kernel_Nivel_3.csv') == True:
            # raise ValueError("Arquivo não encontrado.")
            os.chdir(self.maps_folder)

            # RETIRAR COMENTARIO PARA GERAR O MAPA LOCAL
            # ################################################################
            make_all_flow_maps()  # Gera o mapa após as estatísticas
            # ################################################################
            # Muda para Diretorio um nivel superior
            os.chdir("..")
        

            # MAPA DA FINLANDIA
            if os.path.isfile(self.map_br_folder + 'FI_Nivel_3.csv') == True:
                # raise ValueError("Arquivo não encontrado.")
                os.chdir(self.map_br_folder)
                # # RETIRAR COMENTARIO PARA GERAR UM MAPA GERAL
                # # ################################################################
                # make_fi_flow_map()  # Gera o mapa após as estatísticas
                # # ################################################################
                # Muda para Diretorio um nivel superior
                os.chdir("..")
