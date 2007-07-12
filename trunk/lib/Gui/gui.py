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
import gtk,gtk.glade,pygtk,matplotlib,os,sys,gobject,time,thread,shutil 
import datetime
import freeceilo.Threads.datadecodethread

from gtk import *
from Numeric import *# for a range
from threading import *
from matplotlib.figure import Figure
from matplotlib.axes import Subplot
from matplotlib.dates import date2num, MINUTES_PER_DAY, SEC_PER_DAY
from matplotlib.backends.backend_gtk import FigureCanvasGTK, NavigationToolbar
from matplotlib.numerix import arange, sin, pi,tan,cos
from pylab import *

datadecodethreadlib=freeceilo.Threads.datadecodethread

matplotlib.use('GTK')
gobject.threads_init()#to prevent the hanging interface
gtk.threads_init()#to prevent the hanging interface
unit="m"
getstatusobj=datadecodethreadlib.GetStatus()
Filename=None
VERSION='0.2'
def progress_timeout(gobj):

  #-------------    Progress bar updating   ----------------#

    if (gobj.datpbar==1 and getstatusobj.getdatastatus()==0):
	gobj.progressbar1.pulse()
	gobj.Open.set_sensitive(False)
    else:
        gobj.progressbar1.set_fraction(0.0)
	

    if (gobj.gnupbar==1 and getstatusobj.getgplotstatus()==0):
	gobj.progressbar2.pulse()

    else:
        gobj.progressbar2.set_fraction(0.0)
  #--------------- Progress bar updating ends ---------------#



  #------- Cloud Detect plot button enabling and disabling --------#

    if (getstatusobj.getdatastatus()==0 or gobj.datpbar==0 ):
	gobj.first_cld_plot_button.set_sensitive(False)
	gobj.second_cld_plot_button.set_sensitive(False)
	gobj.third_cld_plot_button.set_sensitive(False)
	gobj.cld_det_clear_button.set_sensitive(False)
	gobj.cld_det_save_button.set_sensitive(False)

    else:

	gobj.first_cld_plot_button.set_sensitive(True)
	gobj.second_cld_plot_button.set_sensitive(True)
	gobj.third_cld_plot_button.set_sensitive(True)
	gobj.cld_det_clear_button.set_sensitive(True)
	gobj.cld_det_save_button.set_sensitive(True)
	gobj.Open.set_sensitive(True)

  #------ Cloud Detect plot button enabling and disabling -------#

  #--------- Gnu plot button enabling and disabling  ----------#

    if (getstatusobj.getgplotstatus()==0 or gobj.gnupbar==0):

	gobj.gnu_plot_button.set_sensitive(False)
	gobj.gnuplot_zoom_in_button.set_sensitive(False)
	gobj.gnuplot_zoom_normal_button.set_sensitive(False)
	gobj.gnuplot_zoom_out_button.set_sensitive(False)
	gobj.gnuplot_save_button.set_sensitive(False)

    else:
	gobj.gnu_plot_button.set_sensitive(True)
	gobj.gnuplot_zoom_in_button.set_sensitive(True)
	gobj.gnuplot_zoom_normal_button.set_sensitive(True)
	gobj.gnuplot_zoom_out_button.set_sensitive(True)
	gobj.gnuplot_save_button.set_sensitive(True)
  #------ Gnu plot button enabling and disabling  ends ------#

    return True
		
