#################################################################################
#    Description:FreeCeilo project.						#
#    Copyright (C) 2007  George John.All rights reserved.			#
#    Supported by SPACE www.space-kerala.org		 			#
#    Author George John <george@space-kerala.org>	      	   		#
#################################################################################
#    This program is free software: you can redistribute it and/or modify	#
#    it under the terms of the GNU General Public License as published by	#
#    the Free Software Foundation, either version 3 of the License, or		#
#    (at your option) any later version.					#
#										#	
#    This program is distributed in the hope that it will be useful,		#
#    but WITHOUT ANY WARRANTY; without even the implied warranty of		#
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the		#
#    GNU General Public License for more details.				#
#										#
#    You should have received a copy of the GNU General Public License		#
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.	#
#################################################################################
import os,time
import freeceilo.Datadecoding.datadecoding#lib file

datadecodinglib=freeceilo.Datadecoding.datadecoding

class GnuPlot:
	def gnuplot(self):
		s='Scattered Intensities from Ceilometer for '+datadecodinglib.gplot_title[-1]
		val=" set title'"+s+"';"
		f=os.popen('gnuplot' ,'w')
		print >>f,"set xdata time;"
		print >>f, "set format x '%H:%M';"
		print >>f,"set timefmt '%H:%M';"
		print >>f, "set mxtics;"
		print >>f, "set mytics;"
		print >>f, "unset key ;"
		print >>f, "set yrange [0:7700];"#15400
		print >>f, "set xlabel '   Time, hr IST';"
		print >>f,"set ylabel '      Altitude, metres  ';"
		print >>f,val
		print >>f,"set cntrparam bspline;" ##order 6
		print >>f,"set cntrparam levels incremental 0, 100, 500;"
		print >>f,"set contour base;"
		print >>f,"set dgrid3d 200, 200, 2;"
		print >>f,"set pm3d map;"
		print >>f,"set colorbox horiz user origin .1,.06 size .8,.04;"#.02
		print >>f,"set cbrange [0:500];"
		print >>f,'set palette defined ( 0 "white", 0.2 "yellow", 0.4 "orange", 0.6 "red", 0.8 "brown", 1 "black" );'
		print >>f,"set key on right;"
		print >>f,"unset surface;"
		print >>f, "set terminal png  size 810,540;" 
		print >>f, "set out '/tmp/FreeCeilo/.gnu.png';"#600,400
		print >>f, "splot '/tmp/FreeCeilo/datx1.dat'using 2:3:4  with lines ;"
	        time.sleep(1)
		f.flush()

