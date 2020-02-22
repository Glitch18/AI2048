#!/usr/bin/env python3
import pygame
import random
import time

# TODO: Already Increased
# TODO: Implement GameOver

pygame.init()
screen = pygame.display.set_mode((400,400))
pygame.display.set_caption('2048')
FPS = 30
FPSCLOCK = pygame.time.Clock()

class GameState:
    def __init__(self):
        random.seed(int(time.clock_gettime(time.CLOCK_REALTIME)))
        self.tiles = {0:'Blank.jpg', 2:'2.jpg', 4:'4.jpg', 8:'8.jpg', 16:'16.jpg', 32:'32.jpg', 64:'64.jpg', 128:'128.jpg', 256:'256.jpg', 512:'512.jpg', 1024:'1024.jpg', 2048:'2048.jpg'}
        self.free = []
        self.running = True
        self.grid = [0]*4
        self.grid = [self.grid[::] for x in range(4)]
        self.makeFree()
        self.spawn()
        self.spawn()

    def frame_step(self,input_actions):
        pygame.event.pump()

        if sum(input_actions) == 0:
            self.printScreen() #Do Nothing
        elif sum(input_actions) > 1:
            raise ValueError("Multiple Actions")
        elif input_actions[0]:
            self.moveLeft()
        elif input_actions[1]:
            self.moveUp()
        elif input_actions[2]:
            self.moveRight()
        elif input_actions[3]:
            self.moveDown()

        FPSCLOCK.tick(FPS)

    def user_Play(self):
        self.frame_step([0,0,0,0])
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    running=False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        running=False
                    if event.key == pygame.K_LEFT:
                        action = [1,0,0,0]
                        self.frame_step(action)
                    if event.key == pygame.K_RIGHT:
                        action = [0,0,1,0]
                        self.frame_step(action)
                    if event.key == pygame.K_UP:
                        action = [0,1,0,0]
                        self.frame_step(action)
                    if event.key == pygame.K_DOWN:
                        action = [0,0,0,1]
                        self.frame_step(action)

    def makeFree(self):
        for i in range(4):
            for j in range(4):
                if(self.grid[i][j]==0):
                    self.free.append((i,j))

    def printScreen(self):
        screen.fill((0,0,0))
        x,y = 4,4
        for i in range(4):
            x = 4
            for j in range(4):
                icon = pygame.image.load(str(self.tiles[self.grid[i][j]]))
                icon = pygame.transform.scale(icon,(95,95))
                screen.blit(icon,(x,y))
                x += 99
            y += 99
        pygame.display.update()

    def gridPrint(self):
        #os.system('clear')
        print(self.grid[0])
        print(self.grid[1])
        print(self.grid[2])
        print(self.grid[3])
        print('\n')

    def spawn(self):
        x = 2 if random.randint(0,10)<=8 else 4
        chosen = random.choice(self.free)
        self.grid[chosen[0]][chosen[1]] = x
        self.free.remove(chosen)

    def moveLeft(self):
        print("------Moving LEFT------")
        self.gridPrint()
        flag=0
        for i in range(4):
            print("Left "+str(i))
            self.gridPrint()
            for j in range(4):
                print("------"+str(j)+"-----"+str(self.grid[i][j]))
                if(self.grid[i][j]==0):
                    continue
                elif(j!=0):
                    x = j-1
                    while(x>=0 and self.grid[i][x]==0):
                        x-=1
                    if(x>=0 and self.grid[i][x]==self.grid[i][j]):
                        self.grid[i][x] = self.grid[i][j]*2
                        self.grid[i][j]=0
                        self.free.append((i,j))
                        flag=1
                        continue
                    elif(x!=j-1):
                        self.grid[i][x+1]=self.grid[i][j]
                        self.gridPrint()
                        self.free.remove((i,x+1))
                        self.grid[i][j]=0
                        self.gridPrint()
                        self.free.append((i,j))
                        flag=1
                        print("".join(str(_) for _ in self.free if _[0]==i))
        if flag:
            self.spawn()
        self.printScreen()

    def moveRight(self):
        print("------Moving Right----")
        self.gridPrint()
        flag=0
        for i in range(4):
            print("Right "+str(i))
            for j in range(3,-1,-1):
                print("------"+str(j)+"-----"+str(self.grid[i][j]))
                if(self.grid[i][j]==0):
                    continue
                elif(j!=3):
                    x = j+1
                    while(x<=3 and self.grid[i][x]==0):
                        x+=1
                    if(x<=3 and self.grid[i][x]==self.grid[i][j]):
                        self.grid[i][x] = self.grid[i][j]*2
                        self.grid[i][j]=0
                        self.free.append((i,j))
                        flag=1
                    elif(x!=j+1):
                        self.grid[i][x-1]=self.grid[i][j]
                        self.free.remove((i,x-1))
                        self.grid[i][j]=0
                        self.free.append((i,j))
                        flag=1
                        print("".join(str(_) for _ in self.free if _[0]==i))
        if flag:
            self.spawn()
        self.printScreen()

    def moveUp(self):
        print("-------Moving up--------")
        self.gridPrint()
        self.grid = [list(x) for x in zip(*self.grid)]
        print("TRANSPOSE-")
        self.gridPrint()
        flag=0
        for i in range(4):
            print("LEFT "+str(i))
            self.gridPrint()
            for j in range(4):
                print("------"+str(j)+"-----"+str(self.grid[i][j]))
                if(self.grid[i][j]==0):
                    continue
                elif(j!=0):
                    x = j-1
                    while(x>=0 and self.grid[i][x]==0):
                        x-=1
                    if(x>=0 and self.grid[i][x]==self.grid[i][j]):
                        self.grid[i][x] = self.grid[i][j]*2
                        self.grid[i][j]=0
                        self.free.append((j,i))
                        flag=1
                        continue
                    elif(x!=j-1):
                        self.grid[i][x+1]=self.grid[i][j]
                        self.gridPrint()
                        self.free.remove((x+1,i))
                        self.grid[i][j]=0
                        self.gridPrint()
                        self.free.append((j,i))
                        flag=1
                        print("".join(str(_) for _ in self.free if _[0]==i))
        self.grid = [list(x) for x in zip(*self.grid)]
        if flag:
            self.spawn()
        self.printScreen()

    def moveDown(self):
        print("---------GOING DOWNNN---------")
        self.gridPrint()
        self.grid = [list(x) for x in zip(*self.grid)]
        print("TRANSPOSE-")
        self.gridPrint()
        flag=0
        for i in range(4):
            print("RIGHT "+str(i))
            self.gridPrint()
            for j in range(3,-1,-1):
                print("------"+str(j)+"-----"+str(self.grid[i][j]))
                if(self.grid[i][j]==0):
                    continue
                elif(j!=3):
                    x = j+1
                    while(x<=3 and self.grid[i][x]==0):
                        x+=1
                    if(x<=3 and self.grid[i][x]==self.grid[i][j]):
                        self.grid[i][x] = self.grid[i][j]*2
                        self.grid[i][j]=0
                        self.free.append((j,i))
                        flag=1
                    elif(x!=j+1):
                        self.grid[i][x-1]=self.grid[i][j]
                        self.gridPrint()
                        self.free.remove((x-1,i))
                        self.grid[i][j]=0
                        self.gridPrint()
                        self.free.append((j,i))
                        flag=1
                        print("".join(str(_) for _ in self.free if _[0]==i))
        self.grid = [list(x) for x in zip(*self.grid)]
        if flag:
            self.spawn()
        self.printScreen()

if(__name__ == "__main__"):
    g = GameState()
    g.user_Play()
