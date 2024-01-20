import numpy as np
import particles

class Environment:
    def __init__(self, fps, width, height, shiftx, shifty, partitions):
        self._dt = 1 / fps
        self.width = width
        self.height = height
        self.shiftx = shiftx # extra x component
        self.shifty = shifty # extra y component
        self.partitions = partitions # all space will be divided in a grix (partition + 2)X(partition + 2) for collision detec.
        # all space goes from (-shiftx - gridx, -shifty - gridy) to (width + shiftx + grix, height + shifty + gridy)
        self.grid = [[set() for i in range(partitions)] for j in range(partitions)]
        self.gridx = np.ceil((width + 2 * shiftx)/(partitions - 2))
        self.gridy = np.ceil((height + 2 * shifty)/ (partitions - 2)) #separation between grids
        self.maxradius = min(self.gridx, self.gridy) // 2

        self.allparticles = [] #list of all particles in the environment, always ordered by layer
        self._idparticles = {} #key=particle.id returns reference to that particle  ########## possible deletion ##############
        self.idcount = 10 #assigns id's to the particles (maybe 0 for mouse and other for keyboard controlled particles)
        self.boundingboxes = [((-shiftx, -shifty), (width + shiftx, height + shifty))]  # first bound box is the whole space, index 0 the whole space ##### only tuples #######
        self.particlesdata = {} #key=particle.id contains list of particle's layer, color and bounding box
        self._mouseid = 0 #unique id to the mouse particle
        self._formerid = 10

    @property
    def idparticles(self):
        return self._idparticles

    @property
    def dt(self):
        return self._dt

    @property
    def formerid(self):
        return self._formerid

    @property
    def mouseid(self):
        return self._mouseid

    def updatedt(self, dt):
        self._dt = dt

    def createparticle(self, radius, mass, springid, gravityid, r0=(0,0), v0=(0,0), color=(255,255,255), iscollidable=True, layer=1, BBindex=0, spring=(0,0), k=0, kspring=0,lamb=0, c=1, \
                       constantacceleration=(0,0), G=1):
        #radius less than maxradius
        p = particles.particle(r0, v0, radius, mass, self.idcount, iscollidable, springid, gravityid, spring, \
                               k, kspring, lamb, c, constantacceleration, G)
        self.allparticles.append(p)
        self._idparticles[self.idcount] = p
        self.particlesdata[self.idcount] = [layer, color, BBindex]

        self._formerid = self.idcount
        self.idcount += 1


    def deleteparticle(self, particleid):

        for i in range(len(self.allparticles)):

            if self.allparticles[i].id == particleid:
                pindex = i

            if particleid in self.allparticles[i].springid:
                self.allparticles[i].springid.pop(particleid)

            if particleid in self.allparticles[i].gravityid:
                self.allparticles[i].gravityid.remove(particleid)

        
        del self.allparticles[pindex]
        del self._idparticles[particleid]

    def addmouseparticle(self, radius ,mass, iscollidable=True, r0=(0,0), color=(255, 255, 255), bbindex=0, layer=1):

        if self.mouseid in self._idparticles.keys():
            raise KeyError

        p = particles.mouseparticle(r0, radius, mass, iscollidable=iscollidable)
        self.allparticles.append(p)
        self._idparticles[self._mouseid] = p
        self.particlesdata[self._mouseid] = [layer, color, bbindex]

    def updatemouseparticle(self, pos):
        self._idparticles[self._mouseid].updateall(pos, self.dt)

    def addparticle(self, particle, color = (255,255,255), bbindex = 0, layer=1):
        """only use to add special particles, id 0-10"""
        self.allparticles.append(particle)
        self._idparticles[particle.id] = particle
        self.particlesdata[particle.id] = [layer, color, bbindex]

    def getoparticleidfrompoint(self, point):
        self.updategrid(self.allparticles)
        target = None

        for p in self.grid[1 + int((point[0] + self.shiftx) // self.gridx)][1 + int((point[1] + self.shifty) // self.gridy)]:
            if  p.radius ** 2 >= np.dot(p.position - point, p.position - point) and p.id != self._mouseid:
                target = p.id
                break

        self.grid = [[set() for i in range(self.partitions)] for j in range(self.partitions)]

        return target

    def clearallparticles(self):
        self.allparticles.clear()
        self._idparticles.clear()
        self.particlesdata.clear()
        self.idcount = 10

    def updateparticleattibutes(self, particleid, layer=None, color=None, boundboxindex=None, position=None, velocity=None,
                           kspring=None, constantacceleration=None, mass=None, iscollidable=None, radius=None, spring=None,
                                k=None, lamb=None, c=None, G=None):
        if layer is not None:
            self.particlesdata[particleid][0] = layer

        if color is not None:
            self.particlesdata[particleid][1] = color

        ###### assert the second contidion before calling the func ########3
        if boundboxindex is not None and boundboxindex <= len(self.boundingboxes) - 1:
            self.particlesdata[particleid][2] = boundboxindex

        if G is not None:
            self._idparticles[particleid].G = G

        if kspring is not None:
            self._idparticles[particleid].kspring = kspring

        if position is not None:
            self._idparticles[particleid].position = np.array(position)

        if velocity is not None:
            self._idparticles[particleid].velocity = np.array(velocity)

        if constantacceleration is not None:
            self._idparticles[particleid].constantacceleration = np.array(constantacceleration)

        if mass is not None:
            self._idparticles[particleid].mass = mass

        if iscollidable is not None:
            self._idparticles[particleid].iscollidable = iscollidable

        if radius is not None:
            self._idparticles[particleid].radius = radius

        if spring is not None:
            self._idparticles[particleid].spring = np.array(spring)

        if k is not None:
            self._idparticles[particleid].k = k

        if lamb is not None:
            self._idparticles[particleid].lamb = lamb

        if c is not None:
            self._idparticles[particleid].c = c

    def updateparticlebond(self, particleid, gravityids=None, springids=None):

        if springids is not None:
            self._idparticles[particleid].springid.update(springids)

        if gravityids is not None:
            self._idparticles[particleid].gravityid.update(gravityids)

    def deleteparticlebond(self, particleid, gravityid=None, springid=None):

        if springid is not None:
            self._idparticles[particleid].springid.pop(springid, None)

        if gravityid is not None:
            self._idparticles[particleid].gravityid.discard(gravityid)

    def boxcollision(self, particle):
        """reverts velocity and corrects position if colliding with the bounding box"""
        #consider set vel = 0 if too small
        #handle when dissapearing in collision
        pos = particle.position
        r = particle.radius
        blt = self.boundingboxes[self.particlesdata[particle.id][2]][0] #left-top coordinate of particle's boundingbox
        brb = self.boundingboxes[self.particlesdata[particle.id][2]][1] #righ-bottom coordinate of particle's boundingbox

        if pos[0] - r <= blt[0]:
            particle.velocity[0] = abs(particle.velocity[0]) * particle.c
            particle.position[0] = blt[0] + r

        if pos[0] + r >= brb[0]:
            particle.velocity[0] = -abs(particle.velocity[0]) * particle.c
            particle.position[0] = brb[0] - r

        if pos[1] - r <= blt[1]:
            particle.velocity[1] = abs(particle.velocity[1]) * particle.c
            particle.position[1] = blt[1] + r

        if pos[1] + r >= brb[1]:
            particle.velocity[1] = -abs(particle.velocity[1]) * particle.c
            particle.position[1] = brb[1] - r

    def deleteboundingbox(self, oldbbindex, newbbindex=0):
        """"assings all particles in bounding box with index [oldbbindex] to [newbbindex]"""
        for p in filter(lambda a: self.particlesdata[p.id][2] == oldbbindex, self.allparticles):
            self.updateparticleattibutes(self, p.id, boundboxindex=newbbindex)

        del self.boundingboxes[oldbbindex]

    def updatecollisions(self):
        """updates velocity and position of particles in allparticles and empties grid"""
        alreadycollisioned = set()

        for i in range(len(self.grid)):

            for j in range(len(self.grid[i])):

                while len(self.grid[i][j]) != 0:
                    body1 = self.grid[i][j].pop()

                    for body2 in self.grid[i][j]:

                        if self.particlesdata[body2.id][0] == self.particlesdata[body1.id][0] and \
                                (min(body1, body2, key=lambda a: a.id), max(body1, body2, key=lambda a: a.id)) not in alreadycollisioned \
                                and  (body1.radius + body2.radius) ** 2 \
                                >= (d := np.dot(body1.position - body2.position, body1.position - body2.position)) > 0:

                            m1 = body1.mass
                            m2 = body2.mass
                            dp = body1.position - body2.position
                            dotvp = np.dot(body1.velocity - body2.velocity, body1.position - body2.position)
                            d2 = d**0.5

                            #offset = (body1.radius + body2.radius - d2) * dp / (4 * np.sqrt(d2))
                            #body1.handlecollision(m2, dp, -dotvp, d, offset)
                            #body2.handlecollision(m1, dp, dotvp, d, -offset)

                            offset = 4.5 * (body1.radius + body2.radius - d2) * dp / (2 * d2) ## assures no particle overlaps
                            m1f = m1 /(m1 + m2)
                            m2f = 1 - m1f

                            body1.handlecollision(m2, dp, -dotvp, d, m2f * offset)
                            body2.handlecollision(m1, dp, dotvp, d, -m1f * offset)



                            alreadycollisioned.add((min(body1, body2, key=lambda a: a.id), max(body1, body2, key=lambda a: a.id)))

    def updategrid(self, particlesiterable):
        """updates the grid in order to calculate collisions"""
        for particle in particlesiterable:
            ###### handle when out of bound and eliminate particle##############################
            pos = particle.position
            r = particle.radius
            try:
                self.grid[1 + int((pos[0] + r + self.shiftx) // self.gridx)][
                    1 + int((pos[1] - r + self.shifty) // self.gridy)].add(particle)

                self.grid[1 + int((pos[0] - r + self.shiftx) // self.gridx)][
                    1 + int((pos[1] + r + self.shifty) // self.gridy)].add(particle)

                self.grid[1 + int((pos[0] + r + self.shiftx) // self.gridx)][
                    1 + int((pos[1] + r + self.shifty) // self.gridy)].add(particle)

                self.grid[1 + int((pos[0] - r + self.shiftx) // self.gridx)][
                    1 + int((pos[1] - r + self.shifty) // self.gridy)].add(particle)
            except:
                self.boxcollision(particle)
                self.grid[1 + int((pos[0] + r + self.shiftx) // self.gridx)][
                    1 + int((pos[1] - r + self.shifty) // self.gridy)].add(particle)

                self.grid[1 + int((pos[0] - r + self.shiftx) // self.gridx)][
                    1 + int((pos[1] + r + self.shifty) // self.gridy)].add(particle)

                self.grid[1 + int((pos[0] + r + self.shiftx) // self.gridx)][
                    1 + int((pos[1] + r + self.shifty) // self.gridy)].add(particle)

                self.grid[1 + int((pos[0] - r + self.shiftx) // self.gridx)][
                    1 + int((pos[1] - r + self.shifty) // self.gridy)].add(particle)

    def updatekinematics(self):
        ##change name###
        # func do something with each particle and arg
        self.updategrid(filter(lambda b: b.iscollidable, self.allparticles))
        for p in self.allparticles:
            p.updateacceleration(self._idparticles)
            p.updatevelocity(self.dt)
        self.updatecollisions()
        for p in self.allparticles:
            self.boxcollision(p)
            p.updateposition(self.dt)

        # self.updatecollisions()
        # for p in self.allparticles: p.updateposition(self.dt)
        #
        # for p in self.allparticles:
        #     p.updateacceleration(self._idparticles)
        #     p.updatevelocity(self.dt)
        #     self.boxcollision(p)

    def updateacceleration(self):
        for p in self.allparticles:
            p.updateacceleration(self._idparticles)

    def updatesettings(self, width=None, height=None, shiftx=None, shifty=None, partitions=None):
        #min width=300, min height=400
        if width is not None:
            self.width = width

        if height is not None:
            self.height = height

        if shifty is not None:
            self.shifty = shifty

        if shiftx is not None:
            self.shiftx = shiftx

        if partitions is not None:
            self.partitions = partitions
            self.grid = [[set() for i in range(self.partitions)] for j in range(self.partitions)]

        self.gridx = np.ceil((self.width + 2 * self.shiftx) / (self.partitions - 2))
        self.gridy = np.ceil((self.height + 2 * self.shifty) / (self.partitions - 2))

        self.maxradius = min(self.gridx, self.gridy) // 2

        for p in self.allparticles:
            if p.radius > self.maxradius:
                p.radius = self.maxradius

        self.boundingboxes[0] = ((-self.shiftx, -self.shifty), (self.width + self.shiftx, self.height + self.shifty))

        for i in range(len(self.boundingboxes) - 1):
            if self.boundingboxes[i+1][0][0] < self.boundingboxes[0][0][0] or self.boundingboxes[i+1][0][1] < self.boundingboxes[0][0][1]\
                or self.boundingboxes[i+1][1][0] > self.boundingboxes[0][1][0] or self.boundingboxes[i+1][1][1] > self.boundingboxes[0][1][1]:
                self.deleteboundingbox(i+1)