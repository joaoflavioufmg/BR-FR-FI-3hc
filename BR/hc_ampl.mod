# ======================================================
# Model: Hierarchical health care design : 3 levels (brown field)
# Joao Flavio F. Almeida <joao.flavio@dep.ufmg.br >
# Fabricio Oliveira <fabricio.oliveira@aalto.fi >
# Data   : 15/01/2023
# Versao: 3.0: Linearizacao de produto de variaveis 
# Solve only hc_glpk.mod (hc_glpk1.mod + hc_glpk2.mod)
# =========================================================

# =========================================================
# Conjuntos e Parametros
# =========================================================
# param Nrun, >0, default 1;

# Conjunto de Todas as Cidades
set I;
# display card(I);

# GeoCodigos das 5 Grandes Regioes do Brasil
param RE{I} integer, >= 0;

# GeoCodigos de Estados
param ES{I} integer, >= 0;

# Nome dos Municipios
param Mun{I} symbolic;

# Populacao dos Municipios
param POP{I} integer, >= 0;

# Latitude dos municipios (2018)
param lat{I};

# Longitude dos municipios
param lng{I};

/*
# Distancias circulares entre os GeoCodigos
param d2r := 3.1415926/180;
param alpha{a in I, b in I} :=
	sin(d2r*(lat[a]-lat[b])/2)**2 +
	cos(d2r*lat[a])*cos(d2r*lat[b])*sin(d2r*(lng[a]-lng[b])/2)**2;
param gcdist{a in I, b in I} :=
    2*6371*atan( sqrt(alpha[a,b]), sqrt(1-alpha[a,b]) );	# Glpk
#     2*6371*atan2( sqrt(alpha[a,b]), sqrt(1-alpha[a,b]) );	# Ampl
*/

# Links - Para facilitar houve um pre-processamento para reduzir o tamanho do conjunto
# set K dimen 2 := I cross (J[1] union J[2] union J[3]);
# set K dimen 2 := I cross I;
set K dimen 2;

# Distancia da tupla (i,j) pre-selecionada: Distancias reais dos municipios do Estado -
# Distancia (km) no arquivo de dados
# param dist1{(i,j) in K};

# Distancia em kilometros do arquivo de dados
# param dist{(i,j) in K}:= if gcdist[i,j] <= 1 then 1 else gcdist[i,j];
# check{(i,j) in K}: dist[i,j] >= 1;
# param dist{(i,j) in K}:= gcdist[i,j];
param dist{(i,j) in K};
param dur{(i,j) in K};

# Distancia da tupla (i,j) pre-selecionada: Distancias reais dos municipios do Estado -
# Distancia (km) no arquivo de dados
# Distancia entre pares de cidade - Matriz Google API (futuramente)
# param D{(i,j) in K};
# param D{(i,j) in K}:= ceil(dist[i,j]);
param D{(i,j) in K}:= round(dur[i,j]/3600,2);
# display D;

# Conjunto de niveis de atendimento
set NA:= 1..3;

# Conjunto de especialidades
/* set E:= 1..16; */
set E;

# Resources description
param Res{E} symbolic;

# param POPmin {n in NA} integer := 0;
param POPmin {n in NA} integer, >= 0, default 0;

# Distancia maxima para atendimento no nivel n pela especilidade e
# Conjutno J deve ser um limite superior, que sera refinado no modelo usando o novo limite DMAX

# param Dist_Max := max{(i,j) in K}D[i,j];
# display Dist_Max;
param Dur_Max := max{(i,j) in K}D[i,j];
# display Dur_Max;
param Pop_Total := sum{i in I}POP[i];
# display Pop_Total;
param Pop_Max := max{i in I}POP[i];
# display Pop_Max;
param Pop_Min := min{i in I}POP[i];
# display Pop_Min;

param Distmax{n in NA};
param DurLower{n in NA}, >=0;
param DurUpper{n in NA}, > DurLower[n];
param DurUB := max{n in NA}DurUpper[n];


