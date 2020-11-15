import matplotlib.pyplot as plt
from shutil import copyfile

class Plots:
	def __init__(self,xdata,ydata,y2data,xlabel,ylabel,fileName,label,label2):
		self.xdata = xdata
		self.ydata = ydata
		self.y2data = y2data
		self.xlabel = xlabel
		self.ylabel = ylabel
		self.label = label
		self.label2 = label2
		self.fileName = fileName
			
	def CreatelinePlot(self):
		plt.plot(self.xdata, self.ydata, label = self.label, color = "green")
		plt.xlabel(self.xlabel) 
		plt.ylabel(self.ylabel) 
		plt.legend()
		#plt.show()
		plt.savefig(self.fileName,bbox_inches='tight')
		
	def Create2linePlot(self):
		plt.plot(self.xdata, self.ydata, label = self.label)
		plt.plot(self.xdata, self.y2data, label = self.label2)
		plt.xlabel(self.xlabel) 
		plt.ylabel(self.ylabel) 
		plt.legend()
		#plt.show()
		plt.savefig(self.fileName,bbox_inches='tight')
		
	
