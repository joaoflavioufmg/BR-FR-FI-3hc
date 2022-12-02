# ======================================================
# Model: Hierarchical health care design : 3 levels (brown field)
# Joao Flavio F. Almeida <joao.flavio@dep.ufmg.br >
# Fabricio Oliveira <fabricio.oliveira@aalto.fi >
# Data   : 24/08/2022
# Versao: 1.0:
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

# Numero de internacoes - Fator de atratividade
# param NInter{i in I};

# Numero de medicos
# param Nmed{i in I, e in E};

# Fator para o calculo da demanda (base Portaria 1631): Numero de medicos por 100 mil.
param DEM{NA,E} default 0;

# Demanda por Cidade i no nivel n e na especialidade k
param Q{i in I,n in NA,e in E} := round((DEM[n,e]*POP[i])/1000,4);
# display{n in NA, e in E}: sum{i in I}Q[i,n,e];
/* display Q; */

# Quantidade minima de demanda medica (FTE) no destino
# Numero minimo de medicos a serem alocados em cada cidade destino
param Qmin{n in NA, e in E} default 0;

# Numero estimado de FTE por nível e especialidade
param QE{n in NA, e in E} default 0;

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

# display DurUpper1;
# display DurUpper2;
# display DurUpper3;

param f1{i in I , j in N1[i]}:= if (D[i,j] <= DurLower[1]) then 0 else (DurUpper[1]-D[i,j])/(DurUpper[1]-DurLower[1]);
param f2{j in J1, k in N2[j]}:= if (D[j,k] <= DurLower[2]) then 0 else (DurUpper[2]-D[j,k])/(DurUpper[2]-DurLower[2]);
param f3{k in J2, l in N3[k]}:= if (D[k,l] <= DurLower[3]) then 0 else (DurUpper[3]-D[k,l])/(DurUpper[3]-DurLower[3]);
check{i in I , j in N1[i]}: f1[i,j] <=1;
check{j in J1, k in N2[j]}: f2[j,k] <=1;
check{k in J2, l in N3[k]}: f3[k,l] <=1;

# Penalty as a logistic cost infrastructure / km.inhabitant
# out of the radious threshold
param P:=1e1; 

# ==================================================
# Variaveis
# ==================================================
# Trajetoria percorrida por cada cidade
/* var x{n in NA, i in I, j in N[i]} binary; */
var x{n in NA, i in I, j in J} binary;
# var x{n in NA, (i,j) in K} binary;

# Extra travel duration
var ex{n in NA, i in I, j in J}, >=0;

# Se a cidade possui ou nao a unidade de saúde de cada nivel
var z{n in NA, j in J} binary;

# ==================================================
# Formulacao
# ==================================================

minimize of: sum{n in NA, j in J} CI[n]*INFR[j]*z[n,j] 
# Total cost of the health care system (assigning origin population)
	+ sum{n in NA, i in I, j in N1[i]: n=1} HC[n]*POP[i]*x[n,i,j]
	+ sum{n in NA, j in J1, k in N2[j]: n=2} HC[n]*POP[j]*x[n,j,k]
	+ sum{n in NA, k in J2, l in N3[k]: n=3} HC[n]*POP[k]*x[n,k,l]
# Effectiveness: Displacement accessibility Cost on all three leves of care
	+ sum{n in NA, i in I, j in N1[i]: n=1 and i <> j} f1[i,j]*D[i,j]*POP[i]*x[n,i,j]
	+ sum{n in NA, j in J1, k in N2[j]: n=2 and j <> k} f2[j,k]*D[j,k]*POP[j]*x[n,j,k]
	+ sum{n in NA, k in J2, l in N3[k]: n=3 and k <> l} f3[k,l]*D[k,k]*POP[k]*x[n,k,l]
# Penalties (logistic Cost / km.pop)
	+ sum{n in NA, i in I, j in N1[i]: n=1 and i <> j} P*POP[i]*ex[n,i,j]
	+ sum{n in NA, j in J1, k in N2[j]: n=2 and j <> k} P*POP[j]*ex[n,j,k]
	+ sum{n in NA, k in J2, l in N3[k]: n=3 and k <> l} P*POP[k]*ex[n,k,l];


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

# Nao eh necessario: R22 eh mais flexivel
# s.t. R9{j in J}: z[3,j] >= POLO[j];

# Restringe as cidades que podem ser escolhidas para receber unidade de saúde como aqueles que atenderem uma demanda minima
# s.t. R13{n in NA,j in J, e in E}: sum{i in I: i in NAE[n,e,j]} Q[i,n,e]*x[n,i,j] >= Qmin[n,e]*z[n,j];

/* HIERARQUIA */
# s.t. R10{n in NA,j in J1, e in E: n=1}: sum{i in I: i in NAE[n,j] and j in N1[i]} Q[i,n,e]*x[n,i,j] >= Qmin[n,e]*z[n,j];

# var xd1{n in NA, j in J1, e in E: n=1}, >= 0;