/* # Distancia maxima e Populacao minima de abrangencia estao relacionados
param Dmax{n in NA, (i,j) in K} := if (n = 1) then Distmax_N1	# 1 h de Casa a 60 km/h: 60
else if (n = 2) then Distmax_N2								# 2 h de N1 a   60 km/h: 180
else Distmax_N3; # Para (n = 3 and e = 2) 							# 3 h de N2 a   60 km/h: 360 */

# Distancia maxima e Populacao minima de abrangencia estao relacionados
# param Dmax{n in NA, (i,j) in K} := if (n = 1) then Distmax[1]	# 1 h de Casa a 60 km/h: 60
# else if (n = 2) then Distmax[2]								# 2 h de N1 a   60 km/h: 180
# else Distmax[3]; # Para (n = 3 and e = 2) 							# 3 h de N2 a   60 km/h: 360
param Dmax{n in NA, (i,j) in K} := if (n = 1) then DurUpper[1]	# 1 h de Casa a 60 km/h: 60
else if (n = 2) then DurUpper[2]								# 2 h de N1 a   60 km/h: 180
else DurUpper[3]; # Para (n = 3 and e = 2) 							# 3 h de N2 a   60 km/h: 360


# Distancia maxima e Populacao minima de abrangencia estao relacionados
# param Dmax{n in NA, (i,j) in K} := if (n = 1) then 70
# else if (n = 2) then 150
# else 400; # Para (n = 3 and e = 2)

param PABmin_N1;
param PABmin_N2;
param PABmin_N3;

# Demanda minima no nivel n: Populacao minima de abrangencia
param PABmin{n in NA, e in E} := if (n = 1) then PABmin_N1
else if (n = 2) then PABmin_N2
else PABmin_N3; # Para (n = 3);

# set N{i in I} := {j in I: (i,j) in K and D[i,j] <= Dmax[i,j]};
# set J{n in N} := setof{j in I: POP[j] >= POPMin[n]} (j);

# Conjunto de origens (i) para o destino seleto (j)
/* set NAE{n in NA, j in I} := {i in I: (i,j) in K and POP[j] >= POPmin[n] and D[i,j] <= Dmax[n,i,j]}; */
set NAE{n in NA, j in I} := {i in I: (i,j) in K and D[i,j] <= Dmax[n,i,j]};
/* display{n in NA, j in I: n = 1} NAE[n,j]; */
set NA2{n in NA} := {i in I: i in NAE[n,i]};
/* display NA2; */

##################################################################
# Conjunto de destinos para o Nivel 1
set N1{i in I} := {j in I: (i,j) in K and POP[j] >= POPmin[1] and D[i,j] <= Dmax[1,i,j]};
set J1 := {i in I: i in N1[i]};
# display N1;
# display{i in I: card(N1[i]) = 0}: N1[i];
param EXT1{i in I: card(N1[i]) = 0}:= min{(i,j) in K: i <> j and POP[j] >= POPmin[1]} D[i,j];

# display EXT1; 
set EX1:= {i in I: card(N1[i]) = 0 and EXT1[i] > 0};
# set EX1:= {i in I: card(N1[i]) = 0};
# check{i in I}: card(N1[i]) > 0;
# display J1;
# display EX1;

set N2{i in J1} := {j in I: (i,j) in K and POP[j] >= POPmin[2] and D[i,j] <= Dmax[2,i,j] and i in N1[i]};
set J2 := {i in J1: i in N2[i]};
# display N2;
param EXT2{i in J1: card(N2[i]) = 0}:= min{(i,j) in K: i <> j and POP[j] >= POPmin[2]} D[i,j];
# display EXT2;
set EX2:= {i in J1: card(N2[i]) = 0 and EXT2[i] > 0};
# set EX2:= {i in J1: card(N2[i]) = 0};
/* check{i in J1}: card(N2[i]) > 0; */
/* display J2; */
# display EX2;

set N3{i in J2} := {j in I: (i,j) in K and POP[j] >= POPmin[3] and D[i,j] <= Dmax[3,i,j] and i in N2[i]};
set J3 := {i in J2: i in N3[i]};
# display N3;
/* display{i in J2: card(N3[i]) = 0} i, min{(i,j) in K: i <> j and POP[j] >= POPmin[3]} D[i,j]; */
param EXT3{i in J2: card(N3[i]) = 0}:= min{(i,j) in K: i <> j and POP[j] >= POPmin[3]} D[i,j];
# display EXT3;
set EX3:= {i in J2: card(N3[i]) = 0 and EXT3[i] > 0};
# set EX3:= {i in J2: card(N3[i]) = 0};
# display EX3;

