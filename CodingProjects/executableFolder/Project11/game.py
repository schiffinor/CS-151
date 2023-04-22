"""game.py
Roman Schiffino 151B Fall Semester
I now am happy to present my most ridiculous project yet! This is my best attempt at a side scroller. I was consideringa and did 
a lot of preparatory work to implement a boss as you might see; however due to time constraints I scrapped it. All the frames are 
drawn though and it wouln't have been terribly hard to implement, alas time killed me as I had to trace down and handle a variety
of errors, one still pervails but it is only triggered when pressing the attack button during the first part of a jump. So I guess
maybe avoid that. In any case everything was hand drawn except for the slimes and eyes. However, the slime colors are custom as I
just color swapped them. Some other pointers, I'll be adding a youtube video as a gameplay demo as I understand my game might run
much faster on my PC compared to others. Finally, to run this game The main folder I will submit (...\Project11) needs to be
contained in a holder folder. Redirect to that holder folder. If all goes well the game should work fine.
All the requisite modules come prepackaged, and I made special effort to make things as easy as possible because I know its an 
enormous project with far too many files. Actually, I'll do something right now in hopes you have a windows PC, I will pre-pack this
folder in another folder and include a bat file to execute the file.
I wrote the bat file and it works great. Works on windows obviously. If you don't have windows and you have trouble running it let me know.
Ill try and fix whatever is wrong."""


import graphicsPlus as gr
import os
import sys
import numpy as np
import math as m
import tkinter as tk
import inspect as ins
import statistics as s
import time as t
import random as r
import bisect as b
from matrix import *
from hitbox import *
from threading import Timer, Thread, Lock
import json as js
from queue import Queue
from collections import deque
import pyglet as p
import ctypes


'''Here we are just initiating all the variables that need to be referenced by several classes and functions. As well as governing
some global settings.'''
# This is mostly for me since my monitor size is 5120*1440, if the game is too small feel free to either comment out this line or changing the tkinter resolution.
ctypes.windll.shcore.SetProcessDpiAwareness(2)
tick = 1/60
enemyLimit = 5
existingEnemies = []
hitTrack = hitList()
enemyTrack = enemyLister()
spriteTrack = spriteLister()
targetTrack = targetLister()
hitDict = hitDic()
hitTrackDeque = deque([hitTrack])
eyeDict = {}
slimeDict = {}
eyePathLists = {}
# Lazy percent drop rates for items.
lootList = [None,None,None,None,None,"Heart","Heart","Heart","Sword","Sword","Shield"]
initInfo = (hitTrack,enemyTrack,spriteTrack,targetTrack,hitDict)
# Custom font.
p.font.add_file("Project11\Horsemen Typeface\OTF\Horsemen.otf")


class Image(gr.Image):
    '''
    Creating child class of gr.Image to add more functionality.
    '''
    def __init__(self, p, *pixmap):
        gr.Image.__init__(self, p, *pixmap)

    def moveTo(self,x,y):
        '''
        A go to version of the move method.
        '''
        prevCenter = self.getAnchor()
        prevCenter = (int(prevCenter.getX()),int(prevCenter.getY()))
        center = (x,y)
        deltas = tuple(map(lambda x,y: int(y-x), prevCenter,center))
        self.move(*deltas)


class positionTracker:
    '''
    Part of a listener observer data type.
    '''
    def __init__(self):
        self._observers = []

    def notify(self,side,amount,exclusionList = []):
        '''
        Notifies all observers not passeds in as exclusions.
        '''
        for trackedEntity in self._observers:
            if trackedEntity not in exclusionList:
                trackedEntity.update(side,amount)

    def registerTracker(self,observer):
        '''
        Adds observer to tracking list.
        '''
        if observer not in self._observers:
            self._observers.append(observer)
        else:
            raise ValueError("Already in tracker list.")

    def deregisterTracker(self,observer):
        '''
        Removes observer from tracking list.
        '''
        if observer in self._observers:
            self._observers.remove(observer)
        elif observer == "All":
            self._observers = []
        else:
            raise ValueError("Not in tracker list.")


class Updater(positionTracker):
    '''
    I should realistically rename this but this is the position tracker and movement updater version of the observer listener
    structure, this adjusts the background, player, and enemy positions to match the player moving off the edges. This allows
    the player to move across the landscape.
    '''
    def __init__(self):
        '''
        Initialize inheritance and position data.
        '''
        positionTracker.__init__(self)
        self._x_Pos = 0
        self._invarPos = 0

    def x_pos(self):
        '''
        Just another way to get the data.
        '''
        return(self._x_Pos)
    
    def x_pos(self,new_x):
        '''
        Redefine x_pos data to be new_x. If player is on edge of the screen but not at the edge of the playing field all the 
        registered trackers get updated. If player is on edge of the screen and at the edge of the playing field the registered
        trackers get deregistered and later reregistered ehrn th player moves back over the other edge of the boundary.
        '''
        # Set position.
        self._x_Pos = new_x
        # Position logic.
        # Right boundary.
        if self._x_Pos>610:
            if self._invarPos>=9250:
                if bg in self._observers and playerActor in self._observers and all(item in self._observers for item in existingEnemies):
                    positionAdapter.deregisterTracker(bg)
                    positionAdapter.deregisterTracker(playerActor)
                    for item in existingEnemies:
                        positionAdapter.deregisterTracker(item)
            else:
                self.notify("R",self._x_Pos-610)
        # Left boundary.
        if self._x_Pos<-610:
            if self._invarPos<=-610:
                if bg in self._observers and playerActor in self._observers and all(item in self._observers for item in existingEnemies):
                    positionAdapter.deregisterTracker(bg)
                    positionAdapter.deregisterTracker(playerActor)
                    for item in existingEnemies:
                        positionAdapter.deregisterTracker(item)
            else:
                self.notify("L",self._x_Pos+610)
        # Middle registry event.
        if self._x_Pos>-610 and self._x_Pos<610 and self._invarPos<=9250 and self._invarPos>=-610:
            if bg not in self._observers and playerActor not in self._observers and all(item not in self._observers for item in existingEnemies):
                    positionAdapter.registerTracker(bg)
                    positionAdapter.registerTracker(playerActor)
                    for item in existingEnemies:
                        positionAdapter.registerTracker(item)
            else:
                pass

    def invarPos(self):
        '''
        Inveriable position, ie. position within playing field.
        '''
        return(self._invarPos)

    def invarPos(self,new_x):
        '''
        Function such that when the playerActor is at the edge of the screen on either side movement further towards that edge is
        diabled.
        '''
        # Define new attr to store previous canvas position.
        self._prevInvarPos = self._invarPos
        # Set new invarPos.
        self._invarPos = new_x
        # Right side boundary.
        if self._invarPos>=9600:
            screen.unbind_all("<d>")
            screen.unbind_all("<d>" "<space>")
        # Left side boundary.
        elif self._invarPos<=-960:
            screen.unbind_all("<a>")
            screen.unbind_all("<a>" "<space>")
        # Rebind rightward movement when no longer at right edge.
        elif self._prevInvarPos>=9600 and self._invarPos<9600:
            screen.bind_all("<d>", moveRight)
            screen.bind_all("<d>" "<space>", jumpRight)
        # Rebind leftward movement when no longer at left edge.
        elif self._prevInvarPos>=-960 and self._invarPos<-960:
            screen.bind_all("<a>", moveLeft)
            screen.bind_all("<a>" "<space>", jumpLeft)
        # Like most of the raised errors here there mostly for my personal use in debugging. Helps me find error.
        else:
            if (self._prevInvarPos>=-960 and self._invarPos>-960) or (self._prevInvarPos<=9600 and self._invarPos<9600):
                pass
            else:
                raise RuntimeError("I don't think this should be possible.")