class GuiApp(object):

    def __init__(self):
	global unit
	self.filename=None
	self.gladefile="/usr/share/freeceilo-%s/ceilo.glade" % VERSION
       	self.wTree=gtk.glade.XML(self.gladefile)
       	self.window=self.wTree.get_widget("FreeCeilo")
       	self.window.maximize()

	self.threadvar=0
      #--------buttons---------#
	self.Open=self.wTree.get_widget("Open")
      #-----cloud detection plotting button------#
	self.first_cld_plot_button=self.wTree.get_widget("first_cld_plot_button")
	self.second_cld_plot_button=self.wTree.get_widget("second_cld_plot_button")
	self.third_cld_plot_button=self.wTree.get_widget("third_cld_plot_button")
	self.cld_det_clear_button=self.wTree.get_widget("cld_det_clear_button")
	self.cld_det_save_button=self.wTree.get_widget("cld_det_save_button")
		
      #------------  gnuplot buttons -------------#
	self.gnu_plot_button=self.wTree.get_widget("gnu_plot_button")			
	self.gnuplot_zoom_in_button=self.wTree.get_widget("gnuplot_zoom_in_button")
	self.gnuplot_zoom_normal_button=self.wTree.get_widget("gnuplot_zoom_normal_button")
	self.gnuplot_zoom_out_button=self.wTree.get_widget("gnuplot_zoom_out_button")	
	self.gnuplot_save_button=self.wTree.get_widget("gnuplot_save_button")

      #--------buttons ends---------#

      #------progressbars------#

	self.progressbar1=self.wTree.get_widget("progressbar1")

	self.progressbar2=self.wTree.get_widget("progressbar2")

        self.progressbar1.set_fraction(0.0)
	self.datpbar=0

        self.progressbar2.set_fraction(0.0)
	self.gnupbar=0

	self.timer = gobject.timeout_add (100, progress_timeout, self)

     #------gnu plot image normal size ----#

	self.imagex= 810
	self.imagey=540
	self.gnuplot_image=self.wTree.get_widget("gnuplot_image")
	self.x=0

     #--------Handles events



	dic={"on_FreeCeilo_destroy":self.quitprogram,"on_Open_activate":self.openfile,
	"on_first_cld_plot_button_clicked":self.firstcloudshow,"on_second_cld_plot_button_clicked"
	:self.secondcloudshow,"on_third_cld_plot_button_clicked":self.thirdcloudshow,	
	"on_zoom_in_x_activate":self.clouddetectzoominx,"on_zoom_out_x_activate":
	self.clouddetectzoomoutx,"on_zoom_in_y_activate":self.clouddetectzoominy,
	"on_zoom_out_y_activate":self.clouddetectzoomouty,"on_cld_det_save_button_clicked"
	:self.clouddetectsave,"on_cld_det_clear_button_clicked":self.clouddetectgraphclear,
	"on_gnu_plot_button_clicked":self.gnuplotshow,"on_gnuplot_zoom_in_button_clicked":
	self.gnuplotzoomin,"on_gnuplot_zoom_normal_button_clicked":self.gnuplotzoomnormal,
	"on_gnuplot_zoom_out_button_clicked":self.gnuplotzoomout,"on_gnuplot_save_button_clicked"
	:self.gnuplotsave}
        self.wTree.signal_autoconnect(dic)


     #-----plotting area for graphs
	
	self.graphview = self.wTree.get_widget("hbox7")

     #-----plotting area for cloud detection graph
 
       	self.figure1 = Figure(figsize=(12,6),facecolor='y',dpi=55,edgecolor='black',linewidth=5.0)
	self.axis1 = self.figure1.add_subplot(111)
	self.axis1.grid(True)

	self.canvas1 = FigureCanvasGTK(self.figure1)
	self.graphview.pack_start(self.canvas1,True,True)
        self.canvas1.show()
	self.axis1.set_autoscale_on(True)

    #-----plotting area for back scatterprofile

	self.figure2 = Figure(figsize=(12,6),facecolor='y', dpi=55,edgecolor='black',linewidth=4.0)
	self.axis2 = self.figure2.add_subplot(111)
	self.axis2.grid(True)
        self.canvas2 = FigureCanvasGTK(self.figure2) 
	self.graphview.pack_end(self.canvas2,True,True)
        self.canvas2.show()

