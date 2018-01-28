#!/usr/bin/gnuplot
set grid
set ylabel "Height of the Sun [deg]"
set y2label "Irradiation [W/m^2]"
set xtics 30
set arrow from 0,0 to 360,0 nohead
set ytics nomirror
set y2tics
set xlabel "Azimuth"
set term png size 1000,1000
set out "docs/path.png"
plot "docs/sun.dat" u 2:3 w p axis x1y1 title "Altitude", "docs/sun.dat" u 2:4 w p axis x1y2 title "Radiation"
