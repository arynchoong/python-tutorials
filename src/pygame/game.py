import pygame

# Dimensions
WIDTH = 640
HEIGHT = 480
#            R    G    B
BLACK   = (  0,   0,   0)
GREEN   = (  3, 192,  60)

class Game():
    def __init__(self):
        pygame.init() # initialise pygame libraries
        self.size = WIDTH, HEIGHT
        self.display = pygame.display.set_mode(self.size)
        self.disp_surf = self.init_display()
        self.running = True if self.disp_surf else False
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
            self.render()
        return

    def render(self):
        '''Render surface'''
        # background
        self.disp_surf.fill(BLACK)
        # draw text
        text = 'PyGame Basics'
        self.draw_text(text, GREEN, (int(WIDTH / 2), int(HEIGHT / 2)))
        # Blit everything to screen
        self.display.blit(self.disp_surf, (0,0))

        # draw ball
        self.ballrect = self.ballrect.move(self.speed)
        if self.ballrect.left < 0 or self.ballrect.right > WIDTH:
            self.speed[0] = -self.speed[0]
        if self.ballrect.top < 0 or self.ballrect.bottom > HEIGHT:
            self.speed[1] = -self.speed[1]        
        self.display.blit(self.ball, self.ballrect)

        # update display
        pygame.display.flip()
        return

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return
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