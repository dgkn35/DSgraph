#-*-coding:utf-8-*-
#!/usr/bin/env python


# DSgraph project
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# Copyright © 2012 Efe Gürkan YALAMAN, Doğukan Sever, Melih Çakır
#
# Authors: Efe Gürkan Yalaman - efeyalaman@gmail.com
#          Doğukan Sever - dogukansever@hotmail.com.tr
#          Melih Çakır


import pygtk
from priodict import priorityDictionary
from operator import itemgetter
from disjointSets import DisjointSet

#arayuz
pygtk.require('2.0') 
import gtk

#Koseleri tutar
graph = {}
VertexCount=0

secim = []


#SABITLER
DRAW_MARGIN = 10
DRAW_X = 1004
DRAW_Y = 550

RECT_SIZE = 20

#Kose ekleme modunu acar
mod =""

class Base:#pencere sınıfı
    def kapat(self,widget,data=None):#Programı kapatmak icin handler
        print "Program kapatıldı!"
        gtk.main_quit()
        
    def vertexSelectionControl(self,func):
        global secim
        if len(secim) <2:
            msg = gtk.MessageDialog(None,0,gtk.MESSAGE_INFO,gtk.BUTTONS_OK,"Bu islem icin en az 2 secim\
yapmis olmak gerekmektedir!\n Sec tusunu aktif hale getirdikten sonra arka arkaya 2 secim yapin.")
            msg.run()
            msg.destroy()
            return False
        elif self.weight.get_text_length()==0 and func == "edge":
            msg1 = gtk.MessageDialog(None,0,gtk.MESSAGE_INFO,gtk.BUTTONS_OK,"Agirlik alani bos birakilmamalidir!")
            msg1.run()
            msg1.destroy()
            return False
        else:
            return True
    
    def onclick(self, ebox, event):#mouse'un bulundugu noktayi belirler kose ekler 
        global VertexCount
        print event.x, event.y
        
        #koselerin cakismasini onler
        if event.x>DRAW_MARGIN and event.x<DRAW_X-DRAW_MARGIN and \
        event.y>DRAW_MARGIN and event.y<DRAW_Y-DRAW_MARGIN and \
        mod == "Ekle" and self.checkVertex(event.x, event.y):
            
            liste = [(event.x,event.y),{}]
            graph[VertexCount] = liste#koseleri tutan sozluge ekle
            self.draw_rect(int(event.x),int(event.y),VertexCount)#koseyi ciz

            VertexCount = len(graph)#kose sayisini yeniden ayarla

        if mod == "Sec":
            secilen = self.findVertex(event.x, event.y)
            text = "Son Secilen: "
            if secilen != None:
                textnew=text + str(secilen)
                self.lblSelected.set_text(textnew)
                secim.append(secilen)
             
    def area_expose(self,area,event):#Cizim alaninin init metodudur.
        self.style = self.area.get_style()
        self.gc = self.style.fg_gc[gtk.STATE_NORMAL]
        self.area.window.draw_rectangle(self.gc,False,DRAW_MARGIN,DRAW_MARGIN,DRAW_X,DRAW_Y)
        
    def draw_rect(self, x, y,i):#kose cizer.
        i = str(i)
        self.area.window.draw_rectangle(self.gc,False,x,y,RECT_SIZE,RECT_SIZE)
        self.pango.set_text(i)
        self.area.window.draw_layout(self.gc,int(x+4),int(y+2),self.pango)

    
    def draw_line(self,p1,p2):
        self.area.window.draw_line(self.gc,p1[0],p1[1],p2[0],p2[1])
        
    def checkVertex(self,x,y):#Koselerin cakismasini kontrol eder.
        for i in graph:
            koord = graph[i][0]
            if x<koord[0]+RECT_SIZE and x> koord[0]-RECT_SIZE and y<koord[1]+RECT_SIZE and y>koord[1]-RECT_SIZE:
                return False
        return True
    
    def redraw(self,widget):#Redraws graph to drawing area
        done = [] 
        for i in graph:
            dot1 = graph[i][0]
            self.draw_rect(int(dot1[0]),int(dot1[1]),i)
            for j in graph[i][1]:
                if not j in done:
                    self.drawKenar(i, j)
            done.append(i)
  
    def findVertex(self,x,y):
        for i in graph:
            koord = graph[i][0]
            if x>koord[0] and x<koord[0]+RECT_SIZE and y>koord[1] and y<koord[1]+RECT_SIZE:
                return i
        return None
    
    def sec(self,widget):
        global mod
        self.Default()
        if mod !="Sec":
            mod = "Sec"
            self.Default()
            self.dugme_Sec.set_label("Secmeyi durdur")
        elif mod == "Sec":
            self.Default()
            mod = ""
        
    def dijksHandler(self,widget):
        global secim,graph
        if self.vertexSelectionControl("dijkstra"):
            secim.reverse()
            ilk = secim[0]
            for i in range(0,len(secim)):
                ikinci = secim[i]
                if ikinci !=ilk:
                    break
            if ikinci != None:
                yol,uzaklik = enKisa(graph, ilk, ikinci)
                
                for i in range(0,len(yol)-1):
                    d1,d2 = yol[i],yol[i+1]
                    self.drawKenar(d1, d2, "red")
                    
                msg = gtk.MessageDialog(None,0,gtk.MESSAGE_INFO,gtk.BUTTONS_OK,"Mesafe:"+str(uzaklik)+"\nEn kisa yol :"+str(yol))
                msg.run()
                msg.destroy()
        secim =[]
    
    def KruskalHandler(self,widget):
        mst = kruskal(graph)
        for i in mst:
            self.drawKenar(i[0], i[1], "red")
        
    def DFSHandler(self,widget):
        global secim
        if secim != []:
            start = secim.pop()
            yol = DFS(graph,start)
            
