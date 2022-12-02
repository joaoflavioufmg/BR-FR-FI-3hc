#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# print(f'importado! Módulo: {__name__}\tPacote: {__package__}')

# Material: https://docs.bokeh.org/en/latest/docs/gallery.html
# https://docs.bokeh.org/en/latest/docs/reference/palettes.html

import sys # Importa modulos do sistema
import os # Local (path) do sistema
import pathlib  # Local do diretório (pasta)

import numpy as np  # Estatísticas (np é um 'alias' para numpy)
import scipy.stats  # Estatísticas

###############################################################
import geoplotlib   # Geração de gráficos e mapas
from geoplotlib.utils import read_csv # Geração de mapas
# kernel density estimation visualization
from geoplotlib.utils import BoundingBox, DataAccessObject
###############################################################

###############################################################
from bokeh.io import show, output_file      # Gráficos
from bokeh.models import ColumnDataSource   # Gráficos
from bokeh.palettes import Spectral6        # Gráficos
from bokeh.palettes import Category20       # Gráficos
from bokeh.plotting import figure           # Gráficos
from bokeh.transform import factor_cmap     # Gráficos
###############################################################

# Importando o módulo 'config' tem-se variáveis globais
# podendo serem usadas entre os módulos que as necessitam
from negocio import config
from negocio.demand import SatisfyDemand


def make_flow_maps(level):
    largura = 1000  # Configuração geral para os três mapas em camadas
    altura = 800    # Configuração geral para os três mapas em camadas
    pontos = read_csv(level + '.csv')
    if level == "Nivel_1":
        geoplotlib.dot(pontos, color='b', point_size= 4,\
                       f_tooltip=lambda r:r['name'])
    elif level == "Nivel_2":
        geoplotlib.dot(pontos, color='g', point_size= 4,\
                       f_tooltip=lambda r:r['name'])
    elif level == "Nivel_3":
        geoplotlib.dot(pontos, color='r', point_size= 4,\
                       f_tooltip=lambda r:r['name'])
    # Configura_janela(largura,altura)
    geoplotlib.set_window_size(largura,altura)
    # [‘watercolor’, ‘toner’, ‘toner-lite’, ‘darkmatter’,’positron’]
    geoplotlib.tiles_provider('positron')
    # geoplotlib.show()

    fluxo = read_csv('fluxo_' + level + '.csv')
    if level == "Nivel_1":
        geoplotlib.graph(fluxo,
                         src_lat='lat_departure',
                         src_lon='lon_departure',
                         dest_lat='lat_arrival',
                         dest_lon='lon_arrival',
                         color='Blues',
                         alpha=50,
                         linewidth=2)
    elif level == "Nivel_2":
        geoplotlib.graph(fluxo,
                         src_lat='lat_departure',
                         src_lon='lon_departure',
                         dest_lat='lat_arrival',
                         dest_lon='lon_arrival',
                         color='Greens',
                         alpha=50,
                         linewidth=4)
    elif level == "Nivel_3":
        geoplotlib.graph(fluxo,
                         src_lat='lat_departure',
                         src_lon='lon_departure',
                         dest_lat='lat_arrival',
                         dest_lon='lon_arrival',
                         color='Reds',
                         alpha=200,
                         linewidth=6)
    else:
        print(">>> Distâncias 'máximas' muito curtas. Não há fluxo!")

    # Configura_janela(largura,altura)
    geoplotlib.set_window_size(largura,altura)
    # [‘watercolor’, ‘toner’, ‘toner-lite’, ‘darkmatter’,’positron’]
    geoplotlib.tiles_provider('positron')
    # geoplotlib.show()

    # kernel density estimation visualization
    kernel_data = read_csv('kernel_' + level + '.csv')
    # Configura_janela(largura,altura)
    geoplotlib.set_window_size(largura,altura)
    # [‘watercolor’, ‘toner’, ‘toner-lite’, ‘darkmatter’,’positron’]
    geoplotlib.tiles_provider('positron')

    # geoplotlib.kde(kernel_data, bw=5, cut_below=1e-4)

    # lowering clip_above changes the max value in the color scale
    # geoplotlib.kde(kernel_data, bw=5, cut_below=1e-4, clip_above=.1)

    # different bandwidths
    # geoplotlib.kde(kernel_data, bw=20, cmap='PuBuGn', cut_below=1e-4)
    geoplotlib.kde(kernel_data, bw=10, cmap='PuBuGn', cut_below=1e-4)
    # geoplotlib.kde(kernel_data, bw=2, cmap='PuBuGn', cut_below=1e-4)

    # linear colorscale
    # geoplotlib.kde(kernel_data, bw=5, cmap='jet', cut_below=1e-4, scaling='lin')

    # https://boundingbox.klokantech.com/
    bbox = BoundingBox(west=-75.2, south=-36.2, east=-33.9, north=5.3)
    geoplotlib.set_bbox(bbox)

    # Keyboard controls
    # P: a screenshot named and saved in current working directory
    # M: toggle base tiles map rendering
    # L: toggle layers rendering
    # I/O: zoom in/out
    # A/D: pan left/right
    # W/S: pan up/down

    geoplotlib.show()


