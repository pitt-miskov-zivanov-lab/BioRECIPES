from graphviz import Digraph
from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image
import pandas as pd

_COLNAMES = [
	# Provenance attributes
	'Source', 'Reader', 'Evidence', 'Evidence Index', 'Notes',
	# Element variable and attributes
	'Element Variable',
	'Element Name', 'Element Text', 'Element Database', 'Element ID', 'Element Type',
	'Element Agent', 'Element Patient',
	'Element ValueJudgment', 'Element Scope',
	'Element Level', 'Element Change', 'Element Degree',
	'Element Location', 'Element Timing',
	# Interaction function and attributes
	'Interaction Function', 
	'Interaction Name', 'Interaction Text', 'Interaction ID', 'Interaction Type', 
	'Interaction Degree',
	'Interaction Location', 'Interaction Timing',
	# Regulator variable and attributes
	'Regulator Variable',
	'Regulator Name', 'Regulator Text', 'Regulator Database', 'Regulator ID', 'Regulator Type',
	'Regulator Agent', 'Regulator Patient',
	'Regulator ValueJudgment', 'Regulator Scope',
	'Regulator Level', 'Regulator Change', 'Regulator Degree',
	'Regulator Location', 'Regulator Timing',
	# Scoring metrics
	'Reader Count', 'Source Count', 'Evidence Count',
	'Total Score', 'Kind Score', 'Match Level', 'Epistemic Value', 'Belief'
	]


def main():
	root = Tk()
	myapp = App( master=root)
	myapp.master.title("Visualization for tabular format")
	myapp.master.maxsize(1600, 800)
	myapp.mainloop()		