#            for i in range(0,len(yol)-1):
#                d1,d2 = yol[i],yol[i+1]
#                self.drawKenar(d1, d2, "red")
            msg = gtk.MessageDialog(None,0,gtk.MESSAGE_INFO,gtk.BUTTONS_OK,"Dolasma sirasi"+str(yol))
            msg.run()
            msg.destroy()
        else:
            msg = gtk.MessageDialog(None,0,gtk.MESSAGE_INFO,gtk.BUTTONS_OK,"Lutfen bir secim yapiniz")
            msg.run()
            msg.destroy()
        pass

    def drawKenar(self,bas,son,renk="black"):
        pos1 = graph[bas][0]
        pos2 = graph[son][0]
        pos1 = (int(pos1[0]),int(pos1[1]))
        pos2 = (int(pos2[0]),int(pos2[1]))
        
        dot1 = None
        dot2 = None
        weightPos = None
        
        if pos1[0] < pos2[0] and pos1[1]<pos2[1]:# pos 1 sol üstte
            dot1 = (pos1[0]+RECT_SIZE,pos1[1]+RECT_SIZE)
            dot2 = pos2
            weightPos = (dot1[0]+RECT_SIZE+abs(dot1[0]-dot2[0])/2,
                         dot1[1]+abs(dot1[1]-dot2[1])/2)
        elif pos1[0] > pos2[0] and pos1[1]>pos2[1]:#pos 1 sağ altta
            dot1 = pos1
            dot2 = (pos2[0]+RECT_SIZE,pos2[1]+RECT_SIZE)
            weightPos = (pos2[0]+RECT_SIZE+abs(dot1[0]-dot2[0])/2,
                         pos2[1]+RECT_SIZE+abs(dot1[1]-dot2[1])/2)
        elif pos1[0]<pos2[0] and pos1[1]>pos2[1]:#pos 1 sol altta
            dot1 = (pos1[0]+RECT_SIZE,pos1[1])
            dot2 = (pos2[0],pos2[1]+RECT_SIZE)
            weightPos = (dot2[0]+RECT_SIZE-abs(dot1[0]-dot2[0])/2,
                         dot2[1]+abs(dot1[1]-dot2[1])/2)
        else: #pos 1 sağ üstte
            dot1 = (pos1[0],pos1[1]+RECT_SIZE)
            dot2 = (pos2[0]+RECT_SIZE,pos2[1])
            weightPos = (dot1[0]+RECT_SIZE-abs(dot1[0]-dot2[0])/2,
                         dot1[1]+abs(dot1[1]-dot2[1])/2)
            
        
         
        color = gtk.gdk.color_parse(renk)
        self.gc.set_rgb_fg_color(color)
        
        self.draw_line(dot1,dot2)
        
        self.pango.set_text(str(graph[bas][1][son]))
        self.area.window.draw_layout(self.gc,weightPos[0],weightPos[1],self.pango)
        
        color = gtk.gdk.color_parse("black")
        self.gc.set_rgb_fg_color(color)
        
    def reset(self,widget):
        self.area.queue_draw()

    def kenarEkle(self,widget):
        global secim
        if self.vertexSelectionControl("edge"):
            secim.reverse()
            ilk = secim[0]
            for i in range(0,len(secim)):
                ikinci = secim[i]
                if ikinci !=ilk:
                    break
            if ikinci in graph[ilk][1]:
                msg2 = gtk.MessageDialog(None,0,gtk.MESSAGE_INFO,gtk.BUTTONS_OK,"Ayni yere ekleme yapamazsiniz.")
                msg2.run()
                msg2.destroy()
                
            elif ikinci != None:
                graph[ilk][1][ikinci]=int(self.weight.get_text())
                graph[ikinci][1][ilk]=int(self.weight.get_text())
                self.drawKenar(ilk, ikinci)
                
        secim =[]
            

    def Default(self):
        self.dugme_Sec.set_label("Sec")
        self.dugme_KoseEkle.set_label("Kose Ekle")
        self.lblSelected.set_label("Son Secilen: ")
        secim = []

    def ekle(self,widget):#kose ekleme modu switchi
        global mod
        if mod != "Ekle":
            mod = "Ekle"
            self.Default()
            self.dugme_KoseEkle.set_label("Kose Eklemeyi Durdur.")
        elif mod == "Ekle":
            self.Default()
            mod =""
             
            
    def __init__(self):
        self.pencere = gtk.Window(gtk.WINDOW_TOPLEVEL)#pencere olustur
        self.pencere.set_position(gtk.WIN_POS_CENTER)#pencereyi hizala
        self.pencere.set_size_request(1024,600)#pencere boyutu ayarla
        self.ebox = gtk.EventBox()
        self.area = gtk.DrawingArea()
        self.vert = gtk.VBox(False)
        self.Hori = gtk.HBox()
        self.ebox.connect ('button-press-event', self.onclick)
        self.area.connect("expose-event",self.area_expose)
        self.ebox.add(self.area)
        
        self.pango = self.area.create_pango_layout("")
        
        self.dugme_KoseEkle = gtk.Button("Kose Ekle")
        self.dugme_KoseEkle.connect("clicked",self.ekle)
        
        self.dugme_Sec = gtk.Button("Kose Sec")
        self.dugme_Sec.connect("clicked",self.sec)
        
        self.weight = gtk.Entry()
        
        self.dugme_kenarEkle = gtk.Button("Kenar ekle")
        self.dugme_kenarEkle.connect("clicked",self.kenarEkle)
        
        self.dugme_Dijkstra = gtk.Button("Dijkstra's")
        self.dugme_Dijkstra.connect("clicked",self.dijksHandler)
       
        self.dugme_Kruskal = gtk.Button("Kruskal's")
        self.dugme_Kruskal.connect("clicked",self.KruskalHandler)
       
        self.dugme_DFS = gtk.Button("DFS")
        self.dugme_DFS.connect("clicked",self.DFSHandler)
       
        self.dugme_redraw = gtk.Button("Yenile")
        self.dugme_redraw.connect("clicked",self.redraw)
        
        self.dugme_temizle = gtk.Button("Temizle")
        self.dugme_temizle.connect("clicked",self.reset)
        
        self.lblSelected = gtk.Label("Son Secilen:")
        
        
        self.Hori.pack_start(self.dugme_KoseEkle)
        self.Hori.pack_start(self.dugme_Sec)
        self.Hori.pack_start(self.lblSelected)
        self.Hori.pack_start(self.weight)
        self.Hori.pack_start(self.dugme_kenarEkle)
        self.Hori.pack_start(self.dugme_Dijkstra)
        self.Hori.pack_start(self.dugme_Kruskal)
        self.Hori.pack_start(self.dugme_DFS)
        self.Hori.pack_start(self.dugme_redraw)
        self.Hori.pack_start(self.dugme_temizle)
                
        self.vert.pack_start(self.Hori,False,False,1)
        self.vert.pack_start(self.ebox,1)
        
        self.pencere.add(self.vert)
        self.pencere.show_all()#pencereyi goster
        self.pencere.connect("destroy",self.kapat)#handler kapatma eventine baglandi

        
    def main(self):
        gtk.main()
        
