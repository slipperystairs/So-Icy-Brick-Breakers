# So-Icy-Brick-Breakers

A simple brick breaker game written in Python.

### Game Objective
The user has 6 lives and they must destroy all the bricks before they die. To do this the player must hit Gucci Mane's face with a paddle to destroy the bricks.

### Setup

Install pygame. For example, if you use `pip`, then run

```
pip install pygame
```

### Running

```
python3 brickbreaker.py
```

### Controls

RTFC:

```python
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
                                      
```