/* s.t. R10a{n in NA, j in J1, e in E: n=1 and DEM[n,e] > 0}: sum{i in I: i in NAE[n,j] and j in N1[i] and i <> j} ((Q[i,n,e]*x[n,i,j]/DEM[n,e])*DEM[2,e]) = xd1[n,j,e]; */
# s.t. R10a{n in NA, j in J1, e in E: n=1 and e<=3 and DEM[n,e]>0}: sum{i in I: i in NAE[n,j] and j in N1[i]} ((Q[i,n,e]*x[n,i,j]/DEM[n,e])*DEM[2,e]) = xd1[n,j,e];

s.t. R10b{n in NA, e in E: n=1}: sum{i in I, j in J1} Q[i,n,e]*x[n,i,j] >= sum{i in I} Q[i,n,e];

# s.t. R11{n in NA, e in E: n=2}: sum{j in J1, k in J2} Q[j,n,e]*x[n,j,k] >= sum{j in J1}xd1[n-1,j,e];
# s.t. R11{n in NA, j in J1, e in E: n=2 and e<=3 and DEM[n,e]>0}: sum{k in J2: j in J1} Q[j,n,e]*x[n,j,k] >= xd1[n-1,j,e];

# var xd2{n in NA, k in J2, e in E: n=2}, >= 0;

/* s.t. R11a{n in NA, k in J2, e in E: n=2 and DEM[n,e] > 0}: sum{j in J1: j in NAE[n,k] and k in N2[j] and j <> k} ((Q[j,n,e]/DEM[n,e])*DEM[3,e])*x[n,j,k] = xd2[n,k,e]; */
# s.t. R11a{n in NA, k in J2, e in E: n=2 and e<=3 and DEM[n,e]>0}: sum{j in J1: j in NAE[n,k] and k in N2[j]} ((Q[j,n,e]*x[n,j,k]/DEM[n,e])*DEM[3,e]) = xd2[n,k,e];


s.t. R11b{n in NA, e in E: n=2}: sum{j in J1, k in J2} Q[j,n,e]*x[n,j,k] >= sum{j in J1} Q[j,n,e];

# s.t. R12{n in NA, e in E: n=3}: sum{k in J2, l in J3} Q[k,n,e]*x[n,k,l] >= sum{k in J2}xd2[n-1,k,e];
# s.t. R12{n in NA, k in J2, e in E: n=3 and e<=3 and DEM[n,e]>0}: sum{l in J3: k in J2} Q[k,n,e]*x[n,k,l] >= xd2[n-1,k,e];

# s.t. R12c{n in NA, k in J2, e in E: n=3 and DEM[n,e]>0}: sum{l in J3: k in J2} Q[k,n,e]*x[n,k,l] >= sum{j in J1: j in NAE[n,k] and k in N2[j]} ((Q[j,n-1,e]*x[n-1,j,k]/DEM[n-1,e])*DEM[n,e]);

s.t. R12b{n in NA, e in E: n=3}: sum{k in J2, l in J3} Q[k,n,e]*x[n,k,l] >= sum{k in J2}Q[k,n,e];


/* s.t. R11b{n in NA, e in E: n = 2}: sum{j in J1, k in J2: j in NAE[n,k] and k in N2[j]} Q[j,n,e]*x[n,j,k] >= 0.8*QE[n,e];
s.t. R12b{n in NA, e in E: n = 3}: sum{k in J2, l in J3: k in NAE[n,l] and l in N3[k]} Q[k,n,e]*x[n,k,l] >= 0.96*QE[n,e]; */

# Fluxo da populacao para cidades mais populosas
# s.t. R16{n in NA, i in I, j in N[i]}: x[n,i,j]*POP[i] <= POP[j];

# s.t. R13{n in NA, i in I, j in N1[i]: n=1}: x[n,i,j]*POP[i] <= 1.2*POP[j];
# s.t. R14{n in NA, j in J1, k in N2[j]: n=2}: x[n,j,k]*POP[j] <= 1.2*POP[k];
# s.t. R15{n in NA, k in J2, l in N3[k]: n=3}: x[n,k,l]*POP[k] <= 1.2*POP[l];

s.t. R16{n in NA, i in I , j in N1[i]: n=1 and i <> j}: D[i,j]*x[n,i,j] <= DurLower[n] + ex[n,i,j];
s.t. R17{n in NA, j in J1, k in N2[j]: n=2 and j <> k}: D[j,k]*x[n,j,k] <= DurLower[n] + ex[n,j,k];
s.t. R18{n in NA, k in J2, l in N3[k]: n=3 and k <> l}: D[k,l]*x[n,k,l] <= DurLower[n] + ex[n,k,l];

# s.t. R16u{n in NA, i in I, j in N1[i]: n=1}: D[i,j]*x[n,i,j] <= DurUpper[n];
# s.t. R17u{n in NA, j in J1, k in N2[j]: n=2}: D[j,k]*x[n,j,k] <= DurUpper[n];
# s.t. R18u{n in NA, k in J2, l in N3[k]: n=3}: D[k,l]*x[n,k,l] <= DurUpper[n];

s.t. R19{n in NA: n=1}: sum{j in J1} z[n,j] <= card(I) - 1;
s.t. R20{n in NA: n=2}: sum{k in J2} z[n,k] <= sum{j in J1}z[n-1,j] - 1;
s.t. R21{n in NA: n=3}: sum{l in J3} z[n,l] <= sum{k in J2}z[n-1,k] - 1;
s.t. R22{n in NA, j in S3: n=3}: z[n,j] >= 1;


end;

