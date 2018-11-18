import math
import os
import random
import sys
import time
import pygame

"""
TODO
- Create a starting menu screen
    * Show game controls
    * Pause game when user adjust the window size
    * Add intro music?
    * Use image as background of start menu?
- Make Gucci Mane's face spin when hit'
- Add new paddle?
- Mess around with new colors
"""
 
class brickBreaker():

    def main(self):
         
        xSpeed_init = 5
        ySpeed_init = 5
        maxLives = 6
        paddleSpeed = 30
        score = 0
        bgColour = 255, 0, 23 # Red background 
        size = width, height = 640, 480
 
        pygame.init()
        pygame.display.set_caption('So Icy Brick Breakers')          
        screen = pygame.display.set_mode(size, pygame.RESIZABLE) # Default window size

        paddle = pygame.image.load("paddle.png").convert()
        paddleRect = paddle.get_rect()
 
        ball = pygame.image.load("guwopball.png").convert()
        ball.set_colorkey((255, 255, 255))
        ballRect = ball.get_rect()

        """
        Create a list with different 
        sounds bits and randomly choose them 
            - need to figure out what sound bits
        pong = pygame.mixer.Sound(['Gucci-Burr.wav', '', ''])
        """
        pong = pygame.mixer.Sound('Gucci-Burr.wav')
        pong.set_volume(10)        
       
        wall = trumpWall()
        wall.buildWall(width)
 
        # Set ready for game loop
        paddleRect = paddleRect.move((width / 2) - (paddleRect.right / 2), height - 20)
        ballRect = ballRect.move(width / 2, height / 2)      
        xSpeed = xSpeed_init
        ySpeed = ySpeed_init
        lives = maxLives
        clock = pygame.time.Clock()
        pygame.key.set_repeat(1,30)      
        
        pause = False
        resume = False

        while 1:
            
            # FPS
            clock.tick(60)
            
            # Create game controls
            for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                    sys.exit()
                    
                if event.type == pygame.KEYDOWN:
 
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()
                    if event.key == pygame.K_LEFT:                        
                        paddleRect = paddleRect.move(-paddleSpeed, 0)  
                        if (paddleRect.left < 0):                          
                            paddleRect.left = 0    
                    if event.key == pygame.K_RIGHT:                    
                        paddleRect = paddleRect.move(paddleSpeed, 0)
                        if (paddleRect.right > width):                            
                            paddleRect.right = width  
                    if event.key == pygame.K_p:
                        pause = True
                    if event.key == pygame.K_r:
                        resume = True
                    if event.key == pygame.K_F11:
                        screen = pygame.display.set_mode(size, pygame.RESIZABLE)
                    if event.key == pygame.K_F12:
                        screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
                                      
            # Check if paddle has hit ball    
            if ballRect.bottom >= paddleRect.top and \
               ballRect.bottom <= paddleRect.bottom and \
               ballRect.right >= paddleRect.left and \
               ballRect.left <= paddleRect.right:
 
                ySpeed = -ySpeed                
                pong.play(0)                
                offSet = ballRect.center[0] - paddleRect.center[0]

                # Offset > 0 means ball has hit the right side of the paddle                  
                # the angle of ball varies depending on where ball hits paddle             
                if offSet > 0:

                    if offSet > 30:  
                        xSpeed = 7
                    elif offSet > 23:                
                        xSpeed = 6
                    elif offSet > 17:
                        xSpeed = 5
 
                else:
 
                    if offSet < -30:                            
                        xSpeed = -7
                    elif offSet < -23:
                        xSpeed = -6
                    elif offSet < -17:
                        xSpeed = -5
 
                     
            # Move paddle/ball
            ballRect = ballRect.move(xSpeed, ySpeed)
 
            if ballRect.left < 0 or ballRect.right > width:
                xSpeed = -xSpeed
                #random.choice(pong).play(0)                
                pong.play(0)
 
            if ballRect.top < 0:
                ySpeed = -ySpeed      
                pong.play(0)  
                          
            # Check if ball has gone past the paddle - lose a life
            if ballRect.top > height:
               
                lives -= 1
               
                # Start a new ball
                xSpeed = xSpeed_init
                rand = random.random()                
               
                if random.random() > 0.5:
                    xSpeed = -xSpeed
               
                ySpeed = ySpeed_init            
                ballRect.center = width * random.random(), height / 3 

                if lives == 0: 

                    msg = pygame.font.Font(None,70).render("Game Over, Pimp", True, (27, 255, 0), bgColour)
                    msgRect = msg.get_rect()
                    msgRect = msgRect.move(width / 2 - (msgRect.center[0]), height / 3)
                    screen.blit(msg, msgRect)
                    pygame.display.flip()
                    """
                        Trigger user key presses
                            - ESC to quit the game
                            - Use any other key to restart the game
                    """
                    while 1:
                        
                        restart = False
                        
                        for event in pygame.event.get():
               
                            if event.type == pygame.QUIT:
                                sys.exit()

                            if event.type == pygame.KEYDOWN:

                                if event.key == pygame.K_ESCAPE:
                                    sys.exit()
                                if event.key == pygame.K_p:
                                    pause = True
                                if event.key == pygame.K_r:
                                    resume = True
                                if event.key == pygame.K_F11:
                                    screen = pygame.display.set_mode(size, pygame.RESIZABLE)
                                if event.key == pygame.K_F12:
                                    screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
                                if not (event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT):                                    
                                    restart = True

                        if restart: 
                            # Reset game
                            screen.fill(bgColour)
                            wall.buildWall(width)
                            lives = maxLives
                            score = 0
                            break  

            if xSpeed < 0 and ballRect.left < 0:
                xSpeed = -xSpeed                                
                pong.play(0)
 
            if xSpeed > 0 and ballRect.right > width:
                xSpeed = -xSpeed                              
                pong.play(0)
           
            # Check if ball makes contact with wall
            # If yes then remove a brick and change the direction of the ball
            index = ballRect.collidelist(wall.brickRect)      
            if index != -1:
               
                if ballRect.center[0] > wall.brickRect[index].right or \
                   ballRect.center[0] < wall.brickRect[index].left:
                   xSpeed = -xSpeed
 
                else:
                    ySpeed = -ySpeed                
 
                pong.play(0)              
                wall.brickRect[index:index + 1] = []
                score += 10

            # Displays lives/score             
            screen.fill(bgColour)
            scoreText = pygame.font.Font(None,30).render("Score: " + str(score), True, (27, 255, 0), bgColour)
            scoretextRect = scoreText.get_rect()
            scoretextRect = scoretextRect.move(width - scoretextRect.right, 0)

            livesText = pygame.font.Font(None, 30).render("Lives: " + str(lives), True, (27, 255, 0), bgColour)
            livestextRect = livesText.get_rect()

            screen.blit(livesText, livestextRect)
            screen.blit(scoreText, scoretextRect)

            for i in range(0, len(wall.brickRect)):
                screen.blit(wall.brick, wall.brickRect[i])    
                        
            # If bricks are gone then rebuild wall
            if wall.brickRect == []:

                # Displays message to user letting them know they won
                winMsg = pygame.font.Font(None,50).render("You Win! Have a SO ICY DAY! BURRR", True, (27, 255, 0), bgColour)
                msgRect = winMsg.get_rect()
                msgRect = msgRect.move(width / 2 - (msgRect.center[0]), height / 3)
                screen.blit(winMsg, msgRect)
                pygame.display.flip()
                time.sleep(3)

                # Reset lives, score and background color
                screen.fill(bgColour)
                lives = maxLives
                score = 0
                
                # Rebuild wall
                wall.buildWall(width)
                xSpeed = xSpeed_init
                ySpeed = ySpeed_init
                ballRect.center = width / 2, height / 2 
            
            # Pretty straight forward... pauses game.
            if pause:

                pauseMsg = pygame.font.Font(None, 35).render("Game Paused! Press R to Resume Game", True, (27, 255,0), bgColour)
                pausemsgRect = pauseMsg.get_rect()
                pausemsgRect = pausemsgRect.move(width / 2 - (pausemsgRect.center[0]), height / 3)
                screen.blit(pauseMsg, pausemsgRect)
                pygame.display.flip()
                time.sleep(1.2)
            
            # ...
            if resume:

                pause = False
                screen.blit(ball,ballRect)
                screen.blit(paddle, paddleRect)
                pygame.display.flip()

            # Display game    
            screen.blit(ball, ballRect)
            screen.blit(paddle, paddleRect)
            pygame.display.flip()
            

class trumpWall():
 
    def __init__(self):
 
        self.brick = pygame.image.load("brick.png").convert()
        brickRect = self.brick.get_rect()
        self.brickLength = brickRect.right - brickRect.left      
        self.brickHeight = brickRect.bottom - brickRect.top            
 
    def buildWall(self, width):        
 
        xPos = 0
        yPos = 60
        adjust = 0
        self.brickRect = []
 
        for i in range (0, 52):
                       
            if xPos > width:
                if adjust == 0:
                    adjust = self.brickLength / 2
                else:
                    adjust = 0
 
                xPos = -adjust
                yPos += self.brickHeight
               
            self.brickRect.append(self.brick.get_rect())    
            self.brickRect[i] = self.brickRect[i].move(xPos, yPos)
            xPos = xPos + self.brickLength 
 
if __name__ == '__main__':
 
    br = brickBreaker()
    br.main()