################################# File Openning and dataprocessing #######################
    def openfile(self,obj):
	self.filename=None
	if(self.threadvar==1):
		os.system("killall -9 gnuplot > /dev/zero")
		self.datpbar=0
		self.gnupbar=0
		self.datadecode_thread_obj.stop()
	dialog = gtk.FileChooserDialog("Open..",
                              None,
                              gtk.FILE_CHOOSER_ACTION_OPEN,
                              (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                               gtk.STOCK_OPEN, gtk.RESPONSE_OK))
	dialog.set_default_response(gtk.RESPONSE_OK)
	filter = gtk.FileFilter()
	filter.set_name("DATA FILES")
	filter.add_pattern("*.dat")
	dialog.add_filter(filter)
	response=dialog.run()
	if response == gtk.RESPONSE_OK:
        	self.filename=dialog.get_filename()
		self.window.set_title("Free Ceilo 0.1 ( "+self.filename+")")
		self.datpbar=1
		self.gnupbar=1
    	     #---- Threads for datadecoding ,gnuplot ---#
		cond=Condition()
		self.datadecode_thread_obj=datadecodethreadlib.DataDecodeThread(cond,self.filename)
		self.datadecode_thread_obj.start()
		self.threadvar=1
             #---- Threads ends ------#
	elif response == gtk.RESPONSE_CANCEL:
       		print 'Closed, no files selected'
	dialog.destroy()

###############################Cloud Detection Graph Plotting #######################

   ##### Show the first cloud  ######

    def firstcloudshow(self,obj):
	
	self.x= getstatusobj.getdataobj()
        self.axis1.set_xlabel('Time')
        self.axis1.set_ylabel('Altitude'+","+unit)
        self.axis1.set_title('Cloud Detection Graph')
	self.axis1.grid(True)
	self.axis1.plot_date(self.x.lwst_time_index,self.x.lwst_cldbse_hgt,'b.',label=" First")
	self.axis1.xaxis.set_major_locator(MaxNLocator(6))

     ####-------for rotating the xticks------------------###########
	#labels = self.axis1.get_xticklabels()
	#setp(labels, rotation=90, fontsize=10)

	self.axis1.legend()
	self.canvas1.draw()

   ##### Show the second cloud  ######

    def secondcloudshow(self,obj):
	self.x= getstatusobj.getdataobj()
        self.axis1.set_xlabel('Time')
        self.axis1.set_ylabel('Altitude'+","+unit)
        self.axis1.set_title('Cloud Detection Graph')
	self.axis1.grid(True)
	self.axis1.plot_date(self.x.sec_time_index,self.x.sec_lwst_cldbse_hgt,'g.',label="Second")
	self.axis1.xaxis.set_major_locator(MaxNLocator(6))
	self.axis1.legend()
	self.canvas1.draw()

   ##### Show the third cloud  ######

    def thirdcloudshow(self,obj):
	self.x= getstatusobj.getdataobj()
        self.axis1.set_xlabel('Time')
        self.axis1.set_ylabel('Altitude'+","+unit)
        self.axis1.set_title('Cloud Detection Graph')
	self.axis1.grid(True)
	self.axis1.plot_date(self.x.higst_time_index,self.x.higst_cldbse_hgt,'r.',label="Third")
	self.axis1.xaxis.set_major_locator(MaxNLocator(6))
	self.axis1.legend()
	self.canvas1.draw()
    
   ####---------Zooming the figure--------########  

    def clouddetectzoominx(self,obj):
	self.axis1.zoomx(2)
	self.canvas1.draw()

    def clouddetectzoomoutx(self,obj):
	self.axis1.zoomx(-2)
	self.canvas1.draw()


    def clouddetectzoominy(self,obj):
	self.axis1.zoomy(2)
	self.canvas1.draw()

    def clouddetectzoomouty(self,obj):
	self.axis1.zoomy(-2)
	self.canvas1.draw()

    def clouddetectgraphclear(self,obj):
	self.axis1.clear()
	self.axis1.set_xlabel('Time')
        self.axis1.set_ylabel('Altitude'+","+unit)
        self.axis1.set_title('Cloud Detection Graph')
	self.axis1.grid(True)
	self.canvas1.draw()

  #############SAVE CLD DETECT#########

    def clouddetectsave(self,obj):
	dialog= gtk.FileChooserDialog("Save Cloud Detection Graph ",
                               None,
                               gtk.FILE_CHOOSER_ACTION_SAVE,
                               (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                gtk.STOCK_SAVE, gtk.RESPONSE_OK))
	dialog.set_default_response(gtk.RESPONSE_OK)
	dialog.set_current_folder(os.curdir)
	dialog.set_do_overwrite_confirmation(True)
	filter = gtk.FileFilter()
	filter.set_name("image(png) file")
	filter.add_pattern("*.png")
	dialog.add_filter(filter)
	response=dialog.run()
	if response == gtk.RESPONSE_OK:
         	plotimagefile=dialog.get_filename()
		dialog.destroy()
		#self.canvas1.print_figure1(plotimagefile, 72,'w', 'w','portrait')
	       	self.figure1.savefig(plotimagefile)
		self.canvas1.destroy()
		self.canvas1 = FigureCanvasGTK(self.figure1) 
		self.graphview.pack_start(self.canvas1, True,True)
        	self.canvas1.show()
	elif response == gtk.RESPONSE_CANCEL:
		print "no file is selected"
		dialog.destroy()
	self.canvas1.show()