class weaponTracker:
    '''
    Another listener observer data structure this time to track player attack activity.
    '''
    def __init__(self):
        self._observers = []

    def notify(self,state,exclusionList = []):
        '''
        Notifies all observers not passeds in as exclusions.
        '''
        for trackedEntity in self._observers:
            if trackedEntity not in exclusionList:
                trackedEntity.update2(state)

    def registerTracker(self,observer):
        '''
        Adds observer to tracking list.
        '''
        if observer not in self._observers:
            self._observers.append(observer)
        else:
            raise ValueError("Already in tracker list.")

    def deregisterTracker(self,observer):
        '''
        Removes observer from tracking list.
        '''
        if observer in self._observers:
            self._observers.remove(observer)
        elif observer == "All":
            self._observers = []
        else:
            raise ValueError("Not in tracker list.")


class Updater2(weaponTracker):
    '''
    Again another vaguely named structure that should probably be renamed. Regardless, this is a part of the above defined listener
    observer pattern. When initiated it sets weaponstate to false and previous weaponstate to false. Whenever it recieves a message
    from the player it checks whether the new state is different from the previous state. If it is different it notifes the observer
    of the new state.
    '''
    def __init__(self):
        weaponTracker.__init__(self)
        self._playerWeaponActive = False
        self.playerWeaponPrevState = False

    def pActive(self):
        return(self._playerWeaponActive)
    
    def pActive(self,state):
        '''
        Sets the previous state, updates current state, compares states.
        If states are not equal notifies observers and passes state value.
        '''
        self.playerWeaponPrevState = self._playerWeaponActive
        self._playerWeaponActive = state
        if self._playerWeaponActive != self.playerWeaponPrevState:
            self.notify(state)
        else:
            pass


positionAdapter = Updater()
weaponUpdater = Updater2()
totalShield = deque([0])


def lootDrop(center):
    '''
    Basic function initialized on enemy death to select a random drop from the loot table. The selected item is srawn on the screen
    for a second before the affect is applied.
    '''
    # Selects drop.
    drop = r.choice(lootList)
    if drop is None:
        # Nothing happens.
        pass
    elif drop == "Heart":
        # Heart drop adds 25 points to player HP.
        droppedHeart = Image(gr.Point(*center),"Project11\sprites\spriteGifs\heart.gif")
        droppedHeart.draw(screen)
        undrawer = Timer(1,droppedHeart.undraw)
        undrawer.start()
        playerActor.hitPoints += 25
    elif drop == "Sword":
        # Sword drop multiplies current sword damage by 1.15. (This Stacks)
        droppedSword = Image(gr.Point(*center),"Project11\sprites\spriteGifs\sword.gif")
        droppedSword.draw(screen)
        undrawer = Timer(1,droppedSword.undraw)
        undrawer.start()
        playerActor.damageUp(1.15)
    elif drop == "Shield":
        # Shield drop multiplies current recieved damage by 0.90. (This Stacks)
        droppedShield = Image(gr.Point(*center),"Project11\sprites\spriteGifs\shield.gif")
        droppedShield.draw(screen)
        t.sleep(.5)
        # Shields are stacked in the upper right corner of the screen and amount of shields active can be noted by how many are stacked.
        droppedShield.move(800-center[0]-20*totalShield[0],450-center[1])
        playerActor.shieldUp(.9)
        totalShield[0] += 1
    else:
        raise RuntimeError("Yet another thing that shouldn't be possible.")


def attack_1():
    '''
    Here we break up the attack into two sections for threading purposes.
    '''
    # Break for anti-spam.
    t.sleep(2*tick)
    # Update weapon-state observer.
    weaponUpdater.pActive(True)
    # Activate player hitbox.
    playerActor.attackBox.activate()
    # Switch to attack animation.
    playerActor.attackImg.draw(screen)
    playerActor.standImg.undraw()
    screen.update()


def attack_2():
    # Active time for attack.
    t.sleep(30*tick)
    # Update weapon-state observer.
    weaponUpdater.pActive(False)
    # Deactivate player hitbox.
    playerActor.attackBox.deactivate()
    # Switch to stand animation.
    playerActor.standImg.draw(screen)
    playerActor.attackImg.undraw()
    screen.update()