# Municipios selecionados que já possuem infraestrutura de nível 3
set S3 within J3 default {};

/* check{i in J2}: card(N3[i]) > 0; */
/* display J3; */
/* display{i in J3}: POP[i]; */
##################################################################

# N não exite
/* set N{i in I}:= N1[i] union N2[i] union N3[i];
display N; */

/* set J := {i in I: i in N[i]}; */
set J := J1 union J2 union J3;
# display J;

# check{i in I, j in N1[i]}: D[i,j] <= Distmax[1];
check{i in I, j in N1[i]}: D[i,j] <= DurUpper[1];

# Relacao de cidades candidatas: filtro por niveis de atendimento (3,2,1), populacao e distancia
# Se a cidade eh atendimento terciario, ela eh de atendimento secundario e primario
# Se a cidade eh atendimento secundario, ela eh de atendimento primario
# Se a cidade eh atendimento primario, beleza. Ela eh so isso...
# set J[1]  := setof{j in I: pop[j] >= 10000} (j);
# set J[2] within J[1]:= setof{j in I: pop[j] >= 20000} (j);
# set J[3] within J[2] inter J[1]:= setof{j in I: pop[j] >= 30000} (j);
# set J{n in N} := if (n = 1) then setof{j in I: POP[j] >= 10000} (j)
#  else if (n = 2) then setof{j in I: POP[j] >= 20000} (j)
#  else setof{j in I: POP[j] >= 30000} (j);

# display J;

# If municipality REQUIRES (because it does not have) health care infrastructure
# 0 - No / 1 - Yes
param INFR{i in I} default 0;

param NINFR{i in I: i in J3}:= if (INFR[i] == 1) then 0 else 1;

# Fator para o calculo da demanda (base Portaria 1631): Numero de medicos por 100 mil.
param DEM{NA,E} default 0;

# ==================================================
# For linearization
# ==================================================
var pop{n in NA,j in J}, >= 0, <= Pop_Total; # \tau Population flow to each destination
var pop2{n in NA,j in J1, k in N2[j]: n=2}, >= 0, <= Pop_Total; # \pi Aux varriable
var pop3{n in NA,k in J2, l in N3[k]: n=3}, >= 0, <= Pop_Total; # \pi Aux varriable

param PMAX1:= max{j in J1}POP[j];
param PMAX2:= max{k in J2}POP[k];
param PMAX3:= max{l in J3}POP[l];
# ==================================================

# Demanda por Cidade i no nivel n e na especialidade k
param Q{i in I,n in NA,e in E} := round((DEM[n,e]*POP[i])/1000,4);
# Demanda no Destino j no nivel n e na especialidade k
var q{j in J,n in NA,e in E}, >=0;
# display{n in NA, e in E}: sum{i in I}Q[i,n,e];


# Quantidade minima de demanda medica (FTE) no destino
# Numero minimo de medicos a serem alocados em cada cidade destino
# param Qmin{n in NA, e in E} default 0;

# Numero estimado de FTE por nível e especialidade
# param QE{n in NA, e in E} default 0;

# Infrastructure fixed Cost per level
param CI{n in NA};

# Health care unit cost per care level (2030)
# Primary health care unit cost (n = 1)
# Secondary health care unit cost (n = 2)
# Tertiary health care unit cost (n = 3)
param HC{n in NA}, >= 0;


# Custo por deslocamento de cada nivel considerando penalidade
# A simple linear decay function: fi(d) =(Ui-d)/(Ui-Li)
# param DurUpper1 := max{i in I, j in N1[i]}D[i,j];
# param DurUpper2 := max{j in J1, k in N2[j]}D[j,k];
# param DurUpper3 := max{k in J2, l in N3[k]}D[k,l];

