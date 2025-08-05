:: REM 	Este eh um comentario
::  	Este tambem eh um comentario
:: Adicionar o PATH variable os enderecos:
	:: C:\Users\Joao\Dropbox\05-Softwares\01-Otimizacao\03-AMPL\00-AMPL\ampl
	:: C:\Users\Joao\Dropbox\05-Softwares\01-Otimizacao\01-GLPK\glpk


:: Otimizando por partes: Usando PL e depois PLIM
:: 1 - Gere uma solucao do problema PL e salve-o usando "-w file.sol"
:: 2 - O arquivo file.sol gerado deve ter na linha de solucao (primeiras) o nome "s" "bas", ou seja, eh uma solucao basica viavel
:: 3 - Chame o glpsol desabilitando presolver do PL (--nopresol) e o presolver do PLIM (--nointopt) e inclua o arquivo de base (--ini file.sol)

:: Exemplo:
:: glpsol -m snp.mod -d snp.dat --simplex --noscale --bib --nopresol --nomip --exact --xcheck -w base.sol --log snp.log
:: glpsol -m snp.mod -d snp.dat --nopresol --nointopt --cuts --ini base.sol --log snp.log


:: ampl v9_run.run
:: glpsol -m v9_3flass_glpk.mod -d v9_dados.dat -d 12_dados.dat -d 12_distancias.txt --cuts --mipgap 0.01 --tmlim 7200 --log v9_log.log
:: glpsol -m v9_3flass_glpk.mod -d v9_dados.dat -d 31_dados.dat -d 31_distancias.txt --cuts --mipgap 0.01 --tmlim 7200 --log v9_log.log

python app.py

@echo off

REM ~ rem if exist previous output file, just kill it
REM ~ del 00-Funcao-Objetivo.txt
REM ~ rem a loop with k% going from 1 to 10, with step 1
REM ~ rem The echo statement is used to displayed information to the screen.

REM ~ for /l %%k in (1,1,10) do (

	REM ~ rem just chit-chating:
	REM ~ echo .
	REM ~ echo ------------------------   Solving Nrun: %%k...   ------------------------
	REM ~ echo .

	REM ~ rem creating a temporary dat file with Nrun parameter
	REM ~ echo data; param Nrun:=%%k; end; > tmp.dat

	REM ~ rem now running glpk!
	REM ~ glpsol -m modv5.mod -d dadosv3.dat -d distv2.dat -d tmp.dat --seed ?
REM ~ )

REM ~ rem remove temporary files and variables
REM ~ del tmp.dat
