#-*-coding:utf-8-*-
#!/usr/bin/env python

import pygtk
from priodict import priorityDictionary

#arayuz
pygtk.require('2.0') 
import gtk

class Base:#pencere sınıfı
    def kapat(self,widget,data=None):#Programı kapatmak icin handler
        print "Program kapatıldı!"
        gtk.main_quit()
        
    def __init__(self):
        self.pencere = gtk.Window(gtk.WINDOW_TOPLEVEL)#pencere olustur
        self.pencere.set_position(gtk.WIN_POS_CENTER)#pencereyi hizala
        self.pencere.set_size_request(1024,600)#pencere boyutu ayarla
        
        #self.dugme1 = gtk.Button("Dugme1") # dugme olusturma
        #self.dugme1.connect("event",handler) #dugmeye handler baglama
        
        #konteyner = gtk.Fixed() #sabit değil vbox,hbox'da olabilir
        #konteyner.put(self.dugme1,xkoord,ykoord)
        #yeni dugmeler de buraya eklenebilir
        
        
        #self.window.add(self.konteyner)
        
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