# f function increases accessibility costs as patients travel increases
# f = 0 if D <= DurLower
# f = 1% up to 100% if travel distance increases <= DurUpper
param f1{i in I , j in N1[i]}:= if (D[i,j] <= DurLower[1]) then 0 else (D[i,j]-DurLower[1])/(DurUpper[1]-DurLower[1]);
param f2{j in J1, k in N2[j]}:= if (D[j,k] <= DurLower[2]) then 0 else (D[j,k]-DurLower[2])/(DurUpper[2]-DurLower[2]);
param f3{k in J2, l in N3[k]}:= if (D[k,l] <= DurLower[3]) then 0 else (D[k,l]-DurLower[3])/(DurUpper[3]-DurLower[3]);
check{i in I , j in N1[i]}: f1[i,j] <=1;
check{j in J1, k in N2[j]}: f2[j,k] <=1;
check{k in J2, l in N3[k]}: f3[k,l] <=1;

# Penalty as a logistic cost infrastructure / h.inhabitant
# out of the radious threshold
# Brazil	85.75		#	https://databank.worldbank.org/source/icp-2017
# Finland	97.65		#	https://doi.org/10.1016/j.tranpol.2020.04.006
# France	117.60		#	https://ars.els-cdn.com/content/image/1-s2.0-S0967070X20301827-mmc1.xlsx
param P;  # L


# Cost reduction (Efficiency)
param CR{n in NA}, >= 0, <= 1; # E_{n} Efficiency gain

# ==================================================
# Variaveis
# ==================================================
# Trajetoria percorrida por cada cidade
/* var x{n in NA, i in I, j in N[i]} binary; */
var x{n in NA, i in I, j in J} binary;
# var x{n in NA, (i,j) in K} binary;

# Extra travel duration
var ex{n in NA, i in I, j in J}, >=0;
# Linearization: pop[n,i]*ex[n,i,j] = ext[n,i,j]
var ext{n in NA, i in I, j in J}, >=0; # \eta
# Auxiliary variable for linearization
# var ex1{n in NA, i in I, j in N1[i]: n=1}, >=0, <= DurUpper[n];
# var ex2{n in NA, j in J1, k in N2[j]: n=2}, >=0, <= DurUpper[n];
# var ex3{n in NA, k in J2, l in N3[k]: n=3}, >=0, <= DurUpper[n];

# Se a cidade possui ou nao a unidade de saúde de cada nivel
var z{n in NA, j in J}, binary;

# ==================================================
# Formulacao
# ==================================================

minimize of: 
# Total cost of the health care system (assigning origin population)
	  sum{n in NA, j in J1: n=1} HC[n]*CR[n]*pop[n,j]
	+ sum{n in NA, k in J2: n=2} HC[n]*CR[n]*pop[n,k]
	+ sum{n in NA, l in J3: n=3} HC[n]*CR[n]*pop[n,l]
# Total cost of new health care services
	+ sum{n in NA, j in J1: n=1} CI[n]*HC[n]*INFR[j]*pop[n,j]
	+ sum{n in NA, k in J2: n=2} CI[n]*HC[n]*INFR[k]*pop[n,k]
	+ sum{n in NA, l in J3: n=3} CI[n]*HC[n]*INFR[l]*pop[n,l]
# Accessibility: Penalties on logistic Cost (h.pop) on all three leves of care
	# + sum{n in NA, i in I, j in N1[i]: n=1 and i <> j} f1[i,j]*P*D[i,j]*POP[i]*ex[n,i,j]
	# + sum{n in NA, j in J1, k in N2[j]: n=2 and j <> k} f2[j,k]*P*D[j,k]*POP[j]*ex[n,j,k]
	# + sum{n in NA, k in J2, l in N3[k]: n=3 and k <> l} f3[k,l]*P*D[k,l]*POP[k]*ex[n,k,l]
	+ sum{n in NA, i in I, j in N1[i]: n=1 and i <> j} f1[i,j]*P*D[i,j]*ext[n,i,j]
	+ sum{n in NA, j in J1, k in N2[j]: n=2 and j <> k} f2[j,k]*P*D[j,k]*ext[n,j,k]
	+ sum{n in NA, k in J2, l in N3[k]: n=3 and k <> l} f3[k,l]*P*D[k,l]*ext[n,k,l]