##########################################GNUPLOT####################################

 #--------- The Functions to display Gnuplot image and zoom the images and save------#

    def gnuplotshow(self,obj):
	self.gnuplot_image.set_from_file("/tmp/FreeCeilo/.gnu.png")
	#----Functions to zoom the images----#
    def gnuplotzoomin(self,obj):
	self.imagex+=30
	self.imagey+=20
	self.gnuplotzoom()
    def gnuplotzoomout(self,obj):
	self.imagex-=30
	self.imagey-=20
	self.gnuplotzoom()
    def gnuplotzoomnormal(self,obj):
	self.imagex=810
	self.imagey=540
	self.gnuplotzoom()
    def gnuplotzoom(self):
	self.gnuplot_image.set_from_pixbuf(gtk.gdk.pixbuf_new_from_file("/tmp/FreeCeilo/.gnu.png").scale_simple(self.imagex,self.imagey,gtk.gdk.INTERP_BILINEAR))

	#---Function to save the gnuplot image in another location using save as option---#

    def gnuplotsave(self,obj):
	dialog= gtk.FileChooserDialog("Save as..",
                         None,
                         gtk.FILE_CHOOSER_ACTION_SAVE,
                         (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                         gtk.STOCK_SAVE, gtk.RESPONSE_OK))
	dialog.set_default_response(gtk.RESPONSE_OK)
	dialog.set_do_overwrite_confirmation(True)
	filter = gtk.FileFilter()
	filter.set_name("image(png) file")
	filter.add_pattern("*.png")
	dialog.add_filter(filter)
	response=dialog.run()
	if response == gtk.RESPONSE_OK:
        	plotimagefile=dialog.get_filename()
		if not plotimagefile.endswith(".png"):
			k=plotimagefile.find(".")
			plotimagefile=plotimagefile[0:k]
			plotimagefile=plotimagefile.__add__(".png")
		shutil.copyfile("/tmp/FreeCeilo/.gnu.png",plotimagefile)
	elif response == gtk.RESPONSE_CANCEL:
		print "no file is selected"
	dialog.destroy()



#################################  Quit the Program #########################

    def quitprogram(self,obj):
	self.id1=os.getpid()
       	gobject.source_remove(self.timer)
       	self.timer = 0
	gtk.main_quit()
	os.system("killall -9 gnuplot > /dev/zero")
	os.popen("kill -9 "+str(self.id1))
	sys.exit(0)


