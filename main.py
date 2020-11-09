import pygame
import math
import subprocess
#subprocess.run(['pip','install','heapdict'])
import heapdict
import sys
import random
pygame.init()
#subprocess.run(['pip','install','pygame'])

BLACK=(0,0,0)
WHITE=(255,255,255)
RED=(255,0,0)
GREEN=(0,255,0)
BLUE=(0,0,255)
GREY=(122,122,122)

class app:

	def __init__(self,num=70):
		self.win=pygame.display.set_mode((500,500))
		pygame.display.set_caption('Pathfinding Visualizer')
		self.rectdict={}
		self.blocked=[]
		self.x=0
		self.y=0
		self.width=10
		self.num=num
		self.loop=True
		self.new=True
		self.start=False
		self.end=False
	
	def drawRect(self):
		for i in range(self.num):
			for j in range(self.num):
				a=pygame.draw.rect(self.win,WHITE,(self.x+j*self.width,self.y+i*self.width,self.width,self.width))
				self.rectdict[i,j]=a
		pygame.display.update()
		return
	
	def flush(self):
		self.start=None
		self.end=None
		self.blocked=[]
		self.rectdict={}
		self.drawRect()
		
	def run(self):
		while self.loop:
			for event in pygame.event.get():
				if event.type==pygame.QUIT:
					self.loop=False
					pygame.quit()
					sys.exit()
				if self.new:
					self.new=False
					self.drawRect()
				if event.type==pygame.KEYDOWN:
					if event.key==pygame.K_0:
						algorithms(self.win,self.rectdict,self.start,self.end,self.blocked).djikstra()
					if event.key==pygame.K_2:
						algorithms(self.win,self.rectdict,self.start,self.end,self.blocked).greedy()
					if event.key==pygame.K_1:
						algorithms(self.win,self.rectdict,self.start,self.end,self.blocked).astar()
					if event.key==pygame.K_n:
						self.flush()
					if event.key==pygame.K_s:
						maze(self.win,self.rectdict,self.start,self.end,self.blocked,self.num)
				if event.type==pygame.MOUSEMOTION or event.type==pygame.MOUSEBUTTONDOWN:
					for rect in self.rectdict:
						rectt=self.rectdict[rect]
						if rectt.collidepoint(pygame.mouse.get_pos()):
							if not self.start:
								pygame.draw.rect(self.win,BLUE,(rectt.x,rectt.y,rectt.width,rectt.height))
								if rect in self.blocked:
									self.blocked.remove(rect)
								self.start=rect
								pygame.display.update()
							elif not self.end:
								if rect!=self.start:
									pygame.draw.rect(self.win,BLUE,(rectt.x,rectt.y,rectt.width,rectt.height))
									if rect in self.blocked:
										self.blocked.remove(rect)
									self.end=rect
									pygame.display.update()
							else:
								if rect!=self.start and rect!=self.end and rect not in self.blocked:
									pygame.draw.rect(self.win,BLACK,(rectt.x,rectt.y,rectt.width,rectt.height))
									self.blocked.append(rect)
									pygame.display.update()

class algorithms:
	
	def __init__(self,win,rectdict,start,end,blocked):
		self.queue=heapdict.heapdict()
		self.win=win
		self.blocked=blocked
		self.rectdict=rectdict
		self.start=start
		self.end=end
		self.value=0
		for i in self.rectdict:
			if i not in self.blocked and i!=self.start and i!=self.end:
				rect=rectdict[i]
				pygame.draw.rect(self.win,WHITE,(rect.x,rect.y,rect.width,rect.height))
		pygame.display.update()
	def djikstra(self):
		if not self.start or not self.end:
			return
		for i in self.rectdict:
			if i==self.start:
				self.queue[i]=0
			elif i not in self.blocked:
				self.queue[i]=float('inf')
		prevnode={}
		s=self.queue.popitem()[0]
		prevnode[s]=None
		while self.queue:
			for i in self.neighbours(self.start):
				if i in self.queue:
					if 1+self.value<self.queue[i]:
						self.queue[i]=1+self.value
						prevnode[i]=self.start
						rect=self.rectdict[i]
						pygame.draw.rect(self.win,GREY,(rect.x,rect.y,rect.width,rect.height))
			pygame.display.update()
			self.start,self.value=self.queue.popitem()
			if self.start==self.end:
				self.showPath(prevnode)
				break
			
	
	def astar(self):
		if not self.start or not self.end:
			return
		for i in self.rectdict:
			if i==self.start:
				self.queue[i]=0+(abs(self.start[0]-self.end[0])+abs(self.start[1]-self.end[1]))
			elif i not in self.blocked:
				self.queue[i]=float('inf')
		prevnode={}
		s=self.queue.popitem()[0]
		prevnode[s]=None
		while self.queue:
			for i in self.neighbours(self.start):
				hcost=abs(i[0]-self.end[0])+abs(i[1]-self.end[1])
				#hcost=max(abs(i[0]-self.end[0]),abs(i[1]-self.end[1]))
				#hcost=math.sqrt((self.end[0]-i[0])**2+(self.end[1]-i[1])**2)
				if i in self.queue:
					if 1+hcost+self.value<self.queue[i]:
						self.queue[i]=1+self.value+hcost
						prevnode[i]=self.start
						rect=self.rectdict[i]
						pygame.draw.rect(self.win,GREY,(rect.x,rect.y,rect.width,rect.height))
			pygame.display.update()
			self.start,self.value=self.queue.popitem()
			self.value=self.value-(abs(self.start[0]-self.end[0])+abs(self.start[1]-self.end[1]))
			#self.value=self.value-max(abs(self.start[0]-self.end[0]),abs(self.start[1]-self.end[1]))
			#self.value=self.value-math.sqrt((self.end[0]-self.start[0])**2+(self.end[1]-self.start[1])**2)
			if self.start==self.end:
				self.showPath(prevnode)
				return
			
	def showPath(self,prevnode,s=None):
		if s:
			a=s
		else:
			a=self.start
		while a:
			rect=self.rectdict[a]
			pygame.draw.rect(self.win,GREEN,(rect.x,rect.y,rect.width,rect.height))
			pygame.display.update()
			a=prevnode[a]
	
	def greedy(self):
		if not self.start or not self.end:
			return
		prevnode={}
		for i in self.rectdict:
			if i==self.start:
				self.queue[i]=hcost=math.sqrt((self.end[0]-i[0])**2+(self.end[1]-i[1])**2)
			else:
				self.queue[i]=float('inf')
		
		while self.queue:
			s=self.queue.popitem()[0]
			if s==self.end:
				prevnode[self.start]=None
				self.showPath(prevnode,s)
				return
			for i in self.neighbours(s):
				if i in self.queue:
					#hcost=math.sqrt((self.end[0]-i[0])**2+(self.end[1]-i[1])**2)
					hcost=abs(i[0]-self.end[0])+abs(i[1]-self.end[1])
					if i not in self.blocked and hcost<self.queue[i]:
						rect=self.rectdict[i]
						pygame.draw.rect(self.win,GREY,(rect.x,rect.y,rect.width,rect.height))
						self.queue[i]=hcost
						prevnode[i]=s
			pygame.display.update()
	
	def neighbours(self,t):
		r,c=t
		return [(r+1,c),(r,c+1),(r,c-1),(r-1,c)]#+[(r+1,c-1),(r-1,c+1),(r+1,c+1),(r-1,c-1)]

