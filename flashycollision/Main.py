import pygame
import environment
from sys import exit
import math


class button:
    def __init__(self, buttonwidth, buttonheight, buttonposition, offsetx, offsety, pressedcolor, nonpressedcolor,
                 updatable=True, isvisible=False):
        self._ispressed = False
        self._isvisible = isvisible
        self.updatable = updatable
        self.pressedcolor = pressedcolor
        self.nonpressedcolor = nonpressedcolor
        self._color = nonpressedcolor
        self._rect = pygame.Rect(buttonposition, (buttonwidth, buttonheight))
        self.width = buttonwidth
        self.height = buttonheight
        self.position = buttonposition
        self.offsetx = offsetx
        self.offsety = offsety

    def updateposition(self, referencepoint):
        if self.updatable:
            self.position = (referencepoint[0] + self.offsetx, referencepoint[1] + self.offsety)
            self._rect = pygame.Rect(self.position, (self.width, self.height))

    def press(self):
        self._ispressed = not self._ispressed
        if self._ispressed: self._color = self.pressedcolor
        else: self._color = self.nonpressedcolor

    @property
    def isvisible(self):
        return self._isvisible

    @isvisible.setter
    def isvisible(self, bool):
        self._isvisible = bool

    @property
    def ispressed(self):
        return self._ispressed

    @property
    def color(self):
        return self._color

    @property
    def rect(self):
        return self._rect


class textbutton(button):
    def __init__(self, buttonposition, offsetx, offsety, pressedcolor, nonpressedcolor, value=0, fontsize = 14,
                 updatable=True, isvisible=False):
        button.__init__(self, 0, 0, buttonposition, offsetx, offsety, pressedcolor, nonpressedcolor, updatable=updatable, isvisible=isvisible)
        self.font = pygame.font.SysFont("timesnewroman", fontsize)
        self._value = value
        self._text = self.font.render(str(value), False, (255, 255, 255), self._color)
        self._rect = self._text.get_rect(topleft=buttonposition)

    @property
    def value(self):
        return self._value

    @property
    def text(self):
        return self._text

    def press(self):
        super().press()
        self._text = self.font.render(str(self._value), False, (255, 255, 255), self._color)

    def updateposition(self, referencepoint):
        if self.updatable:
            self.position = (referencepoint[0] + self.offsetx, referencepoint[1] + self.offsety)
            self._rect = self._text.get_rect(topleft=self.position)

    def updatevalue(self, value):
        self._value = value
        self._text = self.font.render(str(self._value), False, (255, 255, 255), self._color)
        self._rect = self._text.get_rect(topleft=self.position)