class player:
    
    def __init__(self,center):
        '''
        Initialize player object and all stats and attributes.
        '''
        center = (int(center[0]),int(center[1]))
        # Screen-space location.
        self.center = center
        # In-game location.
        self.absCenter = center
        self.hitPoints = 200
        # Incoming damage modifier.
        self.shieldRate = 1
        # Image objects for player attack and stand.
        self.standImg = Image(gr.Point(*center),"Project11\characterDesigns\charpix2\playerCharStand.gif")
        self.attackImg = Image(gr.Point(*center),"Project11\characterDesigns\charpix2\playerCharAttack.gif")
        # Player dimensions.
        self.height = self.standImg.getHeight()
        self.width = self.standImg.getWidth()
        # Initialize and store hitboxes for player body and player attack area.
        self.hitBox = hitboxDefined(center,self.standImg.getWidth()-75,self.standImg.getHeight(),*initInfo,"playerHit",True,hitDeque=hitTrackDeque)
        self.attackBox = hitboxDefined(((center[0]+75),(center[1])),75,self.standImg.getHeight()+50,*initInfo,"attackHit",False,None,None,False,True,hitDeque=hitTrackDeque)
        # Adds damage attributes to hitbox.
        setattr(self.attackBox,"baseDamage",25)
        setattr(self.attackBox,"damage",self.attackBox.baseDamage)
        self.attackBox.deactivate()

    def attack(self):
        '''
        Attack function. player class method that initiates two threads to set up attack.
        '''
        # Creates two thread objects to be initiated simultaneously.
        attackInit = Thread(target=attack_1,daemon=True)
        attackDeInit = Thread(target=attack_2,daemon=True)
        # I wrote this system earlier when this was composed of like 15 threads and this was more efficient.
        # I thought it was cool so I kept it. Basically gets all the local variables removes self and then starts them.
        execList = list(locals())
        execList.remove('self')
        for i in execList:
            locals()[i].start()   
        
    def move(self,x,y):
        '''
        Movement function. player class method that moves the player, and all of its location based attributes by x,y.
        It also updates the position tracker and does some other handy things.
        '''
        # Gets current position and stores it.
        prevCenter = self.standImg.getAnchor()
        prevCenter = (int(prevCenter.getX()),int(prevCenter.getY()))
        # Moves player images,
        self.standImg.move(x,y)
        self.attackImg.move(x,y)
        # Gets new position and stores it.
        center = self.standImg.getAnchor()
        self.center = (int(center.getX()),int(center.getY()))
        # Calculates difference in positions and uses those deltas to update absCenter attribut.
        deltas = tuple(map(lambda x,y: int(y-x), prevCenter,self.center))
        self.absCenter = tuple(map(lambda x,y: int(y+x), self.absCenter,deltas))
        positionAdapter.x_pos(self.center[0])
        positionAdapter.invarPos(self.absCenter[0])
        # Redefines hitboxes around new points.
        self.hitBox.redefine(*self.center)
        self.attackBox.redefine(*map(lambda x,y: int(y+x), self.center,(75,0)))

    def moveTo(self,x,y):
        '''
        Like move function except x,y are an end location. Ie. deltas which define graphics movement are calculated and used to move.
        '''
        # Gets current position and stores it.
        prevCenter = self.standImg.getAnchor()
        prevCenter = (int(prevCenter.getX()),int(prevCenter.getY()))
        # Defines new center.
        self.center = (x,y)
        # Calculates deltas by subtracting current center from next center.
        deltas = tuple(map(lambda x,y: int(y-x), prevCenter,self.center))
        # Moves images to new position using deltas.
        self.standImg.move(*deltas)
        self.attackImg.move(*deltas)
        # Set new absCenter.
        self.absCenter = tuple(map(lambda x,y: int(y+x), self.absCenter,deltas))
        # Updates position adapters.
        positionAdapter.x_pos(self.center[0])
        positionAdapter.invarPos(self.absCenter[0])
        # Redefines hitboxes around new points.
        self.hitBox.redefine(*self.center)
        self.attackBox.redefine(*map(lambda x,y: y+x, self.center,(75,0)))

    def adjust(self,x,y):
        '''
        Basically a move function that doesn't update the absCenter value.
        '''
        # Moves the images to new position.
        self.standImg.move(x,y)
        self.attackImg.move(x,y)
        # Gets new position and stores it as screen space center.
        center = self.standImg.getAnchor()
        self.center = (int(center.getX()),int(center.getY()))
        # Updates position adapter.
        positionAdapter.x_pos(self.center[0])
        # Redefines hitboxes around new points.
        self.hitBox.redefine(*self.center)
        self.attackBox.redefine(*map(lambda x,y: y+x, self.center,(75,0)))

    def update(self,side,amount):
        '''
        This is run by the notifier in the position adapter.
        It runs the adjust function to make the player stay on screen when the background and enemies pan.
        '''
        # Honestly this isn't particularily necessary to have the if, elif, else tree logic; however, it seemed useful at the time.
        if side == "R":
            self.adjust(-2*amount,0)
        elif side == "L":
            self.adjust(-2*amount,0)
        else:
            raise ValueError("Only L or R.")
        screen.update()

    def damageCheck(self):
        '''
        Checks for collision between player hitBoxes and enemies.
        '''
        # Invokes the update method of the active damage class.
        # Then checks all active damage sources to see if they intersect with the player hitbox.
        # Adds intersecting hitboxes to list.
        damageSources.update()
        damages = damageSources.batchCheck()
        # Goes through all damages in list, determines type, then extracts damage from corresponding list.
        for damage in damages:
            if damage[0] == True:
                if damage[1][0] == "e":
                    self.hitPoints = self.hitPoints-self.shieldRate*eyeDict[damage[1]].attackDmg
                elif damage[1][0] == "s":
                    self.hitPoints = self.hitPoints-self.shieldRate*slimeDict[damage[1]].attackDmg
                # If HP dips below 0, HP gets set to 0.
                if self.hitPoints<=0:
                    self.hitPoints = 0
                    break
        # Updates hp readout.
        hitPointReadout.setText("HP: "+str(int(self.hitPoints)))
        screen.update()

    def damageUp(self,damageMult):
        '''
        Multiplies damage.
        '''
        self.attackBox.damage = self.attackBox.baseDamage*damageMult
        self.attackBox.baseDamage = self.attackBox.damage

    def shieldUp(self,shieldMult):
        '''
        Multiplies shield damage reduction coefficient.
        '''
        self.shieldRate = self.shieldRate*shieldMult

    def draw(self):
        '''
        Draws the standImg.
        '''
        self.standImg.draw(screen)


class background:

    def __init__(self,center = (2.25*1920,0)):
        '''
        Creates background image and its data/attributes.
        '''
        self.absCenter = center
        self.center = center
        self.body = Image(gr.Point(*center),"Project11\Resources\Background\Background.gif")

    def draw(self):
        '''
        Draws itself.
        '''
        self.body.draw(screen)

    def adjust(self,x,y):
        '''
        This is executed by the update function.
        When called it pans the background across the screen space in the oposite direction of player movement.
        '''
        self.center = (self.center[0]+x,self.center[1]+y)
        self.body.move(x,y)

    def update(self,side,amount):
        '''
        This is executed by the positionAdapter. This executes the adjust and is a direct part of the listener observer structure.
        '''
        if side == "R":
            self.adjust(-2*amount,0)
        elif side == "L":
            self.adjust(-2*amount,0)
        else:
            raise ValueError("Only L or R.")
        screen.update()


