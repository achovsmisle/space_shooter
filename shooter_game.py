#Создай собственный Шутер!
# Подключение библиотек
from pygame import *
from random import randint
from time import sleep

win_width = 700
win_heigh = 500
lost = 0
score = 0
bullet_speed = 10
font.init()

mixer.init()
mixer.music.load('space.ogg')
#mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')
window = display.set_mode((700, 500))
display.set_caption('Шутер')
background = transform.scale(image.load('galaxy.jpg'), (win_width, win_heigh))
run = True


clock = time.Clock ()
FPS = 60

# Основной класс спрайтов
class GameSprite(sprite.Sprite):
    def __init__ (self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

# Класс спрайта игрока
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys [K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys [K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        if keys [K_SPACE]:
            fire_sound.play()
            self.fire()
    
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, 15) 
        bullets.add(bullet)
 
 
class Enemy(GameSprite): 
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 500:
            lost += 1
            self.rect.y = 0
            self.rect.x = randint(80, 650)

# Класс пуль
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= bullet_speed
        if self.rect.y == 0:
            self.kill()


font1 = font.SysFont('Arial', 40)
font2 = font.SysFont('Arial', 40)
asteroids = sprite.Group()
small_asteroids = sprite.Group()
#   Создание астероидов
for i in range(2):
    x_aster = randint(50, 550)
    asteroid = Enemy('asteroid.png', x_aster, 0, 80, 80, 1)
    asteroids.add(asteroid)

# Создание группы спрайтов пуль
bullets = sprite.Group()

# Создание спрайта игрока
player = Player('rocket.png', 350, 425, 65, 65, 10)

# Создание монстров
# Создаем группу монстров
monsters = sprite.Group()
# В цикле добавляем спрайт монстра в группу монстров
for i in range(5):
    x = randint(50, 650)
    y = 0
    monster = Enemy ('ufo.png', x, y, 65, 65, 3) 
    monsters.add(monster)


# Игровой цикл
while run:
    text_kill = font1.render('Счет: ' + str(score), 1, (255, 255, 255))
    text_lose = font1.render('Пропущено: ' + str(lost), 1, (255, 255, 255))
    for e in event.get():
        if e.type == QUIT:
            run = False
    # Отображение 
    window.blit(background, (0, 0))
    window.blit(text_lose, (1, 50))
    window.blit(text_kill, (1, 20))
    player.reset()
    bullets.update()
    bullets.draw(window)
    player.update()
    monsters.update()
    asteroids.update()
    asteroids.draw(window)
    small_asteroids.update()
    small_asteroids.draw(window)
    monsters.draw(window)

    
    collide_asteroids = sprite.groupcollide(asteroids, bullets, True, True)
    collide_small_asteroids = sprite.groupcollide(small_asteroids, bullets, True, True)
    collides = sprite.groupcollide(monsters, bullets, True, True)
    # Победа
    if score >= 999:
        text_win = font2.render('Ты победил!', 1, (3, 255, 11))  
        window.blit(text_win, (275, 250 ))
        run = False
        sleep(3)
    
    # Проигрыш
    if lost >= 3000:
        text_sus = font2.render('Ты проиграл!', 1, (255, 0, 0))
        window.blit(text_sus, (275, 250))
        run = False
        sleep(3)
    
    # Проверка столкновения монстров и игрока
    if sprite.spritecollide(player, monsters, False):
        text_sus = font2.render('Ты проиграл!', 1, (255, 0, 0))
        window.blit(text_sus, (275, 250))
        run = False
        sleep(3)
    
    # Проверка столкновения астероидов с пулями
    
    for i in collide_asteroids:
        print(i.rect.x)
        x_small = i.rect.x
        y_small = i.rect.y
        x = randint (50, 650)
        y = randint (-200, 1)
        small_asteroid = Enemy('asteroid.png', x_small+20, y_small+25, 40, 40, 1)
        small_asteroids.add(small_asteroid)
        small_asteroid = Enemy('asteroid.png', x_small, y_small-15, 40, 40, 1)
        small_asteroids.add(small_asteroid)
        small_asteroid = Enemy('asteroid.png', x_small-20, y_small, 40, 40, 1)
        small_asteroids.add(small_asteroid)
        asteroid = Enemy('asteroid.png', x, y, 80, 80, 1)
        asteroids.add(asteroid)
    
    # Проверка столкновения монстров с пулями
    for i in collides:
        x = randint (50, 650)
        y = 0
        score += 1
        monster = Enemy ('ufo.png', x, y, 65, 65, 3)
        monsters.add(monster)

    # Обновление экрана
    display.update()
    clock.tick(FPS)