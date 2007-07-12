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
class Settings:
	t={'0':'0000','1':'0001','2':'0010','3':'0011','4':'0100','5':'0101','6':'0110','7':'0111','8':'1000','9':'1001',
   'a':'1010','b':'1011','c':'1100','d':'1101','e':'1110','f':'1111','A':'1010','B':'1011','C':'1100','D':'1101','E':'1110','F':'1111'}
	dicti={(0,0):"Transmitter shut off",(0,1):"Transmitter failure",(0,2):"Receiver failure",(0,3):"Voltage Failure",
		   (1,0):"Alignment Failure",(1,1):"Memory error",(1,2):"Light path obstruction",(1,3):"Receiver saturation",
		   (2,0):"(spare)(A)",(2,1):"(spare)(A)",(2,2):"(spare)(A)",(2,3):"(spare)(A)",
		   (3,0):"(spare)(A)",(3,1):"(spare)(A)",(3,2):"Coaxial cable failure",(3,3):"Ceilometer engine board failure",
		   (4,0):"Window contamination",(4,1):"Battery voltage low",(4,2):"Transmitter expires",(4,3):"High humidity",
		   (5,0):"spare(W)",(5,1):"Blower failure",(5,2):"spare(W)",(5,3):"Humidity sensor failure",
		   (6,0):"Heater fault",(6,1):"High background radiance ",(6,2):"Ceilomater engine board failure",(6,3):"Battery failure",
		   (7,0):"Laser monitor failure",(7,1):"Receiver warning",(7,2):"Tilt angle>45 degrees warning",(7,3):"spare(W)",
		   (8,0):"Blower is on ",(8,1):"Blower heater is on ",(8,2):"Internal heater is on ",(8,3):"Working from battery",
		   (9,0):"Stand by mode is on ",(9,1):"Self test in progress",(9,2):"Manual data acquisition settings are effected",	    (9,3):"spare(S)",
		   (10,0):"Units are meters if on else feet",(10,1):"Manual blower control",(10,2):"Polling mode is on ",(10,3):"spare(S)",
		   (11,0):"spare(S)",(11,1):"spare(S)",(11,2):"spare(S)",(11,3):"spare(S)"}
	date=[]
