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

class BrickBreaker():
    def gucci_main(self):
        xSpeed_init = 6  # roast: consider making these value's members of the class
        ySpeed_init = 6
        maxLives = 6
        paddleSpeed = 30
        score = 0
        bgColor = 255, 0, 23  # Red background
        size = width, height = 640, 480

        pygame.init()
        pygame.display.set_caption("So Icy Brick Breakers")
        screen = pygame.display.set_mode(size, pygame.RESIZABLE)  # Default window size

        backGround = pygame.image.load("thesquadfather.png").convert()
        backGroundRect = backGround.get_rect()  # roast: todo: resize to (width, height)

        paddle = pygame.image.load("paddle.png").convert()
        paddleRect = paddle.get_rect()

        ball = pygame.image.load("guwopball.png").convert()
        ball.set_colorkey((255, 255, 255))
        ballRect = ball.get_rect()

        """
        Create a list with different sounds bits and randomly choose them
            - need to figure out what sound bits
        burr = pygame.mixer.Sound(["Gucci-Burr.wav", "", ""])
        """
        burr = pygame.mixer.Sound("Gucci-Burr.wav")
        burr.set_volume(6)

        wall = TrumpWall()
        wall.buildWall(width)

        # Set ready for game loop
        paddleRect = paddleRect.move((width // 2) - (paddleRect.right // 2), height - 20)
        ballRect = ballRect.move(width // 2, height // 2)
        xSpeed = xSpeed_init
        ySpeed = ySpeed_init
        lives = maxLives
        clock = pygame.time.Clock()
        pygame.key.set_repeat(1,30)

        pause = False
        resume = False

        while True:
            
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
                        if paddleRect.left < 0:                          
                            paddleRect.left = 0 
                    if event.key == pygame.K_RIGHT:                    
                        paddleRect = paddleRect.move(paddleSpeed, 0)
                        if paddleRect.right > width:  # >= mb bruh? brug here?                         
                            paddleRect.right = width  
                    if event.key == pygame.K_p:
                        pause = True
                    if event.key == pygame.K_r:
                        resume = True
                    if event.key == pygame.K_F11:
                        screen = pygame.display.set_mode(size, pygame.RESIZABLE)
                    if event.key == pygame.K_F12:
                        screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
                                      
            # Check whether paddle has hit ball    
            if ballRect.bottom >= paddleRect.top and \
               ballRect.bottom <= paddleRect.bottom and \
               ballRect.right >= paddleRect.left and \
               ballRect.left <= paddleRect.right:
            #if ballRect.colliderect(paddleRect):
 
                ySpeed = -ySpeed                
                burr.play(0)                
                offSet = ballRect.center[0] - paddleRect.center[0]

                # offSet > 0 means ball has hit the right side of the paddle                  
                # the angle of ball varies depending on where ball hits paddle             
                sign = 1 if offSet > 0 else -1
 
                offSet = abs(offSet)
                if offSet > 30:  
                    xSpeed = 7
                elif offSet > 23:                
                    xSpeed = 6
                elif offSet > 17:
                    xSpeed = 5
                xSpeed = sign * xSpeed
                    
            # Move paddle/ball
            ballRect = ballRect.move(xSpeed, ySpeed)
 
            # roast: do you need these or the similar checks below?
            if ballRect.left < 0 or ballRect.right > width:
                xSpeed = -xSpeed
                #random.choice(burr).play(0)                
                burr.play(0) 
            if ballRect.top < 0:
                ySpeed = -ySpeed      
                burr.play(0)                            
            # Check if ball has gone past the paddle - lose a life
            if ballRect.top > height:
                lives -= 1
               
                # Start a new ball
                xSpeed = xSpeed_init
                ySpeed = ySpeed_init            
               
                if random.random() > 0.5:
                    xSpeed = -xSpeed
               
                ballRect.center = int(width * random.random()), height // 3 

                if lives <= 0: 
                    message = pygame.font.Font(None,70).render("Game Over, Pimp", True, (27, 255, 0), bgColor)
                    msgRect = message.get_rect()
                    msgRect = msgRect.move(width // 2 - (msgRect.center[0]), height // 3)
                    screen.blit(message, msgRect)
                    pygame.display.flip()
                    """
                        Trigger user key presses
                            - ESC to quit the game
                            - Use any other key to restart the game
                            - p to pause
                            - r to resume
                            - F11 to resize back to min
                            - F12 for fullscreen 
                    """
                    while True:                        
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
                            screen.fill(bgColor)
                            wall.buildWall(width)
                            lives = maxLives
                            score = 0
                            break  

            if xSpeed < 0 and ballRect.left < 0:
                xSpeed = -xSpeed                                
                burr.play(0) 
            if xSpeed > 0 and ballRect.right > width:
                xSpeed = -xSpeed                              
                burr.play(0)
           
            # Check if ball makes contact with wall
            # If yes then remove a brick and change the direction of the ball
            index = ballRect.collidelist(wall.brickRect)      
            if index != -1:               
                if ballRect.center[0] > wall.brickRect[index].right or \
                   ballRect.center[0] < wall.brickRect[index].left:
                   xSpeed = -xSpeed
                else:
                    ySpeed = -ySpeed                
 
                burr.play(0)              
                wall.brickRect[index:index + 1] = []
                score += 1017

            # Displays lives/score             
            #screen.fill(bgColor)
            screen.blit(backGround, backGroundRect)
            scoreText = pygame.font.Font(None,30).render("Score: " + str(score), True, (27, 255, 0), bgColor)  # roast, don't use bgcolor when drawing text if you want the text on the picture
            scoretextRect = scoreText.get_rect()
            scoretextRect = scoretextRect.move(width - scoretextRect.right, 0)

            livesText = pygame.font.Font(None, 30).render("Lives: " + str(lives), True, (27, 255, 0), bgColor)
            livestextRect = livesText.get_rect()

            screen.blit(livesText, livestextRect)
            screen.blit(scoreText, scoretextRect)

            for i in range(0, len(wall.brickRect)):
                screen.blit(wall.brick, wall.brickRect[i])    
                        
            # If bricks are gone then rebuild wall
            if not wall.brickRect:
                # Displays message to user letting them know they won
                winMsg = pygame.font.Font(None,50).render("You Win! Have a SO ICY DAY! BURRR", True, (27, 255, 0), bgColor)
                msgRect = winMsg.get_rect()
                msgRect = msgRect.move(width // 2 - (msgRect.center[0]), height // 3)
                screen.blit(winMsg, msgRect)
                pygame.display.flip()
                # roast: instead of sleeping, maybe have a smaller do-nothing game loop, that way it won't come back to life until the player actually presses R
                time.sleep(3)  # roast: maybe ACTUALLY pause. this was devastating

                # roast: 
                # Reset lives, score and background color
                screen.fill(bgColor)
                lives = maxLives
                score = 0
                
                # Rebuild wall
                wall.buildWall(width)
                xSpeed = xSpeed_init
                ySpeed = ySpeed_init
                ballRect.center = width // 2, height // 2 
            
            # Pretty straight forward... pauses game.
            if pause:
                pauseMsg = pygame.font.Font(None, 35).render("Game Paused! Press R to Resume Game", True, (27, 255,0), bgColor)
                pausemsgRect = pauseMsg.get_rect()
                pausemsgRect = pausemsgRect.move(width // 2 - (pausemsgRect.center[0]), height // 3)
                screen.blit(pauseMsg, pausemsgRect)
                pygame.display.flip()
                time.sleep(1.2)  # love the specificity
            
            if resume:
                pause = False
                screen.blit(ball,ballRect)
                screen.blit(paddle, paddleRect)
                pygame.display.flip()

            # Display game    
            screen.blit(ball, ballRect)
            screen.blit(paddle, paddleRect)
            pygame.display.flip()
            
class TrumpWall(): 
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
 
        for i in range(0, 52):                       
            if xPos > width:
                if adjust == 0:
                    adjust = self.brickLength // 2
                else:
                    adjust = 0
 
                xPos = -adjust
                yPos += self.brickHeight
               
            self.brickRect.append(self.brick.get_rect())    
            self.brickRect[i] = self.brickRect[i].move(xPos, yPos)
            xPos = xPos + self.brickLength 
 
if __name__ == '__main__': 
    br = BrickBreaker()
    br.gucci_main()
