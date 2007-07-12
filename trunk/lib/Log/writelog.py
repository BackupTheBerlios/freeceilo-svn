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
import string,os
import freeceilo.Ceilosettings.ceilosettings
from user import home

ceilosettingslib=freeceilo.Ceilosettings.ceilosettings

class Log:
	def __init__(self):
		self.time=None
		self.unit_id=None
		self.sw_id=None
		self.msg_no=None
		self.subclass_msg=None
		self.msg_s=None
		self.det_stat=None
		self.warn_alarm=None
		self.low_cloudbase_hight=None
		self.second_cloudbase_hight=None
		self.high_cloudbase_hight=None
		self.aws_stat=None
		self.aws_stat_list=[]
		self.bck_sctr_prfl=[]
		self.bsp_list=[]
		self.log_file=[]
		self.bsp_res=[]
		self.tilt_angle=[]
		self.prof_len=[]

	def assign(self,readobj):
		self.time=readobj.time
		#print self.time
		self.unit_id=readobj.line1[3]
		self.sw_id=int(readobj.line1[4:6])
		self.msg_no=int(readobj.line1[7])
		self.subclass_msg=int(readobj.line1[8])
		self.unit=int(readobj.line2[31])
#########-------------determine the unit --------------##############
		if self.unit>=8:#for meter
			convert=1
		else:
			convert=0.3048
#########--------------determine the sample length-----##############
		if(self.subclass_msg==1):
			self.sample_length=770
			self.message_length=3850
			self.height_increment=10
		elif(self.subclass_msg==2):
			self.sample_length=385
			self.message_length=1925
			self.height_increment=20
###line2	
		self.det_stat=readobj.line2[0]#int( is removed
		self.warn_alarm=readobj.line2[1]#int( is removed
