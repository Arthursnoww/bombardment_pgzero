import pgzrun
import random
from pgzero.rect import Rect

# --- CONFIGURAÇÃO DA JANELA ---
TITLE = "BOMBARDMENT"
TILE_SIZE = 16  
MAP_COLS = 25   
MAP_ROWS = 15   
WIDTH = MAP_COLS * TILE_SIZE 
HEIGHT = MAP_ROWS * TILE_SIZE

# Estados do Jogo
MENU, PLAYING, GAME_OVER, WIN = 0, 1, 2, 3
state = MENU
lives = 3
music_active = True
selected_index = 0
menu_options = ["Começar Jogo", "Som: LIGADO", "Sair"]

# Mapa Base
ORIGINAL_MAP = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

walls, blocks, enemies, bombs, explosions = [], [], [], [], []
exit_actor, player = None, None

def update_music():
    music.stop()
    if not music_active: return
    if state == MENU: music.play('jogo')
    elif state == PLAYING: music.play('jogo2')

def init_game():
    global lives, walls, blocks, enemies, bombs, explosions, player, exit_actor
    lives = 3
    walls, blocks, enemies, bombs, explosions = [], [], [], [], []
    empty_spots = []
    
    for r, row in enumerate(ORIGINAL_MAP):
        for c, cell in enumerate(row):
            x, y = int(c * TILE_SIZE), int(r * TILE_SIZE)
            if cell == 1:
                walls.append(Actor("tile_0040", topleft=(x, y)))
            elif cell == 3:
                exit_actor = Actor("tile_0009", topleft=(x, y))
            elif cell == 0:
                if not (c < 3 and r < 3):
                    empty_spots.append((x, y))

    random.shuffle(empty_spots)
    num_blocks = min(140, len(empty_spots))
    for _ in range(num_blocks):
        pos = empty_spots.pop()
        blocks.append(Actor("tile_0023", topleft=pos))
    
    num_enemies = min(8, len(empty_spots))
    for _ in range(num_enemies):
        pos = empty_spots.pop()
        ex, ey = pos[0] + TILE_SIZE//2, pos[1] + TILE_SIZE//2
        enemies.append(Enemy(ex, ey, random.choice(["e1", "e2"])))
    
    player = Hero(TILE_SIZE + TILE_SIZE//2, TILE_SIZE + TILE_SIZE//2)
    update_music()

# --- CLASSES ---

class AnimatedEntity:
    def __init__(self, folder, prefix, x, y, num_frames):
        self.folder, self.prefix, self.num_frames = folder, prefix, num_frames
        self.frame, self.timer, self.direction = 0, 0, "f"
        self.actor = Actor(f"{folder}/{prefix}f0", (x, y))

    def update_animation(self, dt, moving):
        if moving:
            self.timer += dt
            if self.timer > 0.12:
                self.timer = 0; self.frame = (self.frame + 1) % self.num_frames
        else: self.frame = 0
        self.actor.image = f"{self.folder}/{self.prefix}{self.direction}{self.frame}"

class Hero(AnimatedEntity):
    def __init__(self, x, y):
        super().__init__("hero", "p", x, y, 3)
        self.speed = 2
        self.invincible_timer = 0 # Tempo de proteção

    def update(self, dt, obstacles):
        # Diminui o tempo de proteção
        if self.invincible_timer > 0:
            self.invincible_timer -= dt

        dx, dy, moving = 0, 0, False
        if keyboard.left: dx = -self.speed; self.direction = "l"; moving = True
        elif keyboard.right: dx = self.speed; self.direction = "r"; moving = True
        elif keyboard.up: dy = -self.speed; self.direction = "b"; moving = True
        elif keyboard.down: dy = self.speed; self.direction = "f"; moving = True
        
        old_pos = self.actor.pos
        self.actor.x += dx; self.actor.y += dy
        for obs in obstacles:
            if self.actor.colliderect(obs):
                self.actor.pos = old_pos
                moving = False; break
        self.update_animation(dt, moving)

class Enemy(AnimatedEntity):
    def __init__(self, x, y, type_p):
        super().__init__("enemy", type_p, x, y, 3)
        self.speed = 1; self.choice = random.choice(["f", "b", "l", "r"]); self.move_timer = 0

    def update(self, dt, obstacles):
        self.move_timer += dt
        if self.move_timer > 1.2:
            self.choice = random.choice(["f", "b", "l", "r"]); self.direction = self.choice; self.move_timer = 0
        old_pos = self.actor.pos
        if self.choice == "f": self.actor.y += self.speed
        elif self.choice == "b": self.actor.y -= self.speed
        elif self.choice == "l": self.actor.x -= self.speed
        elif self.choice == "r": self.actor.x += self.speed
        for obs in obstacles:
            if self.actor.colliderect(obs):
                self.actor.pos = old_pos
                self.choice = random.choice(["f", "b", "l", "r"]); break
        self.update_animation(dt, True)

class Bomb:
    def __init__(self, x, y):
        self.actor = Actor("bomb/1", topleft=(x, y))
        self.timer, self.frame, self.anim_timer = 2.0, 1, 0

    def update(self, dt):
        self.timer -= dt; self.anim_timer += dt
        if self.anim_timer > 0.2:
            self.anim_timer = 0
            self.frame = 1 if self.frame == 3 else self.frame + 1
            self.actor.image = f"bomb/{self.frame}"

class Explosion:
    def __init__(self, x, y):
        self.actor = Actor("explosion/1", topleft=(x, y))
        self.timer, self.frame, self.anim_timer = 0.5, 1, 0

    def update(self, dt):
        self.timer -= dt; self.anim_timer += dt
        if self.anim_timer > 0.1 and self.frame < 3:
            self.anim_timer = 0; self.frame += 1
            self.actor.image = f"explosion/{self.frame}"

def handle_explosion(b):
    global lives, state
    tx, ty = int(b.actor.left), int(b.actor.top)
    positions = [(0,0), (TILE_SIZE,0), (-TILE_SIZE,0), (0,TILE_SIZE), (0,-TILE_SIZE)]
    
    hit_this_bomb = False # Para não perder 2 vidas na mesma bomba
    for dx, dy in positions:
        ex, ey = tx + dx, ty + dy
        e_rect = Rect(ex, ey, TILE_SIZE, TILE_SIZE)
        
        hit_wall = False
        for w in walls:
            if w.colliderect(e_rect): hit_wall = True; break
        if hit_wall: continue
        
        explosions.append(Explosion(ex, ey))
        
        # Só perde vida se não estiver invencível
        if not hit_this_bomb and player.invincible_timer <= 0:
            if player.actor.colliderect(e_rect):
                lives -= 1
                player.invincible_timer = 2.0 # 2 segundos de proteção
                player.actor.pos = (TILE_SIZE + TILE_SIZE//2, TILE_SIZE + TILE_SIZE//2)
                hit_this_bomb = True
                if lives <= 0: 
                    state = GAME_OVER
                    music.stop()
                    sounds.game_over.play()

        for en in enemies[:]:
            if en.actor.colliderect(e_rect): enemies.remove(en)
        for blk in blocks[:]:
            if blk.colliderect(e_rect): blocks.remove(blk)

# --- LOOPS PRINCIPAIS ---

def update(dt):
    global state, lives
    if state == PLAYING:
        obs_total = walls + blocks + [b.actor for b in bombs]
        player.update(dt, walls + blocks)
        
        if player.actor.colliderect(exit_actor): 
            state = WIN
            music.stop()
            sounds.game_win.play()

        # Checa colisão com monstros apenas se NÃO estiver invencível
        if player.invincible_timer <= 0:
            for en in enemies[:]:
                en.update(dt, obs_total)
                if player.actor.colliderect(en.actor):
                    lives -= 1
                    player.invincible_timer = 2.0 # Dá 2 segundos de proteção
                    player.actor.pos = (TILE_SIZE + TILE_SIZE//2, TILE_SIZE + TILE_SIZE//2)
                    if lives <= 0: 
                        state = GAME_OVER
                        music.stop()
                        sounds.game_over.play()
                    break # Para de checar outros monstros neste frame
        else:
            # Monstros continuam se movendo mesmo se você estiver protegido
            for en in enemies:
                en.update(dt, obs_total)

        for b in bombs[:]:
            b.update(dt)
            if b.timer <= 0: 
                handle_explosion(b)
                bombs.remove(b)

        for e in explosions[:]:
            e.update(dt)
            if e.timer <= 0: explosions.remove(e)

def draw():
    screen.clear()
    if state == MENU:
        screen.fill((45, 27, 46))
        screen.draw.text("BOMBARDMENT", center=(WIDTH//2, 40), fontsize=30)
        for i, opt in enumerate(menu_options):
            c = "yellow" if i == selected_index else "white"
            screen.draw.text(opt, center=(WIDTH//2, 100 + i * 30), fontsize=20, color=c)
    
    elif state == PLAYING:
        for r in range(MAP_ROWS):
            for c in range(MAP_COLS):
                screen.blit("tile_0000", (c * TILE_SIZE, r * TILE_SIZE))
        exit_actor.draw()
        for w in walls: w.draw()
        for blk in blocks: blk.draw()
        for b in bombs: b.actor.draw()
        for e in explosions: e.actor.draw()
        
        # Efeito de piscar quando está invencível
        if player.invincible_timer <= 0 or int(player.invincible_timer * 10) % 2 == 0:
            player.actor.draw()
            
        for en in enemies: en.actor.draw()
        screen.draw.text(f"VIDAS: {lives}", (10, 5), fontsize=20)
    
    elif state == WIN:
        screen.fill((34, 139, 34)) 
        screen.draw.text("VITÓRIA!", center=(WIDTH//2, HEIGHT//2 - 10), fontsize=40, color="white")
        screen.draw.text("Pressione R para o Menu", center=(WIDTH//2, HEIGHT//2 + 20), fontsize=20)

    elif state == GAME_OVER:
        screen.fill((20, 0, 0))
        screen.draw.text("GAME OVER", center=(WIDTH//2, HEIGHT//2 - 10), fontsize=40, color="red")
        screen.draw.text("Pressione R para o Menu", center=(WIDTH//2, HEIGHT//2 + 20), fontsize=20)

def on_key_down(key):
    global state, selected_index, music_active
    if state in [GAME_OVER, WIN] and key == keys.R:
        state = MENU; update_music()
    elif state == MENU:
        if key == keys.UP: selected_index = (selected_index - 1) % 3
        elif key == keys.DOWN: selected_index = (selected_index + 1) % 3
        elif key == keys.RETURN:
            if selected_index == 0: state = PLAYING; init_game()
            elif selected_index == 1:
                music_active = not music_active
                menu_options[1] = f"Som: {'LIGADO' if music_active else 'DESLIGADO'}"
                update_music()
            elif selected_index == 2: exit()
    elif state == PLAYING and key == keys.SPACE:
        bx = (int(player.actor.x) // TILE_SIZE) * TILE_SIZE
        by = (int(player.actor.y) // TILE_SIZE) * TILE_SIZE
        if not any(b.actor.topleft == (bx, by) for b in bombs):
            bombs.append(Bomb(bx, by))

update_music()
pgzrun.go()