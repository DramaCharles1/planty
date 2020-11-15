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
		self.fig, self.ax = plt.subplots()
		#self.thisPlot = plt.subplot(Plots.rows,Plots.cols,Plots.index)
			
	def CreatelinePlot(self):
		self.ax.plot(self.xdata, self.ydata, label = self.label, color = "green")
		plt.xlabel(self.xlabel) 
		plt.ylabel(self.ylabel) 
		self.ax.legend()
		#plt.show()
		plt.savefig(self.fileName,bbox_inches='tight')
		
	def Create2linePlot(self):
		self.ax.plot(self.xdata, self.ydata, label = self.label)
		self.ax.plot(self.xdata, self.y2data, label = self.label2)
		plt.xlabel(self.xlabel) 
		plt.ylabel(self.ylabel) 
		self.ax.legend()
		#plt.show()
		plt.savefig(self.fileName,bbox_inches='tight')
		
	