;

# Linearization: product of two linear variables
# ========================================================
# x1x2 = z when l1 <= x1 <= u1, l2 <= x2 <= u2, 
# y1 = 1/2 (x1+x2)
# y2 = 1/2 (x1-x2)
# The bounds on y1 and y2 are:
# 1/2(l1+l2) <= y1 <= 1/2(u1+u2) and 
# 1/2(l1-u2) <= y2 <= 1/2(u1-l2)
# x1x2 = z when l1 >= 0, l2 >= 0 and one variable 
# is not rerefenced in any other term, except on x1x2.
# Assuming x1 is that variable, use z, and the following 
# constraint: l1x2 <= z <= u1x2. After solving, 
# x1 = z/x2, x2 > 0.
# ========================================================
# x1 = ex[n,i,j] => x1 = z/x2 => ex[n,i,j] = ext[n,i,j]/pop[n,j]
# x2 = pop[n,j]
# x1x2 = ext[n,i,j]

# ext[n,i,j] = sum{b in I: j in N1[b]}POP[b]*x[n,b,j]*ex[n,b,j];
# x[n,b,j]*ex[n,b,j] = ex1[n,b,j]
# s.t. Rz1{n in NA,i in I, j in N1[i]: n=1}: ext[n,i,j] = sum{b in I: j in N1[b]}POP[b]*ex1[n,b,j];
# s.t. Rz1b{n in NA,i in I, j in N1[i]: n=1}: ex1[n,i,j] <= DurUpper[n]*x[n,i,j];
# s.t. Rz1c{n in NA,i in I, j in N1[i]: n=1}: ex1[n,i,j] <= ex[n,i,j];
# s.t. Rz1d{n in NA,i in I, j in N1[i]: n=1}: ex1[n,i,j] >= ex[n,i,j] - DurUpper[n]*(1-x[n,i,j]);

# s.t. Rz2{n in NA,j in J1, k in N2[j]: n=2}: ext[n,j,k] >= sum{b in J1: k in N2[b]}POP[b]*ex2[n,b,k];
# s.t. Rz2b{n in NA,j in J1, k in N2[j]: n=2}: ex2[n,j,k] <= DurUpper[n]*x[n,j,k];
# s.t. Rz2c{n in NA,j in J1, k in N2[j]: n=2}: ex2[n,j,k] <= ex[n,j,k];
# s.t. Rz2d{n in NA,j in J1, k in N2[j]: n=2}: ex2[n,j,k] >= ex[n,j,k] - DurUpper[n]*(1-x[n,j,k]);

# s.t. Rz3{n in NA,k in J2, l in N3[k]: n=3}: ext[n,k,l] >= sum{b in J2: l in N3[b]}POP[b]*ex3[n,b,l];
# s.t. Rz3b{n in NA,k in J2, l in N3[k]: n=3}: ex3[n,k,l] <= DurUpper[n]*x[n,k,l];
# s.t. Rz3c{n in NA,k in J2, l in N3[k]: n=3}: ex3[n,k,l] <= ex[n,k,l];
# s.t. Rz3d{n in NA,k in J2, l in N3[k]: n=3}: ex3[n,k,l] >= ex[n,k,l] - DurUpper[n]*(1-x[n,k,l]);

s.t. Rz1e{n in NA, i in I, j in N1[i]: n=1}: ext[n,i,j] <= DurUpper[n]*pop[n,j];
s.t. Rz2e{n in NA, j in J1, k in N2[j]: n=2}: ext[n,j,k] <= DurUpper[n]*pop[n,k];
s.t. Rz3e{n in NA, k in J2, l in N3[k]: n=3}: ext[n,k,l] <= DurUpper[n]*pop[n,l];

s.t. R16b{n in NA, i in I, j in N1[i]: n=1}: ex[n,i,j]*POP[j] <= ext[n,i,j];
s.t. R17b{n in NA, j in J1, k in N2[j]: n=2}: ex[n,j,k]*POP[k] <= ext[n,j,k];
s.t. R18b{n in NA, k in J2, l in N3[k]: n=3}: ex[n,k,l]*POP[l] <= ext[n,k,l];