class maze:
	def __init__(self,win,rectdict,start,end,blocked,num):
		self.win=win
		self.rectdict=rectdict
		self.start=start
		self.end=end
		self.blocked=blocked
		self.flush()
		self.door={'x':[],'y':[]}
		self.walls={'x':[],'y':[]}
		self.generate(0,num-1,0,num-1)
	
	def flush(self):
		for i in self.rectdict:
			if i==self.start or i==self.end:
				rect=self.rectdict[i]
				pygame.draw.rect(self.win,BLUE,(rect.x,rect.y,rect.width,rect.height))
			else:
				rect=self.rectdict[i]
				pygame.draw.rect(self.win,WHITE,(rect.x,rect.y,rect.width,rect.height))
		pygame.display.update()
		self.blocked.clear()
	
	def generate(self,xmin,xmax,ymin,ymax):
		if self.start:
			self.door['x'].append(self.start)
			self.door['y'].append(self.start)
		if self.end:
			self.door['x'].append(self.end)
			self.door['y'].append(self.end)
		if xmax-xmin<1 or ymax-ymin<1:
			return
		def vertical():
			li=[x for x in range(ymin,ymax+1)]
			b=False
			for _ in range(len(li)):
				i=random.choice(li)
				for g in range(xmin-1,xmax+2):
					if (i-1,g) not in self.walls['y'] and (i+1,g) not in self.walls['y'] and (i,xmin-1) not in self.door['y'] and (i,xmax+1) not in self.door['y']:
						n=i
						j=random.randint(xmin,xmax)
						if g==xmax+1:
							b=True
							break
					else:
						li.remove(i)
						if not li:
							return True
						break
				if b:
					break
			for i in range(xmin,xmax+1):
				if (n,i)==self.start or (n,i)==self.end:
					self.door['x'].append((i,n))
				elif i==j:
					self.door['x'].append((j,n))
				else:
					self.blocked.append((n,i))
					rect=self.rectdict[n,i]
					pygame.draw.rect(self.win,BLACK,(rect.x,rect.y,rect.width,rect.height))
				self.walls['y'].append((n,i))
			pygame.display.update()
			#pygame.time.delay(50)
			self.generate(xmin,xmax,ymin,n-1)
			self.generate(xmin,xmax,n+1,ymax)
		def horizontal():
			li=[x for x in range(xmin,xmax+1)]
			b=False
			for _ in range(len(li)):
				i=random.choice(li)
				for g in range(ymin-1,ymax+2):
					if (i-1,g) not in self.walls['x'] and (i+1,g) not in self.walls['x'] and (i,ymin-1) not in self.door['x'] and (i,ymax+1) not in self.door['x']:
						n=i
						j=random.randint(ymin,ymax)
						if g==ymax+1:
							b=True
							break
					else:
						li.remove(i)
						if not li:
							return True
						break
				if b:
					break
			for i in range(ymin,ymax+1):
				if (i,n)==self.start or (i,n)==self.end:
					self.door['y'].append((i,n))
				elif i==j:
					self.door['y'].append((j,n))
				else:
					self.blocked.append((i,n))
					rect=self.rectdict[i,n]
					pygame.draw.rect(self.win,BLACK,(rect.x,rect.y,rect.width,rect.height))
				self.walls['x'].append((n,i))
			pygame.display.update()
			#pygame.time.delay(50)
			self.generate(xmin,n-1,ymin,ymax)
			self.generate(n+1,xmax,ymin,ymax)
		if ymax-ymin>xmax-xmin:
			if vertical():
				horizontal()
		elif xmax-xmin>ymax-ymin:
			if horizontal():
				vertical()
		else:
			li=[vertical,horizontal]
			p=random.choice(li)
			if p():
				li.remove(p)
				li[0]()
					
					
if __name__=='__main__':
	app().run()
