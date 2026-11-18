from math import sin, cos, atan, sqrt, pi
from random import randrange as rng
import sys
sys.path.append('C:\\Users\\cwade_c20\\OneDrive - King Edward VI Grammar School\\Code\\Libraries')
# sys.path.append('C:\\Users\\Chris\\OneDrive - King Edward VI Grammar School\\Code\\Libraries')
import pyxel as px

class Player:
    def __init__(self):
        self.loc = [SCREENWIDTH*SCALE/2, SCREENHEIGHT*SCALE/2, 1.5*pi]
        self.vel = [0, 0, 0]

        self.maxHealth = 100
        self.health = 100

        self.turnAcc = 0.07
        self.moveAcc = 1

        self.rockets = 100
        self.maxRockets = 100

        self.fuel = 500
        self.maxFuel = 500

    def friction(self):
        for i in range(3):
            if self.vel[i] > 0:
                self.vel[i] = max(self.vel[i] - (0.12 * sqrt(abs(self.vel[i]))), 0)
            elif self.vel[i] < 0:
                self.vel[i] = min(self.vel[i] + (0.12 * sqrt(abs(self.vel[i]))), 0)

    def damage(self, damage): #Takes damage
        self.changeHealth(-5-damage)
        self.checkDead()

    def changeHealth(self, add): #Changes health
        self.health += add
        self.health = min(self.health, self.maxHealth)
        self.checkDead()

    def changeMaxHealth(self, add): #Changes max health
        self.maxHealth += add
        self.health = min(self.health, self.maxHealth)

    def checkDead(self): #Checks if the player is dead
        if self.health < 1:
            self.health = 0
            global gameOver
            gameOver = True
    
    def devTools(self): #Edits stuff on command
        if px.btn(px.KEY_U):
            self.damage(-15)
        if px.btn(px.KEY_I):
            self.damage(5)
        if px.btn(px.KEY_O):
            self.maxHealth += 10
        if px.btn(px.KEY_P):
            self.maxHealth -= 10

    def move(self): #Moves the player
        #Get inputs
        acc = [0, 0, 0] #LRUD relative to direction, rotation
        if self.fuel >= 1:
            if px.btn(px.KEY_LEFT):
                acc[2] -= self.turnAcc
                self.fuel -= 1
                #print("left")
            if px.btn(px.KEY_RIGHT):
                acc[2] += self.turnAcc
                self.fuel -= 1
                #print("right")
            if px.btn(px.KEY_UP) or px.btn(px.KEY_W):
                acc[1] += self.moveAcc
                self.fuel -= 1
                #print("up")
            if px.btn(px.KEY_DOWN) or px.btn(px.KEY_S):
                acc[1] -= self.moveAcc
                self.fuel -= 1
                #print("down")
            if px.btn(px.KEY_A):
                acc[0] -= self.moveAcc
                self.fuel -= 1
                #print("slide left")
            if px.btn(px.KEY_D):
                acc[0] += self.moveAcc
                self.fuel -= 1
                #print("slide right")
        
        
        #Do velocities
        # if px.btn(px.KEY_E):
        #     print(end="")
        self.vel[2] += acc[2]
        self.loc[2] += self.vel[2]

        # print(acc)
        self.vel[0] += acc[1]*cos(self.loc[2]) - acc[0]*sin(self.loc[2])
        self.vel[1] += acc[1]*sin(self.loc[2]) + acc[0]*cos(self.loc[2])
        self.friction()

        #Move
        for i in range(2):
            self.loc[i] += self.vel[i]
        
        self.loc[0] = self.loc[0]%(SCREENWIDTH*SCALE)
        self.loc[1] = self.loc[1]%(SCREENHEIGHT*SCALE)

    def addFuel(self, fuel):
        self.maxFuel += sqrt(abs(fuel))/10
        self.fuel += fuel
        self.fuel = min(self.fuel, self.maxFuel)

    def addRockets(self):
        if self.rockets < self.maxRockets:
            self.addFuel(-0.5)
            self.rockets += 0.5
            self.rockets = min(self.rockets, self.maxRockets)

    def update(self):
        self.move()
        if px.btn(px.KEY_SPACE):
            if self.rockets >= 1:
                rocket = Rocket(self.loc, self.vel)
                rockets.append(rocket)
                self.rockets -= 1
                # print("shoot", end="")
                self.maxRockets += 0.1
        if (not px.btn(px.KEY_E)) and self.fuel/self.maxFuel > 0.2:
            self.addRockets()
        self.devTools()

    def draw(self):
        px.circb(self.loc[0], self.loc[1], 9, px.COLOR_ORANGE)
        
        size = 15
        for angle in [(2/3)*pi*i for i in [1, 2]]:
            px.tri(self.loc[0], self.loc[1], self.loc[0] + size*cos(self.loc[2]), self.loc[1] + size*sin(self.loc[2]), self.loc[0] + size*cos(self.loc[2] + angle), self.loc[1] + size*sin(self.loc[2] + angle), px.COLOR_DARK_BLUE)