s.t. R16c{n in NA, i in I, j in N1[i]: n=1}: ex[n,i,j]*PMAX1 >= ext[n,i,j];
s.t. R17c{n in NA, j in J1, k in N2[j]: n=2}: ex[n,j,k]*PMAX2 >= ext[n,j,k];
s.t. R18c{n in NA, k in J2, l in N3[k]: n=3}: ex[n,k,l]*PMAX3 >= ext[n,k,l];

# ========================================================
# Cada Municipio segue uma unica trajetoria.
# Em Dmax e Pop de destino limitados, apenas os municipios selecionados tem um destino
# s.t. R1{n in NA,i in I}: sum{j in N[i]} x[n,i,j] = 1 ;
# s.t. R1{n in NA,i in NA2[n]: n = 1}: sum{j in N1[i]} x[n,i,j] = 1 ;
# Em Dmax sem limites, todos os municipios tem um destino
s.t. R1a{n in NA, i in I diff (EX3 union EX2 union EX1): n=1}: sum{j in N1[i]} x[n,i,j] = 1;
# s.t. R1a{n in NA, i in I: n=1}: sum{j in N1[i]} x[n,i,j] = 1;
/* s.t. R1b{n in NA,j in J1: n=2}: sum{k in N2[j]} x[n,j,k] = 1; */
/* s.t. R1c{n in NA,k in J2: n=3}: sum{l in N3[k]} x[n,k,l] = 1; */

# Garanta que tenha a unidade de saúde daquele nivel para a trajetoria escolhida
# s.t. R4{n in NA, i in I, j in N1[i]}: x[n,i,j] <= z[n,j] ;
# s.t. R5{n in NA, i in I, j in N2[i]}: x[n,i,j] <= z[n,j] ;
# s.t. R6{n in NA, i in I, j in N3[i]}: x[n,i,j] <= z[n,j] ;
# s.t. R4{n in NA, i in NA2[n], j in N1[i]: n = 1}: x[n,i,j] <= z[n,j] ;
# s.t. R5{n in NA, j in NA2[n], k in N2[j]: n = 2}: x[n,j,k] <= z[n,k] ;
# s.t. R6{n in NA, k in NA2[n], l in N3[k]: n = 3}: x[n,k,l] <= z[n,l] ;
s.t. R2{n in NA, i in I, j in N1[i]: (i,j) in K and n=1}: x[n,i,j] <= z[n,j];
s.t. R3{n in NA, j in J1, k in N2[j]: (j,k) in K and n=2}: x[n,j,k] <= z[n,k];
s.t. R4{n in NA, k in J2, l in N3[k]: (k,l) in K and n=3}: x[n,k,l] <= z[n,l];

s.t. R5{n in NA, j in J1 diff (EX2 union EX1): n=2}: sum{k in N2[j]} x[n,j,k] = z[n-1,j];
s.t. R6{n in NA, k in J2 diff (EX3 union EX2): n=3}: sum{l in N3[k]} x[n,k,l] = z[n-1,k];
# s.t. R5{n in NA, j in J1: n=2}: sum{k in N2[j]} x[n,j,k] = z[n-1,j];
# s.t. R6{n in NA, k in J2: n=3}: sum{l in N3[k]} x[n,k,l] = z[n-1,k];

# Garante que a damanda da cidade com a unidade de saúde seja atendida por ela mesma
/* s.t. R7{n in NA, i in J}: x[n,i,i] = z[n,i] ; */
s.t. R7a{n in NA, i in J1, j in N1[i]: n=1 and i in NAE[n,j] and i=j}: x[n,i,j] = z[n,j];
s.t. R7b{n in NA, j in J2, k in N2[j]: n=2 and j in NAE[n,k] and j=k}: x[n,j,k] = z[n,k];
s.t. R7c{n in NA, k in J3, l in N3[k]: n=3 and k in NAE[n,l] and k=l}: x[n,k,l] = z[n,l];
# Garante que sempre que a unidade de saúde possa atender niveis superiores, o mesmo vale para os niveis inferiores.
s.t. R8{n in NA, j in J: n > 1}: z[n,j] <= z[n-1,j];

