import numpy
import numpy as np
import pygame
import particles
import random
from sys import exit

def getparticle(target, particles):
    """"returns a particle in particles if colliding with the tuple target, None otherwise"""
    for particle in particles:
        if numpy.linalg.norm((target[0] - particle.position[0], target[1] - particle.position[1])) <= particle.radius:
            return particle

    return None

def updateparticles():
    """"advance animation by dt"""
    screen.blit(background, (0,0))

    #assign particles to grid
    for particle in collisionbodies:
        ###### handle when out of bound and eliminate particle##############################
        grid[1 + int((particle.position[0] + particle.radius + sftx) // gridx)][
            1 + int((particle.position[1] - particle.radius + sfty)// gridy)].add(particle)

        grid[1 + int((particle.position[0] - particle.radius + sftx)// gridx)][
            1 + int((particle.position[1] + particle.radius + sfty)// gridy)].add(particle)

        grid[1 + int((particle.position[0] + particle.radius + sftx) // gridx)][
            1 + int((particle.position[1] + particle.radius + sfty) // gridy)].add(particle)

        grid[1 + int((particle.position[0] - particle.radius + sftx) // gridx)][
            1 + int((particle.position[1] - particle.radius + sfty) // gridy)].add(particle)

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            while len(grid[i][j]) != 0:
                body1 = grid[i][j].pop()

                for body2 in grid[i][j]:

                    if (min(body1, body2, key=lambda a: a.id),max(body1, body2, key=lambda a: a.id)) in collisions \
                            or layers[body2.id] != layers[body1.id]:

                        continue

                    else:
                        d = numpy.dot(body1.position - body2.position, body1.position - body2.position)

                        if (body1.radius + body2.radius)**2 >= d > 0:

                            particles.collisioncalc(body1, body2, d)
                            collisions.add(
                                (min(body1, body2, key=lambda a: a.id), max(body1, body2, key=lambda a: a.id)))

    for particle in allparticles:
        particle.updateacceleration(gravitybodies[particle.id])
        particle.updatevelocity(dt)
        particle.boxcollision()

        #pygame.draw.line(screen, (255, 255, 255), particle.position, particle.velocity + particle.position)
        #pygame.draw.line(screen, (100, 100, 100), particle.position, particle.acceleration + particle.position)
        pygame.draw.circle(screen, particle.color, particle.position, particle.radius)
        particle.updateposition(dt)

    collisions.clear()

pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()

FPS = 120
dt = 1/FPS
width = 1920
height = 1000
sftx = 1000
sfty = 1000
#width + 2*sftx and height + 2*sfty must be a multiple of partitions - 2
partitions = 60
gridx = np.ceil((width + 2 * sftx)/(partitions - 2))
gridy = np.ceil((height + 2 * sfty)/ (partitions - 2)) #important max radius is the min of gridx and gridy
maxradius = min(gridy, gridy)

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("flashycollision")
background = pygame.image.load("../data/background2.png").convert()

collisionbodies = list() #list of considered collisionable objects
allparticles = list() #list of considered noncollisionable objects
gravitybodies = {} #key=particle.id returns list of particles
layers = {} #key=particle.id contains int, only particles with this same int can interact

collisions = set()
grid = [[set() for i in range(partitions)] for j in range(partitions)]

for i in range(50):
    a = particles.particle((random.randint(-sftx, width + sftx), random.randint(-sfty, height + sfty)), (random.randint(300,300)*2), \
                           random.randint(1, maxradius), random.randint(50, 50), (-sftx,-sfty), (width + sftx, height + sfty), \
                           (random.randint(1,255), random.randint(1,255), random.randint(1,255)), i, constantacceleration=(0,0))
    allparticles.append(a)
    collisionbodies.append(a)
    gravitybodies[i] = []
    layers[i] = [1]

allparticles.sort(reverse=True, key=lambda b: layers[b.id])
#for average performance
a= list()

while True:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("performance: ",sum(a) / len(a))
            pygame.quit()
            exit()

    updateparticles()

    a.append(clock.tick())
    pygame.display.update()