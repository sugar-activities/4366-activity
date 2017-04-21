#!/usr/bin/python
# Tessellations.py
"""
    Copyright (C) 2010  Peter Hewitt

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

"""
import g,utils,pygame,tess,buttons,gtk,sys

class Tessellations:

    def __init__(self):
        self.tess_n=1; self.max_n=0
        self.journal=True # set to False if we come in via main()
        
    def display(self):
        if self.tessl.complete():
            g.screen.fill((0,0,0))
        else:
            cols=[(128,0,128),(255,255,192),(0,255,0),(0,255,0),(128,0,128)]
            cols+=[(0,255,0),(0,0,255),(255,193,127),(255,255,255),(0,0,0)]
            cols+=[(255,255,192),[0,0,0]]
            g.screen.fill(cols[g.tesses[g.tess_n-1]-1])
        self.tessl.draw()
        pygame.draw.rect(g.screen,(0,0,0),(g.sx(0),g.sy(21.55),g.sy(32),g.sy(2.55)))
        if self.tessl.complete():
            if g.max_n<g.tess_n: g.max_n=g.tess_n; self.max_n=g.max_n
            utils.centre_blit(g.screen,g.magician,(g.sx(16.6),g.sy(16.9)))
            g.button_display=True
        if self.tessl.carrying: g.button_display=False
        self.buttons_control()
        buttons.draw()
        x=g.sx(.2); y=g.sy(.2)
        s=str(g.tess_n)+' / '+str(len(g.tesses))+'  ('+str(g.max_n)+')'
        utils.display_string(s,(x,y))

    def do_button(self,bu):
        max_n=len(g.tesses)
        if bu=='fd': # next tessellation
            g.tess_n+=1
            if g.tess_n>max_n: g.tess_n=1
            self.tessl=tess.Tess(g.tesses[g.tess_n-1])
        elif bu=='back': # previous tessellation
            g.tess_n-=1
            if g.tess_n<1: g.tess_n=max_n
            self.tessl=tess.Tess(g.tesses[g.tess_n-1])
        elif bu=='solve':
            self.tessl.solve(); buttons.off('solve')
        self.tess_n=g.tess_n

    def buttons_control(self):
        if g.button_display:
            buttons.on(['back','fd'])
            if g.tess_n==1:buttons.off('back')
            if g.tess_n>g.max_n:buttons.off('fd')
            if g.tess_n==len(g.tesses):buttons.off('fd')
            if g.tess_n>g.max_n or self.tessl.complete():
                buttons.off('solve')
            else:
                buttons.on('solve')
        else:
            buttons.off(['back','fd','solve'])

    def run(self):
        g.init()
        if not self.journal:
            utils.load(); self.tess_n=g.tess_n; self.max_n=g.max_n
        else:
            g.tess_n=self.tess_n; g.max_n=self.max_n
        self.tessl=tess.Tess(g.tesses[g.tess_n-1])
        dx=g.sy(2.4); bx=g.sx(16)-dx/2; by=g.sy(20.2)
        buttons.Button("back",(bx,by),True); bx+=dx
        buttons.Button("fd",(bx,by),True)
        bx=g.sx(16); by=g.sy(11)
        buttons.Button("solve",(bx,by),True)
        if self.journal: # Sugar only
            a,b,c,d=pygame.cursors.load_xbm('my_cursor.xbm','my_cursor_mask.xbm')
            pygame.mouse.set_cursor(a,b,c,d)
        going=True

        while going:
            # Pump GTK messages.
            while gtk.events_pending():
                gtk.main_iteration()

            # Pump PyGame messages.
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    if not self.journal: utils.save()
                    going=False
                elif event.type == pygame.MOUSEMOTION:
                    g.redraw=True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    g.redraw=True
                    if event.button==2: # centre button
                        if not self.journal:
                            g.version_display=not g.version_display; break
                    bu=''
                    if not self.tessl.carrying:
                        bu=buttons.check()
                    if bu<>'': self.do_button(bu)
                    else: self.tessl.click()
            self.tessl.update()
            if g.redraw:
                self.display()
                if g.version_display: utils.version_display()
                pygame.display.flip()
                g.redraw=False
            tf=False
            if pygame.mouse.get_focused(): tf=True
            pygame.mouse.set_visible(tf)
            g.clock.tick(40)

if __name__=="__main__":
    pygame.init()
    pygame.display.set_mode((800, 600))
    game=Tessellations()
    game.journal=False
    game.run()
    pygame.display.quit()
    pygame.quit()
    sys.exit(0)
