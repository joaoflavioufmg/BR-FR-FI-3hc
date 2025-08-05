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
from utils.states_info import states_pop


class SatisfyDemand:
    def __init__(self, file_name, level, state_pop):
        # global result_folder
        self.result_folder = config.result_folder
        self.file_name = file_name
        self.level = level
        self.state_pop = states_pop(state_pop)

        # Verifica de argumento do objeto (arquivo de entrada) está ok
        if os.path.isfile(self.result_folder + self.file_name) == False:
            raise ValueError("Arquivo não encontrado.")

        os.chdir(self.result_folder)
        # Diretório atual
        # print(pathlib.Path().absolute())

        # Leitura do arquivo excluindo a primeira linha
        # Atribuição de valores csv à variáveis
        municipios		=[]
        pop_atendida    =[]
        physicians		=[]
        nurses		    =[]
        other_cadres	=[]
        community_based	=[]
        beds		    =[]
        ct_scanners		=[]
        mri_units	    =[]
        mammography		=[]
        radiotherapy	=[]
        # oftalmologia	=[]
        # otorrino		=[]
        # dermatologia	=[]
        # pneumologia		=[]
        # reumatologia	=[]
        # urologia	    =[]
        # ortopedia	    =[]
        ##########################################################
        self.municipios = municipios
        self.pop_atendida = pop_atendida
        self.physicians = physicians
        self.nurses = nurses
        self.other_cadres = other_cadres
        self.community_based = community_based
        self.beds = beds
        self.ct_scanners = ct_scanners
        self.mri_units = mri_units
        self.mammography = mammography
        self.radiotherapy = radiotherapy
        # self.oftalmologia = oftalmologia
        # self.otorrino = otorrino
        # self.dermatologia = dermatologia
        # self.pneumologia = pneumologia
        # self.reumatologia = reumatologia
        # self.urologia = urologia
        # self.ortopedia = ortopedia
        ##########################################################

        with open(self.file_name,"r", encoding = "utf-8") as file:
            next(file)

            for line in file.readlines():
                # line.rstrip()
                # print(line.rstrip())
                items = line.replace('"','').rstrip().split(",")
                lev = items[0]           # level
                cod = items[1]           # level
                mun = str(items[2])
                pop = {mun : items[3]}   # população served
                phy = {mun : items[4]}   # physicians
                nur = {mun : items[5]}   # nurses
                oca = {mun : items[6]}   # other_cadres
                cba = {mun : items[7]}   # community_based
                bed = {mun : items[8]}   # beds
                cts = {mun : items[9]}   # ct_scanners
                mri = {mun : items[10]}   # mri_units
                mam = {mun : items[11]}   # mammography
                rat = {mun : items[12]}   # radiotherapy
                # oft = {mun : items[13]}  # oftalmologia
                # oto = {mun : items[14]}  # otorrino
                # der = {mun : items[15]}  # dermatologia
                # pne = {mun : items[16]}  # pneumologia
                # reu = {mun : items[17]}  # reumatologia
                # uro = {mun : items[18]}  # urologia
                # ort = {mun : items[19]}  # ortopedia

                # print(items)

                demand_met = np.array([mun, pop[mun], 
                              phy[mun], nur[mun], oca[mun],
                              cba[mun], bed[mun], cts[mun], 
                              mri[mun], mam[mun], rat[mun]
                            #   , 
                            #   ort[mun], oto[mun], der[mun], 
                            #   pne[mun], reu[mun],  uro[mun],
                            #   oft[mun]
                              ])

                # print(demand_met)

                self.municipios.append(mun)
                self.pop_atendida.append(int(float(pop[mun])))
                self.physicians.append(float(phy[mun]))
                self.nurses.append(float(nur[mun]))
                self.other_cadres.append(float(oca[mun]))
                self.community_based.append(float(cba[mun]))
                self.beds.append(float(bed[mun]))
                self.ct_scanners.append(float(cts[mun]))
                self.mri_units.append(float(mri[mun]))
                self.mammography.append(float(mam[mun]))
                self.radiotherapy.append(float(rat[mun]))
                # self.oftalmologia.append(float(oft[mun]))
                # self.otorrino.append(float(oto[mun]))
                # self.dermatologia.append(float(der[mun]))
                # self.pneumologia.append(float(pne[mun]))
                # self.reumatologia.append(float(reu[mun]))
                # self.urologia.append(float(uro[mun]))
                # self.ortopedia.append(float(ort[mun]))

            # print('>>> self.urologia:', sum(self.urologia))
            # print(self.municipios)
            # print(len(self.municipios))
            # print(sum(self.pop_atendida))
            # print()

        # Para teste: Vericação de arquivo
        # if file.closed: print('Arquivo já fechado.')
        print()

        # Calcula estatísticas
        linha = 78*'='
        print(linha)
        print('Demand meet statistics ', end='')
        print(f' - {self.level}')
        print(linha)
        if self.level == "Nivel_1":
            print("Pop served:\t\t{0:>6d} ({1:5.2f}%)."
                  .format(sum(self.pop_atendida),(sum(self.pop_atendida)/int(self.state_pop))*100))

        d_n    = len(self.municipios) # Número de municípios que fazem o atendimento
        print("Municipalities (hub):\t{0:>8d} mun.".format(d_n))
        print(linha)

        d_phy = dict(zip(municipios, physicians))
        d_nur = dict(zip(municipios, nurses))
        d_oca = dict(zip(municipios, other_cadres))
        d_cba = dict(zip(municipios, community_based))
        d_bed = dict(zip(municipios, beds))
        d_cts = dict(zip(municipios, ct_scanners))
        d_mri = dict(zip(municipios, mri_units))
        d_mam = dict(zip(municipios, mammography))
        d_rat = dict(zip(municipios, radiotherapy))
        # d_oft = dict(zip(municipios, oftalmologia))
        # d_oto = dict(zip(municipios, otorrino))
        # d_der = dict(zip(municipios, dermatologia))
        # d_pne = dict(zip(municipios, pneumologia))
        # d_reu = dict(zip(municipios, reumatologia))
        # d_uro = dict(zip(municipios, urologia))
        # d_ort = dict(zip(municipios, ortopedia))

        especialidades = {
                            'Physicians': d_phy,
                            'Nurses': d_nur,    
                            'OtherCadres': d_oca, 
                            'CommunityBased': d_cba, 
                            'Beds': d_bed,  
                            'CTScanner': d_cts,
                            'MRIUnit': d_mri, 
                            'Mammography': d_mam, 
                            'Radiotherapy': d_rat, 
                            # 'Oftalmologia': d_oft,
                            # 'Otorrino': d_oto,
                            # 'Dermatologia': d_der,
                            # 'Pneumologia': d_pne,
                            # 'Reumatologia': d_reu,
                            # 'Urologia': d_uro,
                            # 'Ortopedia': d_ort,
        }

        self.especialidades = especialidades

        # Listas e Dicionários de listas.
        # print(ginecologia)
        # print(especialidades['Angiologia'])
        # print(especialidades['Angiologia'].values())
        # print(list(especialidades['Angiologia'].values()))
        # print(list(especialidades['Angiologia'].keys())
        #       [list(especialidades['Angiologia'].values()).index(1.95)])

        for nome in especialidades:
            if sum(especialidades[nome].values()) > 0:
                print("Resource:\t\t{0:s}\t\t[FTE or unit (equipment)]"
                      .format(nome))
                print(linha)
                # Transforma o dicionário em lista de valores
                d_max  = np.amax(list(especialidades[nome].values()))
                d_min  = np.amin(list(especialidades[nome].values()))
                d_mean = np.mean(list(especialidades[nome].values()))
                d_med  = np.median(list(especialidades[nome].values()))

                print("Minimum:\t\t{0:>6.2f} ({1:s})."
                      .format(d_min, list(especialidades[nome].keys())
                              [list(especialidades[nome].values()).index(d_min)]))
                print("Mean:\t\t\t{0:>6.2f}".format(d_mean))
                print("Median:\t\t\t{0:>6.2f}".format(d_med))
                print("Maximum:\t\t{0:>6.2f} ({1:s})."
                      .format(d_max, list(especialidades[nome].keys())
                              [list(especialidades[nome].values()).index(d_max)]))
                print(linha)
        print()


        # Arquivos de saída: Relatório de estatísticas de distâncias
        #################################################################
        # Verifica o nome do arquivo passado no parâmetro do objeto
        atend_stat_file = 'Estatisticas_de_atendimento.txt'

        if os.path.isfile(atend_stat_file) == True:
            with open(atend_stat_file, 'a') as file_out:
                print('\n', file = file_out)
                print('{0:s}'.format(linha), file = file_out)
                print('{0:s}{1:s}'.format('Demand meet statistics - ',self.level), file = file_out)
                print('{0:s}'.format(linha), file = file_out)
                if self.level == "Nivel_1":
                    print("Pop served:\t\t{0:>6d} ({1:5.2f}%).".format(sum(self.pop_atendida),(sum(self.pop_atendida)/int(self.state_pop))*100), file = file_out)
                print("Municipalities (hub):\t{0:>8d} mun.".format(d_n), file = file_out)
                print('{0:s}'.format(linha), file = file_out)
                print('\n', file = file_out)

                for nome in especialidades:
                    if sum(especialidades[nome].values()) > 0:
                        print("Resource:\t\t{0:s}\t\t[FTE or unit (equipment)]".format(nome), file = file_out)
                        print('{0:s}'.format(linha), file = file_out)
                        # Transforma o dicionário em lista de valores
                        d_max  = np.amax(list(especialidades[nome].values()))
                        d_min  = np.amin(list(especialidades[nome].values()))
                        d_mean = np.mean(list(especialidades[nome].values()))
                        d_med  = np.median(list(especialidades[nome].values()))
                        print("Minimum:\t\t{0:>6.2f} ({1:s})."
                              .format(d_min, list(especialidades[nome].keys())
                                      [list(especialidades[nome].values()).index(d_min)]), file = file_out)
                        print("Mean:\t\t\t{0:>6.2f}".format(d_mean), file = file_out)
                        print("Median:\t\t\t{0:>6.2f}".format(d_med), file = file_out)
                        print("Maximum:\t\t{0:>6.2f} ({1:s})."
                              .format(d_max, list(especialidades[nome].keys())
                                      [list(especialidades[nome].values()).index(d_max)]), file = file_out)
                        print('{0:s}'.format(linha), file = file_out)
                print('\n', file = file_out)

        else:
            print(f'>>> Generating Report {atend_stat_file}...')
            # Abrir arquivo para escerver 'w' - write
            with open(atend_stat_file, 'w') as file_out:
                print('{0:s}'.format(linha), file = file_out)
                print('{0:s}{1:s}'.format('Demand meet statistics - ',self.level), file = file_out)
                print('{0:s}'.format(linha), file = file_out)
                if self.level == "Nivel_1":
                    print("Pop served:\t\t{0:>6d} ({1:5.2f}%).".format(sum(self.pop_atendida),(sum(self.pop_atendida)/int(self.state_pop))*100), file = file_out)
                print("Municipalities (hub):\t{0:>8d} mun.".format(d_n), file = file_out)
                print('{0:s}'.format(linha), file = file_out)
                print('\n', file = file_out)

                for nome in especialidades:
                    if sum(especialidades[nome].values()) > 0:
                        print("Resource:\t\t{0:s}\t\t[FTE or unit (equipment)]".format(nome), file = file_out)
                        print('{0:s}'.format(linha), file = file_out)
                        # Transforma o dicionário em lista de valores
                        d_max  = np.amax(list(especialidades[nome].values()))
                        d_min  = np.amin(list(especialidades[nome].values()))
                        d_mean = np.mean(list(especialidades[nome].values()))
                        d_med  = np.median(list(especialidades[nome].values()))
                        print("Minimum:\t\t{0:>6.2f} ({1:s})."
                              .format(d_min, list(especialidades[nome].keys())
                                      [list(especialidades[nome].values()).index(d_min)]), file = file_out)
                        print("Mean:\t\t\t{0:>6.2f}".format(d_mean), file = file_out)
                        print("Median:\t\t\t{0:>6.2f}".format(d_med), file = file_out)
                        print("Maximum:\t\t{0:>6.2f} ({1:s})."
                              .format(d_max, list(especialidades[nome].keys())
                                      [list(especialidades[nome].values()).index(d_max)]), file = file_out)
                        print('{0:s}'.format(linha), file = file_out)
                print('\n', file = file_out)


        # Muda para Diretorio um nivel superior
        os.chdir("..")
        # Diretório atual: Retorna ao diretório anterior
        # print(pathlib.Path().absolute())


    def get_x_range(self):
        # x_range = np.array(list(self.especialidades.keys()))
        # print('self.especialidades.items(): ', self.especialidades.values())
        # espec_ativas = dict(filter(lambda elem: int(elem[1])> 0,
        #                            self.especialidades.values()))
        # print('>>> espec_ativas:', espec_ativas)

        y_range = np.array([sum(self.physicians),
                           sum(self.nurses),
                           sum(self.other_cadres),
                           sum(self.community_based),
                           sum(self.beds),
                           sum(self.ct_scanners),
                           sum(self.mri_units),
                           sum(self.mammography),
                           sum(self.radiotherapy)
                           ,
                        #    sum(self.oftalmologia),
                        #    sum(self.otorrino),
                        #    sum(self.dermatologia),
                        #    sum(self.pneumologia),
                        #    sum(self.reumatologia),
                        #    sum(self.urologia),
                        #    sum(self.ortopedia)
                           ])

        # print('prev_y_range:', y_range)

        x_range = np.array(list(self.especialidades.keys()))
        xy_dic_range = dict(zip(x_range, y_range))
        # filter(function, iterable)
        xy_dic_range_filtered = dict(filter(lambda elem: elem[1]>0,
                                            xy_dic_range.items()))
        # print('xy_dic_range_filtered: ', xy_dic_range_filtered)
        self.x_range = list(xy_dic_range_filtered.keys())
        self.y_range = list(xy_dic_range_filtered.values())
        # print('x_range:', self.x_range)
        # print('y_range:', self.y_range)
        return self.x_range

    def get_y_range(self):
        return self.y_range