class enemy:

    def __init__(self,center,nameRef,enemylist,enemyType,frames):
        '''
        This initiates a standard enemy object and defines attributes related to it. All enemies are of this type.
        '''
        center = (int(center[0]),int(center[1]))
        # Creates all attributes based on the type in the enemy dictionary and passed variables.
        self.nameRef = nameRef
        self.center = center
        self.absCenter = (self.center[0]+playerActor.absCenter[0]-playerActor.center[0],self.center[1])
        self.stats = enemylist.enemyDict[enemyType]
        self.type = enemyType
        self.name = self.stats[0]
        self.attackDmg = enemylist.enemyDict[enemyType][1]
        self.HP = enemylist.enemyDict[enemyType][2]
        self.enemyFrames = {}
        self.playerState = False
        # Creates all enemy frames and adds them to indexable dictionary.
        for frame in range(frames):
            frameName = "frame"+str(frame)
            self.enemyFrames[frameName] = Image(gr.Point(*center),enemylist.enemyDict[enemyType][3][frame])
        # Creates enemy-type hitbox.
        self.hitBox = hitboxDefined(center,self.enemyFrames["frame0"].getWidth(),self.enemyFrames["frame0"].getHeight(),*initInfo,self.nameRef,enemyType=enemyType,hitDeque=hitTrackDeque)
        self.height = self.enemyFrames["frame0"].getHeight()
        self.width = self.enemyFrames["frame0"].getWidth()
        # Registers item to tracker lists.
        weaponUpdater.registerTracker(self)
        if positionAdapter._x_Pos>-610 and positionAdapter._x_Pos<610 and positionAdapter._invarPos<=9250 and positionAdapter._invarPos>=-610:
            positionAdapter.registerTracker(self)
        # Adds item to queue to only allow 5 enemies at a time. Preserves memory and makes the game playable.
        spawnTool.maximalActiveEnemyQueue.put(self)

    def update(self,side,amount):
        '''
        Standard updater you've seen for the other two classes. Pans enemies with background.
        '''
        if side == "R":
            self.adjust(-2*amount,0)
        elif side == "L":
            self.adjust(-2*amount,0)
        else:
            raise ValueError("Only L or R.")
        screen.update()

    def update2(self,state):
        '''
        This is updated by the notifier in Updater2. This sets up the enemy to recieve damage as it will only do a damage check when
        the state is true to save up on memory.
        '''
        self.playerState = state

    def adjust(self,x,y):
        '''
        Pretty much same adjust function as defined in the background class but all in all this just again moves without updating
        absCenter.
        '''
        self.enemyFrames["frame0"].move(x,y)
        center = self.enemyFrames["frame0"].getAnchor()
        self.center = (int(center.getX()),int(center.getY()))
        self.hitBox.redefine(*self.center)

    def adjustTo(self,x,y):
        '''
        A go to version of the adjust method.
        '''
        self.center = (int(x),int(y))
        self.enemyFrames["frame0"].moveTo(x,y)
        self.hitBox.redefine(*self.center)

    def localDmgCheck(self,attackBox):
        '''
        Checks for intersection between self and player.attackbox. If there is an intersection the attack box damage is extracted and 
        the enemy takes that damage. A hit indicator get raised as well. Also disables weapon after hit to disable per tick damage.
        '''
        collisions = None
        if m.sqrt(((self.center[0]-attackBox.center[0])**2)+((self.center[1]-attackBox.center[1])**2)) <= 200 and playerActor.attackBox.state == True:
                collisionState = attackBox.collision(self.hitBox)
                if collisionState[0] == True:
                    callout = gr.Text(gr.Point(*tuple(map(lambda x,y: x+y,self.center,(0,75)))),"HIT!")
                    callout2 = gr.Text(gr.Point(*tuple(map(lambda x,y: x+y,self.center,(0,75)))),"HIT!")
                    callout.setFace("helvetica")
                    callout2.setFace("helvetica")
                    callout.setSize(24)
                    callout2.setSize(25)
                    callout.setFill("red")
                    callout2.setFill("black")
                    callout2.draw(screen)
                    callout.draw(screen)
                    undraw = Timer(.5,callout.undraw)
                    undraw2 = Timer(.5,callout2.undraw)
                    undraw.start()
                    undraw2.start()
                    self.takeDamage(attackBox.damage)
                    self.playerState = False

    def takeDamage(self,damage):
        '''
        This lowers the enemy HP, and if the HP reaches or crosses 0 the enemy dies.
        '''
        self.HP = self.HP-damage
        if self.HP <= 0:
            self.die()        

    def die(self):
        '''
        This function is designed to make the enemy no longer possible to be interacted with, free up memory, and facilitate loot 
        drops and the creation of mor enemies.
        As such its pretty lengthy.
        '''
        center = self.center
        # Makes space in queue.
        spawnTool.maximalActiveEnemyQueue.get()
        # Deregisters trackers.
        weaponUpdater.deregisterTracker(self)
        if self in positionAdapter._observers:
            positionAdapter.deregisterTracker(self)
        # Deactivates hitboxes.
        self.hitBox.deactivate()
        # Removes from active enemy list.
        existingEnemies.remove(self)
        # Deletes every enemy frame.
        for frame in range(len(self.enemyFrames)):
            frameName = "frame"+str(frame)
            self.enemyFrames[frameName].undraw()
            del self.enemyFrames[frameName]
        # Initiates loot drop thread.
        loot = Thread(target=lootDrop,args=[center],daemon=True)
        loot.start()
    
    def dieNoDrop(self):
        '''
        Same as above no loot.
        '''
        center = self.center
        spawnTool.maximalActiveEnemyQueue.get()
        weaponUpdater.deregisterTracker(self)
        positionAdapter.deregisterTracker(self)
        self.hitBox.deactivate()
        existingEnemies.remove(self)
        for frame in range(len(self.enemyFrames)):
            frameName = "frame"+str(frame)
            self.enemyFrames[frameName].undraw()
            del self.enemyFrames[frameName]


class eyeEnemy(enemy):

    def __init__(self,center,ref):
        '''
        Child class of enemy. Passes along 'eyeBall' type to enemy class, and defines movement for enemy type. 
        '''
        enemy.__init__(self,center,ref,enemyTrack,"eyeBall",1)
        self.enemyFrames["frame0"].draw(screen)
    
    def move(self,pathPoints):
        '''
        Movement system for eye enemies. pathPoints are passed in and generated by the path generator function using a random 
        pathfinding algorithm. Regardless it doubles the amount of points in the list to make the movement a little smoother. 
        At several points the function checks to make sure that the enemy HP has not fallen below or equal to zero. 
        If it has the function is interrupted and is stopped.
        '''
        smoothPath = pathPoints
        # Point doubling.
        for i in range(len(pathPoints)-1):
            inpointDisplace = list(map(lambda x,y: (y-x),pathPoints[i],pathPoints[i+1]))
            stepDisplace = list(map(lambda x: x/2,inpointDisplace))
            for j in range(1):
                stepPoint = list(map(lambda x,y: int(x+((1)*y)),pathPoints[i],stepDisplace))
                smoothPath.append(stepPoint)
        # Sorting points by distance from final destination.
        smoothPath.sort(key=lambda x: m.sqrt((x[0]-playerActor.center[0])**2+(x[1]-playerActor.center[1])**2))
        start = t.time()
        # Iterates through points in smoothPath
        for k in range(len(smoothPath)-1):
            if self.HP<=0:
                return
            t.sleep(tick*.000001)
            if self.HP<=0:
                return
            # Defines new point and attributes relating to location.
            (dx,dy) = tuple(map(lambda x,y: -(y-x),smoothPath[k],smoothPath[k+1]))
            self.center = (self.center[0]+dx,self.center[1]+dy)
            self.absCenter = (self.center[0]+dx,self.center[1]+dy)
            if self.HP<=0:
                return
            # Goes to point.
            self.enemyFrames["frame0"].move(dx,dy)
            # Redefines hitboxes.
            self.hitBox.redefine(*self.center)
            screen.update()
            # This whole system is to make the path get recalculated using new end and beginning points every .1 seconds.
            end = t.time()
            if self.playerState == True:
                self.localDmgCheck(playerActor.attackBox)
            timeElapsed = end-start
            if timeElapsed>.1:
                break


def eyeCreator(name, eyePos):
    '''
    Creates an eye enemy with name at eyePos. It creates this enemy in a seperate thread,
    constantly running the path gen and movement functions until the eye is dead.
    '''
    # Makes enemy spawning toggleable.
    if spawnTool.activityState == False:
        return
    # Creates enemy and adds it to a dictionary of all eye-type enemies. Then appends it to the list of active enemies.
    eyeDict[name] = eyeEnemy(eyePos,name)
    existingEnemies.append(eyeDict[name])
    # While loop with condition eye enemy HP being greater than 0.
    while eyeDict[name].HP > 0:
        # Calculates distance between current point and player center. If distance is less than 5 it stops executing the code.
        distance = m.sqrt(((eyeDict[name].center[0]-playerActor.center[0])**2)+((eyeDict[name].center[1]-playerActor.center[1])**2))
        if distance <= 5:
            if eyeDict[name].HP <= 0:
                break
            t.sleep(1)
        if distance>5:
            if eyeDict[name].HP <= 0:
                break
            pathPasser = Timer(.9,pathGenerator,[name,eyeDict[name].center,playerActor.center,7,5])
            pathPasser.start()
            path = pathGenerator(name,eyeDict[name].center,playerActor.center,7,5)
            if eyeDict[name].HP <= 0:
                break
            eyeDict[name].move(path)
            if eyeDict[name].HP <= 0:
                break
            path = eyePathLists[name][0]


def qCheck(actor):
    '''
    Runs a local damage check on an actor from the player weapon eight times once every five ticks.
    '''
    for i in range(8):
        if actor.playerState == True:
            actor.localDmgCheck(playerActor.attackBox)
        t.sleep(5*tick)


