# > gnuplot
# > load 'box.gnu' (entre aspas)
# set terminal pngcairo  transparent enhanced font "arial,10" fontscale 1.0 size 600, 400 
set terminal pngcairo background rgb 'white' enhanced font "times new roman,12" fontscale 2.0 size 1500, 1000 

# ############################################
set output 'box.FR.png'
# set output 'box.FI.png'
# set output 'box.BR.png'
# ############################################

set linetype 1 lc rgb "blue"
set linetype 2 lc rgb "green"
set linetype 3 lc rgb "red"

# ############################################
set title "Accessibility to primary, secondary and tertiary care (France)" font "times new roman,16"
# set title "Accessibility to primary, secondary and tertiary care (Finland)" font "times new roman,16"
# set title "Accessibility to primary, secondary and tertiary care (Brazil)" font "times new roman,16"
# ############################################

set ylabel "Journey duration (h)" font "times new roman,14" off -1,0 

set xlabel "Levels of care" font "times new roman,14"

unset key
set pointsize 1.0
# set style data boxplot
# set style fill   solid 0.80 border lt -1
set style fill solid 0.90 border -1
set style boxplot outliers pointtype 7
set style data boxplot

set bmargin 4 
set lmargin 12
set rmargin 1 
set tmargin 4
# set border 2 front lt black linewidth 1.000 dashtype solid
set boxwidth 0.5 absolute

# set xtics border in scale 0,0 nomirror norotate  autojustify
set xtics  norangelimit 
# set ytics border in scale 1,0.5 nomirror norotate  autojustify
set xrange [ * : * ] noreverse writeback
set x2range [ * : * ] noreverse writeback
set yrange [ 0.00000 : * ] noreverse nowriteback
set y2range [ * : * ] noreverse writeback
set zrange [ * : * ] noreverse writeback
set cbrange [ * : * ] noreverse writeback
set rrange [ * : * ] noreverse writeback
# NO_ANIMATION = 1
## Last datafile plotted: "silver.dat"
# plot 'silver.dat' using (1):2, '' using (2):(5*$3)
set xtics ('Primary Care' 1, 'Secondary Care' 2, 'Tertiary Care' 3)

# ############################################
plot for [i=1:3] 'box.FR.dat' using (i):i
# plot for [i=1:3] 'box.FI.dat' using (i):i
# plot for [i=1:3] 'box.BR.dat' using (i):i
# ############################################

reset
