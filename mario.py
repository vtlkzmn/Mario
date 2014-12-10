import pygame
import tmx
import sys
import time


def play_sound(filename, repeats = 0):
    sound = pygame.mixer.Sound('sounds\\' +filename)
    sound.play()
    
def load_img(image):
    image = pygame.image.load('images\\' + image)
    return image

def display_text(screen, text, x, y, size):
    text = str(text)
    font = pygame.font.SysFont('monospace', size)
    text = font.render(text, True, (255, 255, 255))
    screen.blit(text, (x,y))

    

mario_imgsR = []
mario_imgsL = []
mario_imgs = []
    
mario_imgsR.append(load_img('running1.png'))
mario_imgsR.append(load_img('running2.png'))
mario_imgsR.append(load_img('running3.png'))
mario_imgsR.append(load_img('running2.png'))
mario_imgsR.append(load_img('brake.png'))
mario_imgsR.append(load_img('jump.png'))
mario_imgsR.append(load_img('dead.png'))
mario_imgsR.append(load_img('standing.png'))
mario_imgsR.append(load_img('poleslide1.png'))
mario_imgsR.append(load_img('poleslide2.png'))

# [0] running1
# [1] running2
# [2] running3
# [3] running2
# [4] brake
# [5] jump
# [6] dead
# [7] standing
# [8] poleslide1
# [9] poleslide2

for image in mario_imgsR:
    new_img = pygame.transform.flip(image, True, False)
    mario_imgsL.append(new_img)

mario_imgs = [mario_imgsR, mario_imgsL]



enemy_imgs = []

enemy_imgs.append(load_img('enemy1.png'))
enemy_imgs.append(load_img('enemy2.png'))
enemy_imgs.append(load_img('dead_enemy.png'))



blocks = []
blocks.append(load_img('coinblock1.png'))
blocks.append(load_img('coinblock2.png'))
blocks.append(load_img('coinblock3.png'))
blocks.append(load_img('coinblock4.png'))
blocks.append(load_img('coinblock5.png'))


bricks = []

bricks.append(load_img('brickblock1.png'))



coins = []

coins.append(load_img('coin3.png'))
new_img = pygame.transform.flip(load_img('coin3.png'), True, False)
coins.append(new_img)
new_img = pygame.transform.flip(load_img('coin2.png'), True, False)
coins.append(new_img)
coins.append(load_img('coin.png'))
coins.append(load_img('coin4.png'))
new_img = pygame.transform.flip(load_img('coin.png'), True, False)
coins.append(new_img)
coins.append(load_img('coin2.png'))



score = 0
player_dead = False
game_won = False



class Player(pygame.sprite.Sprite):
    def __init__(self, location, *groups):
        super(Player, self).__init__(*groups)
        
        self.ani_timer = 2
        self.frame = 7
        self.facing_right = False
        self.jump = False
        self.vel_x = 0
        
        self.image = mario_imgs[0][6]
        self.rect = pygame.rect.Rect(location, self.image.get_size())
        self.resting = False
        self.dy = 0

        self.dead = False
        self.dead2 = False
        self.dead3 = True
        
        self.won = False
        self.end_ani = True
        self.end_ani2 = True
        self.score = 0
   

    def update(self, dt, game):
        global player_dead
        global game_won
        game_won = self.won
        player_dead = self.dead
        last = self.rect.copy()
        self.ani_timer -= 1
        
        
        if not self.won:
                
            key = pygame.key.get_pressed()
            
            leftkey = key[pygame.K_LEFT]
            rightkey = key[pygame.K_RIGHT]
            jumpkey = key[pygame.K_SPACE]

            if leftkey : # running left
                
                self.facing_right = False

                if self.ani_timer == 0:
                    self.frame += 1
                if self.frame > 3:
                    self.frame = 0

                if self.vel_x > -1:
                    self.vel_x -= 0.05
                     
            if rightkey : #running right
                
                self.facing_right = True

                if self.ani_timer == 0:
                    self.frame += 1
                if self.frame > 3:
                    self.frame = 0
                if self.vel_x < 1:
                    self.vel_x += 0.05

            if not rightkey and not leftkey and self.vel_x != 0: 
                if self.vel_x > 0:
                    self.vel_x -= 0.05
                    if self.vel_x < 0.05:
                        self.vel_x = 0
                if self.vel_x < 0:
                    self.vel_x += 0.05
                    if self.vel_x > 0.05:
                        self.vel_x = 0
                if abs(self.vel_x) > 0.5:
                    self.frame = 4
                else:
                    self.frame = 7


            if self.vel_x == 0:
                self.frame = 7
            
            if self.resting and jumpkey:
                
                play_sound('small_jump.ogg')
                self.dy = -340
                self.jump = True


            if self.jump:
                self.frame = 5
                    

            self.rect.x += 120 * dt * self.vel_x

            if self.rect.x >= 3008: # final jump
                self.rect.x += 110 *dt * self.vel_x
            
            self.dy = min(300, self.dy + 30)

            self.rect.y += self.dy * dt

            
            new = self.rect

            self.resting = False
            for cell in game.tilemap.layers['triggers'].collide(new, 'blockers'):
                if last.right <= cell.left and new.right > cell.left:
                    new.right = cell.left
                if last.left >= cell.right and new.left < cell.right:
                    new.left = cell.right
                if last.bottom <= cell.top and new.bottom > cell.top:
                    self.resting = True
                    self.jump = False
                    new.bottom = cell.top
                    self.dy = 0
                if last.top >= cell.bottom and new.top < cell.bottom:
                    new.top = cell.bottom
                    self.dy = 0

            if self.rect.x >= 3160:
                self.rect.x = 3160
                self.won = True
            if self.rect.y > 300:
                self.dead = True


        if self.won:
            self.frame = 8
            if not self.end_ani and self.end_ani2:
                pygame.mixer.stop()
                play_sound('stage_clear.wav')
                self.end_ani2 = False
                time.sleep(2)
                
            
            global score

            if self.rect.y < 168:
                score += 5
                self.rect.y += 2
            if self.rect.y >= 168 and self.rect.y <= 180:
                self.frame = 5
                self.rect.y += 4
                
                
            if self.rect.y >= 180:
                self.rect.y = 184
                self.frame = 7

            self.end_ani = False



        if self.dead:
            self.frame = 6

            if self.dead2 and self.dead3:
                pygame.mixer.stop()
                play_sound('death.wav')
                time.sleep(3)
                self.dead3 = False
                self.kill()
            if self.rect.y < 300 and self.dead2:
                self.rect.y -= 1

            self.dead2 = True

            
        if self.facing_right:
            lor = 0
        if not self.facing_right:
            lor = 1

        if self.ani_timer == 0:
            self.ani_timer = 2
        
        self.image = mario_imgs[lor][self.frame]
    
        game.tilemap.set_focus(self.rect.x, self.rect.y)

                

