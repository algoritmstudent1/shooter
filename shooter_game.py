from pygame import *
mixer.init()
#переменные для картинок
img_boss = 'isometric.png'
img_bullet = 'bullet.png'
img_enemy = "ufo.png" # враг
img_hero = "rocket.png" #герой
mixer.music.load('space.ogg')
#mixer.music.play()
img_back = "galaxy.jpg" #фон игры
win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))
#класс-родитель для других спрайтов
class GameSprite(sprite.Sprite):
    #конструктор класса
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        #Вызываем конструктор класса (Sprite):
        sprite.Sprite.__init__(self)
        #каждый спрайт должен хранить свойство image - изображение
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        #каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    #метод, отрисовывающий героя на окне
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
#класс главного игрока
class Player(GameSprite):
    #метод для управления спрайтом стрелками клавиатуры
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        if keys[K_SPACE]:
            self.fire()
    #метод "выстрел" (используем место игрока, чтобы создать там пулю)
    def fire(self):
        global reload
        if reload%4 == 0:
            bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
            bullets.add(bullet)



class Enemy(GameSprite):
    #движение врага
    def update(self):
        self.rect.y += self.speed
        global lost
        #исчезает, если дойдет до края экрана
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost +=1

class Bullet(GameSprite):
    #движение врага
    def update(self):
        self.rect.y += self.speed
        #исчезает, если дойдет до края экрана
        if self.rect.y < 0:
            self.kill()
bullets = sprite.Group()


from random import*
monsters = sprite.Group()
for i in range(1, 12):
   monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 3))
   monsters.add(monster)

ship = Player(img_hero, 5, win_height - 100, 80, 100, 15)
run = True
finish = False

font.init()
font2 = font.SysFont('Arial', 36)
lost = 0
score = 0

font1 = font.SysFont('Arial', 80)
win = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))
max_lost = 10
goal = 300

hp_boss = 25
class Boss(GameSprite):
    def update(self):
        global hp_boss
        if score >= 100 and hp_boss > 0:
            self.rect.y +=1
        if hp_boss <= 0:
            self.rect.y -=500

boss = Boss(img_boss, win_width/2 , -250, 250, 270, 2)
reload = 0
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
    if not finish:
        window.blit(background,(0,0))            
        ship.reset()
        ship.update()
        boss.reset()
        boss.update()
        monsters.update()
        monsters.draw(window)
        bullets.update()
        bullets.draw(window)
        text = font2.render("Счет: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))
        text_lose = font2.render("Пропущено: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))
        #проверка столкновения пули и монстров (и монстр, и пуля при касании исчезают)
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            #этот цикл повторится столько раз, сколько монстров подбито
            score = score + 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)
        #возможный проигрыш: пропустили слишком много или герой столкнулся с врагом
        if lost >= max_lost or sprite.spritecollide(ship, monsters, False):
            finish = True #проиграли, ставим фон и больше не управляем спрайтами.
            window.blit(lose, (200, 200))
        #проверка выигрыша: сколько очков набрали?
        if hp_boss <= 0:
            finish = True
            window.blit(win, (200, 200))
        if sprite.spritecollide(boss, bullets, True):
            hp_boss -=1
        reload +=1
    #цикл срабатывает каждые 0.035 секунд
    display.update()
    time.delay(35)












































'''
from pygame import *

#фоновая музыка
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()

#нам нужны такие картинки:
img_back = "galaxy.jpg" #фон игры

#Создаем окошко
win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))



img_hero = "rocket.png" #герой
#класс-родитель для других спрайтов
class GameSprite(sprite.Sprite):
    #конструктор класса
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        #Вызываем конструктор класса (Sprite):
        sprite.Sprite.__init__(self)
        #каждый спрайт должен хранить свойство image - изображение
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        #каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    #метод, отрисовывающий героя на окне
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

#класс главного игрока
class Player(GameSprite):
    #метод для управления спрайтом стрелками клавиатуры
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        if keys[K_SPACE]:
            self.fire()
    #метод "выстрел" (используем место игрока, чтобы создать там пулю)
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)
img_bullet = 'bullet.png'

#создаем спрайты
ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)

img_enemy = "ufo.png" # враг
#класс спрайта-врага  
score = 0
lost = 0
class Enemy(GameSprite):
    #движение врага
    def update(self):
        self.rect.y += self.speed
        global lost
        #исчезает, если дойдет до края экрана
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1

boss_timer = 0
class BigBossEnemy(GameSprite):
    #движение врага
    def update(self):
        global boss_timer
        boss_timer +=1
        if boss_timer >= 50:
            self.rect.x = 200
            self.rect.y += self.speed
            if self.rect.y > win_height:
                self.rect.x = randint(80, win_width - 80)
                self.rect.y = 0
img_boss = 'space-ship.png'
boss = BigBossEnemy(img_boss, -200, -50, 150, 150, 1)

class Bullet(GameSprite):
    #движение врага
    def update(self):
        self.rect.y += self.speed
        #исчезает, если дойдет до края экрана
        if self.rect.y < 0:
            self.kill()
bullets = sprite.Group()

from random import*
monsters = sprite.Group()
for i in range(1, 10):
   monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
   monsters.add(monster)
#переменная "игра закончилась": как только там True, в основном цикле перестают работать спрайты
finish = False
#Основной цикл игры:
run = True #флаг сбрасывается кнопкой закрытия окна
#шрифты и надписи
font.init()
font2 = font.SysFont('Arial', 36)

font1 = font.SysFont('Arial', 80)
win = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))
max_lost = 10
goal = 200
hp_boss = 50
while run:
    #событие нажатия на кнопку Закрыть
    for e in event.get():
        if e.type == QUIT:
            run = False
    if not finish:
        #обновляем фон
        window.blit(background,(0,0))
        text = font2.render("Счет: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))
        text_lose = font2.render("Пропущено: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))
        #производим движения спрайтов
        ship.update()
        monsters.update()
        bullets.update()
        #обновляем их в новом местоположении при каждой итерации цикла
        monsters.draw(window)
        bullets.draw(window)
        #обновляем их в новом местоположении при каждой итерации цикла
        ship.reset()
        if hp_boss >= 0:
            boss.reset()
            boss.update()
        
        #проверка столкновения пули и монстров (и монстр, и пуля при касании исчезают)
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            #этот цикл повторится столько раз, сколько монстров подбито
            score = score + 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)


        #возможный проигрыш: пропустили слишком много или герой столкнулся с врагом
        if lost >= max_lost:
            finish = True #проиграли, ставим фон и больше не управляем спрайтами.
            window.blit(lose, (200, 200))


        #проверка выигрыша: сколько очков набрали?
        if score >= goal:
            finish = True
            window.blit(win, (200, 200))

        if sprite.spritecollide(boss, bullets, True):
            hp_boss -=2
            score +=1
        if hp_boss <= 0:
            boss.kill()
            boss.rect.y = -500

           
            
        display.update()
    #цикл срабатывает каждые 0.035 секунд
    time.delay(35)
'''