class slider:
    def __init__(self, ballradius, initialrectwidth, initialrectheight, minvalue, maxvalue, slidertext, lefttopcoordinate,
                 initialscreenwidth=800, initialscreenheight=600, defaultvalue=0, fontsize=15, scale=False, reposition=True, valueconverter=lambda val: val,
                 ballcolor=(255, 255, 255), slidercolor=(255, 255, 255), slidertextcolor=(255, 255, 255), offsetx=0, offsety=0):
        self.repositionable = reposition
        self.offsetx = offsetx
        self.offsety = offsety
        self.scalable = scale
        self.font = pygame.font.SysFont('timesnewroman',  fontsize)
        self.minvaluetext = self.font.render(str(minvalue), False, (255,255,255), (0,0,0))
        self.maxvaluetext = self.font.render(str(maxvalue), False, (255, 255, 255), (0, 0, 0))
        self.actualvaluetext = self.font.render(str(defaultvalue), False, (255, 255, 255), (0, 0, 0))
        self.slidertext = self.font.render(slidertext, False, slidertextcolor, (0, 0, 0))
        self.xrectanglescale = initialrectwidth / initialscreenwidth
        self.yrectanglescale = initialrectheight / initialscreenheight
        self.xpositionscale = lefttopcoordinate[0] / initialscreenwidth
        self.ypositionscale = lefttopcoordinate[1] / initialscreenheight
        self.lefttop = lefttopcoordinate
        self._actualvalue = defaultvalue
        self.sliderwidth = initialrectwidth
        self.sliderheight = initialrectheight
        self.minvalue = minvalue
        self.maxvalue = maxvalue
        self._rectangle = pygame.Rect(lefttopcoordinate, (initialrectwidth, initialrectheight))
        self._ball = [[lefttopcoordinate[0] + initialrectwidth * (defaultvalue-minvalue) / (maxvalue - minvalue),
                       lefttopcoordinate[1] + initialrectheight/2], ballradius, ballcolor]
        self._valconverter = valueconverter
        self.slidercolor = slidercolor
        self.minvaluetextrect = self.minvaluetext.get_rect(center=(self.lefttop[0] - self.minvaluetext.get_width()/2 -
                                                                   ballradius, self.lefttop[1] + self.sliderheight / 2))

        self.maxvaluetextrect = self.maxvaluetext.get_rect(center=(self.lefttop[0] + self.sliderwidth +
                                self.maxvaluetext.get_width()/2 + ballradius, self.lefttop[1] + self.sliderheight/2))

        self.actualvaluetextrect = self.actualvaluetext.get_rect(center=(self.lefttop[0] + self.sliderwidth/2,
                                                    self.lefttop[1] - self.actualvaluetext.get_height()/2 - ballradius))

        self.slidertextrect = self.slidertext.get_rect(center=(self.lefttop[0] + self.sliderwidth/2, self.lefttop[1] +
                                                               self.slidertext.get_height()))

    @property
    def actualvalue(self):
        return self._actualvalue

    @actualvalue.setter
    def actualvalue(self, nv):
        if nv < self.minvalue or nv > self.maxvalue: raise ValueError

        else:
            self._actualvalue = nv
            self.actualvaluetext = self.font.render(str(self._actualvalue), False, (255, 255, 255), (0, 0, 0))
            self.actualvaluetextrect = self.actualvaluetext.get_rect(center=(self.lefttop[0] + self.sliderwidth / 2,
                                            self.lefttop[1] - self.actualvaluetext.get_height() / 2 - self._ball[1]))
            self._ball[0][0] = self.lefttop[0] + self.sliderwidth * (self.actualvalue - self.minvalue) / (
                                                    self.maxvalue - self.minvalue)

    @property
    def valconverter(self):
        return self._valconverter

    @valconverter.setter
    def valconverter(self, f):
        self._valconverter = f

    @property
    def rectangle(self):
        return self._rectangle

    @rectangle.setter
    def rectangle(self, newr):
        self._rectangle = newr

    @property
    def ball(self):
        return self._ball

    @ball.setter
    def ball(self, newb):
        self._ball = newb

    def collidepoint(self, point):
        return self._rectangle.collidepoint(point)

    def updatevaluefrompoint(self, xpoint):
        if xpoint <= self.lefttop[0]:
            lamb = 0
            self._ball[0][0] = self.lefttop[0]
        elif xpoint >= self.lefttop[0] + self.sliderwidth:
            lamb = 1
            self._ball[0][0] = self.lefttop[0] + self.sliderwidth
        else:
            lamb = (xpoint - self.lefttop[0]) / self.sliderwidth
            self._ball[0][0] = xpoint

        self._actualvalue = self._valconverter(lamb * self.maxvalue + (1 - lamb) * self.minvalue)
        self.actualvaluetext = self.font.render(str(self._actualvalue), False, (255, 255, 255), (0, 0, 0))
        self.actualvaluetextrect = self.actualvaluetext.get_rect(center=(self.lefttop[0] + self.sliderwidth / 2,
                                                self.lefttop[1] - self.actualvaluetext.get_height()/2 - self._ball[1]))

    def updateextremevalues(self, minvalue, maxvalue):
        if minvalue > maxvalue: raise ValueError
        self.minvalue = minvalue
        self.maxvalue = maxvalue
        self.minvaluetextrect = self.minvaluetext.get_rect(center=(self.lefttop[0] - self.minvaluetext.get_width()/2 -
                                                                self._ball[1],self.lefttop[1] + self.sliderheight / 2))
        self.maxvaluetextrect = self.maxvaluetext.get_rect(center=(self.lefttop[0] + self.sliderwidth +
                                self.maxvaluetext.get_width()/2 + self._ball[1], self.lefttop[1] + self.sliderheight/2))

        if self._actualvalue < self.minvalue:
            self._actualvalue = self.minvalue
            self.actualvaluetext = self.font.render(str(self.actualvalue), False, (255, 255, 255), (0, 0, 0))
        elif self._actualvalue > self.maxvalue:
            self._actualvalue = self.maxvalue
            self.actualvaluetext = self.font.render(str(self.actualvalue), False, (255, 255, 255), (0, 0, 0))

        if self.maxvalue != self.minvalue:
            self._ball[0][0] = self.lefttop[0] + self.sliderwidth * (self.actualvalue - self.minvalue) / (
                    self.maxvalue - self.minvalue)
        else:
            self._ball[0][0] = self.lefttop[0]
        self.minvaluetext = self.font.render(str(minvalue), False, (255, 255, 255), (0, 0, 0))
        self.maxvaluetext = self.font.render(str(maxvalue), False, (255, 255, 255), (0, 0, 0))

    def updatescreendimensions(self, newwidth, newheight, refpoint):
        if self.repositionable:
            self.lefttop = (refpoint[0] + self.offsetx, refpoint[1] + self.offsety)
            self._ball[0][0] = self.lefttop[0] + self.sliderwidth * (self.actualvalue - self.minvalue) / (
                        self.maxvalue - self.minvalue)
            self._ball[0][1] = self.lefttop[1] + self.sliderheight / 2
            self._rectangle = pygame.Rect(self.lefttop, (self.sliderwidth, self.sliderheight))
            self.minvaluetextrect = self.minvaluetext.get_rect(center=(
            self.lefttop[0] - self.minvaluetext.get_width() / 2 - self._ball[1], self.lefttop[1] + self.sliderheight / 2))
            self.maxvaluetextrect = self.maxvaluetext.get_rect(center=(
            self.lefttop[0] + self.sliderwidth + self.maxvaluetext.get_width() / 2 + self._ball[1],
                                                                               self.lefttop[1] + self.sliderheight / 2))
            self.actualvaluetextrect = self.actualvaluetext.get_rect(center=(self.lefttop[0] + self.sliderwidth / 2,
                                       self.lefttop[1] - self.actualvaluetext.get_height() / 2 - self._ball[1]))
            self.slidertextrect = self.slidertext.get_rect(
                center=(self.lefttop[0] + self.sliderwidth / 2, self.lefttop[1] + self.slidertext.get_height()))

        if self.scalable:
            self.lefttop = (newwidth * self.xpositionscale, newheight * self.ypositionscale)
            self.sliderwidth = newwidth * self.xrectanglescale
            self.sliderheight = newheight * self.yrectanglescale
            self._ball[0][0] = self.lefttop[0] + self.sliderwidth * (self._actualvalue - self.minvalue) / \
                                                                                        (self.maxvalue - self.minvalue)
            self._ball[0][1] = self.lefttop[1] + self.sliderheight/2
            self._rectangle = pygame.Rect(self.lefttop, (self.sliderwidth, self.sliderheight))
            self.minvaluetextrect = self.minvaluetext.get_rect(center=(
                self.lefttop[0] - self.minvaluetext.get_width() / 2 - self._ball[1],
                self.lefttop[1] + self.sliderheight / 2))
            self.maxvaluetextrect = self.maxvaluetext.get_rect(center=(
                self.lefttop[0] + self.sliderwidth + self.maxvaluetext.get_width() / 2 + self._ball[1],
                self.lefttop[1] + self.sliderheight / 2))
            self.actualvaluetextrect = self.actualvaluetext.get_rect(
                center=(self.lefttop[0] + self.sliderwidth / 2, self.lefttop[1] - self.actualvaluetext.get_height()))
            self.slidertextrect = self.slidertext.get_rect(
                center=(self.lefttop[0] + self.sliderwidth / 2, self.lefttop[1] + self.slidertext.get_height()))