def Dijkstra(Graph,ilk,son=None):
    
    uzaklik={}#son uzakliklari tutacak
    gelis={}#noktaya gelinen yeri tutar.
    nodedist = priorityDictionary()#nodların yaklasik hesaplamasini tutar
    
    nodedist[ilk]=0
    for node in nodedist:
        uzaklik[node] = nodedist[node]
        if node == son:
            break
        for node2 in Graph[node][1]:
            sonrasininUzakligi = uzaklik[node] + Graph[node][1][node2]
            if node2 in uzaklik:
                if sonrasininUzakligi < uzaklik[node2]:
                    raise ValueError 
            elif node2 not in nodedist or sonrasininUzakligi < nodedist[node2]:
                nodedist[node2] = sonrasininUzakligi
                gelis[node2] = node 
    
    return (uzaklik,gelis)

def enKisa(Graph,ilk,son):
    yol = []
    
    uzaklik , gelis = Dijkstra(Graph, ilk, son)
    while True:
        yol.append(son)
        if ilk == son:
            break
        son = gelis[son]
#    yol.reverse()
    return yol ,uzaklik

def kruskal(Graph):
    #def kruskal( nodes, edges ):
    nodes = []
    edges = []
    
    for i in Graph:
        nodes.append(i)
        for j in Graph[i][1]:
            tup = (i,j,Graph[i][1][j])
            edges.append(tup)
        
    forest = DisjointSet()
    mst = []
    for k in nodes:
        forest.add( k )
 
    size = len(nodes) - 1
 
    for e in sorted( edges, key=itemgetter( 2 ) ):
        n1, n2, _ = e
        t1 = forest.find(n1)
        t2 = forest.find(n2)
        if t1 != t2:
            mst.append(e)
            size -= 1
            if size == 0:
                return mst
         
            forest.union(t1, t2)
    
def DFS(graph, start, path=[]):
    q=[start]
    while q:
        v=q.pop(0)
        if v not in path:
            path=path+[v]
            
            liste = []
            for i in graph[v][1]:
                liste.append(i)
            q=liste+q
            
    print path
    return path
        
if __name__ == "__main__":
    base = Base()
    base.main()
