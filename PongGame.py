import pygame
import pygame.freetype

SCREEN_WIDTH = 720
SCREEN_HEIGHT = 480

class Player():
    def __init__(self,position,width,height,RecievesInput = False):
        self.width = width
        self.height = height
        self.color = (255,255,255)
        self.RecievesInput = RecievesInput
        self.position  = position
        self.rect = pygame.Rect(self.position[0],self.position[1],self.width,self.height)
        self.player = None
        self.movSpeed = 6
        self.score = 0

    def Move(self,direction):
        if direction == 0:
            return
        if self.RecievesInput == False:
            #print("Some sorts of AI") # TODO Implement some sorts of simple AI
            return
        prevPos = self.position
        self.position = (self.position[0],self.position[1]+direction*self.movSpeed)
        if self.position[1]<0 or self.position[1]+self.height>SCREEN_HEIGHT:
            self.position = prevPos
        self.rect = pygame.Rect(self.position[0],self.position[1],self.width,self.height)
        #print(self.position)
        #print(newPos)

    def draw(self,surface):
        self.player = pygame.draw.rect(surface,self.color,self.rect)

class Ball():
    def __init__(self,radius,startPos = (100,100),scoredPointFunction = None):
        self.ballSpeed = 5.0
        self.radius = radius
        self.position = startPos
        self.rect = pygame.Rect(self.position[0],self.position[1],self.radius,self.radius)
        self.movDir = (1.0,0.5)
        if scoredPointFunction == None:
            raise AttributeError
        self.scoredPoint = scoredPointFunction

    def move(self):
        prevPos = self.position
        self.position = ((self.position[0]+self.movDir[0]*self.ballSpeed),(self.position[1]+self.movDir[1]*self.ballSpeed))

        if self.position[0]>= SCREEN_WIDTH:
            print("Player 1 wins")
            self.scoredPoint(0)

        if  self.position[0]<= 0:
            print("Player 2 wins")
            self.scoredPoint(1)

        if self.position[1]>= SCREEN_HEIGHT or self.position[1]<= 0:
            self.movDir = (self.movDir[0],self.movDir[1]*-1)
            self.position = prevPos
        self.rect = pygame.Rect(self.position[0],self.position[1],self.radius,self.radius)

    def bounce(self,newDir):
        if self.movDir[1]<0.0:
            self.movDir = (newDir[0] * -1.0, newDir[1] * 1.0)
            return
        self.movDir = (newDir[0] * -1.0, newDir[1] * -1.0)

    def draw(self,surface):
        pygame.draw.ellipse(surface,(255,255,255),self.rect)

class Pong():
    def __init__(self,numPlayers,surface):
        self.players = [Player((((1+i)%2*600)+50,50),20,50) for i in range(numPlayers)]
        self.players[0].RecievesInput = True
        self.ball = Ball(25,(SCREEN_WIDTH/2,SCREEN_HEIGHT/2),scoredPointFunction= self.scoredBall)
        self.surface = surface
        self.moveDir = 0.0
        self.scoreText = pygame.freetype.Font("airstrikeacad.ttf",64)
        self.winningNum = 3

    def scoredBall(self,playerIndex):
        self.restartGame()
        if playerIndex !=0:
            self.players[1].score +=1
            if self.players[1].score == self.winningNum:
                self.gameOver()
        else:
            self.players[0].score +=1
            if self.players[0].score == self.winningNum:
                self.gameOver()
        print(playerIndex)
    def update(self):
        self.ball.move()
        for player in self.players:
            player.Move(self.moveDir)

    def draw(self):
        # Draw UI
        score = f"{self.players[0].score} : {self.players[1].score}"
        self.scoreText.render_to(self.surface,(300,20),str(score),(255,255,255))

        # Draw game elements
        self.ball.draw(self.surface)
        for player in self.players:
            player.draw(self.surface)
            if self.ball.rect.colliderect(player):
                print("Collided")
                self.ball.bounce((1.0,-1.0))

        pygame.display.update()
        screen.fill((0, 0, 0))
        pygame.time.wait(13)

    def pause(self):
        paused = True
        while paused:
            for event in pygame.event.get():
                print(event)
                # only do something if the event is of type QUIT
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        # change the value to False, to exit the main loop
                        paused = False
                        keys = None
            pygame.time.wait(8)

    def restartGame(self,reset = False):
        self.ball = Ball(25, (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2), scoredPointFunction=self.scoredBall)
        if reset:
            self.players[0].score = 0
            self.players[1].score = 0

    def gameOver(self):
        gameOverT = pygame.freetype.Font("airstrikeacad.ttf",60)
        gameOverT.render_to(self.surface,(200,230),"GAME OVER",(255,255,252))
        score = f"{self.players[0].score} : {self.players[1].score}"
        self.scoreText.render_to(self.surface, (300, 150), str(score), (255, 255, 255))

        pygame.display.update()
        isOver = True
        while isOver:
            for event in pygame.event.get():
                print(event)
                # only do something if the event is of type QUIT
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN or pygame.K_UP or pygame.K_LEFT or pygame.K_RIGHT:
                        # change the value to False, to exit the main loop
                        isOver = False
                        self.restartGame(reset=True)
            pygame.time.wait(8)

pygame.init()
pygame.display.set_caption("Pong game")
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

running = True
game = Pong(2,screen)
paused = False

while running:
    # Get Player input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        #   Movement
    keys = pygame.key.get_pressed()
    game.moveDir = 0
    if keys[pygame.K_DOWN] == True:
        #print("Key Down")
        game.moveDir = 1.0
    if keys[pygame.K_UP] == True:
        #print("Key UP")
        game.moveDir = -1.0
    print(keys[pygame.K_ESCAPE])
    if keys[pygame.K_ESCAPE] == True:
        game.pause()


    game.update()
    game.draw()