def updateguipositions(newwidth, newheight):
    buttons["gui"].isvisible = True
    # update slides positions
    if buttons["settings"].isvisible and buttons["settings"].ispressed:
        for key in configslides:
            sliders[key].updatescreendimensions(newwidth, newheight, (0, newheight))

    if buttons["attributes"].isvisible:
        for key in attributeslides:
            sliders[key].updatescreendimensions(newwidth, newheight, (newwidth, 0))
        buttons["collision"].updateposition(
            (sliders["mass"].minvaluetextrect.topleft[0], sliders["mass"].lefttop[1]))

    ##update buttons positions
    for key in ["gui", "settings"]:
        if buttons[key].isvisible: buttons[key].updateposition((0, newheight))

    for key in ["pause", "vectorval", "select"]:
        if buttons[key].isvisible: buttons[key].updateposition((newwidth // 2, 0))

    for key in ["attributes"]:
        if buttons[key].isvisible: buttons[key].updateposition((newwidth, 0))

    if buttons["attributes"].isvisible:
        for key in ["vx", "vy", "ax", "ay", "plus", "minus", "selector"]:
            buttons[key].updateposition((newwidth, newheight))

    buttons["grid"].updateposition(
        (sliders["partitions"].maxvaluetextrect.topright[0], sliders["partitions"].lefttop[1]))

def updateslidesvalues(sliderkey, selectid):
    if sliderkey in configslides:
        if sliderkey == "dt":
            env.updatedt(sliders["dt"].actualvalue)
        elif sliderkey == "shifty":
            env.updatesettings(shifty=sliders["shifty"].actualvalue)
            sliders["radius"].updateextremevalues(0, int(env.maxradius))
        elif sliderkey == "shiftx":
            env.updatesettings(shiftx=sliders["shiftx"].actualvalue)
            sliders["radius"].updateextremevalues(0, int(env.maxradius))
        elif sliderkey == "partitions":
            env.updatesettings(partitions=sliders["partitions"].actualvalue)
            sliders["radius"].updateextremevalues(0, int(env.maxradius))
        return

    if sliderkey in attributeslides and selectid in env.idparticles:
        if sliderkey in {"red", "green", "blue"}:
            env.updateparticleattibutes(selectid, color=(sliders["red"].actualvalue, sliders["green"].actualvalue, sliders["blue"].actualvalue))
        elif sliderkey == "mass":
            env.updateparticleattibutes(selectid, mass=10**sliders["mass"].actualvalue)
        elif sliderkey == "radius":
            env.updateparticleattibutes(selectid, radius=sliders["radius"].actualvalue)
        elif sliderkey == "layer":
            env.updateparticleattibutes(selectid, layer=sliders["layer"].actualvalue)
        elif sliderkey == "k":
            env.updateparticleattibutes(selectid, k=sliders["k"].actualvalue)
        elif sliderkey == "kspring":
            env.updateparticleattibutes(selectid, kspring=sliders["kspring"].actualvalue)
        elif sliderkey == "c":
            env.updateparticleattibutes(selectid, c=sliders["c"].actualvalue)
        elif sliderkey == "lambda":
            env.updateparticleattibutes(selectid, lamb=sliders["lambda"].actualvalue)
        elif sliderkey == "G":
            env.updateparticleattibutes(selectid, G=sliders["G"].actualvalue)

def selectparticle(selectid):
    sliders["red"].actualvalue = env.particlesdata[selectid][1][0]
    sliders["green"].actualvalue = env.particlesdata[selectid][1][1]
    sliders["blue"].actualvalue = env.particlesdata[selectid][1][2]
    sliders["mass"].actualvalue = sliders["mass"].valconverter(math.log10(env.idparticles[selectid].mass))
    sliders["radius"].actualvalue = sliders["radius"].valconverter(env.idparticles[selectid].radius)
    sliders["layer"].actualvalue = env.particlesdata[selectid][0]
    sliders["k"].actualvalue = sliders["k"].valconverter(env.idparticles[selectid].k )
    sliders["kspring"].actualvalue = sliders["kspring"].valconverter(env.idparticles[selectid].kspring )
    sliders["lambda"].actualvalue = sliders["lambda"].valconverter(env.idparticles[selectid].lamb)
    sliders["c"].actualvalue = sliders["c"].valconverter(env.idparticles[selectid].c)
    sliders["G"].actualvalue = sliders["G"].valconverter(env.idparticles[selectid].G)

    if buttons["collision"].ispressed != env.idparticles[selectid].iscollidable:
        buttons["collision"].press()

    # if buttons["attributes"].ispressed is False:
    #     buttons["attributes"].press()
    #     for key in ["collision", "vx", "vy", "ax", "ay"]:
    #         buttons[key].isvisible = not buttons[key].isvisible

def keyhandler(mousepos, selectid, event):
    targetid = env.getoparticleidfrompoint(mousepos)

    if event.key == pygame.K_v:
        newvelocity = (mousepos[0] - env.idparticles[selectid].position[0], mousepos[1] - env.idparticles[selectid].position[1])
        env.updateparticleattibutes(selectid, velocity=newvelocity)
        return

    if event.key == pygame.K_a:
        newaccel = (mousepos[0] - env.idparticles[selectid].position[0], mousepos[1] - env.idparticles[selectid].position[1])
        env.updateparticleattibutes(selectid, constantacceleration=newaccel)
        return

    if event.key == pygame.K_d:
        env.deleteparticle(selectid)
        return

    if event.key == pygame.K_c:
        env.updateparticleattibutes(selectid, spring=mousepos)
        return

    if event.key == pygame.K_q:
        env.updateparticleattibutes(selectid, position=mousepos)

    if event.key == pygame.K_h and env.mouseid in env.idparticles:
        if env.mouseid in env.idparticles[selectid].gravityid:
            env.deleteparticlebond(selectid, gravityid={env.mouseid})
            return
        env.updateparticlebond(selectid, gravityids={env.mouseid})
        return

    if event.key == pygame.K_l and env.mouseid in env.idparticles:
        if env.mouseid in env.idparticles[selectid].springid:
            env.deleteparticlebond(selectid, springids=env.mouseid)
            return
        env.updateparticlebond(selectid, springids={env.mouseid : sliders["l0"].actualvalue})
        return

    if targetid != selectid and targetid in env.idparticles:
        if event.key == pygame.K_g:

            if targetid in env.idparticles[selectid].gravityid:
                env.deleteparticlebond(selectid, gravityid=targetid)
                return
            env.updateparticlebond(selectid, gravityids={targetid})
            return

        elif event.key == pygame.K_k:
            if targetid in env.idparticles[selectid].springid:
                env.deleteparticlebond(selectid, springid=targetid)
                return
            env.updateparticlebond(selectid, springids={targetid : sliders["l0"].actualvalue})
            return

pygame.init()
pygame.mixer.init() ########3 posible deletion #######33
clock = pygame.time.Clock()

fps = 60

screen = pygame.display.set_mode((800, 600), pygame.DOUBLEBUF | pygame.RESIZABLE)
pygame.display.set_caption("flashycollision")

sliders = {}
sliders["partitions"] = slider(6, 140, 5, 3, min(screen.get_width()//4, screen.get_height()//4), "partitions", (50, 220),
                               defaultvalue=3, valueconverter=int, offsetx=50, offsety=-380)
sliders["shiftx"] = slider(6, 140, 5, -(screen.get_width()//3), screen.get_width(), "shiftx", (50, 300), valueconverter=int,
                           offsetx=50, offsety=-300)
sliders["shifty"] = slider(6, 140, 5, -(screen.get_height()//3), screen.get_height(), "shifty", (50, 380), valueconverter=int,
                           offsetx=50, offsety=-220)
sliders["fps"] = slider(6, 140, 5, 1, 120, "fpscap", (50, 460), defaultvalue=60, valueconverter=int, offsetx=50, offsety=-140)

sliders["dt"] = slider(6, 140, 5, 0.001, 0.2, "dt", (50, 540), defaultvalue=0.017, valueconverter=lambda val: round(val, ndigits=3),
                       offsetx=50, offsety=-60)

sliders["red"] = slider(5, 168, 4, 0, 255, "", (screen.get_width() - 206, 25), defaultvalue=255, fontsize=14, valueconverter=int,
                 ballcolor=(255,0,0), slidercolor=(255,0,0), slidertextcolor=(255,0,0), offsetx=-206, offsety=25)
sliders["green"] = slider(5, 168, 4, 0, 255, "", (screen.get_width() - 206, 55), defaultvalue=0, fontsize=14, valueconverter=int,
                 ballcolor=(0,255,0), slidercolor=(0,255,0), slidertextcolor=(0,255,0), offsetx=-206, offsety=55)
sliders["blue"] = slider(5, 168, 4, 0, 255, "", (screen.get_width() - 206, 85), defaultvalue=0, fontsize=14, valueconverter=int,
                 ballcolor=(0,0,255), slidercolor=(0,0,255), slidertextcolor=(0,0,255), offsetx=-206, offsety=85)
sliders["mass"] = slider(5, 168, 4, 0, 10, "mass (base 10)", (screen.get_width() - 206, 115), defaultvalue=0, fontsize=14, valueconverter=lambda val: round(val, ndigits=3),
                 slidertextcolor=(255,255,255), offsetx=-206, offsety=115)
sliders["radius"] = slider(5, 168, 4, 0, min(screen.get_width(), screen.get_height())//2, "radius", (screen.get_width() - 206, 165),
                 defaultvalue=10, fontsize=14, valueconverter=int, offsetx=-206, offsety=165)
sliders["layer"] = slider(5, 168, 4, 0, 4, "layer", (screen.get_width() - 206, 215),fontsize=14, valueconverter=int,
                 offsetx=-206, offsety=215)
sliders["k"] = slider(5, 168, 4, -4, 4, "k/m (other particles)", (screen.get_width() - 206, 265),fontsize=14, valueconverter=lambda val: round(val, ndigits=3) ,
                 offsetx=-206, offsety=265, slidertextcolor=(78, 78, 191), slidercolor=(78, 78, 191))

### add button to ks and lambdas
sliders["l0"] = slider(5, 168, 4, 0, 400, "l_0 (other particles)", (screen.get_width() - 206, 315),fontsize=14, valueconverter=int,
                 offsetx=-206, offsety=315, slidertextcolor=(60, 26, 180), slidercolor=(60, 26, 180))
sliders["kspring"] = slider(5, 168, 4, -4, 4, "k_s/m (fixed point)", (screen.get_width() - 206, 365),fontsize=14, valueconverter=lambda val: round(val, ndigits=3) ,
                 offsetx=-206, offsety=365, slidertextcolor=(200, 0, 0), slidercolor=(200, 0, 0))
sliders["lambda"] = slider(5, 168, 4, -4, 4, "λ/m (viscosity constant)", (screen.get_width() - 206, 415),fontsize=14, valueconverter=lambda val: round(val, ndigits=3) ,
                 offsetx=-206, offsety=415)

sliders["c"] = slider(5, 168, 4, 0, 2, "c (restitution constant)", (screen.get_width() - 206, 465),fontsize=14, valueconverter=lambda val: round(val, ndigits=3) ,
                 offsetx=-206, offsety=465, defaultvalue=1)
sliders["G"] = slider(5, 168, 4, -1, 1, "G (gravity constant)", (screen.get_width() - 206, 515),fontsize=14, valueconverter=lambda val: round(val, ndigits=2),
                 offsetx=-206, offsety=515, defaultvalue=1, slidertextcolor=(59, 156, 122), slidercolor=(59, 156, 122))

configslides = {"partitions", "shiftx", "shifty", "fps", "dt"}
attributeslides = {"green", "blue", "mass", "red", "radius", "layer", "k", "kspring", "c", "lambda", "G", "l0"}

buttons = {}
buttons["gui"] = button(25, 25, (0, screen.get_height() - 25), 0, -25, (255, 0, 255), (100, 100, 100), isvisible=True)
buttons["gui"].press()
buttons["settings"] = button(25, 25, (25, screen.get_height() - 25), 25, -25, (200, 60, 200), (80, 100, 200), isvisible=True)
buttons["grid"] = button(10, 10, (sliders["partitions"].maxvaluetextrect.topright[0] + 10, sliders["partitions"].lefttop[1]), 10, 0, (255, 255, 255), (255, 255, 255), isvisible=False)
buttons["pause"] = button(30, 30, (screen.get_width()//2 -15, 0), -15, 0, (250, 0, 0), (0, 171, 240), isvisible=True)
buttons["vectorval"] = button(15, 15, (screen.get_width()//2 + 15, 0), 15, 0, (250, 255, 255), (255, 255, 255), isvisible=True)
buttons["select"] = button(20, 20, (screen.get_width()//2 -35, 0), -35, 0, (150, 150, 150), (90, 90, 90), isvisible=True)
buttons["mouseparticle"] = button(20, 20, (0, 0), 0, 0, (200, 200, 200), (30, 30, 30), updatable=False, isvisible=True)
buttons["mouseattributes"] = button(15, 15, (20, 0), 0, 0, (255, 255, 255), (255, 255, 255), updatable=False, isvisible=False)
buttons["attributes"] = button(15, 15, (screen.get_width() - 15, 0), -15, 0, (255, 255, 255), (200, 200, 200), isvisible=True)
buttons["collision"] = button(10, 10, (sliders["mass"].minvaluetextrect.topleft[0] - 20, sliders["mass"].lefttop[1]), -20, 0,
                              (255,255,255), (100, 100, 100), isvisible=False)
buttons["collision"].press()
buttons["vx"] = textbutton((screen.get_width() - 328, screen.get_height() - 20), -328, -20, (70, 70, 70), (70, 70, 70), value=0)
buttons["vy"] = textbutton((screen.get_width() - 328, screen.get_height() - 40), -328, -40, (70, 70, 70), (70, 70, 70), value=0)
buttons["ax"] = textbutton((screen.get_width() - 428, screen.get_height() - 20), -428, -20, (70, 70, 70), (70, 70, 70), value=0)
buttons["ay"] = textbutton((screen.get_width() - 428, screen.get_height() - 40), -428, -40, (70, 70, 70), (70, 70, 70), value=0)
buttons["minus"] = textbutton((screen.get_width() - 20, screen.get_height() - 20), -20, -20, (70, 70, 70), (70, 70, 70), value=" - ", fontsize=18)
buttons["plus"] = textbutton((screen.get_width() - 18, screen.get_height() - 40), -18, -40, (70, 70, 70), (70, 70, 70), value="+", fontsize=18)
buttons["selector"] = textbutton((screen.get_width() - 60, screen.get_height() - 40), -60, -40, (70, 70, 70), (70, 70, 70), value="Ax", fontsize=16)


issliding = False
sliderkey = ""
movingparticle = False
movid = None
selectid = None


env = environment.Environment(fps, screen.get_width(), screen.get_height(), 0, 0, 3)
a = []

while True:
    clock.tick(fps)
    screen.fill((0,0,0))

    if selectid not in env.idparticles and selectid is not None:
        selectid = None

    if movid in env.idparticles:
        env.updateparticleattibutes(movid, position=pygame.mouse.get_pos(), velocity=(0,0))

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            print("performance: ", sum(a) / len(a))
            pygame.quit()
            exit()

        elif event.type == pygame.VIDEORESIZE:
            newheight = event.h
            newwidth = event.w

            ## updating sliders depending of screen dimensions
            sliders["shiftx"].updateextremevalues(-(newwidth // 3), newwidth)
            sliders["shifty"].updateextremevalues(-(newheight // 3), newheight)
            sliders["partitions"].updateextremevalues(3, 4 + min(newwidth // 4, newheight // 4))
            sliders["radius"].updateextremevalues(0, int(env.maxradius))
            env.updatesettings(shiftx=sliders["shiftx"].actualvalue, shifty=sliders["shifty"].actualvalue,
                               height=newheight, width=newwidth, partitions=sliders["partitions"].actualvalue)

            if newheight < 580 or newwidth < 500:
                buttons["gui"].isvisible = False

            else: updateguipositions(newwidth, newheight)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mousepos = pygame.mouse.get_pos()
                targetid = env.getoparticleidfrompoint(mousepos)

                if buttons["select"].ispressed and buttons["select"].isvisible and \
                        targetid is not None:
                    if targetid != selectid:
                        selectid = targetid
                        selectparticle(selectid)
                    else: selectid = None
                    buttons["select"].press()

                if not env.mouseid in env.idparticles and targetid is not None:
                    movingparticle = True
                    movid = targetid

                if buttons["gui"].rect.collidepoint(mousepos):
                    buttons["gui"].press()

                elif buttons["gui"].isvisible and buttons["gui"].ispressed:
                    buttonkey = ""

                    for key, button in buttons.items():
                        if button.rect.collidepoint(mousepos) and button.isvisible:
                            button.press()
                            buttonkey = key
                            break

                    if buttonkey != "":
                        ### do something depending on the button pressed
                        if buttonkey == "settings":
                            buttons["grid"].isvisible = not buttons["grid"].isvisible

                        elif buttonkey == "mouseparticle":
                            buttons["mouseattributes"].isvisible = not buttons["mouseattributes"].isvisible

                            if buttons["mouseparticle"].ispressed:
                                env.addmouseparticle(sliders["radius"].actualvalue, int(10**sliders["mass"].actualvalue),
                                    iscollidable=buttons["collision"].ispressed, color=(sliders["red"].actualvalue,
                                    sliders["green"].actualvalue, sliders["blue"].actualvalue), layer=sliders["layer"].actualvalue)
                                selectid = env.mouseid
                                selectparticle(selectid)

                            else:
                                env.deleteparticle(env.mouseid)

                        elif buttonkey == "attributes":
                            for key in ["collision", "vx", "vy", "ax", "ay", "plus", "minus", "selector"]:
                                buttons[key].isvisible = not buttons[key].isvisible

                        elif buttonkey == "mouseattributes":
                            if selectid == env.mouseid: selectid = None
                            else:
                                selectid = env.mouseid
                                selectparticle(selectid)

                        elif buttonkey == "collision" and selectid is not None:
                            env.updateparticleattibutes(selectid, iscollidable=buttons["collision"].ispressed)
                        elif buttonkey == "vx" and selectid is not None:
                            env.updateparticleattibutes(selectid, velocity=(0, env.idparticles[selectid].velocity[1]))
                        elif buttonkey == "vy" and selectid is not None:
                            env.updateparticleattibutes(selectid, velocity=(env.idparticles[selectid].velocity[0], 0))
                        elif buttonkey == "ax" and selectid is not None:
                            env.updateparticleattibutes(selectid, constantacceleration=(0, env.idparticles[selectid].constantacceleration[1]))
                        elif buttonkey == "ay" and selectid is not None:
                            env.updateparticleattibutes(selectid, constantacceleration=(env.idparticles[selectid].constantacceleration[0], 0))
                        elif buttonkey == "selector":
                            i = (["Ax", "Ay", "k", "λ", "k_s"].index(buttons["selector"].value) + 1) % 5
                            buttons["selector"].updatevalue(["Ax", "Ay", "k", "λ", "k_s"][i])
                        elif buttonkey == "plus":

                            val = buttons["selector"].value
                            if val == "Ax" and selectid is not None:
                                env.updateparticleattibutes(selectid, constantacceleration=(2 * env.idparticles[selectid].constantacceleration[0],
                                                                                            env.idparticles[selectid].constantacceleration[1]))
                            elif val == "Ay" and selectid is not None:
                                env.updateparticleattibutes(selectid, constantacceleration=(
                                env.idparticles[selectid].constantacceleration[0], 2 * env.idparticles[selectid].constantacceleration[1]))
                            elif val == "k":
                                sliders["k"].updateextremevalues(sliders["k"].minvalue - 20, sliders["k"].maxvalue + 20)
                            elif val == "λ":
                                sliders["lambda"].updateextremevalues(sliders["lambda"].minvalue - 20, sliders["lambda"].maxvalue + 20)
                            elif val == "k_s":
                                sliders["kspring"].updateextremevalues(sliders["kspring"].minvalue - 20, sliders["kspring"].maxvalue + 20)
                        elif buttonkey == "minus":

                            val = buttons["selector"].value
                            if val == "Ax" and selectid is not None:
                                env.updateparticleattibutes(selectid, constantacceleration=(0.5 * env.idparticles[selectid].constantacceleration[0],
                                                                                            env.idparticles[selectid].constantacceleration[1]))
                            elif val == "Ay" and selectid is not None:
                                env.updateparticleattibutes(selectid, constantacceleration=(
                                env.idparticles[selectid].constantacceleration[0], 0.5 * env.idparticles[selectid].constantacceleration[1]))
                            elif val == "k" and ( minv := sliders["k"].minvalue + 20 ) < 0 and ( maxv := sliders["k"].maxvalue - 20 ) > 0:
                                sliders["k"].updateextremevalues(minv, maxv)
                            elif val == "λ" and ( minv := sliders["lambda"].minvalue + 20 ) < 0 and ( maxv := sliders["lambda"].maxvalue - 20 ) > 0:
                                sliders["lambda"].updateextremevalues(minv, maxv)
                            elif val == "k_s" and ( minv := sliders["kspring"].minvalue + 20 ) < 0 and ( maxv := sliders["kspring"].maxvalue - 20 ) > 0:
                                sliders["kspring"].updateextremevalues(minv, maxv)

                    else:
                        # check slides collision
                        keys = set()
                        if buttons["settings"].ispressed:
                            keys.update(configslides)

                        if buttons["attributes"].ispressed:
                            keys.update(attributeslides)

                        for key in keys:
                            if sliders[key].collidepoint(mousepos):
                                sliders[key].updatevaluefrompoint(mousepos[0])
                                issliding = True
                                sliderkey = key
                                break

                        if sliderkey != "":
                            updateslidesvalues(sliderkey, selectid)
                            if sliderkey == "fps": fps = sliders["fps"].actualvalue

            if event.button == 2:
                env.clearallparticles()
                selectid = None

            if event.button == 3:
                layer = sliders["layer"].actualvalue
                radius = sliders["radius"].actualvalue
                mass = 10**sliders["mass"].actualvalue
                k = sliders["k"].actualvalue
                lamb = sliders["lambda"].actualvalue
                c = sliders["c"].actualvalue
                kspring = sliders["kspring"].actualvalue
                color = (sliders["red"].actualvalue, sliders["green"].actualvalue, sliders["blue"].actualvalue)
                G = sliders["G"].actualvalue
                constantacc = (buttons["ax"].value, buttons["ay"].value)
                if selectid is not None:
                    springid = env.idparticles[selectid].springid.copy()
                    gravityid = env.idparticles[selectid].gravityid.copy()
                else:
                    springid = {}
                    gravityid = set()
                env.createparticle(radius, mass, springid, gravityid, v0=(0, 0), layer= layer, r0=pygame.mouse.get_pos(), c=c,
                            lamb=lamb, constantacceleration=constantacc, k=k, iscollidable=buttons["collision"].ispressed, color=color,
                            kspring=kspring, spring=(screen.get_width()//2, screen.get_height()//2), G=G)
                selectid = env.formerid

        elif event.type == pygame.MOUSEBUTTONUP:
            if issliding:
                issliding = False
                sliderkey = ""

            if movingparticle:
                if movid in env.idparticles:
                    formerposition = env.idparticles[movid].position
                    newposition = pygame.mouse.get_pos()
                    env.updateparticleattibutes(movid, velocity=( (newposition[0] - formerposition[0])/env.dt,
                                                                  (newposition[1] - formerposition[1])/env.dt))
                movingparticle = False
                movid = None

        elif event.type == pygame.MOUSEMOTION:
            if issliding:
                sliders[sliderkey].updatevaluefrompoint(pygame.mouse.get_pos()[0])
                updateslidesvalues(sliderkey, selectid)
                fps = sliders["fps"].actualvalue

        elif event.type == pygame.KEYDOWN:
            mousepos = pygame.mouse.get_pos()
            if event.key not in {pygame.K_s, pygame.K_p, pygame.K_x} and selectid in env.idparticles:
                keyhandler(mousepos, selectid, event)

            elif event.key == pygame.K_s:
                if ( targetid := env.getoparticleidfrompoint(mousepos) ) in env.idparticles and targetid != selectid:
                    selectid = targetid
                    selectparticle(selectid)
                else: selectid = None

            elif event.key == pygame.K_p:
                buttons["pause"].press()

            elif event.key == pygame.K_x:
                if selectid is not None and ( targetid := env.getoparticleidfrompoint(mousepos) ) is not None:
                    p1 = env.idparticles[selectid].position
                    p2 = env.idparticles[targetid].position
                    print(math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2))


    if (env.mouseid in env.idparticles) != buttons["mouseparticle"].ispressed:
        buttons["mouseparticle"].press()
        buttons["mouseattributes"].isvisible = not buttons["mouseattributes"].isvisible

    if not buttons["pause"].ispressed:
        if buttons["mouseparticle"].ispressed: env.updatemouseparticle(pygame.mouse.get_pos())
        env.updatekinematics()

    if buttons["vectorval"].ispressed:
        for p in env.allparticles:
            pygame.draw.circle(screen, env.particlesdata[p.id][1], p.position, p.radius)
            pygame.draw.line(screen, (65, 100, 255), p.position,
                             (p.acceleration[0] + p.position[0], p.acceleration[1] + p.position[1]))
            pygame.draw.line(screen, (200, 200, 200), p.position,
                             (p.velocity[0] + p.position[0], p.velocity[1] + p.position[1]))
    else:
        for p in env.allparticles:
            pygame.draw.circle(screen, env.particlesdata[p.id][1], p.position, p.radius)

    if selectid in env.idparticles:
        p = env.idparticles[selectid]
        env.updateacceleration()
        pygame.draw.line(screen, (200, 0, 0), (p.spring[0] - 8, p.spring[1] - 8), (p.spring[0] + 8, p.spring[1] + 8))
        pygame.draw.line(screen, (200, 0, 0), (p.spring[0] + 8, p.spring[1] - 8), (p.spring[0] - 8, p.spring[1] + 8))
        pygame.draw.circle(screen, (255,255,255), p.position, p.radius, width=2)
        pygame.draw.line(screen, (65, 100, 255), p.position, (p.acceleration[0] + p.position[0], p.acceleration[1] + p.position[1]))
        pygame.draw.line(screen, (200, 200, 200), p.position, (p.velocity[0] + p.position[0], p.velocity[1] + p.position[1]))
        buttons["vx"].updatevalue(round(p.velocity[0], 2))
        buttons["vy"].updatevalue(round(p.velocity[1], 2))
        buttons["ax"].updatevalue(round(p.constantacceleration[0], 2))
        buttons["ay"].updatevalue(round(p.constantacceleration[1], 2))
        for gid in p.gravityid:
            pygame.draw.circle(screen, (59, 156, 122), env.idparticles[gid].position, env.idparticles[gid].radius, width=2)
        for sid in p.springid:
            pygame.draw.circle(screen, (78, 78, 191), env.idparticles[sid].position, env.idparticles[sid].radius,
                               width=2)

    if buttons["grid"].ispressed:
        # draw partitions grid
        for j in range(-1, env.partitions):
            pygame.draw.line(screen, (255, 255, 255), (j * env.gridx - env.shiftx, -env.shifty - env.gridy),
                             (j * env.gridx - env.shiftx, screen.get_height() + env.shifty + env.gridy))
        for j in range(-1, env.partitions):
            pygame.draw.line(screen, (255, 255, 255), (-env.shiftx-env.gridx, j * env.gridy - env.shifty),
                             (screen.get_width() + env.shiftx + env.gridx, j * env.gridy - env.shifty))

    if buttons["gui"].isvisible:
        pygame.draw.rect(screen, buttons["gui"].color, buttons["gui"].rect)

        if buttons["gui"].ispressed:
            for button in filter(lambda b: b.isvisible, buttons.values()):
                pygame.draw.rect(screen, button.color, button.rect)

            for key in ["vx", "vy", "ax", "ay", "minus", "plus", "selector"]:
                if buttons[key].isvisible: screen.blit(buttons[key].text, buttons[key].rect)
            keys = set()
            # draw sliders
            if buttons["settings"].ispressed and buttons["settings"].isvisible:
                keys.update(configslides)

            if buttons["attributes"].ispressed and buttons["attributes"].isvisible:
                keys.update(attributeslides)

            for key in keys:
                pygame.draw.rect(screen, sliders[key].slidercolor, sliders[key].rectangle)
                pygame.draw.circle(screen, sliders[key].ball[2], sliders[key].ball[0], sliders[key].ball[1])
                screen.blit(sliders[key].minvaluetext, sliders[key].minvaluetextrect)
                screen.blit(sliders[key].maxvaluetext, sliders[key].maxvaluetextrect)
                screen.blit(sliders[key].slidertext, sliders[key].slidertextrect)
                screen.blit(sliders[key].actualvaluetext, sliders[key].actualvaluetextrect)

    a.append(clock.get_fps())
    pygame.display.update()
