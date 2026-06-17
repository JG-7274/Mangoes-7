# Joshua Gansner
# No date, only a purpose... (June 9, 2026)
# Block D

import random
import time as wait

# neato trick from pyga.me's article on cursors
import pygame as pg

pg.init()
pg.mixer.init

# COLOURS - (R, G, B)
# CONSTANTS ALL HAVE CAPS FOR THEIR NAMES
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GREY = (128, 128, 128)
MANGO_JUICE_YELLOW = (255, 211, 0)
JUICE_PUNCH = (250, 240, 120)
LESS_EYE_SEARING_WHITE = (200, 200, 200)

# CONSTANTS
WIDTH = 1600
HEIGHT = 900
SIZE = (WIDTH, HEIGHT)

# load sounds
atk_sound = pg.mixer.Sound("Assets/half-life-crowbar.mp3")
atk_sound.set_volume(0.2)  # from pygame org's docs
mi_bombo_sound = pg.mixer.Sound("Assets/mi-bombo.mp3")
mi_bombo_sound.set_volume(0.4)
fortnite_sound = pg.mixer.Sound("Assets/fortnite.mp3")
fortnite_sound.set_volume(0.25)
shot_fortnite_sound = pg.mixer.Sound("Assets/pump-shotgun-fortnite-loud.mp3")
shot_fortnite_sound.set_volume(0.17)  # from pygame org's docs

# I made the variable names long on purpose
# I probably don't have to explain these.
start_count_NGBarrels = 10
start_count_mango = 7  # mangoes? 7

death_sounds = [mi_bombo_sound, fortnite_sound, shot_fortnite_sound]


# Load image assets below
menu_bg = pg.image.load("Assets/menu_screen.jpg")
menu_bg = pg.transform.scale(menu_bg, (WIDTH, HEIGHT))

# yandere dev level spaghetti code
wall1 = pg.image.load("Assets/Wall1.png")
wall1 = pg.transform.scale(wall1, (WIDTH, HEIGHT))
wall2 = pg.image.load("Assets/Wall2.png")
wall2 = pg.transform.scale(wall2, (WIDTH, HEIGHT))
wall3 = pg.image.load("Assets/Wall3.png")
wall3 = pg.transform.scale(wall3, (WIDTH, HEIGHT))
wall4 = pg.image.load("Assets/Wall4.png")
wall4 = pg.transform.scale(wall4, (WIDTH, HEIGHT))
wall5 = pg.image.load("Assets/Wall5.png")
wall5 = pg.transform.scale(wall5, (WIDTH, HEIGHT))
wall6 = pg.image.load("Assets/Wall6.png")
wall6 = pg.transform.scale(wall6, (WIDTH, HEIGHT))
wall7 = pg.image.load("Assets/Wall7.png")
wall7 = pg.transform.scale(wall7, (WIDTH, HEIGHT))

walls = [wall1, wall2, wall3, wall4, wall5, wall6, wall7]

# couldve used a for loop i think but i already coded it


# Create all classes here.
class CH_Player(pg.sprite.Sprite):
    def __init__(self):
        """Player Crosshair. Represents the player."""
        super().__init__()

        self.image = pg.image.load("Assets/crosshair.png")
        self.image = pg.transform.scale_by(self.image, 5)

        self.rect = self.image.get_rect()

        # 'health'
        self.lifetime = 1800

        # cap for cursor speed (?)
        self.agility = 0.15

        # fix my  bullet code ?
        mouse_pos = pg.mouse.get_pos()
        self.rect.centerx = mouse_pos[0]
        self.rect.centery = mouse_pos[1]

    def update(self):
        """Updates position."""
        mouse_pos = pg.mouse.get_pos()
        self.lifetime -= 1
        if self.lifetime > 1800:
            self.lifetime = 1800
        if self.lifetime < 1:
            self.kill()

        # Would like a feature that makes the cursor lag a bit behind to simulate agility (?)
        # self.rect.centerx = mouse_pos[0]
        # self.rect.centery = mouse_pos[1]

        self.rect.centerx += (mouse_pos[0] - self.rect.centerx) * self.agility
        self.rect.centery += (mouse_pos[1] - self.rect.centery) * self.agility
        # this is called linear interpolation
        # it took me forever to figure out a way to implement this
        # AKA 'lerp'

        # unrelated but the people on stack overflow are rude

        # attempt 1 below
        # self.Xvel = 0
        # self.Yvel = 0
        # if mouse_pos[0] > self.rect.centerx:
        #   self.Xvel -= self.agility
        # elif mouse_pos[0] < self.rect.centerx:
        #   self.Xvel += self.agility

        # self.rect = pg.Rect(int("self.rect.centerx", 0))


