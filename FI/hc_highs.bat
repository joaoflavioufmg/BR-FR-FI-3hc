@echo off
    REM Batch file for running optimization solvers
    REM State code: 1

    echo Running GLPSOL to generate MPS file...
    glpsol -m hc_glpk.mod -d hc.dat -d 1_dados.dat -d 1_dist_dur.txt --wmps hc_glpk.mps --check

    echo Running HiGHS solver...
    highs --model_file hc_glpk.mps --options_file hc_highs.opt

    echo Running GLPSOL with HiGHS solution...
    glpsol -m hc_glpk.mod -d hc.dat -d 1_dados.dat -d 1_dist_dur.txt -r hc_highs.sol

    echo All solver commands completed.
    pause
    