class Rocket:
    def __init__(self, loc, vel):
        self.loc = loc[:]
        self.vel = [cos(loc[2])*10, sin(loc[2])*10]
        self.vel[0] += vel[0]
        self.vel[1] += vel[1]
        self.lifeSpan = 120
        px.play(0, 0)

    def update(self):
        for i in range(2):
            self.loc[i] += self.vel[i]
        self.loc[0] = self.loc[0]%(SCREENWIDTH*SCALE)
        self.loc[1] = self.loc[1]%(SCREENHEIGHT*SCALE)
        

        self.lifeSpan -= 1
    
    def draw(self):
        px.line(self.loc[0], self.loc[1], self.loc[0] + cos(self.loc[2])*10, self.loc[1] + sin(self.loc[2])*10, px.COLOR_WHITE)

class Asteroid:
    def __init__(self, loc=None, vel=None, size=None):
        if loc == None:
            self.loc = [rng(0, SCREENWIDTH*SCALE), rng(0, SCREENHEIGHT*SCALE)]
            while self.distance(player.loc) < 25/max((min(sqrt(score)/10000, 100)), 1):
                self.loc = [rng(0, SCREENWIDTH*SCALE), rng(0, SCREENHEIGHT*SCALE)]
            
            self.vel = [self.rSpeed(), self.rSpeed()]
            self.size = rng(1000 + int(sqrt(score)), 1500 + int(sqrt(score)))
        else:
            self.loc = [0,0]
            self.vel = [0,0]
            for i in range(2):
                self.loc[i] += loc[i]
                self.vel[i] += vel[i]
            self.size = size
        
        
        self.radius = sqrt(self.size/pi)
        self.lifeSpan = 1

    def rSpeed(self): #For making a new Asteroid
        positive = rng(0, 2)
        if positive == 0:
            positive -= 1
        return (rng(0, 100+int(score**(1/3.25)))**0.5)*positive

    def distance(self, loc): #Find distance between asteroid and another location
        return sqrt((loc[0] - self.loc[0])**2 + (loc[1] - self.loc[1])**2)

    def kill(self): #Kills the asteroid
        self.lifeSpan = 0
        if self.size > 600:
            eSpeed = sqrt(self.vel[0]**2 + self.vel[1]**2)/5 + 1
            if self.vel[1] != 0:
                angleExtra = atan(-self.vel[0]/self.vel[1])
                extra = [cos(angleExtra)*eSpeed, sin(angleExtra)*eSpeed]
            else:
                extra = [0, eSpeed]
            
            for j in [-1, 1]:
                velocity = [self.vel[i] + extra[i]*j for i in range(2)]
                asteroids.append(Asteroid(self.loc, velocity, self.size*0.4))
        
        global score
        score += self.size
        player.changeMaxHealth(0.1)
        player.changeHealth(1)

        player.addFuel(10)

    def checkHit(self): #Checks every rocket to see if it has been hit
        for rocket in rockets:
            if self.distance(rocket.loc) < self.radius and rocket.lifeSpan != 0 and self.lifeSpan == 1:
                rocket.lifeSpan = 0

                self.kill()
                break
    
    def hitPlayer(self): #Checks if it has hit the player
        if self.distance(player.loc) < self.radius:
            damage = 0
            damage += sqrt((player.vel[0]-self.vel[0])**2 + (player.vel[1] - self.vel[1])**2)
            player.damage(damage)
            self.kill()
    
    def update(self):
        for i in range(2):
            self.loc[i] += self.vel[i]
        self.loc[0] = self.loc[0]%(SCREENWIDTH*SCALE)
        self.loc[1] = self.loc[1]%(SCREENHEIGHT*SCALE)


        self.checkHit()
        self.hitPlayer()

    def draw(self):
        px.circb(self.loc[0], self.loc[1], self.radius, px.COLOR_GRAY)