class slimeEnemy(enemy):

    def __init__(self,center,slimeType,ref):
        '''
        Child class of enemy. Passes along slime-type type to enemy class, and defines movement for enemy type. 
        '''
        enemy.__init__(self,center,ref,enemyTrack,slimeType,1)
        self.enemyFrames["frame0"].draw(screen)
    
    def move(self):
        '''
        Movement system for slime enemies. Determines whether slime is to the left, right, or located on the player. Depending on that 
        the sideStep is either defined as 1,, -1, or 0, respectively. If the space between the slime and the player is less than 180 a
        small jump is performed. This jump is of lesser height and range than the full jump. If the distance is greater than 180 then
        the jump range is set to 180 and a normal jump is performed.
        '''
        self.playerCenter = playerActor.center
        # Direction variable.
        directionVar = self.center[0]-self.playerCenter[0]
        if directionVar<0:
            sideStep = 1
        elif directionVar>0:
            sideStep = -1
        elif directionVar==0:
            sideStep = 0
        else:
            raise ValueError("Oi' mate this shouldn't be possible.")
        # Long jump. For when the distance exceeds or is equal to 180.
        if abs(directionVar)>=180:
            directionVar = 180
            for i in range(-90,91):
                # We frequently use this if statement to check if in the process of executing this code the hp has dropped to zero.
                if self.HP<=0:
                    return
                upstep = (-i)/30
                # newFoot and tempFloor are used to make it such that if the slime ever falls below or above the uneven floor he is
                # adjusted to meet the floor again. 
                newFoot = int(self.center[1]-int(self.height/2)+upstep)
                tempFloor = (540-floorData[960+sideStep+int(self.absCenter[0])][1])
                if self.HP<=0:
                    return
                # Movement along parabola.
                prevCenter = self.enemyFrames["frame0"].getAnchor()
                prevCenter = (prevCenter.getX(),prevCenter.getY())
                self.enemyFrames["frame0"].move(sideStep,upstep)
                screen.update()
                if self.HP<=0:
                    return
                if newFoot+25<tempFloor:
                    break
                # Adjustment of attributes and redefining hitbox.
                center = self.enemyFrames["frame0"].getAnchor()
                self.center = (int(center.getX()),int(center.getY()))
                deltas = tuple(map(lambda x,y: y-x, prevCenter,self.center))
                self.absCenter = tuple(map(lambda x,y: int(y+x), self.absCenter,deltas))
                self.hitBox.redefine(*self.center)
                # Damage check
                if self.playerState == True:
                    self.localDmgCheck(playerActor.attackBox)
            prevCenter = self.enemyFrames["frame0"].getAnchor()
            prevCenter = (prevCenter.getX(),prevCenter.getY())
            if self.HP<=0:
                return
            # Movement back to floor.
            self.enemyFrames["frame0"].moveTo(self.center[0],(540-int(floorData[960+int(self.absCenter[0])][1]-int(self.height/2))))
            screen.update()
            if self.HP<=0:
                return
            # Adjustment of attributes and redefining hitbox.
            center = self.enemyFrames["frame0"].getAnchor()
            self.center = (int(center.getX()),int(center.getY()))
            deltas = tuple(map(lambda x,y: y-x, prevCenter,self.center))
            self.absCenter = tuple(map(lambda x,y: int(y+x), self.absCenter,deltas))
            self.hitBox.redefine(*self.center)
            if self.playerState == True:
                self.localDmgCheck(playerActor.attackBox)
        # Short jump. For when the distance is less than 180.
        elif abs(directionVar)<180 and abs(directionVar)!=0:
            rangeTuple = (-int(abs(directionVar)/2),int(abs(directionVar)/2)+1)
            for i in range(*rangeTuple):
                upstep = (-i)/(m.ceil((abs(directionVar)/4)))
                # newFoot and tempFloor are used to make it such that if the slime ever falls below or above the uneven floor he is
                # adjusted to meet the floor again. 
                newFoot = int(self.center[1]-int(self.height/2)+upstep)
                tempFloor = (540-floorData[961+int(self.absCenter[0])][1])
                if self.HP<=0:
                    return
                prevCenter = self.enemyFrames["frame0"].getAnchor()
                prevCenter = (prevCenter.getX(),prevCenter.getY())
                self.enemyFrames["frame0"].move(sideStep,upstep)
                screen.update()
                if self.HP<=0:
                    return
                if newFoot+25<tempFloor:
                    break
                # Adjustment of attributes and redefining hitbox.
                center = self.enemyFrames["frame0"].getAnchor()
                self.center = (int(center.getX()),int(center.getY()))
                deltas = tuple(map(lambda x,y: y-x, prevCenter,self.center))
                self.absCenter = tuple(map(lambda x,y: int(y+x), self.absCenter,deltas))
                self.hitBox.redefine(*self.center)
                # Damage check
                if self.playerState == True:
                    self.localDmgCheck(playerActor.attackBox)
                if self.HP<=0:
                    return
            prevCenter = self.enemyFrames["frame0"].getAnchor()
            prevCenter = (prevCenter.getX(),prevCenter.getY())
            if self.HP<=0:
                return
            # Movement back to floor.
            self.enemyFrames["frame0"].moveTo(self.center[0],(540-int(floorData[960+int(self.absCenter[0])][1]-self.height/2)))
            screen.update()
            if self.HP<=0:
                return
            # Adjustment of attributes and redefining hitbox.
            center = self.enemyFrames["frame0"].getAnchor()
            self.center = (int(center.getX()),int(center.getY()))
            deltas = tuple(map(lambda x,y: y-x, prevCenter,self.center))
            self.absCenter = tuple(map(lambda x,y: int(y+x), self.absCenter,deltas))
            self.hitBox.redefine(*self.center)
            # Damage Check.
            if self.playerState == True:
                self.localDmgCheck(playerActor.attackBox)
        # In place jump. Same as above just no horizontal component.
        elif abs(directionVar)==0:
            for i in range(-90,91):
                upstep = (-i)/30
                newFoot = int(self.center[1]-int(self.height/2)+upstep)
                tempFloor = (540-floorData[961+int(self.absCenter[0])][1])
                # Same break seen before.
                if self.HP<=0:
                    return
                prevCenter = self.enemyFrames["frame0"].getAnchor()
                prevCenter = (prevCenter.getX(),prevCenter.getY())
                # Move along vertical parabola.
                self.enemyFrames["frame0"].move(sideStep,upstep)
                screen.update()
                if self.HP<=0:
                    return
                if newFoot+25<tempFloor:
                    break
                # Data adjustments and hitbox definition.
                center = self.enemyFrames["frame0"].getAnchor()
                self.center = (int(center.getX()),int(center.getY()))
                deltas = tuple(map(lambda x,y: y-x, prevCenter,self.center))
                self.absCenter = tuple(map(lambda x,y: int(y+x), self.absCenter,deltas))
                self.hitBox.redefine(*self.center)
                # Damage Check.
                if self.playerState == True:
                    self.localDmgCheck(playerActor.attackBox)
        else:
            raise ValueError("Again this should be impossible. FYI most of these error messages are for debugging to trace erroe causes.")
        # More damage checking and wait between jumps.
        if self.playerState == True:
            self.localDmgCheck(playerActor.attackBox)
        interimTimer = Timer(5*tick,qCheck,[self])
        interimTimer.start()
        t.sleep(10*tick)
        if self.HP<=0:
            return
        t.sleep(r.random()*2)


def slimeCreator(name, slimePos):
    '''
    Creates a slime enemy with name at slimePos. It also chooses between green, blue, and purple slime randomly.
    It creates this enemy in a seperate thread,constantly running the path gen and movement functions until the eye is dead.
    '''
    slimeType = r.choice(["greenSlime","greenSlime","greenSlime","blueSlime","blueSlime","purpleSlime"])
    if spawnTool.activityState == False:
        return
    slimeDict[name] = slimeEnemy(slimePos,slimeType,name)
    existingEnemies.append(slimeDict[name])
    while slimeDict[name].HP > 0:
        slimeDict[name].move()


