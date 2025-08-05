REM glpsol -m hc_glpk.mod -d hc.dat -d v9_dados.dat --wlp hc_glpk.lp --check
REM highs --model_file .\hc_glpk.lp --options_file hc_glpk.opt 
REM glpsol -m hc_glpk.mod -d hc.dat -d v9_dados.dat -r hc_glpk.sol

@echo off
echo Running GLPSOL to generate LP...
REM call glpsol -m hc_glpk.mod -d hc.dat -d 17_dados.dat -d 17_dist_dur.txt --wlp hc_glpk.lp --check
call glpsol -m hc_glpk.mod -d hc.dat -d 17_dados.dat -d 17_dist_dur.txt --wmps hc_glpk.mps --check

echo Running HiGHS solver...
REM call highs --model_file .\hc_glpk.lp --options_file hc_highs.opt
call highs --model_file .\hc_glpk.mps --options_file hc_highs.opt

echo Running GLPSOL again to generate solution...
call glpsol -m hc_glpk.mod -d hc.dat -d 17_dados.dat -d 17_dist_dur.txt -r hc_highs.sol

echo Done.
pause