class Attack(pg.sprite.Sprite):
    def __init__(self, x: int, y: int):
        """
        Would it be morally wrong to depict gun violence against mangoes?
        x determines the x coord, y determines the y coord."""
        super().__init__()

        self.image = pg.Surface((10, 10))
        self.image.fill(JUICE_PUNCH)

        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

        # would use delta time but i never learned how to use it
        self.lifetime = 30

    def update(self):
        """Despawn after some frames"""
        self.image.set_alpha(int(self.lifetime * 8.5))
        if self.lifetime == 30:
            # deal damage
            pass
        if self.lifetime < 1:
            self.kill()
            # had to learn .kill() from pygame org
        self.lifetime -= 1


class Nerve_gas_barrel(pg.sprite.Sprite):
    def __init__(self, x: int, y: int):
        """Stationary barrel, shooting it would end your run."""
        super().__init__()
        self.image = pg.image.load("Assets/ngbarrel.png")
        self.size = random.uniform(0.18, 0.2)
        self.image = pg.transform.scale_by(self.image, self.size)
        self.realimage = pg.mask.from_surface(self.image)
        # thx pygame org, takes pixels from image for pixel perfect collision (for transparent images)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - int(self.rect.width))
        self.rect.y = random.randint(0, HEIGHT - int(self.rect.height))

    def update(self):
        """..."""
        pass


class Mango(pg.sprite.Sprite):
    def __init__(self):
        """TTK's Mortal enemies."""
        super().__init__()
        self.image = pg.image.load("Assets/mango.png")
        self.size = random.uniform(0.05, 0.2)
        self.image = pg.transform.scale_by(self.image, self.size)
        self.realimage = pg.mask.from_surface(self.image)
        # thx pygame org, takes pixels from image for pixel perfect collision (for transparent images)

        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - int(self.rect.width))
        self.rect.y = random.randint(0, HEIGHT - int(self.rect.height))

    def update(self):
        """..."""
        pass


# load menu screen
def menu_screen(clock: pg.time.Clock, screen: pg.Surface) -> str:
    """Display to the user choices.
    Depending on their choice it will return a string.

    Params:
        clock - used to set the frequency of updates
        screen - surface on which we draw
    Returns:
        "game" if the user wants to play the game
        "done" if the user wants to quit
    """
    # show mouse if applicable
    pg.mouse.set_visible(True)
    # load high score here so PB can be displayed on menu screen.
    with open("personal-best.txt") as score_reader:
        personal_best = int(score_reader.read())

    # some text based exposition
    # my favourite least favourite staple of indie games
    arial_font = pg.font.SysFont("Arial", 20)
    menu_line0 = arial_font.render(f"Personal best: {personal_best}", True, WHITE)
    menu_line1 = arial_font.render(
        "Life was peachy until your whole juiceline was pressed in front of your eyes by mangoes.",
        True,
        WHITE,
    )
    menu_line2 = arial_font.render("Your name? Timmy Tuff Knuckles.", True, WHITE)
    menu_line3 = arial_font.render(
        "Your purpose? Hunt, juice, and blend mangoes.", True, WHITE
    )

    lmb2play_instruction = arial_font.render(
        "Left mouse button to play.", True, MANGO_JUICE_YELLOW
    )

    # ------------ MENU LOOP
    while True:
        # ------ MAIN EVENT LISTENER
        for event in pg.event.get():
            if event.type == pg.QUIT:
                # Click the RED X
                return "done"
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    return "done"
            if event.type == pg.MOUSEBUTTONDOWN:
                return "game"

        # ------ GAME LOGIC

        # ------ DRAWING TO SCREEN

        # screen fill white just in case image doesn't load
        screen.fill(BLACK)
        # used white but changed to black so text is still visible
        screen.blit(menu_bg, (0, 0))

        the_blit = (
            menu_line0,
            menu_line1,
            menu_line2,
            menu_line3,
            lmb2play_instruction,
        )
        starting_linetext_pos = -80
        for line_of_text in the_blit:
            # see what i did there? no?
            screen.blit(
                line_of_text,
                (
                    WIDTH // 2 - line_of_text.get_width() // 2,
                    HEIGHT // 2
                    - line_of_text.get_height() // 2
                    + starting_linetext_pos,
                ),
            )
            starting_linetext_pos += 40

        # Update screen
        pg.display.flip()

        # ------ CLOCK TICK
        dt = clock.tick(60) / 1000
        # found this on pyga.me, stands for delta time


