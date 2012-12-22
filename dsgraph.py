#-*-coding:utf-8-*-
#!/usr/bin/env python

import pygtk
from priodict import priorityDictionary

#arayuz
pygtk.require('2.0') 
import gtk

#Koseleri tutar
vertices = {}
VertexCount=0

#SABITLER
DRAW_MARGIN = 10
DRAW_X = 1004
DRAW_Y = 550

RECT_SIZE = 20

#Kose ekleme modunu acar
isEkleOn = False

class Base:#pencere sınıfı
    def kapat(self,widget,data=None):#Programı kapatmak icin handler
        print "Program kapatıldı!"
        gtk.main_quit()
        
    def onclick(self, ebox, event):#mouse'un bulundugu noktayi belirler kose ekler 
        global VertexCount
        print event.x, event.y
        
        #koselerin cakismasini onler
        if event.x>DRAW_MARGIN and event.x<DRAW_X and \
        event.y>DRAW_MARGIN and event.y<DRAW_Y-DRAW_MARGIN and \
        isEkleOn and self.checkVertex(event.x, event.y):
            
            self.draw_rect(int(event.x),int(event.y))#koseyi ciz
            vertices[VertexCount] = (event.x,event.y)#koseleri tutan sozluge ekle
            VertexCount = len(vertices)#kose sayisini yeniden ayarla
             
    def area_expose(self,area,event):#Cizim alaninin init metodudur.
        self.style = self.area.get_style()
        self.gc = self.style.fg_gc[gtk.STATE_NORMAL]
        self.area.window.draw_rectangle(self.gc,False,DRAW_MARGIN,DRAW_MARGIN,DRAW_X,DRAW_Y)
        
    def draw_rect(self, x, y):#kose cizer.
        self.area.window.draw_rectangle(self.gc,False,x,y,RECT_SIZE,RECT_SIZE)
    
    def checkVertex(self,x,y):#Koselerin cakismasini kontrol eder.
        for i in vertices:
            koord = vertices[i]
            if x<koord[0]+RECT_SIZE and x> koord[0]-RECT_SIZE and y<koord[1]+RECT_SIZE and y>koord[1]-RECT_SIZE:
                return False
        return True
    
    def ekle(self,widget):#kose ekleme modu switchi
        global isEkleOn
        if isEkleOn:
            self.dugme_KoseEkle.set_label("Kose Ekle")
            isEkleOn = False
        else:
            self.dugme_KoseEkle.set_label("Kose Eklemeyi Durdur!")
            isEkleOn = True
             
            
    def __init__(self):
        self.pencere = gtk.Window(gtk.WINDOW_TOPLEVEL)#pencere olustur
        self.pencere.set_position(gtk.WIN_POS_CENTER)#pencereyi hizala
        self.pencere.set_size_request(1024,600)#pencere boyutu ayarla
        
        self.dugme_KoseEkle = gtk.Button("Ekle")
        self.dugme_KoseEkle.connect("clicked",self.ekle)
        
        self.vert = gtk.VBox(False)
        
        self.sabit = gtk.HBox()
        self.sabit.pack_start(self.dugme_KoseEkle)
        
        self.ebox = gtk.EventBox()
        self.ebox.connect ('button-press-event', self.onclick)
        self.area = gtk.DrawingArea()
        
        self.area.connect("expose-event",self.area_expose)
        self.ebox.add(self.area)
        
        self.vert.pack_start(self.sabit,False,False,1)
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
    
    for node in nodedist:
        uzaklik[node] = gelis[node]
        if node == son:
            break
        for node2 in Graph:
            sonrasininUzakligi = uzaklik[node] + Graph[node][node2]
            if node2 in uzaklik:
                if sonrasininUzakligi < uzaklik[node2]:
                    raise ValueError 
            elif node2 not in nodedist or sonrasininUzakligi < nodedist[node2]:
                nodedist[node2] = sonrasininUzakligi
                gelis[node2] = node 
    
    return (uzaklik,gelis)

def enKisa(Graph,ilk,son):
    yol = []
    
    uzaklik = Dijkstra(Graph, ilk, son)
    while True:
        yol.append(son)
        if ilk == son:
            break
        son = uzaklik[son]
    yol.reverse()
    return yol 
        
        
if __name__ == "__main__":
    base = Base()
    base.main()