class App(Frame):

	def __init__(self, master=None):
		Frame.__init__(self, master)
		self.row = 0
		# defining all widgets
		self.viewWindow=None
		self.img = None
		self.returnButton = None
		self.chooseButton = None
		self.previous = None
		self.next = None
		self.returnButton = None
		self.searchbar = None
		self.submit = None
		# defining all search variab;es
		self.search_key = None
		self.query_result = []
		self.query_index = 0
		# initializing widget
		self.grid(sticky="nsew")
		self.homePage()

	def homePage(self):
		# Text box
		self.title = Label(self, text="Welcome to the translation visualizer!")
		self.title["font"] = ["calibri", 16, "normal"]
		self.title.grid(row=0, column=0, padx=20)
		# File Select Button
		self.chooseButton = Button(self)
		self.chooseButton["text"] = "Select File"
		self.chooseButton["command"] = self.selectFile
		self.chooseButton["width"] = 10
		self.chooseButton["height"] = 3
		self.chooseButton["border"] = 3
		self.chooseButton["font"] = ["calibri", 24, "bold"]
		self.chooseButton["anchor"] = "center"
		self.chooseButton.grid(row=0, column=1, padx=50, pady=80)

		
	def navigation(self):

		# if returning from query
		if self.returnButton:
			self.returnButton.destroy()
			self.searchbar.destroy()
			self.submit.destroy()
		# previous vis
		self.previous = Button(self)
		self.previous["text"] = "Previous"
		self.previous["command"] = self.previousViz
		self.previous["width"] = 10
		self.previous["height"] = 3
		self.previous["border"] = 3
		self.previous["font"] = ["calibri", 24, "bold"]
		self.previous["anchor"] = "center"
		self.previous.grid(row=1, column=0, padx=30, pady=30)
		# next vis
		self.next = Button(self)
		self.next["text"] = "Next"
		self.next["command"] = self.nextViz
		self.next["width"] = 10
		self.next["height"] = 3
		self.next["border"] = 3
		self.next["font"] = ["calibri", 24, "bold"]
		self.next["anchor"] = "center"
		self.next.grid(row=1, column=1, padx=30, pady=30)
		#Search Button
		self.search = Button(self, text="Search",
						   command=self.searchViz, width=10, height=3,
						   border=3, font=["calibri",24,"bold"])
		self.search.grid(row=0, column=1, padx=30, pady=30)

	def previousViz(self):
		if self.row != 0:
			self.row -=1
			self.visualize(self.data_dicts[self.row])
			self.title['text'] = "Now showing row "+str(self.row)+"\n"
		else:
			self.title['text'] = "Too far, go the other way or quit!"


	def nextViz(self):
		if self.row < self.length-1:
			self.row +=1
			self.visualize(self.data_dicts[self.row])
			self.title['text'] = "Now showing row "+str(self.row)+"\n"
		else:
			self.title['text'] = "Too far, go the other way or quit!"

	def searchViz(self):
		# entering from navigation window
		self.next.destroy()
		self.previous.destroy()
		self.search.destroy()

		self.returnButton = Button(self,text="back", command=self.navigation, width=10, height=3, border=3)
		self.returnButton["font"] = ["calibri", 24, "bold"]
		self.returnButton.grid(row=0,column=1,padx=30, pady=30)

		self.searchbar = Entry(self)
		self.searchbar.grid(row=1,column=0,padx=30, pady=30)

		self.submit = Button(self, text="submit query", command=self.queryViz,width=10, height=3, border=3)
		self.submit["font"] = ["calibri", 24, "bold"]
		self.submit.grid(row=1,column=1,padx=30, pady=30)


	def queryViz(self):
		if self.search_key == self.searchbar.get():
			print("next item in search")
			self.query_index +=1
			# resets index value if too high
			if self.query_index >= len(self.query_result):
				self.query_index = 0
			# displaying first item of results
			if self.query_result:
				self.row = self.query_result[self.query_index][1]
				self.visualize(self.query_result[self.query_index][0])
				self.title['text'] = "Now showing row "+str(self.row)+"\n"
			else:
				self.title['text'] = "No matches found"

		else:
			self.search_key = self.searchbar.get()
			self.query_index = 0;
			self.query_result = []
			# creating results list
			element_index = 0
			for row, element in self.data_dicts.items():
				element_index +=1
				print(element)
				for key, value, in element.items():
					if isinstance(value,float):
						self.data_dicts[row][key] = ''
					if self.search_key in self.data_dicts[row][key]:
						print("hey I found something")
						self.query_result.append((self.data_dicts[row],element_index))
						break
			# displaying first item of results
			if self.query_result:
				print(self.query_result)
				self.row = self.query_result[0][1]
				self.visualize(self.query_result[0][0])
				self.title['text'] = "Now showing row "+str(self.row)+"\n"
			else:
				self.title['text'] = "No matches found"


	def selectFile(self):
		# Ask for a file to read
		filePath = filedialog.askopenfilename()
		if '.xlsx' in filePath:
			# get data
			data = pd.read_excel(filePath)
			self.data_dicts = data.to_dict(orient='index')
			self.length = len(self.data_dicts)
			try:
				self.visualize(self.data_dicts[0])
				# update gui
				self.title['text'] = "Now showing row 0"
				self.chooseButton.destroy()
				self.navigation()
			except KeyError:
				self.title['text'] = "File is empty, please select another"
				self.chooseButton.pack(side="top", padx=30, pady=30, fill="both")
		else:
			self.title['text'] = "File is not a spreadsheet, please select another"
			self.chooseButton.pack(side="top", padx=30, pady=30, fill="both")

	def visualize(self, element):

		print(element)
		# cleaning up raw element data
		for key, value in element.items():
			if isinstance(value,float):
				element[key] = ''
		rawText = element.get('Evidence')
		if rawText is None:
			rawText = element.get('Sentence')
		prettyText = []
		for word in rawText.split():
			prettyText.append(word)
			if len(prettyText) % 20 == 0 : prettyText.append('\n') #20 words per line
		prettyText = ' '.join(prettyText)
		print(prettyText)

		# setting up the graph itself
		dot = Digraph(format='png', filename='currElement')
		dot.attr(rankdir='LR', label=prettyText)
		# initializing all affected nodes
		with dot.subgraph(name='cluster_1') as c:
			c.node_attr.update(style='filled')
			c.node('element',element.get('Element Text'))
			if element.get('Element Change') : 
				c.node('elChange', element.get('Element Change'))
				c.edge('element','elChange', arrowhead='none')
			if element.get('Element Location') : 
				c.node('elLocation', element.get('Element Location'))
				c.edge('element','elLocation', arrowhead='none')
			if element.get('Element Timing') : 
				c.node('elTiming', element.get('Element Timing'))
				c.edge('element','elTiming', arrowhead='none')
			if element.get('Element Degree') : 
				c.node('elDegree', element.get('Element Degree'))
				c.edge('element','elDegree', arrowhead='none')
			c.attr(label='Element')
			c.attr(color='blue')
		# initializing all regulator nodes
		with dot.subgraph(name='cluster_2') as c:
			c.node_attr.update(style='filled')
			c.node('regulator',element.get('Regulator Text'))
			if element.get('Regulator Change') : 
				c.node('regChange', element.get('Regulator Change'))
				c.edge('regulator','regChange', arrowhead='none')
			if element.get('Regulator Location') : 
				c.node('regLocation', element.get('Regulator Location'))
				c.edge('regulator','regLocation', arrowhead='none')
			if element.get('Regulator Timing') : 
				c.node('regTiming', element.get('Regulator Timing'))
				c.edge('regulator','regTiming', arrowhead='none')
			if element.get('Regulator Degree') : 
				c.node('regDegree', element.get('Regulator Degree'))
				c.edge('regulator','regDegree', arrowhead='none')
			c.attr(label='Regulator')
			c.attr(color='red')
		# connecting regulators to affected nodes
		dot.edge('regulator', 'element', label=element.get('Interaction Text', 'NA'), penwidth='3.0')
		dot.node_attr.update(style='filled')
		dot.node('regulator', element.get('Regulator Text', 'none'), shape='rectangle')
		dot.node('element', element.get('Element Text', 'none'), shape='rectangle')

		# Rendering image as PNG and displaying in window
		dot.render(view=False)
		if self.viewWindow is None:
			self.viewWindow = Toplevel()
			self.viewWindow.title("GraphViz plot")
		self.render = ImageTk.PhotoImage(Image.open("currElement.png"))
		if self.img is not None:
			self.img.destroy()
		self.img = Label(self.viewWindow, image=self.render)
		self.img.pack()    


if __name__ == '__main__':
	main()