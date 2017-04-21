#tess.py
import g,utils,random,pygame

class Tess:
    # __init__ @ the end
    
    def clear(self):
        self.pieces=[]; self.images=[]
        self.grey=[]; self.glow=[]; self.black=[]

    def init(self,l1,img_n,shape):
        img=utils.load_image(shape+'.png',True); self.images.append(img)
        img=utils.load_image(shape+'.png',True,'grey'); self.grey.append(img)
        img=utils.load_image(shape+'.png',True,'glow'); self.glow.append(img)
        img=utils.load_image(shape+'.png',True,'black'); self.black.append(img)
        for (cx,cy) in l1:
            piece=Piece(img_n,(cx,cy)); self.pieces.append(piece)

    def setup(self):
        for piece in self.pieces:
            x=0; y=0
            while x<20 and y<16:
                x=random.randint(1,32); y=random.randint(1,21)
            piece.c=(g.sx(x),g.sy(y)); piece.done=False
        piece=self.pieces[0]; piece.c=piece.c0; piece.done=True
        self.carrying=None; self.glowing=None; self.ms=None
        if self.n==2:
            for ind in [1,6,12,18]:
                piece=self.pieces[ind]; piece.c=piece.c0; piece.done=True
        if self.n==3:
            for ind in [6,10]:
                piece=self.pieces[ind]; piece.c=piece.c0; piece.done=True

    def ind(self,piece):
        i=0
        for pce in self.pieces:
            if pce==piece: return i
            i+=1
        return 0 # shouldn't happen
     
    def solve(self):
        for piece in self.pieces:
            piece.done=True; piece.c=piece.c0
        self.carrying=None
                     
    def complete(self):
        for piece in self.pieces:
            if not piece.done: return False
        return True
                     
    def draw(self):
        for piece in self.pieces:
            if piece<>self.carrying:
                img=self.grey[piece.img_n]
                if piece.done: img=self.images[piece.img_n]
                utils.centre_blit(g.screen,img,piece.c)
            else:
                mx,my=pygame.mouse.get_pos()
                c=(mx+self.dx,my+self.dy)
                utils.centre_blit(g.screen,self.black[piece.img_n],c)
                utils.centre_blit(g.screen,self.grey[piece.img_n],c)
        if self.glowing<>None:
            piece=self.glowing
            utils.centre_blit(g.screen,self.glow[piece.img_n],piece.c)

    def update(self):
        if self.glowing<>None:
            d=pygame.time.get_ticks()-self.ms
            if d<0 or d>300: self.glowing=None; g.redraw=True
        
    def top(self,ind):
        l=self.pieces; l1=l[:ind]+l[ind+1:]+l[ind:ind+1]
        self.pieces=l1

    def bottom(self,ind):
        l=self.pieces; l1=l[ind:ind+1]+l[:ind]+l[ind+1:]
        self.pieces=l1

    def click(self): # deal with click
        mx,my=pygame.mouse.get_pos()
        if self.carrying<>None: # dropping piece
            piece=self.carrying; self.carrying=None
            piece.c=(mx+self.dx,my+self.dy)
            if self.check(piece): # check if in place
                self.glowing=piece; self.ms=pygame.time.get_ticks()
            else: # check not out of sight
                cx,cy=piece.c; h2=self.images[piece.img_n].get_height()/2
                ylim=g.sy(21.55)
                if (cy-h2)>ylim: piece.c=(cx,ylim+h2-g.sy(.4))
            return True
        else:
            for ind in range(len(self.pieces)-1,0,-1):
                piece=self.pieces[ind]
                if not piece.done:
                    img=self.images[piece.img_n]
                    if utils.mouse_on_img(img,piece.c):
                        self.top(ind)
                        self.dx=piece.c[0]-mx
                        self.dy=piece.c[1]-my
                        self.carrying=piece
                        return True
            return False

    def check(self,piece):
        for pce in self.pieces:
            if not pce.done:
                if pce.img_n==piece.img_n:
                    dx=abs(pce.c0[0]-piece.c[0]); dy=abs(pce.c0[1]-piece.c[1])
                    d=g.sy(1.5) # was .8
                    if dx<d and dy<d:
                        if piece<>pce: # swap pieces
                            c0=piece.c0; piece.c0=pce.c0; pce.c0=c0
                        piece.c=piece.c0; piece.done=True;
                        self.bottom(self.ind(piece))
                        return True
        return False

    def __init__(self,n): # n is the tessellation number
        self.clear(); self.n=n

        if n==1: #Hexagons
            shape='hex2'; img_n=0; l1=[]
            s=70.0/11; h=s*1.732/2; dx=s*1.5; dy=h
            x0=s/2-.4; y0=0-.3
            x=x0;y=y0
            for i in range(4):
                l1.append((x,y)); x+=dx; y+=dy; dy=-dy
            x=x0;y=y0+2*h
            for i in range(4):
                l1.append((x,y)); x+=dx; y+=dy; dy=-dy
            x=x0;y=y0+4*h
            for i in range(2):
                l1.append((x,y)); x+=2*dx
            self.init(l1,img_n,shape)

        elif n==2: # Squares
            # square 1
            shape='sq1'; img_n=0; l1=[]
            s=5.33; d=s*2
            y=s/2
            for r in range(2):
                x=s/2
                for c in range(3):
                    l1.append((x,y)); x+=d
                y+=d
            y=s/2+s
            for r in range(2):
                x=s/2+s
                for c in range(3):
                    l1.append((x,y)); x+=d
                y+=d
            self.init(l1,img_n,shape)
            # square 2
            shape='sq2'; img_n=1; l1=[]
            y=s/2
            for r in range(2):
                x=s/2+s
                for c in range(3):
                    l1.append((x,y)); x+=d
                y+=d
            y=s/2+s
            for r in range(2):
                x=s/2
                for c in range(3):
                    l1.append((x,y)); x+=d
                y+=d
            self.init(l1,img_n,shape)

        elif n==3: #Triangles
            shape='tri1'; img_n=0; l1=[]
            s=5.33; d=s*2; y0=s*.866-3
            y=y0
            for r in range(2):
                x=s
                for c in range(3):
                    l1.append((x,y)); x+=d
                y+=s*1.732*2
            y=y0+s*1.732
            for r in range(1):
                x=0
                for c in range(4):
                    l1.append((x,y)); x+=d
                y+=s*1.732*2
            self.init(l1,img_n,shape)
            shape='tri2'; img_n=1; l1=[]
            y=y0
            for r in range(2):
                x=0
                for c in range(4):
                    l1.append((x,y)); x+=d
                y+=s*1.732*2
            y=y0+s*1.732
            for r in range(1):
                x=s
                for c in range(3):
                    l1.append((x,y)); x+=d
                y+=s*1.732*2
            self.init(l1,img_n,shape)

        elif n==4:
            # dodecagons
            shape='dodec'; img_n=0
            l1=((0,1.5),(16,1.5),(32,1.5),(8,15.3),(24,15.3))
            self.init(l1,img_n,shape)
            # hexagons
            shape='hex'; img_n=1 
            l1=((8,6),(24,6),(0,10.8),(16,10.8),(32,10.8),(0,19.8),(16,19.8),(32,19.8))
            self.init(l1,img_n,shape)
            # squares @ 30deg
            shape='sq30'; img_n=2
            l1=((12,8.4),(28,8.4),(4,22.1),(20,22.1))
            self.init(l1,img_n,shape)
            # squares @ -30deg
            shape='sq_30'; img_n=3
            l1=((4,8.4),(20,8.4),(12,22.1),(28,22.1))
            self.init(l1,img_n,shape)
            # squares
            shape='sq'; img_n=4
            l1=((8,1.5),(24,1.5),(0,15.3),(16,15.3),(32,15.3))
            self.init(l1,img_n,shape)

        elif n==5: # Alhambra
            x0=2.9; y0=2.4; dx=6.55; dy=6.55 
            # red
            shape='red'; img_n=0; l1=[]
            y=y0
            for r in range(2):
                x=x0
                for c in range(3):
                    l1.append((x,y)); x+=2*dx
                y+=2*dy
            y=y0+dy
            for r in range(2):
                x=x0+dx
                for c in range(2):
                    l1.append((x,y)); x+=2*dx
                y+=2*dy
            self.init(l1,img_n,shape)
            # yellow
            shape='yellow'; img_n=1; l1=[]
            y=y0
            for r in range(2):
                x=x0+dx
                for c in range(2):
                    l1.append((x,y)); x+=2*dx
                y+=2*dy
            y=y0+dy
            for r in range(2):
                x=x0
                for c in range(3):
                    l1.append((x,y)); x+=2*dx
                y+=2*dy
            self.init(l1,img_n,shape)
            # blue
            shape='blue'; img_n=2; l1=[]
            y=y0+dy/2
            for r in range(2):
                x=x0+dx/2
                for c in range(3):
                    l1.append((x,y)); x+=2*dx
                y+=2*dy
            y=y0-dy/2
            for r in range(2):
                x=x0+dx+dx/2
                for c in range(2):
                    if r==1 and c==0: l1.append((x-2*dx,y),)
                    l1.append((x,y)); x+=2*dx
                y+=2*dy
            self.init(l1,img_n,shape)
            # green
            shape='green'; img_n=3; l1=[]
            y=y0+dy/2
            for r in range(2):
                x=x0-dx/2
                for c in range(3):
                    l1.append((x,y)); x+=2*dx
                y+=2*dy
            y=y0-dy/2
            for r in range(2):
                x=x0+dx-dx/2
                for c in range(2):
                    if r==1 and c==1: l1.append((x+2*dx,y),)
                    l1.append((x,y)); x+=2*dx
                y+=2*dy
            self.init(l1,img_n,shape)

        elif n==6: # Hexagons & Triangles
            shape='hex3'; img_n=0; l1=[]
            s=5.333; d=s*2; x0=0; y0=0; h=s*1.732/2
            y=y0
            for r in range(2):
                x=x0+s
                for c in range(3): l1.append((x,y)); x+=d
                y+=h*4
            x=x0+0; y=y0+h*2
            for c in range(4): l1.append((x,y)); x+=d
            self.init(l1,img_n,shape)
            shape='tri3'; img_n=1; l1=[]; y=y0+h/2
            for r in range(2):
                x=x0
                for c in range(4): l1.append((x,y)); x+=d
                y+=h*4
            x=x0+s; y=y0+h*2.5
            for c in range(3): l1.append((x,y)); x+=d
            self.init(l1,img_n,shape)
            shape='tri4'; img_n=2; l1=[]; x=x0+s; y=y0+h*1.5
            for c in range(3): l1.append((x,y)); x+=d
            x=x0; y=y0+h*3.5
            for c in range(4): l1.append((x,y)); x+=d
            self.init(l1,img_n,shape)

        elif n==7: # Hexagons & Triangles & Squares
            shape='hex6'; img_n=0; l1=[]
            s=4.96; y0=.55; h=s*1.732/2; x0=16-s-2*h
            y=y0; dx=s+2*h; dy=3*s+2*h
            for r in range(2):
                x=x0
                for c in range(3): l1.append((x,y)); x+=dx
                y+=dy
            x=x0+s/2+h; y=y0+1.5*s+h
            l1+=((x,y),(x+dx,y))
            self.init(l1,img_n,shape)
            c0=l1[0]; c3=l1[3]; c6=l1[6]
            shape='sq6'; img_n=1; l1=[]
            x=x0+h+s/2; y=y0
            l1=[(x,y),(x+dx,y)]
            x=x0; y=y0+1.5*s+h
            l1+=((x,y),(x+dx,y),(x+2*dx,y))
            self.init(l1,img_n,shape)
            shape='sq7'; img_n=2
            (x,y1)=utils.avg(c0,c6)
            l1=[(x,y1),(x+dx,y1),(x+2*dx,y1)]
            x-=dx/2; (t,y2)=utils.avg(c6,c3)
            l1+=[(x,y2),(x+dx,y2),(x+2*dx,y2)]
            self.init(l1,img_n,shape)           
            shape='sq8'; img_n=3
            l1=[(x,y1),(x+dx,y1),(x+2*dx,y1)]
            x+=dx/2
            l1+=[(x,y2),(x+dx,y2),(x+2*dx,y2)]
            self.init(l1,img_n,shape)           
            shape='tri6'; img_n=4; dy=y2-y1
            x=x0+h+s/2; y1=y0+s/2+h/2
            l1=[(x,y1),(x+dx,y1)]
            x-=dx/2; y=y1+dy
            l1+=[(x,y),(x+dx,y),(x+2*dx,y)]
            self.init(l1,img_n,shape)           
            shape='tri7'; img_n=5
            x=x0+h+s/2-dx/2; y1=y0+s+h/2
            l1=[(x,y1),(x+dx,y1),(x+2*dx,y1)]
            x+=dx/2; y=y1+dy
            l1+=[(x,y),(x+dx,y)]
            self.init(l1,img_n,shape)           

        elif n==8: # Octagons & Squares
            shape='oct'; img_n=0; l1=[]
            y=4
            for r in range(3):
                x=4
                for c in range(4): l1.append((x,y)); x+=8
                y+=8
            self.init(l1,img_n,shape)       
            shape='sq9'; img_n=1; l1=[]
            y=0
            for r in range(3):
                x=0
                for c in range(5): l1.append((x,y)); x+=8
                y+=8
            self.init(l1,img_n,shape)       

        elif n==9: # Dodecagons & Triangles
            shape='dodec9'; img_n=0; l1=[]
            y=4.68; dx=22.48; dy=12.88
            for r in range(2):
                x=4.76
                for c in range(2): l1.append((x,y)); x+=dx
                y+=dy
            x=16; y=4.68-dy/2
            for r in range(3): l1.append((x,y)); y+=dy 
            self.init(l1,img_n,shape)       

        elif n==10: # Squares & Triangles
            shape='tri10'; img_n=0; l1=[]
            s=5.856; h=s*1.732/2; dx=16; dy=dx
            y=s/2
            for r in range(2):
                x=h/2
                for c in range(2): l1.append((x,y)); x+=dx
                y+=dy
            x=h/2+dx/2; y=s/2+dy/2
            for c in range(2): l1.append((x,y)); x+=dx
            self.init(l1,img_n,shape)       
            shape='sq10'; img_n=1; l1=[]
            y=(1.5*s+h)/2
            for r in range(2):
                x=(.5*s+h)/2
                for c in range(2): l1.append((x,y)); x+=dx
                y+=dy
            y=(1.5*s+h)/2-dy/2
            for r in range(2):
                x=(.5*s+h)/2+dx/2
                for c in range(2): l1.append((x,y)); x+=dx
                y+=dy
            self.init(l1,img_n,shape)       
            shape='sq11'; img_n=2; l1=[]
            y=(1.5*s+h)/2-dy/2
            for r in range(2):
                x=(.5*s+h)/2
                for c in range(2): l1.append((x,y)); x+=dx
                y+=dy
            y=(1.5*s+h)/2
            for r in range(2):
                x=(.5*s+h)/2+dx/2
                for c in range(2): l1.append((x,y)); x+=dx
                y+=dy
            self.init(l1,img_n,shape)       
            shape='tri11'; img_n=3; l1=[]
            y=s/2
            for r in range(2):
                x=16-h/2
                for c in range(2): l1.append((x,y)); x+=dx
                y+=dy
            x=s/2+h/2; y=s/2+dy/2
            for c in range(2): l1.append((x,y)); x+=dx
            self.init(l1,img_n,shape)       
            shape='tri12'; img_n=4; l1=[]
            y=s+h/2-dy/2
            for r in range(2):
                x=h+s/2
                for c in range(2): l1.append((x,y)); x+=dx
                y+=dy
            x=0; y=s+h/2
            for c in range(3): l1.append((x,y)); x+=dx
            self.init(l1,img_n,shape)       
            shape='tri13'; img_n=5; l1=[]
            y=s/2+h/2
            for r in range(2):
                x=h+s/2
                for c in range(2): l1.append((x,y)); x+=dx
                y+=dy
            x=0; y=s+h+h/2
            for c in range(3): l1.append((x,y)); x+=dx
            self.init(l1,img_n,shape)       

        elif n==11: # Squares & Triangles
            shape='sq14'; img_n=0; l1=[]; s=8; h=s*1.732/2
            x=s/2; y=s/2; dx=s; dy=s+h
            for c in range(4): l1.append((x,y)); x+=dx
            x=0; y+=dy
            for c in range(5): l1.append((x,y)); x+=dx
            self.init(l1,img_n,shape)       
            shape='tri15'; img_n=1; l1=[]
            x=s/2; y=s+h/2; dx=s
            for c in range(4): l1.append((x,y)); x+=dx
            self.init(l1,img_n,shape)       
            shape='tri14'; img_n=2; l1=[]
            x=0; y=s+h/2; dx=s
            for c in range(5): l1.append((x,y)); x+=dx
            self.init(l1,img_n,shape)       

        elif n==12: # Hexagons & Triangles
            s=5.333; h=s*1.732/2
            shape='hex16'; img_n=0; l1=[]
            l1.append((s/2,h))
            l1.append((3*s,2*h))
            l1.append((5*s,0))
            l1.append((s,4*h))
            l1.append((3.5*s,5*h))
            l1.append((5.5*s,3*h))
            self.init(l1,img_n,shape)
            shape='tri16'; img_n=1; l1=[]
            dx=s
            x=1.5*s; y=.5*h
            for c in range(3): l1.append((x,y)); x+=dx
            x=4*s; y=1.5*h
            for c in range(3): l1.append((x,y)); x+=dx
            l1.append((2*s,y))
            x=s/2; y=2.5*h
            for c in range(2): l1.append((x,y)); x+=dx
            l1.append((4.5*s,y))
            x=2*s; y=3.5*h
            l1.append((0,y))
            for c in range(3): l1.append((x,y)); x+=dx
            x=4.5*s; y=4.5*h
            l1.append((2.5*s,y))
            for c in range(2): l1.append((x,y)); x+=dx
            self.init(l1,img_n,shape)
            
            shape='tri17'; img_n=2; l1=[]
            x=2*s; y=.5*h
            for c in range(3): l1.append((x,y)); x+=dx
            l1.append((32,y))
            x=4.5*s; y=1.5*h
            l1.append((1.5*s,y))
            for c in range(2): l1.append((x,y)); x+=dx
            x=0; y=2.5*h
            for c in range(3): l1.append((x,y)); x+=dx
            l1.append((4*s,y))
            x=2.5*s; y=3.5*h
            for c in range(3): l1.append((x,y)); x+=dx
            y=4.5*h
            l1.append((0,y)); l1.append((2*s,y)); l1.append((5*s,y)); l1.append((32,y))
            self.init(l1,img_n,shape)
        self.setup()

class Piece:
    def __init__(self,img_n,(cx,cy)):
        self.img_n=img_n; self.c0=(g.sx(cx),g.sy(cy))
        self.done=False; self.c=(0,0)
    
