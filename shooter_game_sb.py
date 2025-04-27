#Создай собственный Шутер!
from pygame import *
window = display.set_mode((700,500))
display.set_caption('Шутер')
background = transform.scale(image.load('galaxy.jpg'), (700,500))
game =True
clock = time.Clock()
FPS = 60
'''mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()'''
class GameSprite(sprite.Sprite):
    def __init__ (self,player_image, player_x,player_y, player_speed, w, h):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (w,h))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -=  self.speed
        if keys[K_RIGHT] and self.rect.x < 700-80:
            self.rect.x +=  self.speed
        if keys[K_SPACE]:
            self.fire()
    #метод "выстрел" (используем место игрока, чтобы создать там пулю)
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, -15, 20, 15)
        bullets.add(bullet)
img_bullet = 'bullet.png'
img_hero = 'rocket.png'
player = Player(img_hero, 200, 400, 80, 100, 100)
finish = False
from random import *
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 700:
            self.rect.x = randint(80, 420)
            self.rect.y = 0
            lost += 1  

class Bullet(GameSprite):
    #движение врага
    def update(self):
        self.rect.y += self.speed
        #исчезает, если дойдет до края экрана
        if self.rect.y < 0:
            self.kill()
bullets = sprite.Group()


img_enemy = 'ufo.png'
monsters = sprite.Group()
for i in range (1, 10):
    monster = Enemy(img_enemy, randint(80, 420), -40, randint(1,2), 80, 80)
    monsters.add(monster)
font.init()
font2 = font.SysFont('Arial', 40)
lost = 0
score = 0

goal = 100
max_lost = 5
font1 = font.SysFont('Arial', 80)
win = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))
while game:
    for e in event.get(): 
        if e.type == QUIT:
            game = False
    if not finish: 
        window.blit(background,(0,0))
        player.update()
        player.reset()
        monsters.update()
        monsters.draw(window)

        bullets.update()
        bullets.draw(window)
        
        text = font2.render('Счёт:' + str(score), 1, (255,255,255))
        window.blit(text, (10, 20))
        text_lose = font2.render('Пропущено:' + str(lost), 1, (255,255,255))
        window.blit(text_lose, (10, 50))

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            #этот цикл повторится столько раз, сколько монстров подбито
            score = score + 1
            monster = Enemy(img_enemy, randint(80, 420), -40, randint(1, 2), 80, 80)m
            monsters.add(monster)
        #возможный проигрыш: пропустили слишком много или герой столкнулся с врагом
        if lost >= max_lost or sprite.spritecollide(player, monsters, False):
            finish = True #проиграли, ставим фон и больше не управляем спрайтами.
            window.blit(lose, (200, 200))
        #проверка выигрыша: сколько очков набрали?
        if score >= goal:
            finish = True
            window.blit(win, (200, 200))
    clock.tick(FPS)
    display.update()