def demand_meet_graphics(file_name, level, state):
    # global maps_folder
    # Diretório atual: Retorna ao diretório atual
    # print('>>> Local atual:', pathlib.Path().absolute())

    fn = file_name
    l = level
    sp = state
    ranges = SatisfyDemand(fn, l, sp)

    # # Prepare some data
    # # output to static HTML file (with CDN resources)
    # # Create a new plot - Call figure()
    # # Ask Bokeh to show() or save() the results.


    # output to static HTML file (with CDN resources)
    # output_file(file_name)
    file_name = 'Atend-Demanda-' + level + '.html'

    if level == "Nivel_1":
        level = "Primary Care"
    elif level == "Nivel_2":
        level = "Secondary Care"
    elif level == "Nivel_3":
        level = "Tertiary Care"
    title_name = 'Worforce (FTE) and Equipment requirements - '+ 'in ' \
    + state + ' (Brazil) ' + level

    os.chdir(config.maps_folder)
    output_file(file_name, mode="cdn")

    TOOLS = "crosshair,pan,wheel_zoom,box_zoom,reset,box_select,lasso_select"

    # Prepare some data
    # x = ['Apples', 'Pears', 'Nectarines', 'Plums', 'Grapes', 'Strawberries']
    # y = [5, 3, 4, 2, 4, 6]
    especialists = ranges.get_x_range()
    qty_fte = ranges.get_y_range()

    source = ColumnDataSource(data=dict(especialists=especialists, \
                                        qty_fte=qty_fte))

    p = figure(x_range=especialists, plot_height=650, plot_width=1550,\
               # toolbar_location=None,
               title=title_name,
               x_axis_label='Workforce or equipment', y_axis_label='(FTE or unit)',
               tools=TOOLS, background_fill_color="#fafafa")

    # https://docs.bokeh.org/en/latest/docs/reference/palettes.html
    if len(qty_fte) <= 6:
        palette = Spectral6
    else:
        palette = Category20[len(qty_fte)]

    p.vbar(x='especialists', top='qty_fte', width=0.9, source=source,
           legend_field="especialists",
           line_color='white', fill_color=factor_cmap('especialists',
                                                      palette=palette,
                                                      factors=especialists))

    p.xgrid.grid_line_color = None
    p.y_range.start = 0
    p.y_range.end = np.amax(qty_fte) + 50
    p.legend.orientation = "horizontal"
    p.legend.location = "top_center"

    
    # Ask Bokeh to show() or save() the results.
    show(p)  # COMENTAR PARA GERAR RELATORIOS APENAS

    # Muda para Diretorio um nivel superior
    os.chdir('..')
