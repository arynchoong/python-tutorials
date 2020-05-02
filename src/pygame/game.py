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
        self.ball = Ball()
        self.hand = Hand()
        self.allsprites = pygame.sprite.RenderPlain((self.ball, self.hand))
        self.sound_hit = pygame.mixer.Sound("thump.wav")
        self.sound_missed = pygame.mixer.Sound("swish.wav")
        self.score = 0
    
    def init_display(self):
        pygame.display.set_caption('PyGame Basics Workshop')
        pygame.mouse.set_visible(0)
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
        text = "Spin the Ball : %s" % self.score
        self.draw_text(text, GREEN, (int(WIDTH / 2), int(HEIGHT / 2)))
        # Blit everything to screen
        self.display.blit(self.disp_surf, (0,0))

        # draw ball
        self.allsprites.update()
        self.allsprites.draw(self.display)

        # update display
        pygame.display.flip()
        return

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.hand.hit(self.ball):
                    self.ball.hit()
                    self.sound_hit.play()
                    self.score += 1
                    if self.score % 10 == 0:
                        self.ball.level_up()
                else:
                    self.sound_missed.play()
            elif event.type == pygame.MOUSEBUTTONUP:
                self.hand.unhit()
        return
    
    def draw_text(self, text, colour, center):
        '''Draws text onto diplay surface'''
        text_surf = self.font.render(text, True, colour)
        text_rect = text_surf.get_rect()
        text_rect.center = center
        self.disp_surf.blit(text_surf, text_rect)


# classes for our game objects

class Ball(pygame.sprite.Sprite):
    """Bounce a ball around the screen. It can spin when it is hit."""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)  # call Sprite intializer
        self.screen = pygame.display.get_surface()
        self.image = pygame.image.load("ball.png")
        self.rect = self.image.get_rect()
        self.speed = [2, 2]
        self.spin = 0

    def update(self):
        """move or spin, depending on the spin state"""
        if self.spin:
            self._spin()
        else:
            self._move()

    def _move(self):
        """move the ball across the screen, reverse speed at the ends"""
        self.rect = self.rect.move(self.speed)
        if self.rect.left < 0 or self.rect.right > WIDTH:
            self.speed[0] = -self.speed[0]
        if self.rect.top < 0 or self.rect.bottom > HEIGHT:
            self.speed[1] = -self.speed[1]

    def _spin(self):
        """spin the ball image"""
        center = self.rect.center
        self.spin += 60
        if self.spin >= 360:
            self.spin = 0
            self.image = self.original
        else:
            rotate = pygame.transform.rotate
            self.image = rotate(self.original, self.spin)
        self.rect = self.image.get_rect(center=center)

    def hit(self):
        """this will cause the ball to start spinning"""
        if not self.spin:
            self.spin = 60
            self.original = self.image
            # Reverse direction
            self.speed = [-x for x in self.speed]

    def level_up(self):
        self.speed = [2*x for x in self.speed]


class Hand(pygame.sprite.Sprite):
    """moves a hand icon on the screen, following the mouse"""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.image = pygame.image.load("hand.png")
        self.rect = self.image.get_rect()
        self.hitting = 0

    def update(self):
        """move the fist based on the mouse position"""
        pos = pygame.mouse.get_pos()
        self.rect.center = pos
        if self.hitting:
            self.rect.move_ip(5, 10)

    def hit(self, target):
        """returns true if the hand collides with the target"""
        if not self.hitting:
            self.hitting = 1
            hitbox = self.rect.inflate(-5, -5)
            return hitbox.colliderect(target.rect)

    def unhit(self):
        """called to pull the hand back"""
        self.hitting = 0


if __name__ == "__main__":
    game = Game()
    game.execute()