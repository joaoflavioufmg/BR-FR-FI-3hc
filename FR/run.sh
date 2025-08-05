# !/bin/bash

# Para rodar a primeira vez: sudo chmod +x run.sh
# Para rodar digite: ./runAmpl.sh

# REM 	Este eh um comentario
#   	Este tambem eh um comentario
# Adicionar o PATH variable os enderecos:
# 	C:\Users\Joao\Dropbox\05-Softwares\01-Otimizacao\03-AMPL\00-AMPL\ampl
# 	C:\Users\Joao\Dropbox\05-Softwares\01-Otimizacao\01-GLPK\glpk


# Otimizando por partes: Usando PL e depois PLIM
# 1 - Gere uma solucao do problema PL e salve-o usando "-w file.sol"
# 2 - O arquivo file.sol gerado deve ter na linha de solucao (primeiras) o nome "s" "bas", ou seja, eh uma solucao basica viavel
# 3 - Chame o glpsol desabilitando presolver do PL (--nopresol) e o presolver do PLIM (--nointopt) e inclua o arquivo de base (--ini file.sol)

# Exemplo:
# glpsol -m snp.mod -d snp.dat --simplex --noscale --bib --nopresol --nomip --exact --xcheck -w base.sol --log snp.log
# glpsol -m snp.mod -d snp.dat --nopresol --nointopt --cuts --ini base.sol --log snp.log


# ampl cgh.run
# glpsol -m cgh.mod -d cgh.dat
python v12_3flass.py

# rm v9_log.log
#
# for k in {1..10..1}
#
#   do
#   echo "."
#   echo "------------------------   Solving Nrun: $k ...   ------------------------"
#   echo "."
#
#   # rem creating a temporary dat file with n parameter
#   echo "data; param Nrun:=$k; end;" > tmp.dat

  # # rem now running glpk!
  # # rem please note that you need to set the correct path to glpsol.exe (gusek folder)
  # # rem C:\solvers\glpsol --cuts -m 02-snpDetGlpk.mod -d 01-smallDet.dat -d "tmp.dat" --mipgap 0.01 --tmlim 3600 --log 13-smallCicleDetGlpk.log
  # # C:\solvers\ampl 061-snp.run
  # # ampl 061-snp.run;
  # glpsol -m v9_3flass.mod -d v9_dados.dat -d 31_dados.dat -d ../otimizacao/configuracoes/conf_1200000.dat -d 31_distancias.txt --mipgap 0.01 --tmlim 7200 --log v9_log.log
  # rm tmp.dat
  #
  # done
  # exit 0



# @echo off

# rem if exist previous output file, just kill it
# rem del 00-Funcao-Objetivo.txt
# rem a loop with k% going from 1 to 100, with step 1
# rem The echo statement is used to displayed information to the screen.

# for /l %%k in (1,1,100) do (

# 	rem just chit-chating:
# 	echo .
# 	echo ------------------------   Solving Nrun: %%k...   ------------------------
# 	echo .

# 	rem creating a temporary dat file with Nrun parameter
# 	echo data; param Nrun:=%%k; end; > tmp.dat

# 	rem now running glpk!
# 	glpsol -m cgh.mod -d cgh.dat -d tmp.dat --seed ?
# )

# rem remove temporary files and variables
# del tmp.dat