s.t. R9{j in J1,n in NA,e in E: n=1}: q[j,n,e] = (DEM[n,e]*pop[n,j])/1000;
s.t. R10{k in J2,n in NA,e in E: n=2}: q[k,n,e] = (DEM[n,e]*pop[n,k])/1000;
s.t. R11{l in J3,n in NA,e in E: n=3}: q[l,n,e] = (DEM[n,e]*pop[n,l])/1000;

# s.t. R10b{n in NA, e in E: n=1}: sum{i in I, j in J1} Q[i,n,e]*x[n,i,j] >= sum{i in I} Q[i,n,e];
s.t. R9b{n in NA, e in E: n=1}: sum{j in J1} q[j,n,e] >= sum{i in I} Q[i,n,e]-1;


s.t. R16{n in NA, i in I , j in N1[i]: n=1 and i <> j}: D[i,j]*x[n,i,j] <= DurLower[n] + ex[n,i,j];
s.t. R17{n in NA, j in J1, k in N2[j]: n=2 and j <> k}: D[j,k]*x[n,j,k] <= DurLower[n] + ex[n,j,k];
s.t. R18{n in NA, k in J2, l in N3[k]: n=3 and k <> l}: D[k,l]*x[n,k,l] <= DurLower[n] + ex[n,k,l];

# For tree design
s.t. R19{n in NA: n=1}: sum{j in J1} z[n,j] <= card(I) - 1;
s.t. R20{n in NA: n=2}: sum{k in J2} z[n,k] <= sum{j in J1}z[n-1,j] - 1;
s.t. R21{n in NA: n=3}: sum{l in J3} z[n,l] <= sum{k in J2}z[n-1,k] - 1;

# Municipalities with reference centres for health care 
s.t. R22{n in NA, j in S3: n=3}: z[n,j] >= 1;
# s.t. R23{n in NA, j in J3: n=3}: z[n,j] >= NINFR[j];

s.t. R3b{n in NA, j in J1, k in N2[j]: (j,k) in K and n=2}: x[n,j,k]*POPmin[n] <= pop[n,k];
s.t. R4b{n in NA, k in J2, l in N3[k]: (k,l) in K and n=3}: x[n,k,l]*POPmin[n] <= pop[n,l];


s.t. R27{n in NA,j in J1: n=1}: pop[n,j] = sum{i in I: j in N1[i]}POP[i]*x[n,i,j];
s.t. R28{n in NA,k in J2: n=2}: pop[n,k] = sum{j in J1: k in N2[j]}pop2[n,j,k];
s.t. R29{n in NA,l in J3: n=3}: pop[n,l] = sum{k in J2: l in N3[k]}pop3[n,k,l]; 

# linear x binario
# pop[n,k] = sum{j in J1: k in N2[j]}pop[n-1,j]*x[n,j,k];
# pop[1,j]*x[n,j,k] = pop2[n,j,k]

s.t. R30{n in NA,j in J1, k in N2[j]: n=2}: pop2[n,j,k] <= Pop_Max*x[n,j,k];
s.t. R31{n in NA,j in J1, k in N2[j]: n=2}: pop2[n,j,k] <= pop[n-1,j];
s.t. R32{n in NA,j in J1, k in N2[j]: n=2}: pop2[n,j,k] >= pop[n-1,j] - Pop_Max*(1-x[n,j,k]);

s.t. R33{n in NA,k in J2, l in N3[k]: n=3}: pop3[n,k,l] <= Pop_Max*x[n,k,l];
s.t. R34{n in NA,k in J2, l in N3[k]: n=3}: pop3[n,k,l] <= pop[n-1,k];
s.t. R35{n in NA,k in J2, l in N3[k]: n=3}: pop3[n,k,l] >= pop[n-1,k] - Pop_Max*(1-x[n,k,l]);

s.t. R36{n in NA: n=1}: sum{j in J1}pop[n,j] = Pop_Total;
s.t. R37{n in NA: n=2}: sum{j in J2}pop[n,j] = Pop_Total;
s.t. R38{n in NA: n=3}: sum{j in J3}pop[n,j] = Pop_Total;


end;