###line 2 heaxa decimel_status 
		self.aws_stat=readobj.line2[21:33]

		if (self.msg_no==1):
			self.line4=readobj.line3
			self.line5=readobj.line4
		if (self.msg_no==2):
			self.line4=readobj.line4
			self.line5=readobj.line5

		if self.det_stat=='1':
			self.low_cloudbase_hight=int(readobj.line2[3:8])*convert
		       
		elif self.det_stat=='2':
			self.low_cloudbase_hight=int(readobj.line2[3:8])*convert
			self.second_cloudbase_hight=int(readobj.line2[9:14])*convert
		elif self.det_stat=='3':
			self.low_cloudbase_hight=int(readobj.line2[3:8])*convert
			self.second_cloudbase_hight=int(readobj.line2[9:14])*convert
			self.high_cloudbase_hight=int(readobj.line2[15:20])*convert
		elif self.det_stat=='4':
			self.vertical_visibility=int(readobj.line2[3:8])*convert
			self.highest_signal_det=int(readobj.line2[9:14])*convert		

		for i in range(21,33):
			temp=ceilosettingslib.Settings.t[readobj.line2[i]]
			
			self.aws_stat_list.append(temp)	# alarm warning internel status
		
		k=0
		for i in range(0,self.message_length,5):
			k+=self.height_increment
			if self.line5[i]=='f':
					t= int(self.line5[i+1:i+5],16)
					val=self.d2b(t)
			else:
					val=int(self.line5[i+1:i+5],16)	
			self.bck_sctr_prfl.append((k,val))
		for k in range(0,self.sample_length):
			self.bsp_list.append(self.bck_sctr_prfl[k][1])
		self.bsp_res=self.line4[6:8]
		self.tilt_angle=self.line4[26:28]
		self.prof_len=int(self.line4[9:13])
		
	def logwrite(self):
		log_message=LogInit()#t1=log_message

	 	self.log_file=file("%s/FreeCeilo/log/"%home+self.time[0:10]+".log","a")		

		self.log_file.write("\n ------------------------------------------------------------------------------------- \n ")
		self.log_file.write("\n time :\t "+self.time[11:19])
		self.log_file.write("\n unit id is \t  "+str(self.unit_id)+'\t')
		self.log_file.write( "\t sw id is \t "+str(self.sw_id)+'\t')
		if self.msg_no==1:
			self.log_file.write( " \t message  without sky condition")
			if self.subclass_msg==1:
				
				log_message.assign(10,"msg1_10*770",3956,28.8,4890,4800,815)
				self.msg_s=log_message.string()
			elif self.subclass_msg==2:
				log_message.assign(10,"msg1_20*385",2031,14.4,2510,2400,418)
				self.msg_s=log_message.string()
			elif self.subclass_msg==3:
				log_message.assign(5,"msg1_5*1500",7606,28.8,6267,9600,1253)
				self.msg_s=log_message.string()
			elif self.subclass_msg==4:
				log_message.assign(5,"msg2_5*770",3956,14.4,3260,4800,625)
				self.msg_s=log_message.string()
			elif self.subclass_msg==5:
				log_message.assign(5,"msg1_base",55,300,45,300,9)
				self.msg_s=log_message.string()
			else:
				self.msg_s="No Error Detected"
		if self.msg_no==2:
			self.log_file.write( " \n message   with sky condition")
			if self.subclass_msg==1:
				log_message.assign(10,"msg2_10*770",3993,28.8,4940,4800,423)
				self.msg_s=log_message.string()
			elif self.subclass_msg==2:
				log_message.assign(10,"msg2_20*385",2068,14.4,2560,2400,425)
				self.msg_s=log_message.string()
			elif self.subclass_msg==3:
				log_message.assign(5,"msg1_5*1500",7643,28.8,6230,9600,1260)
				self.msg_s=log_message.string()
			elif self.subclass_msg==4:
				log_message.assign (5,"msg2_5*770",3993,14.4,3290,4800,660)
				self.msg_s=log_message.string()
			elif self.subclass_msg==5:
				log_message.assign(10,"msg2_base",92,600,114,300,19)
				self.msg_s=log_message.string()
			else:
				self.msg_s="No Error Detected"
		self.log_file.write('\n Message _Resolution \t '+str(self.msg_s))
		if self.det_stat=='1':
			self.log_file.write('\n lowest cloud detected h='+str(self.low_cloudbase_hight))
		elif self.det_stat=='2':
			self.log_file.write("\n lowest and second lowest cloud detected ")
			self.log_file.write("\n lowest="+str(self.low_cloudbase_hight)+"\t second lowest="+str(self.second_cloudbase_hight))
		elif self.det_stat=='3':
			self.log_file.write("\n three cloud base detected ")
			self.log_file.write("\n lowest="+str(self.low_cloudbase_hight)+" \t  second lowest="+str(self.second_cloudbase_hight))
			self.log_file.write("\t  third cloudbase="+str( self.high_cloudbase_hight))
		elif self.det_stat=='4':
			self.log_file.write("\n no cloud base detected ")
			self.log_file.write("\n vertical visibility="+str(self.vertical_visibility))
			self.log_file.write("\t highest signal="+str( self.highest_signal_det))
		elif self.det_stat=='5':
			self.log_file.write("\n some obstruction detected but transparent")
		elif self.det_stat=='/':
			self.log_file.write("\n Raw data input to algorithm missing or suspend")
			i=0
			for i in range (0,11):
				 ch=self.aws_stat_list[i]
		                 j=0
				 while j<4:
					if ch[j]=="1":
						self.log_file.write("\n \t stat list "+str(ceilosettingslib.Settings.dicti[(i,j)]))
					
					j=j+1
		
		self.log_file.close()

	def d2b(self,n):
		bStr =" "
    		if n < 0:  raise ValueError, "must be a positive integer"
    		if n == 0: bStr= '0'
   		while n > 0:
        		bStr = str(n % 2) + bStr
        		n = n >> 1
		bStr=string.replace(bStr,'1','x')
		bStr=string.replace(bStr,'0','1')
		bStr=string.replace(bStr,'x','0')
        	a=int(bStr,2)+int('1',2)
		y=a*-1
		return y
class LogInit:#message==logint
	def __init__(self):
		self.resolution=0
		self.name=0
		self.length=0
		self.MinBPS_2=0
		self.DpM_2=0
		self.MinBPS_12=0
		self.DpM_12=0
	def assign(self,val1,val2,val3,val4,val5,val6,val7):
		self.resolution=val1
		self.name=val2
		self.length=val3
		self.MinBPS_2=val4
		self.DpM_2=val5
		self.MinBPS_12=val6
		self.DpM_12=val7
	def string(self):
		 return  "resolution="+str(self.resolution)+" \n name="+self.name+"\n length="+str(self.length)+"  \n Min BPS _2="+str(self.MinBPS_2)+"\n DpM_2= "+str(self.DpM_2)+" \n MinBPS_12="+str(self.MinBPS_12)+"\n DpM_12="+str(self.DpM_12)		
		
