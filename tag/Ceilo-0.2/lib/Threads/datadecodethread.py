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
import thread,threading,time,os
import freeceilo.Datadecoding.datadecoding,freeceilo.GnuPlot.gplot

from threading import *
from Numeric import *# for a range

datadecodinglib=freeceilo.Datadecoding.datadecoding
gplotlib=freeceilo.GnuPlot.gplot

datastatus=0
gplotstatus=0
File_name_obj=None
class GetStatus:

    def getgplotstatus(self):
	return gplotstatus

    def getdatastatus(self):
	return datastatus

    def getdataobj(self):
	return 	File_name_obj	

class DataDecodeThread(Thread):

    def __init__(self,condition,filename,sleeptime=.001):
        Thread.__init__(self)
	self.stopthread=threading.Event()
        self.cond=condition
        self.filename=filename
        self.sleeptime=sleeptime
	global datastatus,gplotstatus
	datastatus=0
	gplotstatus=0
    def run(self):
	global File_name_obj,datastatus
        self.filename
	self.cond.acquire()
        time.sleep(self.sleeptime)
	File_name_obj=datadecodinglib.DataDecoding()
	File_name_obj.cleardata()
	File_name=open(self.filename,"r")
	File_name_obj.processingdata(File_name,File_name_obj)
	datastatus=1
	self.gplotthread()
	self.cond.release()
	self.stop()
    def gplotthread(self):
	global gplotstatus
	os.system("killall -9 gnuplot > /dev/zero")
        time.sleep(.001)
	Gplot_obj=gplotlib.GnuPlot()
	Gplot_obj.gnuplot()
	gplotstatus=1
    def stop(self):
	print "Threadstopped"
	self.stopthread.set()