class enemySpawner:

    def __init__(self):
        '''
        Initiates spawner tool. This tool is to be initiated in a seperate thread. It creates a queue with a max size of enemyLimit.
        If the queue is not full a random enemy will be spawned at a semi random location. 
        '''
        self.maximalActiveEnemyQueue = Queue(enemyLimit)
        self.activityState = True

    def spawn(self):
        self.spawnChoice = ["slime","slime","eyeBall"]
        self.enemyTypeChoice = r.choice(self.spawnChoice)
        if self.maximalActiveEnemyQueue.full() is not True:
            if self.enemyTypeChoice == "slime":
                x = r.randint(1000,2000)
                y = 600-floorData[960+int(playerActor.absCenter[0])+x][1]
                self.creator = Thread(target=slimeCreator,args=["slime"+str(len(slimeDict)),(x,y)],daemon=True)
                self.creator.start()
            elif self.enemyTypeChoice == "eyeBall":
                x = r.randint(-1200,1800)
                y = 540
                self.creator = Thread(target=eyeCreator,args=["eyeBall"+str(len(eyeDict)),(x,y)],daemon=True)
                self.creator.start()
            else:
                raise RuntimeError("Not possible, yo!")


def enemySpawnerThreader():
    '''
    Runs spawnTool in seperate thread. Tries to spawn an enemy once every 2 seconds while the spawner is not disabled.
    '''
    global spawnTool
    spawnTool = enemySpawner()
    while spawnTool.activityState == True:
        t.sleep(2)
        if spawnTool.activityState == False:
            break
        spawnTool.spawn()


def screensize():
    '''
    Determines screen size dynamically and returns dimensions. Ended up not using this because images didn't scale. 
    It could be worked back in by messing with tkinters resolution scaling and dpi awareness.
    '''
    scrGrab = tk.Tk()
    width = scrGrab.winfo_screenwidth()
    height = scrGrab.winfo_screenheight()
    scrGrab.destroy()
    return (width,height)

# A bunch of variables needed for code execution.
fov = 360
shapeList = []
'''
screenParam = screensize()
width = screenParam[0]
height = screenParam[1]
'''
width =1920
height=1080
# Honestly this logo is barely viible but I made the effort so here it is.
logo = tk.PhotoImage(file="Project11\Daco_6135086.png")
# We disable autoflush to decrease inefficiency, to prevent foreground flashing, and because it is bad.
screen = gr.GraphWin("Yeah, We Doin' a Project.'", width=width, height=height, autoflush=False)
screen.setCoords(-width/2,-height/2,width/2,height/2)
# I made a program that interprets my background image and generates floor data from the image. I already ran the code.
# The stores the necessary data to a text file which we open and extract here.
with open("Project11\FloorData.txt") as floorFile:
    floorData = js.load(floorFile)
floorFile.close()
# Here we add a a couple extra points on the right side for padding to make sure we get no errors.
floorData.extend([[10560, 899], [10561, 899], [10562, 899], [10563, 899], [10564, 899]])
# Initiate some of the necessary objects.
playerActor = player((0,int(540-floorData[int(width/2)][1])+76))
bg = background()
damageSources =  activeDamage(playerActor,hitTrackDeque[0])


def restartProgram():
    '''
    Restarts program. Only really works as expected if run from a terminal, so please use the bat file I included.
    '''
    os.execv(sys.executable, [sys.executable,__file__] + sys.argv)


def quitProgram():
    '''
    Quick program killer. This and the above function are triggered by button presses of the buttons that show up when you die.
    '''
    screen.destroy()
    exit()


def constantDamageCheck():
    '''
    This is constantly running in a seperate thread and checks player collision once everey five ticks while HP is above zero. Once HP reaches zero it cleans up the program, 
    runs the death sequence and initiates the buttons to restart or quit.
    '''
    while playerActor.hitPoints>0:
        t.sleep(5*tick)
        playerActor.damageCheck()
    print("You DIED!")
    screen.unbind_all("<a>")
    screen.unbind_all("<d>")
    screen.unbind_all("<Control-space>")
    screen.unbind_all("<a>" "<space>")
    screen.unbind_all("<d>" "<space>")
    screen.unbind_all("<1>")
    spawnTool.activityState = False
    for item in existingEnemies:
        item.takeDamage(item.HP)
    flash()
    deathSplash = Image(gr.Point(0,0),"Project11\Resources\FAIL\gitGud.gif")
    deathSplash.draw(screen)
    restartGame = tk.Button(screen.master,text="RESTART?",activeforeground="black",activebackground="white",bd=0,command=restartProgram,bg="black",fg="white",font=("horsemen",25))
    quitGame = tk.Button(screen.master,text="Quit?",activeforeground="black",activebackground="white",bd=0,command=quitProgram,bg="black",fg="white",font=("horsemen",25))
    restartGame.pack()
    quitGame.pack()
    restartGame.place(anchor=tk.NE, x=675, y=800)
    quitGame.place(anchor=tk.NW, x=1225, y=800)


def screenFull(self, event=''):
    '''
    Sooooooo long story short this function right here gave me a lot of grief. I had hoped to make it just toggleable with <F11>;
    however, unfortunately when I made the function change the togglestate it broke everything... So just use <F11> to fullscreen and <Escape> to exit fullscreen.
    '''
    screen.master.attributes("-fullscreen", True)


def screenEsc(self, event=''):
    '''
    Same Story as above this is the toggle off function.
    '''
    screen.master.attributes("-fullscreen", False)


def flash():
    '''
    This function creates a "flash of light" effect that rapidly grows from the center of the screen
    and then disapears.
    '''
    # Initiates output list.
    tempList = []
    # Parameters for initial circle.
    center = gr.Point(0,0)
    radius = 1
    # Draw initial circle.
    flash = gr.Circle(center,radius)
    flash.setFill("black")
    tempList.append(flash)
    tempList[0].draw(screen)
    screen.update()
    radius = 0
    # Animation Loop.
    for i in range(50):
        # Updates radius and creates circle.
        radius += 40
        flash = gr.Circle(center,radius)
        flash.setFill("black")
        tempList.append(flash)
    for i in range(50):
        # Draws circle.
        tempList[i+1].draw(screen)
        screen.update()
    for i in range(51):
        # Removes all circles.
        tempList[i].undraw()
    screen.update()


def compColor(hexColor):
    '''
    This gets the complement to the initial color. 
    It is effectively the oposite or negative color. 
    That is that 255,255,255 "white" is the inputted color plus the returned color.
    Oh also I modified the Graphics plus package, getFill() command to return hex instead of tuples.
    This is because I prefer hex.
    ''' 
    # This takes an inputted string and removes the #
    modif = hexColor.lstrip("#")
    # Turns hex code into tuples in 255 format.
    tupColor = (int(modif[0:2], 16), int(modif[2:4], 16), int(modif[0:2], 16))
    # Calculates the complement color.
    complementColor = tuple(int(255-tupColor[i]) for i in range(len(tupColor)))
    # reformats tuple as hex.
    hexFormat = '#{:02x}{:02x}{:02x}'.format(*complementColor)
    # Returns hex color.
    return hexFormat