class Enemy(pygame.sprite.Sprite):
    def __init__(self, location, *groups):
        self.image = enemy_imgs[0]
        self.ani_timer = 3
        self.death_clock = 20
        self.dead = False
        super(Enemy, self).__init__(*groups)
        self.rect = pygame.rect.Rect(location, (16,16))
        self.direction = 1
        self.dy = 0
        self.frame = 0

    def update(self, dt, game):
        
        last = self.rect.copy()
        
        self.ani_timer -= 1

        if self.frame != 2:
            if self.ani_timer == 0:
                self.frame += 1
            if self.frame > 1:
                self.frame = 0
        else:
            self.death_clock -= 1
            
            if self.death_clock == 0:
                self.kill()
                self.death_clock = 20

        if self.ani_timer == 0:
            self.ani_timer = 3

        self.image = enemy_imgs[self.frame]

        if self.frame != 2:
            self.rect.x += self.direction * 45 * dt
        
        self.dy = min(400, self.dy + 30)

        self.rect.y += self.dy * dt 

        new = self.rect

        for cell in game.tilemap.layers['triggers'].collide(new, 'blockers'): 
            if last.right <= cell.left and new.right > cell.left:
                new.right = cell.left
                self.direction *= -1
            if last.left >= cell.right and new.left < cell.right:
                new.left = cell.right
                self.direction *= -1
            if last.bottom <= cell.top and new.bottom > cell.top:
                new.bottom = cell.top
                self.dy = 0
            if last.top >= cell.bottom and new.top < cell.bottom:
                new.top = cell.bottom
                self.dy = 0

        for cell in game.tilemap.layers['triggers'].collide(new, 'reverse'):
            if last.right <= cell.left and new.right > cell.left:
                new.right = cell.left
                self.direction *= -1
            if last.left >= cell.right and new.left < cell.right:
                new.left = cell.right
                self.direction *= -1
     
        if self.rect.colliderect(game.player.rect):
            if self.rect.y <= game.player.rect.y:
                game.player.dead = True
            elif self.rect.y > game.player.rect.y:
                self.frame = 2
                play_sound('bump.ogg')
                game.player.dy -= 200
                

            if self.rect.right < game.player.rect.left:
                game.player.rect.midleft = self.rect.midright
            if self.rect.left > game.player.rect.right:
                game.player.rect.right = self.rect.left 
            

