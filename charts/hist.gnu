# > gnuplot
# > load 'hist.gnu' (entre aspas)
# set terminal pngcairo transparent enhanced font "arial,10" fontscale 1.0 size 600, 400
set terminal pngcairo background rgb 'white' enhanced font "times new roman,10" fontscale 3.0 size 3000, 2000 

# ############################################
# set output 'histograms.BR.png'
# set output 'histograms.FR.png'
set output 'histograms.FI.png'
# ############################################

# set term pos eps font 10
# set output 'histograms.BR.eps'
# set border 3 front lt black linewidth 1.000 dashtype solid
set boxwidth 0.75 absolute
set style fill   solid 1.00 border lt -1
# set grid nopolar
# set grid noxtics nomxtics ytics nomytics noztics nomztics nortics nomrtics \
#  nox2tics nomx2tics noy2tics nomy2tics nocbtics nomcbtics
# set grid layerdefault   lt 0 linecolor 0 linewidth 0.500,  lt 0 linecolor 0 linewidth 0.500
set key outside center bottom horizontal Left reverse invert noenhanced \
autotitle columnhead box lt black linewidth 1.000 dashtype solid  spacing 1 width 1 maxrows 1
set style histogram columnstacked title textcolor lt -1
# unset parametric
# set datafile missing '-'
set style data histograms
# set xtics border in scale 3,1 nomirror norotate  autojustify
# set xtics  norangelimit 
# set xtics   ()
# set ytics border in scale 0,0 mirror norotate  autojustify
# set ztics border in scale 0,0 nomirror norotate  autojustify
# set cbtics border in scale 0,0 mirror norotate  autojustify
# set rtics axis in scale 0,0 nomirror norotate  autojustify

set title "Model results for health care costs (per level of care)" font "times new roman,12"

# ############################################
# set xlabel "Brazilian states"
# set xlabel "French regions"
set xlabel "Finnish regions"
# ############################################

set bmargin 6 
set lmargin 12
set xrange [ * : * ] noreverse writeback
# set x2range [ * : * ] noreverse writeback
set ylabel "Million dolars" off -1,0
set yrange [ 0.00000 : * ] noreverse writeback
# set y2range [ * : * ] noreverse writeback
# set zrange [ * : * ] noreverse writeback
# set cbrange [ * : * ] noreverse writeback
# set rrange [ * : * ] noreverse writeback
# set format y "%'g"
set colorbox vertical origin screen 0.9, 0.2 size screen 0.05, 0.6 front  noinvert bdefault
set linetype 1 lc rgb "blue"
set linetype 2 lc rgb "green"
set linetype 3 lc rgb "red"
set linetype 4 lc rgb "yellow"
# NO_ANIMATION = 1
# set key center bottom
## Last datafile plotted: "immigration.dat"
# plot 'hist.dat' using 6 ti col, '' using 12 ti col,      '' using 13 ti col, '' using 14:key(1) ti col
# plot 'hist.dat' using 2:xtic(1), for [i=3:26] '' using i, '' using 27:key(1) ti col
# plot 'hist.dat' using 2 t col, for [i=3:26] '' using i t col, '' using 27:key(1) t col

# ############################################
# plot 'hist.dat' using 2:key(1), for [i=3:27] '' using i    # BR
# plot 'hist.dat' using 2:key(1), for [i=3:14] '' using i  # FR
plot 'hist.dat' using 2:key(1), for [i=3:20] '' using i  # FI
# ############################################