def game(clock: pg.time.Clock, screen: pg.Surface):
    """Displays the game.

    Parameters:
        clock - used to set the framerate.
        screen - surface on which we draw
    """

    pg.mixer.music.load("Assets/AmogOST.mp3")
    pg.mixer.music.play()

    # hide mouse in the style of the remake of one of my favourite flash games Sierra 7
    pg.mouse.set_visible(False)
    # access PB so it can be potentially overwritten by current_score
    with open("personal-best.txt") as score_reader:
        personal_best = int(score_reader.read())

    current_score = 0
    adjuster = 0  # adjust difficulty
    death_sound_played = False

    # Sprite Groups
    all_sprites = pg.sprite.Group()
    mango_sprites = pg.sprite.Group()
    barrel_sprites = pg.sprite.Group()
    attack_sprites = pg.sprite.Group()
    player_spritegroup = pg.sprite.Group()

    # Add sprites to all_sprites

    for _ in range(start_count_mango):
        mango = Mango()
        all_sprites.add(mango)
        mango_sprites.add(mango)

    for _ in range(start_count_NGBarrels):
        gas_barrel = Nerve_gas_barrel(
            random.randint(0, WIDTH), random.randint(0, HEIGHT)
        )
        all_sprites.add(gas_barrel)
        barrel_sprites.add(gas_barrel)

    player = CH_Player()
    all_sprites.add(player)
    player_spritegroup.add(player)

    # quick font load hotfix
    score_font = pg.font.SysFont("League Gothic", 30)
    dead_font = pg.font.SysFont("League Gothic", 50)

    # preload death message
    death_message = dead_font.render("You have died. Press ESC to return.", True, RED)

    # how long the gap is between black screen and death message. set to 0 only once.
    time = 0

    new_wall = random.choice(walls)

    # ------------ MENU LOOP
    while True:
        # ------ MAIN EVENT LISTENER
        for event in pg.event.get():
            if event.type == pg.QUIT:
                # Click the RED X
                return "done"

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    return

            if event.type == pg.MOUSEBUTTONDOWN:
                # print("pew")
                ch_x = player.rect.centerx
                ch_y = player.rect.centery

                atk_sound.play()

                if player.lifetime > 0:
                    attack = Attack(ch_x, ch_y)
                    all_sprites.add(attack)
                    attack_sprites.add(attack)
                    # only be able to attack if the player is alive
                    player.lifetime -= 25
                    # punish spamming by taking off a quarter second of their life

        # ------ GAME LOGIC
        all_sprites.update()
        if not mango_sprites:
            for _ in range(start_count_mango + adjuster):
                mango = Mango()
                all_sprites.add(mango)
                mango_sprites.add(mango)
            barrel_sprites.empty()
            for _ in range(start_count_NGBarrels + int(adjuster / 2)):
                gas_barrel = Nerve_gas_barrel(
                    random.randint(0, WIDTH), random.randint(0, HEIGHT)
                )
                all_sprites.add(gas_barrel)
                barrel_sprites.add(gas_barrel)
            new_wall = random.choice(walls)
            adjuster += 1

        if current_score > personal_best:
            personal_best = current_score
            with open("personal-best.txt", "w") as score_reader:
                # "w" overwrites, "a" appends.
                score_reader.write(f"{personal_best}")

        # after everything is updated is where I think i should code collision
        for attack in attack_sprites:
            # for every attack, check all attack_sprites
            mango_got = pg.sprite.spritecollide(
                attack, mango_sprites, True, pg.sprite.collide_mask
            )
            ngB_got = pg.sprite.spritecollide(
                attack, barrel_sprites, False, pg.sprite.collide_mask
            )
            # straight spaghetti here
            # i hate python

            if mango_got:
                current_score += len(mango_got)
                attack.kill()
                player.lifetime += 50
            if ngB_got:
                player.lifetime = 0
                # makes killing the player more consistent rather than returning to menu screen
                # which is what i did before.

        # ------ DRAWING TO SCREEN

        # incase image wont load fill green.
        screen.fill(BLACK)
        # should draw score counter
        screen.blit(new_wall, (0, 0))

        # Firstly update internal values
        current_score_reader = score_font.render(
            f"Current score: {current_score}", True, WHITE
        )
        time_left_reader = score_font.render(
            f"Time Remaining: {player.lifetime // 60}", True, MANGO_JUICE_YELLOW
        )
        pastscore_message = score_font.render(
            f"Your score: {current_score}", True, LESS_EYE_SEARING_WHITE
        )
        best_message = score_font.render(
            f"Your best: {personal_best}", True, LESS_EYE_SEARING_WHITE
        )

        # Now print them.
        screen.blit(
            time_left_reader,
            (
                WIDTH // 2 - time_left_reader.get_width() // 2,
                HEIGHT - time_left_reader.get_height() * 4,
            ),
        )
        screen.blit(
            current_score_reader,
            (
                WIDTH // 2 - current_score_reader.get_width() // 2,
                HEIGHT - current_score_reader.get_height() * 2,
            ),
        )
        # Update screen

        if player.lifetime < 1:
            # immediately blacken screen on death and remove all sprites.
            for sprite in all_sprites:
                sprite.kill()
            screen.fill(BLACK)

            if death_sound_played == False:
                random.choice(death_sounds).play()
                death_sound_played = True

            # now check my variable if its been more than a frame
            if time > 0:
                pg.mixer.music.stop()
                screen.blit(
                    death_message,
                    (
                        WIDTH // 2 - death_message.get_width() // 2,
                        HEIGHT // 2 - death_message.get_height() // 2,
                    ),
                )
                if time > 1:
                    screen.blit(
                        pastscore_message,
                        (
                            WIDTH // 2 - pastscore_message.get_width() // 2,
                            HEIGHT // 2 - death_message.get_height() // 2 + 40,
                        ),
                    )
                    screen.blit(
                        best_message,
                        # not the best message
                        (
                            WIDTH // 2 - best_message.get_width() // 2,
                            HEIGHT // 2 - death_message.get_height() // 2 + 60,
                        ),
                    )
            # if time was 0, make it 1.
            time = time + 1

        mango_sprites.draw(screen)
        barrel_sprites.draw(screen)
        player_spritegroup.draw(
            screen
        )  # made player a sprite group so i could draw in this order.

        pg.display.flip()
        # wait a second in between game over and red text.
        if player.lifetime < 1:
            # TODO play a sound here
            wait.sleep(1)
        # code works better than other things I came up with

        # ------ CLOCK TICK
        dt = clock.tick(60) / 1000


def main():
    # Creating the Screen
    screen = pg.display.set_mode(SIZE)
    pg.display.set_caption("Mangoes 7 V1.4.1")

    # Variables
    done = False
    clock = pg.time.Clock()

    while True:
        choice = menu_screen(clock, screen)

        if choice == "done":
            break
        elif choice == "game":
            game(clock, screen)
            # if choice == "death":
            # so you have chosen... death
            # death(clock, screen)
            # TAKING TOO LONG TO IMPLEMENT SOMETHING UNNECESSARY.
            # deleted the screen as well.

    pg.quit()


if __name__ == "__main__":
    main()