class Coinblock(pygame.sprite.Sprite):
    def __init__(self, location, *groups):
        self.image = blocks[0]
        self.ani_timer = 2
        super(Coinblock, self).__init__(*groups)
        self.rect = pygame.rect.Rect(location, (16,16))
        self.rect_x = self.rect.x # original location
        self.rect_y = self.rect.y
        self.frame = 0
        self.dy = 0
        self.bump_timer = 3
        self.bump_dir = 1
        self.bump_ani = False
        self.is_coin = True

    def update(self, dt, game):
        self.ani_timer -= 1

        if self.rect.colliderect(game.player.rect):
            self.bump_ani = True
            game.player.dy = 0

        if self.bump_ani:
            self.dy = 3 * self.bump_dir
            self.bump_timer -= 1
            if self.bump_timer == 0 and self.bump_dir == -1:
                self.bump_timer = 2
                self.bump_dir = 1
                self.dy = 0
                self.bump_ani = False
                self.rect.x = self.rect_x
                self.rect.y = self.rect_y
            elif self.bump_timer == 0:
                self.bump_dir = -1
                self.bump_timer = 3

            if self.is_coin :
                Coin(self.rect.topleft, 1, game.sprites)
                self.is_coin = False
                
        if self.ani_timer == 0:
            self.frame += 1
        if self.frame == 4:
            self.frame = 0
        if self.ani_timer == 0:
            self.ani_timer = 2

        if not self.is_coin:
            self.frame = 4
            
        self.image = blocks[self.frame]
        self.rect.y -= self.dy

        if not self.bump_ani:
            self.dy = 0

class Coin(pygame.sprite.Sprite):
    
    def __init__(self, location, direction, *groups):
        super(Coin, self).__init__(*groups)
        self.image = load_img('coin.png')
        self.rect = pygame.rect.Rect(location, self.image.get_size())
        self.lifespan = 14
        self.ani_timer = 2
        self.ani_len = len(coins)
        self.frame = 0
        play_sound('coin.ogg')
        global score
        score += 50

    def update(self, dt, game):
        self.lifespan -= 1
        self.ani_timer -= 1

        if self.ani_timer == 0:
            self.frame += 1
            self.ani_timer = 2

        if self.frame == self.ani_len:
            self.frame = 0
            
        if self.lifespan < 0:
            self.kill()
        self.rect.y -= 100 * dt

        self.image = coins[self.frame]


class Brickblock(pygame.sprite.Sprite):
    def __init__(self, location, *groups):
        self.image = bricks[0]
        super(Brickblock, self).__init__(*groups)
        self.rect = pygame.rect.Rect(location, self.image.get_size())
        self.rect_x = self.rect.x # original location
        self.rect_y = self.rect.y
        self.dy = 0
        
        self.bump_timer = 3
        self.bump_dir = 1
        self.bump_ani = False

    def update(self, dt, game):

        if self.rect.colliderect(game.player.rect):
            self.bump_ani = True
            play_sound('bump.ogg')
            game.player.dy = 0

        if self.bump_ani:
            self.dy = 2 * self.bump_dir
            self.bump_timer -= 1
            if self.bump_timer == 0 and self.bump_dir == -1:
                self.bump_timer = 2
                self.bump_dir = 1
                self.dy = 0
                self.bump_ani = False
                self.rect.x = self.rect_x
                self.rect.y = self.rect_y
            elif self.bump_timer == 0:
                self.bump_dir = -1
                self.bump_timer = 3
            
                
        self.rect.y -= self.dy

        if not self.bump_ani:
            self.dy = 0

class Game(object):
    def main(self, screen):
        clock = pygame.time.Clock()
        
        pygame.mixer.init()

        self.tilemap = tmx.load('map.tmx', screen.get_size())
        
        self.sprites = tmx.SpriteLayer()
        start_cell = self.tilemap.layers['triggers'].find('player')[0]
        self.player = Player((start_cell.px, start_cell.py), self.sprites)
        self.tilemap.layers.append(self.sprites)

        self.enemies = tmx.SpriteLayer()
        for enemy in self.tilemap.layers['triggers'].find('enemy'):
            Enemy((enemy.px, enemy.py), self.enemies)
        self.tilemap.layers.append(self.enemies)

        self.coinblox = tmx.SpriteLayer()
        for block in self.tilemap.layers['triggers'].find('coinblock'):
            Coinblock((block.px, block.py), self.coinblox)
        self.tilemap.layers.append(self.coinblox)

        self.bricks = tmx.SpriteLayer()
        for block in self.tilemap.layers['triggers'].find('brickblock'):
            Brickblock((block.px, block.py), self.bricks)
        self.tilemap.layers.append(self.bricks)

        play_sound('main_theme.ogg')

        global score

        while True:
            dt = clock.tick(30)
            global player_dead
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            self.tilemap.update(dt / 1000., self)
            self.tilemap.draw(screen)
            display_text(screen, score , 0, 0, 15)
            if player_dead:
                display_text(screen, 'Game over.  Press esc to quit.',0, 40, 17)

            if game_won:
                display_text(screen, 'You win. Press esc to quit.', 0, 40, 17)
            pygame.display.flip()
            
if __name__ == '__main__':
    pygame.init()
    pygame.mouse.set_visible(False)
    screen = pygame.display.set_mode((300, 224), pygame.FULLSCREEN)
    Game().main(screen)