class App:
    def __init__(self):
        px.init(SCREENWIDTH*SCALE, SCREENHEIGHT*SCALE)
        px.load("gaem.pyxres")
        self.musicTime = 0
        px.run(self.update, self.draw)

    def end(self):
        print(f"Your score was: {int(score)}")
        try: #If a highscore has already been saved
            file = open("highScore.txt", "r")
            line = file.readline().split(",")
            file.close()
            if int(score) > int(line[0]):
                print(f"New high score!\nPrevious high score: {line[0]}")
                file = open("highScore.txt", "w")
                file.write(f"{int(score)},\n")
                file.close()
            else: #If no high score has been saved
                print(f"High score: {line[0]}")
        except:
            file = open("highScore.txt", "w")
            file.write(f"{int(score)},\n")
            file.close()
        px.quit()

    def barColour(self, maximum, curr): #Returns the colour of the bar
        if curr > maximum*0.8:
            col = px.COLOR_GREEN
        elif curr > maximum*0.6:
            col = px.COLOR_YELLOW
        elif curr > maximum*0.4:
            col = px.COLOR_ORANGE
        elif curr > maximum*0.2:
            col = px.COLOR_RED
        else:
            col = px.COLOR_BROWN
        return col

    def drawBar(self, x, y, bar, maxBar, col): #Draws the bar
        thickness = 12
        gapSize = 5
        px.rect(x + 50, y, maxBar + 2*thickness + 2*gapSize, 3*thickness + 2*gapSize, px.COLOR_DARK_BLUE) #Outer
        px.rect(x + 50 + thickness, y + thickness, maxBar + 2*gapSize, thickness + 2*gapSize, px.COLOR_BLACK) #Remove inner
        
        px.rect(x + 50 + thickness + gapSize, y + thickness + gapSize, bar, thickness, px.COLOR_GREEN) #Inner bar

    def update(self):
        global paused
        if self.musicTime == 0:
            px.play(1, 1)
        self.musicTime = (self.musicTime + 1)%(18*5)
        
        if paused:
            if px.btn(px.KEY_SPACE) or px.btn(px.KEY_KP_ENTER):
                paused = False
        
        else:
            if rng(0, 10) == 0 and len(asteroids) < player.maxHealth//10:
                asteroids.append(Asteroid())
            
            player.update()
            
            for group in [rockets, asteroids]:
                i = 0
                while i < len(group):
                    group[i].update()
                    if group[i].lifeSpan < 1: #Also isalive need to be careful
                        group.pop(i)
                    else:
                        i += 1
            
            if gameOver or player.fuel < 1:
                self.end()
            if px.btn(px.KEY_Q):
                paused = True

    def draw(self):
        px.cls(0)
        
        player.draw()
        for rocket in rockets:
            rocket.draw()
        for asteroid in asteroids:
            asteroid.draw()
        

        x = 10
        y = 10
        #Healthbar
        col = self.barColour(player.maxHealth, player.health)

        px.circ(x + 10, y + 10, 10, col)
        px.circ(x + 30, y + 10, 10, col)
        px.tri(x, y + 10, x + 40, y + 10, x + 20, y + 40, col)
        px.tri(x + 2, y + 15, x + 38, y + 15, x + 20, y + 40, col)

        self.drawBar(x, y, player.health, player.maxHealth, col)

        #Fuel bar
        y += 54
        
        col = self.barColour(player.maxFuel, player.fuel)

        px.rect(x, y, 30, 30, px.COLOR_DARK_BLUE)
        px.rect(x + 5, y, 20, 25, px.COLOR_BLACK)
        px.rect(x + 5, y + 25 - 25*(player.fuel/player.maxFuel), 20, 25*(player.fuel/player.maxFuel), col)

        self.drawBar(x, y, player.fuel/5, player.maxFuel/5, col)

        #Rocket bar
        y += 54

        col = self.barColour(player.maxRockets, player.rockets)

        px.rect(x + 10, y + 10, 10, 34, px.COLOR_GRAY)
        px.tri(x + 15, y, x + 7, y + 10, x + 23, y + 10, col)
        px.tri(x + 15, y + 38, x + 7, y + 44, x + 23, y + 44, col)

        self.drawBar(x, y, player.rockets, player.maxRockets, col)


SCREENWIDTH = 16
SCREENHEIGHT = 9
SCALE = 80

player = Player()
rockets = []
asteroids = []
gameOver = False
score = 0
paused = False

App()