def pathGenerator(identifier,p1,pN,noiseLength=50,terminatingLength=50):
    '''
    This uses the deque to be thread safe. This is the aforementioned path generation algorithm for the eyeball enemies.
    This function is recursive, while the distance between the current point and the final point pN is greater than the terminating length
    this function will generate a point between the two that is random (with max distance controlled by noise length) yet does not make the distance
    between the two point longer, ie the path gets shorter every recursion.
    '''
    eyePathLists[identifier] = deque()
    point0 = p1
    pointN = pN
    pointsList = []
    # Length petween initial and terminal.
    Length1 = m.sqrt(sum(map(lambda x,y: (y-x)**2,point0,pointN)))
    # If distance between initial and terminal is lessthan terminating length just passes terminal point as goTo.
    if Length1 <= terminatingLength:
        pointsList.append(pointN)
        eyePathLists[identifier].append(pointsList)
        return pointsList
    # Initiates condition for while loop. Once the didtance between current point and terminal point is less than or equal to the terminating length endState is set equal to True.
    endState = False
    while endState == False:
        lengthState = False
        # Generates new point and makes sure that new point makes the path shorter not longer.
        while lengthState == False:
            newPoint = tuple(map(lambda x,y: x+y, point0, (r.randint(-noiseLength,noiseLength),r.randint(-noiseLength,noiseLength))))
            Length2 = m.sqrt(sum(map(lambda x,y: (y-x)**2,newPoint,pointN)))
            if Length2<Length1:
                pointsList.append(newPoint)
                lengthState = True
        Length1 = Length2
        point0 = newPoint
        # Checks if new point is within terminating distance of the terminal point.
        if Length2<terminatingLength:
            endState = True
    # Adds terminal point to go to list and returns list.
    pointsList.append(pointN)
    eyePathLists[identifier].append(pointsList)
    return pointsList
    

def mountainBackground(color=0,y=0,roughness=0,displacement=0,iterations=0,beginx=(-.5)*width,endx=(.5)*width,floor=-10,varName=None):
    '''
    Woohoo, this was actually pretty fun. Difficult, but fun. Honestly I had to read a blogpost to get the idea for this algorithm. However, the implementation is my own.
    However, I doubt the implementation is too different from others because its a pretty unique idea. Basically a midpoint bisection algorithm.

    Also FYI this is compound shape 2.
    '''
    # This determines the x coordinates of the bounds of the mountain ranges depending on visible x coordinates in this screenspace dependant on z coordinates.
    x1 = beginx
    x2 = endx
    # Initiates our terrain array.
    pointList = [[x1,y],[x2,y]]
    grPointList = []
    # Splits our line however many times specified in iterations.
    for i in range(iterations):
        # Turns list to tuple because tuple values are better for this math.
        workablePoints = tuple(pointList)
        for j in range(len(workablePoints)-1):
            # Calculates midpoint x coordinate.
            midx = (workablePoints[j][0]+workablePoints[j+1][0])/2
            # Calculates midpoint y coordinate.
            midy = (workablePoints[j][1]+workablePoints[j+1][1])/2
            # Bundles these two values into a list like all other points.
            midpoint = list((midx,midy))
            # Changes the y value of the list.
            midpoint[1] += r.randrange(-1,1)*displacement
            # Prevents negative values.
            if midpoint[1] < floor:
                midpoint[1] = floor-(midpoint[1]-floor)
            # Puts the list into the right place in the list of lists. (Sorts by x coordinate.)
            b.insort(pointList,midpoint)
        # Lowers displacement paramater each iteration.
        displacement *= 2**(roughness)
    # Dynamically names and converts points to gr.Points. Then adds to grPointList.
    for i in range(len(pointList)):
        points = "point" + str(i+1)
        globals()[points] = tuple(pointList[i])
        grPoints = "grPoint" + str(i+1)
        globals()[grPoints] = gr.Point(*globals()[points])
        grPointList.append(globals()[grPoints])
    # Creates our desired polygon.
    backShape = gr.Polygon(*tuple(grPointList),gr.Point(x2,floor),gr.Point(x1,floor))
    # Sets color.
    backShape.setFill(color)
    # Handles naming when requested.
    if varName is not None:
        globals()[varName] = backShape
        return globals()[varName]


def quit(self):
    '''
    Key-bindable quit function. Click "<Del>" to quit game at any time.
    '''
    screen.close()
    exit()


def attack(self):
    '''
    Key-bindable attack function. Click "<1>", mouse -1, to attack with player character.
    You can only attack once per half second.
    '''
    screen.unbind_all("<1>")
    playerActor.attack()
    bind = Timer(30*tick,screen.bind_all, ["<1>", attack])
    bind.start()


def moveLeft(self):
    '''
    Key-bindable move left function. Click "<a>" to move left with player character.
    Moves to the left one point five times and adjust height to floor.
    '''
    screen.unbind_all("<a>")
    screen.unbind_all("<d>")
    # Makes function toggleable only once per half tick.
    time1 = Timer(.5*tick,screen.bind_all,["<d>", moveRight])
    time1.start()
    # Does not rebind function if at left edge of in game space.
    if positionAdapter._invarPos>=-960:
        time2 = Timer(.5*tick,screen.bind_all,["<a>", moveLeft])
        time2.start()
    for i in range(5):
        # Breaks loop if at left edge of in game space.
        if positionAdapter._invarPos<=-960:
            break
        # Adjustment of attributes and movement.
        center = playerActor.absCenter
        height = playerActor.height
        dx = -1
        dy = (540-floorData[int(center[0])+961][1])+height/2-center[1]
        playerActor.move(dx,dy)
        screen.update()
        

def moveRight(self):
    '''
    Key-bindable move right function. Click "<d>" to move right with player character.
    Moves to the right one point five times and adjust height to floor.
    '''
    screen.unbind_all("<a>")
    screen.unbind_all("<d>")
    # Makes function toggleable only once per half tick.
    time1 = Timer(.5*tick,screen.bind_all,["<a>", moveLeft])
    time1.start()
    # Does not rebind function if at right edge of in game space.
    if positionAdapter._invarPos<=9600:
        time2 = Timer(.5*tick,screen.bind_all,["<d>", moveRight])
        time2.start()
    for i in range(5):
        # Breaks loop if at right edge of in game space.
        if positionAdapter._invarPos>=9600:
            break
        # Adjustment of attributes and movement.
        center = playerActor.absCenter
        height = playerActor.height
        dx = 1
        dy = (540-floorData[int(center[0])+961][1])+height/2-center[1]
        playerActor.move(dx,dy)
        screen.update()
        

def jumpUp(self):
    '''
    Key-bindable jump up function. Click ""<Control-space>"" to move up with player character.
    Moves up in a rate controlled by the derivative of a parabola essentialy.
    '''
    # Unbinds all other movement inputs, for execution.
    screen.unbind_all("<a>")
    screen.unbind_all("<d>")
    screen.unbind_all("<Control-space>")
    screen.unbind_all("<a>" "<space>")
    screen.unbind_all("<d>" "<space>")
    # Jump movement.
    for i in range(-90,91):
        upstep = (-i)/30
        playerActor.move(0,upstep)
        screen.update()
    # Rebinds all other movements.
    screen.bind_all("<a>", moveLeft)
    screen.bind_all("<d>", moveRight)
    screen.bind_all("<a>" "<space>", jumpLeft)
    screen.bind_all("<Control-space>", jumpUp)
    screen.bind_all("<d>" "<space>", jumpRight)


