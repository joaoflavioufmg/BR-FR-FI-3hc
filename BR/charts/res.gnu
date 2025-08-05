# > gnuplot
# > load 'hist.gnu' (entre aspas)
# set terminal pngcairo transparent enhanced font "arial,10" fontscale 1.0 size 600, 400
set terminal pngcairo background rgb 'white' enhanced font "times new roman,12" fontscale 2.0 size 1500, 1000 

# ############################################
# set output 'FR_workforce.png'
# set output 'FR_equipment.png'

# set output 'FI_workforce.png'
# set output 'FI_equipment.png'

set output 'BR_workforce.png'
# set output 'BR_equipment.png'
# ############################################


# set border 3 front lt black linewidth 1.000 dashtype solid
# set boxwidth 0.75 absolute
set style fill   solid 1.00 border lt -1
# set grid nopolar
# set grid noxtics nomxtics ytics nomytics noztics nomztics nortics nomrtics \
#  nox2tics nomx2tics noy2tics nomy2tics nocbtics nomcbtics
# set grid layerdefault   lt 0 linecolor 0 linewidth 0.500,  lt 0 linecolor 0 linewidth 0.500
set key outside center bottom horizontal Left reverse invert noenhanced \
autotitle columnhead box lt black linewidth 1.000 dashtype solid  spacing 1 width 1 maxrows 1

set style data histogram
set style histogram cluster gap 1
set style fill solid border -1
set boxwidth 0.9 absolute

# set xtics border in scale 3,1 nomirror norotate  autojustify
# set xtics  norangelimit 
# set xtics   ()
# set ytics border in scale 0,0 mirror norotate  autojustify
# set ztics border in scale 0,0 nomirror norotate  autojustify
# set cbtics border in scale 0,0 mirror norotate  autojustify
# set rtics axis in scale 0,0 nomirror norotate  autojustify

# ############################################
# set title "Workforce for minimum cost universal coverage health care (France)" font "times new roman,16"
# set title "Equipment for minimum cost universal coverage health care (France)" font "times new roman,16"

# set title "Workforce for minimum cost universal coverage health care (Finland)" font "times new roman,16"
# set title "Equipment for minimum cost universal coverage health care (Finland)" font "times new roman,16"

set title "Workforce for minimum cost universal coverage health care (Brazil)" font "times new roman,16"
# set title "Equipment for minimum cost universal coverage health care (Brazil)" font "times new roman,16"
# ############################################

set bmargin 4 
set lmargin 10
set rmargin 2 
set tmargin 4

set auto x
set xrange [ * : * ] noreverse writeback
# set x2range [ * : * ] noreverse writeback

# ############################################
set ylabel "Workforce and beds per 1,000 pop." off -1,0
# set ylabel "Equipment per 1,000,000 pop." off -1,0
# ############################################


set yrange [ 0.00000 : * ] noreverse writeback
# set y2range [ * : * ] noreverse writeback
# set zrange [ * : * ] noreverse writeback
# set cbrange [ * : * ] noreverse writeback
# set rrange [ * : * ] noreverse writeback
# set format y "%'g"
# set colorbox vertical origin screen 0.9, 0.2 size screen 0.05, 0.6 front  noinvert bdefault

# gnuplot > show colornames
set linetype 1 lc rgb "web-blue"
set linetype 2 lc rgb "dark-magenta"

# ############################################
plot 'res.dat' using 2:xtic(1), for [i=3:3] '' using i ti col
# ############################################

reset
