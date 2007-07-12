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
import datetime,os,thread,time
import freeceilo.Log.writelog #lib file
	
from matplotlib.dates import date2num, MINUTES_PER_DAY, SEC_PER_DAY
from user import home

writeloglib=freeceilo.Log.writelog

gplot_title=[]
def time_convert(s): ### convert time into datetime formatt
	d0 = date2num(datetime.date(int(s[0:4]),int(s[5:7]),int(s[8:11])))
	st=s[11:]
	h,m,s = map(float,st.split(':'))
	return d0 + h/24. + m/MINUTES_PER_DAY + s/SEC_PER_DAY
class DataDecoding:  #read.py
	def __init__(self):
		self.line1=[]
		self.line2=[]
		self.line3=[]
		self.line4=[]
		self.line5=[]
		self.line6=[]
		self.i=0
		self.ceilo_list=[]
		self.timeindex=[]
		self.lwst_time_index=[]
		self.sec_time_index=[]
		self.higst_time_index=[]
		self.lwst_cldbse_hgt=[]
		self.sec_lwst_cldbse_hgt=[]
		self.higst_cldbse_hgt=[]

	def cleardata(self):
		self.ceilo_list=[]
		self.i=0
		self.timeindex=[]
		self.lwst_time_index=[]
		self.sec_time_index=[]
		self.higst_time_index=[]
		self.lwst_cldbse_hgt=[]
		self.sec_lwst_cldbse_hgt=[]
		self.higst_cldbse_hgt=[]

	def readfile(self,File):

		self.time=File.readline()
		if len(self.time)!=0:
			self.line1=File.readline()
			self.line2=File.readline()
			self.line3=File.readline()
			self.line4=File.readline()
			self.line5=File.readline()
			if (self.line1[7]=='2'):
				self.line6=File.readline()
		
		return self.time



	def processingdata(self,FileName,FileNameObject):
           dat_file=file("/tmp/FreeCeilo/datx1.dat","w")
	   self.i=0
	   while 1:
		TimeIndex=self.readfile(FileName)
		if len(TimeIndex)==0:
			dat_file.close()
			break
		self.ceilo_list.append(writeloglib.Log())
		self.ceilo_list[-1].assign(FileNameObject)
		if len(self.ceilo_list)==1:
			global gplot_title
			gplot_title=[]
			gplot_title.append(self.ceilo_list[-1].time[0:10])
			print "time",gplot_title
			logfile=file("%s/FreeCeilo/log/"%home+self.ceilo_list[-1].time[0:10]+".log","w")	
			logfile.write(" Log report generated  by  Free ceilo 0.1")
			logfile.write("  \n (c)  SPACE  \n mail :contact@space-kerala.org  ")
			logfile.close()
			dat_file.write(" Date   \t  Time   \t  Bck Profile 0  \t  Bck Profile 1  \n\n")
		self.ceilo_list[-1].logwrite()
        	time.sleep(.001)
		for k in range(0,self.ceilo_list[-1].sample_length):
			dat_file.write(self.ceilo_list[-1].time[0:10]+"\t "+self.ceilo_list[-1].time[11:16]+"\t \t\t"+str(self.ceilo_list[-1].bck_sctr_prfl[k][0])+"\t\t\t"+str(self.ceilo_list[-1].bck_sctr_prfl[k][1])+"\n")
		if self.ceilo_list[-1].det_stat=='1':
			self.timeindex.append(self.ceilo_list[self.i].time[0:10])
			self.lwst_time_index.append(time_convert(self.ceilo_list[self.i].time))
			self.lwst_cldbse_hgt.append(self.ceilo_list[self.i].low_cloudbase_hight)
		elif self.ceilo_list[-1].det_stat=='2':
			self.timeindex.append(self.ceilo_list[self.i].time)
			self.lwst_time_index.append(time_convert(self.ceilo_list[self.i].time))
			self.sec_time_index.append(time_convert(self.ceilo_list[self.i].time))
			self.lwst_cldbse_hgt.append(self.ceilo_list[-1].low_cloudbase_hight)
			self.sec_lwst_cldbse_hgt.append(self.ceilo_list[-1].second_cloudbase_hight)
		elif self.ceilo_list[-1].det_stat=='3':
			self.timeindex.append(self.ceilo_list[self.i].time)
			self.lwst_time_index.append(time_convert(self.ceilo_list[self.i].time))
			self.sec_time_index.append(time_convert(self.ceilo_list[self.i].time))
			self.higst_time_index.append(time_convert(self.ceilo_list[self.i].time))
			self.lwst_cldbse_hgt.append(self.ceilo_list[-1].low_cloudbase_hight)
			self.sec_lwst_cldbse_hgt.append(self.ceilo_list[-1].second_cloudbase_hight)
			self.higst_cldbse_hgt.append(self.ceilo_list[-1].high_cloudbase_hight)
		
		self.i+=1


	 
