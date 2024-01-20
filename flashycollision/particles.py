import numpy as np
import numpy.linalg

class particle:
    def __init__(self, r0, v0, radius, mass, id, iscollidable, springid, gravityid, spring, k, kspring, lamb, c, constantacceleration, G):
        #quit box color quit =default
        self._position = np.array(r0)
        self._radius = radius
        self._velocity = np.array(v0)
        self._acceleration = np.array((0,0))
        self._mass = mass
        self._id = id #unique number representing this particle
        self._iscollidable = iscollidable
        self._spring = np.array(spring) # spring coordinates
        self._k = k #spring constant to other particles
        self._kspring = kspring #spring constant to spring position
        self._lamd = lamb #viscosity constant
        self._c = c #restitution coeff used in collisions
        self._constantacceleration = np.array(constantacceleration) #acceleration that experiences forever
        self._springid = springid #contains id's of particles and l0 from which experiences spring acceleration
        self._gravityid = gravityid #contains id's of particles from which experiences gravitational acceleration
        self._G = G

    @property
    def id(self):
        return self._id

    @property
    def G(self):
        return self._G

    @G.setter
    def G(self, Gnew):
        self._G = Gnew

    @property
    def l0(self):
        return self._l0

    @l0.setter
    def l0(self, l0new):
        self._l0 = l0new

    @property
    def iscollidable(self):
        return self._iscollidable

    @iscollidable.setter
    def iscollidable(self, bool):
        self._iscollidable = bool

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, pn):
        self._position = pn

    @property
    def velocity(self):
        return self._velocity

    @velocity.setter
    def velocity(self, vnew):
        self._velocity = vnew

    @property
    def acceleration(self):
        return self._acceleration

    @acceleration.setter
    def acceleration(self, anew):
        self._acceleration = np.array(anew)

    @property
    def springid(self):
        return self._springid

    @springid.setter
    def springid(self, snew):
        self._springid = snew

    @property
    def gravityid(self):
        return self._gravityid

    @gravityid.setter
    def gravityid(self, gnew):
        self._gravityid = gnew

    @property
    def constantacceleration(self):
        return self._constantacceleration

    @constantacceleration.setter
    def constantacceleration(self, cnew):
        self._constantacceleration = cnew

    @property
    def k(self):
        return self._k

    @k.setter
    def k(self, knew):
        self._k = knew

    @property
    def kspring(self):
        return self._kspring

    @kspring.setter
    def kspring(self, nk):
        self._kspring = nk

    @property
    def lamb(self):
        return self._lamd

    @lamb.setter
    def lamb(self, lnew):
        self._lamd = lnew

    @property
    def c(self):
        return self._c

    @c.setter
    def c(self, cnew):
        self._c = cnew

    @property
    def spring(self):
        return self._spring

    @spring.setter
    def spring(self, sp):
        self._spring = sp

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, rnew):
        self._radius = rnew

    @property
    def mass(self):
        return self._mass

    @mass.setter
    def mass(self, mnew):
        self._mass = mnew

    def updateacceleration(self, particledict):

        externalacceleration = np.array((0,0)) #sum of gravity and spring acc. due to other bodies

        if self._G != 0:
            for id in self._gravityid:
                if self._position[0] == particledict[id].position[0] and self._position[1] == particledict[id].position[1]: continue
                d = ( (self._position[0] - particledict[id].position[0])**2 + (self._position[1] - particledict[id].position[1])**2 )**(-3/2)
                externalacceleration = externalacceleration - self._G * particledict[id].mass * (self._position - particledict[id].position)*d

        if self.k != 0:
            for id, l0 in self._springid.items():
                if l0 != 0 and (particledict[id].position[0] != self._position[0] or particledict[id].position[1] != self._position[1]) and\
                        ( d := ((particledict[id].position[0] - self._position[0])**2 + (particledict[id].position[1] - self._position[1])**2 )**-0.5 )!= 0:

                    externalacceleration = externalacceleration + self._k * (1 - l0*d) * (
                                particledict[id].position - self._position)
                else:
                    externalacceleration = externalacceleration + self._k * (particledict[id].position - self._position)

        self._acceleration = self.kspring * (self._spring - self._position) + self._lamd * self._velocity\
                             + self._constantacceleration + externalacceleration

    def updatevelocity(self, dt):
        #updates velocity by dt
        self._velocity = self._velocity + dt * self._acceleration

    def updateposition(self, dt):
        #updates position by dt
        self._position = self._position + dt * self._velocity

    def handlecollision(self, m2, dp, dotvp, d, offset):
        """updates velocity and position so that no particle overlaps"""
        self._velocity = self._velocity + (1 + self.c) * m2 * dotvp * dp / (d * (self.mass + m2))
        self._position = self._position + offset

class mouseparticle(particle):
    def __init__(self, r0, radius, mass, iscollidable, v0=(0,0), id=0):
        particle.__init__(self, r0, v0, radius, mass, id, iscollidable, set(), set(), (0,0), 0, 0, 0, 1, (0,0), 0)

    def updateacceleration(self, particledict):
        pass
    def updatevelocity(self, dt):
        pass
    def updateposition(self, dt):
        pass
    def handlecollision(self, m2, dp, dotvp, d, offset):
        pass
    def updateall(self, pos, dt):
        self._velocity = (pos - self._position) / dt
        self._position = np.array(pos)

class keyboardparticle(particle):
    def __init__(self, r0, v0, radius, mass, color, directedacc1, directedacc2, id=1, springid=set(), gravityid=set(), spring=(0,0), k=0, lamb=0, c=1,\
                 constantacceleration=(0,0)):

        particle.__init__(self, r0, v0, radius, mass, color, id, springid, gravityid, spring, k, lamb, c, constantacceleration)
        self.diracc1 = np.array(directedacc1)
        self.diracc2 = directedacc2

    def updateacceleration(self, particledict, d1=0, d2=0):
        super(keyboardparticle, self).updateacceleration(self, particledict)
        #mov keys
        self.acceleration = self.acceleration + d1 * self.diracc1 + d2 * self.diracc2

def collisioncalc(body1, body2, d):
    ##eliminate
    #calculates collision
    m1 = body1.mass
    m2 = body2.mass
    M = m1 + m2
    dp = body1.position - body2.position
    dotvp = np.dot(body1.velocity - body2.velocity, body1.position - body2.position)

    body1.velocity = body1.velocity - 2 * body1.c * m2 * dotvp * dp / (M * d)
    body2.velocity = body2.velocity + 2 * m1 * body2.c * dotvp * dp / (M * d)

    # corrects position so that no particle overlaps
    d2 = numpy.sqrt(d)
    shift = (body1.radius + body2.radius - d2) * dp / (4 * d2)
    body1.position = body1.position + shift
    body2.position = body2.position - shift

def particularcollision(particle, m2, pos2, vel2, r2, d):
###eliminate
    dp = particle.position - pos2
    dotvp = np.dot(particle.velocity - vel2, particle.position - pos2)

    particle.velocity = particle.velocity - 2 * particle.c * m2 * dotvp * dp / ( (particle.mass + m2) * d )

    d2 = numpy.sqrt(d)
    shift = (particle.radius + r2 - d2) * dp / (4 * d2)
    particle.position = particle.position + shift
