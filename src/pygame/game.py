import pygame

# Dimensions
WIDTH = 640
HEIGHT = 480
# States
START = 1
PLAYING = 2
GAMEOVER = 3
#            R    G    B
BLACK   = (  0,   0,   0)
GREEN   = (  0, 255,   0)

class Game():
    def __init__(self):
        pygame.init() # initialise pygame libraries
        self.size = WIDTH, HEIGHT
        self.display = pygame.display.set_mode(self.size)
        self.disp_surf = self.init_display()
        self.running = True if self.disp_surf else False
        self.state = START
        self.font = pygame.font.Font(pygame.font.get_default_font(), 36)
        self.ball = pygame.image.load("ball.png")
        self.ballrect = self.ball.get_rect()
        self.speed = [2, 2]
    
    def init_display(self):
        pygame.display.set_caption('PyGame Basics Workshop')
        # Create surface
        disp_surf = pygame.Surface(self.size)
        return disp_surf.convert()
    
    def execute(self):
        # Event loop
        while self.running:
            self.check_events()
            if self.state == PLAYING:
                self.render_play()
            else:
                self.render()
        return

    def render(self):
        '''Render surface'''
        self.disp_surf.fill(BLACK)

        # set the text for display
        if self.state == START:
            text = 'PyGame Basics'
            message = 'Press space to play.'
        else:
            text = 'Game Over'
            message = 'State: %s' % self.state
        # draw the messages
        self.draw_text(text, GREEN, (int(WIDTH / 2), int(HEIGHT / 2) - 50))
        self.draw_text(message, GREEN, (int(WIDTH / 2), int(HEIGHT / 2) + 50))
      
        # Blit everything to screen
        self.display.blit(self.disp_surf, (0,0))
        pygame.display.flip()
        return

    def render_play(self):
        '''Render surface'''
        # draw ball
        self.ballrect = self.ballrect.move(self.speed)
        if self.ballrect.left < 0 or self.ballrect.right > WIDTH:
            self.speed[0] = -self.speed[0]
        if self.ballrect.top < 0 or self.ballrect.bottom > HEIGHT:
            self.speed[1] = -self.speed[1]
        
        # fill background and draw ball
        self.display.fill(BLACK)
        self.display.blit(self.ball, self.ballrect)

        # update display
        pygame.display.flip()
        return

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.state = GAMEOVER
                return
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    if self.state == GAMEOVER:
                        self.state = START
                    else:
                        self.state +=1
        return
    
    def draw_text(self, text, colour, center):
        '''Draws text onto diplay surface'''
        text_surf = self.font.render(text, True, colour)
        text_rect = text_surf.get_rect()
        text_rect.center = center
        self.disp_surf.blit(text_surf, text_rect)


if __name__ == "__main__":
    game = Game()
    game.execute()