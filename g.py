# g.py - globals
import pygame,utils

XO=False # affects the pygame.display.set_mode() call only
app='Tessellations'; ver='1.0'
ver='1.1'
# no Esc on XO
# only check buttons if mouse in area -> pick up quicker?
# save g.tess_n
# bgd selection fixed
ver='1.2'
# position tolerance doubled
ver='1.3' #<<<< Release 1
# changed spelling to double 'l'
# removed grey button - arrows only on completion
#   off after 1st piece picked up
# g.max_n -> max # solved
# added number display
ver='1.4'
# removed tess # from x display
# swapped 6 & 7 then 7 & 8
ver='1.5'
# solve button
ver='2.0'
# sugar version
ver='2.1'
# pieces prevented from disappearing at bottom of display
ver='3.0'
# redraw implemented
ver='3.1'
# glow finishes without mousr move - see tess.update()
ver='4.0'
# new sugar cursor etc

tesses=(1,2,3,9,11,8,6,12,4,7,10,5) # display order

def init(): # called by main()
    global redraw
    global screen,w,h,font1,font2,clock,click_snd
    global factor,offset,imgf,message,version_display
    redraw=True
    version_display=False
    screen = pygame.display.get_surface()
    pygame.display.set_caption(app)
    screen.fill((70,0,70))
    pygame.display.flip()
    w,h=screen.get_size()
    if float(w)/float(h)>1.5: #widescreen
        offset=(w-4*h/3)/2 # we assume 4:3 - centre on widescreen
    else:
        h=int(.75*w) # allow for toolbar - works to 4:3
        offset=0
    clock=pygame.time.Clock()
    factor=float(h)/24 # measurement scaling factor (32x24 = design units)
    offset=(w-4*h/3)/2 # we assume 4:3 - centre on widescreen
    imgf=float(h)/900 # image scaling factor - all images built for 1200x900
    if pygame.font:
        t=int(54*imgf); font1=pygame.font.Font(None,t)
        t=int(36*imgf); font2=pygame.font.Font(None,t)
    message=''
    
    # this activity only
    global magician,tess_n,max_n,button_display
    magician=utils.load_image('magician.png',True)
    tess_n=1; max_n=0; button_display=True

def sx(f): # scale x function
    return f*factor+offset

def sy(f): # scale y function
    return f*factor