def jumpLeft(self):
    '''
    Key-bindable jump left function. Click ""<Control-space>"" to move up and left with player character.
    Moves up in a rate controlled by the derivative of a parabola essentialy, and left at a rate of one point per loop.
    Jump is a parabola.
    '''
    # Unbinds all other movement inputs, for execution.
    screen.unbind_all("<a>")
    screen.unbind_all("<d>")
    screen.unbind_all("<Control-space>")
    screen.unbind_all("<a>" "<space>")
    screen.unbind_all("<d>" "<space>")
    stepSet = None
    # Jump movement. Same as slime checks player position relative to floor at each loop to make sure the player has not crossed the floor boundary,
    # if this is the case the loop breaks and the player is adjusted to the floor.
    for i in range(-90,91):
        # Checks if player has met left boundary, if this is the case disables horizontal component of jump.
        if positionAdapter._invarPos<=-960:
            stepSet = i
            break
        upstep = (-i)/30
        newFoot = playerActor.center[1]-playerActor.height/2+upstep
        tempFloor = (540-floorData[960+int(playerActor.absCenter[0])][1])
        playerActor.move(-1,upstep)
        screen.update()
        # Checks player position relative to floor.
        if newFoot+25<tempFloor:
            break
    # Jump with no horizontal component.
    if stepSet is not None:
        for j in range(stepSet+1,91):
            upstep = (-j)/30
            newFoot = playerActor.center[1]-playerActor.height/2+upstep
            tempFloor = (540-floorData[960+int(playerActor.absCenter[0])][1])
            playerActor.move(0,upstep)
            screen.update()
            # Checks player position relative to floor.
            if newFoot+25<tempFloor:
                break
    # Adjusts player position back to floor.
    if newFoot>tempFloor:
        playerActor.move(0,tempFloor-newFoot)
    screen.update()
    # Rebinds all movement except leftward, if the player is at left boundary.
    screen.bind_all("<d>", moveRight)
    screen.bind_all("<d>" "<space>", jumpRight)
    screen.bind_all("<Control-space>", jumpUp)
    if positionAdapter._invarPos>=-960:
        screen.bind_all("<a>", moveLeft)
        screen.bind_all("<a>" "<space>", jumpLeft)


def jumpRight(self):
    '''
    Key-bindable jump right function. Click ""<Control-space>"" to move up andright with player character.
    Moves up in a rate controlled by the derivative of a parabola essentialy, and right at a rate of one point per loop.
    Jump is a parabola.
    '''
    # Unbinds all other movement inputs, for execution.
    screen.unbind_all("<a>")
    screen.unbind_all("<d>")
    screen.unbind_all("<Control-space>")
    screen.unbind_all("<a>" "<space>")
    screen.unbind_all("<d>" "<space>")
    stepSet = None
    # Jump movement. Same as slime checks player position relative to floor at each loop to make sure the player has not crossed the floor boundary,
    # if this is the case the loop breaks and the player is adjusted to the floor.
    for i in range(-90,91):
        # Checks if player has met right boundary, if this is the case disables horizontal component of jump.
        if positionAdapter._invarPos>=9600:
            stepSet = i
            break
        upstep = (-i)/30
        newFoot = playerActor.center[1]-playerActor.height/2+upstep
        tempFloor = (540-floorData[960+int(playerActor.absCenter[0])][1])
        playerActor.move(1,upstep)
        screen.update()
        # Checks player position relative to floor.
        if newFoot+25<tempFloor:
            break
    # Jump with no horizontal component.
    if stepSet is not None:
        for j in range(stepSet+1,91):
            upstep = (-j)/30
            newFoot = playerActor.center[1]-playerActor.height/2+upstep
            tempFloor = (540-floorData[960+int(playerActor.absCenter[0])][1])
            playerActor.move(0,upstep)
            screen.update()
            # Checks player position relative to floor.
            if newFoot+25<tempFloor:
                break
    # Adjusts player position back to floor.
    if newFoot>tempFloor:
        playerActor.move(0,tempFloor-newFoot)
    screen.update()
    # Rebinds all movement except rightward, if the player is at right boundary.
    screen.bind_all("<a>", moveLeft)
    screen.bind_all("<a>" "<space>", jumpLeft)
    screen.bind_all("<Control-space>", jumpUp)
    if positionAdapter._invarPos<=9600:
        screen.bind_all("<d>", moveRight)
        screen.bind_all("<d>" "<space>", jumpRight)


def main():
    # Unfortunately because of tkinters scaling, which I only found out about too late. I have to use not 1080p, and I got around that by creating a fullscreen function.
    # Regardless lead to not as clean an ouput as I had hoped.
    global hitPointReadout
    # Register enemy types and defines their stats and images, I had issues with the animations on the slimes thus three of their images are not used.
    enemyTrack.newType("eyeBall",10,30,["Project11\characterDesigns\charGifs\eye.gif"])
    enemyTrack.newType("greenSlime",5,15,["Project11\characterDesigns\charGifs\greenSlimeF1.gif","Project11\characterDesigns\charGifs\greenSlimeF2.gif","Project11\characterDesigns\charGifs\greenSlimeF3.gif","Project11\characterDesigns\charGifs\greenSlimeF4.gif"])
    enemyTrack.newType("blueSlime",10,20,["Project11\characterDesigns\charGifs\BlueSlimeF1.gif","Project11\characterDesigns\charGifs\BlueSlimeF2.gif","Project11\characterDesigns\charGifs\BlueSlimeF3.gif","Project11\characterDesigns\charGifs\BlueSlimeF4.gif"])
    enemyTrack.newType("purpleSlime",15,35,["Project11\characterDesigns\charGifs\purpleSlimeF1.gif","Project11\characterDesigns\charGifs\purpleSlimeF2.gif","Project11\characterDesigns\charGifs\purpleSlimeF3.gif","Project11\characterDesigns\charGifs\purpleSlimeF4.gif"])
    # Creates spawn tool in seperate thread.
    spawnThread = Thread(target=enemySpawnerThreader,daemon=True)
    spawnThread.start()
    # Binds all functions.
    screen.bind_all("<F11>", screenFull)
    screen.bind_all("<Escape>", screenEsc)
    screen.bind_all("<Delete>", quit)
    screen.bind_all("<1>", attack)
    screen.bind_all("<a>", moveLeft)
    screen.bind_all("<d>", moveRight)
    screen.bind_all("<Control-space>", jumpUp)
    screen.bind_all("<a>" "<space>", jumpLeft)
    screen.bind_all("<d>" "<space>", jumpRight)
    # Sets Icon.
    screen.master.iconphoto(False, logo)
    # Sets inital screenstate as not fullscreen.
    screen.master.attributes("-fullscreen", False)
    # Draws basic screen objects.
    bg.draw()
    playerActor.draw()
    # Creates HP Readout box.
    hpBox = gr.Rectangle(gr.Point(-955,535),gr.Point(-750,490))
    hpBox.setFill("white")
    hitPointReadout = gr.Text(gr.Point(-850,513),("HP: "+str(int(playerActor.hitPoints))))
    hitPointReadout.setFace("helvetica")
    hitPointReadout.setSize(25)
    hpBox.draw(screen)
    hitPointReadout.draw(screen)
    # Initiates player hit/hp tracker in seperate thread.
    hitTracker = Thread(target=constantDamageCheck,daemon=True)
    hitTracker.start()
    # Registers player and background to position adapter.
    positionAdapter.registerTracker(bg)
    positionAdapter.registerTracker(playerActor)
    tk.mainloop()


main()