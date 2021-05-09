import arcade
import math
import time
import PIL
from explosions import *

# Constants
SCREEN_WIDTH = 1300
SCREEN_HEIGHT = 750
SCREEN_TITLE = 'Underworld Heist'
PLAYER_MOVEMENT_SPEED = 1
PLAYER_MAX_MOVEMENT_SPEED = 13
GROUND_FRICTION = 1.12
AIR_FRICTION = 1
GRAVITY = -1
PLAYER_JUMP_SPEED = 25
PLAYER_MARGIN = 30
INITIAL_GRENADE_SPEED_Y = 35
INITIAL_GRENADE_SPEED_X = 28

class InstructionMenuView(arcade.View):
    """ Class for the main menu view """
    def __init__(self):
        super().__init__()
        self.texture = arcade.load_texture('Images/title.png')
        self.mouse_pressed = False
    def on_show(self):
        arcade.set_background_color(arcade.csscolor.DARK_SLATE_BLUE)
    def on_draw(self):
        self.texture.draw_sized(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, SCREEN_WIDTH, SCREEN_HEIGHT)
    def on_mouse_press(self, x, y, btn, mod):
        if self.mouse_pressed:
            game_view = GameView()
            game_view.setup()
            self.window.show_view(game_view)
        else:
            self.texture = arcade.load_texture('Images/tutorial.png')
            self.mouse_pressed = True

class GameOverView(arcade.View):
    """class for the game over view"""
    def __init__(self):
        super().__init__()
        self.texture = arcade.load_texture('Images\gameOver.png')
    def on_show(self):
        arcade.set_background_color(arcade.csscolor.DARK_SLATE_BLUE)
    def on_draw(self):
        self.texture.draw_sized(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, SCREEN_WIDTH, SCREEN_HEIGHT)
    def on_mouse_press(self, x, y, btn, mod):
        instructionMenu = InstructionMenuView()
        self.window.show_view(instructionMenu)

class VictoryView(arcade.View):
    """class for the victory screen view"""
    def __init__(self, music, player):
        super().__init__()
        self.music = music
        self.player = player
        self.texture = arcade.load_texture('Images/victory.png')
    def on_show(self):
        arcade.set_background_color(arcade.csscolor.DARK_SLATE_BLUE)
    def on_draw(self):
        self.texture.draw_sized(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, SCREEN_WIDTH, SCREEN_HEIGHT)
    def on_mouse_press(self, x, y, btn, mod):
        """stop the music and exit to main menu when mouse is clicked"""
        self.music.stop(self.player)
        instructionMenu = InstructionMenuView()
        self.window.show_view(instructionMenu)


class GameView(arcade.View):
    """ The game """

    def __init__(self):

        # Call the parent class and set up the window
        super().__init__()

        arcade.set_background_color((100, 50, 50))

        # game conditions
        self.game_over = False
        self.game_win = False
        self.player_health = 100

        # music
        self.music = None
        self.music_player = None

        # cursor position
        self.cursor_x = 0
        self.cursor_y = 0

        # Object lists
        self.list_of_sprite_lists = []
        self.player_list = None
        self.weapon_list = None
        self.wall_list = None
        self.projectile_list = None
        self.enemy_list = None
        self.explosions_list = None
        self.hazard_list = None
        self.relic_list = None

        # sprites with one of each
        self.player = None
        self.relic = None
        self.launcher = None

        # load the sound effects
        self.sound_explosion = arcade.load_sound('sounds\explosion2.mp3')
        self.sound_launch = arcade.load_sound('sounds\launch.mp3')
        self.sound_click = arcade.load_sound('sounds\click.mp3')
        self.sound_player_death = arcade.load_sound('sounds\player_death.mp3')
        self.sound_enemy_death = arcade.load_sound('sounds\enemy_death.mp3')

        # keyboard keys
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        # lists of game objects
        self.enemy_ai_list = []
        self.physics_engine_list = []

        # timer for animations
        self.timer = 50

    def setup(self):
        """ sets up each new game """

        # game constants
        self.game_over = False
        self.player_health = 100

        # start the music
        self.music = arcade.Sound('sounds\DemonSlayer.mp3', streaming=True)
        self.music_player = self.music.play(1)
        time.sleep(0.03)

        # initialize the sprite lists
        self.player_list = arcade.SpriteList()
        self.weapon_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.explosions_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.projectile_list = arcade.SpriteList()
        self.hazard_list = arcade.SpriteList()
        self.relic_list = arcade.SpriteList()

        # put each sprite list object into one big list for easier management
        self.list_of_sprite_lists.append(self.player_list)
        self.list_of_sprite_lists.append(self.weapon_list)
        self.list_of_sprite_lists.append(self.wall_list)
        self.list_of_sprite_lists.append(self.projectile_list)
        self.list_of_sprite_lists.append(self.enemy_list)
        self.list_of_sprite_lists.append(self.explosions_list)
        self.list_of_sprite_lists.append(self.hazard_list)
        self.list_of_sprite_lists.append(self.relic_list)

        # use the create map method to load in each sprite
        self.create_map('Images\map1.png')

        # load in the launcher sprite at the players position
        self.launcher = arcade.Sprite('Images\player\launcher.png')
        self.launcher.append_texture(arcade.load_texture('Images\player\launcherInverted.png'))
        self.launcher.bottom = self.player.bottom + 50
        self.launcher.left = self.player.left + 50
        self.weapon_list.append(self.launcher)

        #start the physics engine for the player
        self.physics_engine = MyPhysicsEngine(self.player, self.wall_list, GRAVITY)
        self.physics_engine_list.append(self.physics_engine)

    def create_map(self, map_img):
        """ load in all the sprites based on rgb values from an image """
        map = PIL.Image.open(map_img)
        pix = map.load()
        # iterate through each pixel in the map image
        for x in range(map.size[0]):
            for y in range(map.size[1]):
                # check the RGB value for each pixel and place sprites accordingly
                if pix[x,y] == (255, 255, 255,255):
                    # white, do nothing
                    pass
                elif pix[x,y] == (0,0,0,255):
                    # black, place a platform
                    self.floor = arcade.Sprite('Images\platforms\platform.png')
                    self.floor.bottom = y * 75
                    self.floor.left = x * 75
                    self.wall_list.append(self.floor)
                elif pix[x,y] == (255,255,0,255):
                    # yellow, place lava
                    self.lava = arcade.Sprite('Images\lava.png')
                    self.lava.append_texture(arcade.load_texture('Images\lava2.png'))
                    self.lava.bottom = y * 75
                    self.lava.left = x * 75
                    self.hazard_list.append(self.lava)
                elif pix[x,y] == (255,0,0,255):
                    # red, place an enemy
                    self.enemy = arcade.Sprite('Images\monsters\monster10.png')
                    self.enemy.left = x * 75
                    self.enemy.bottom = y * 75
                    self.enemy.health = 100
                    self.enemy.append_texture(arcade.load_texture('Images\monsters\monster09.png'))
                    self.enemy.append_texture(arcade.load_texture('Images\monsters\monster11.png'))
                    # start the enemy AI
                    enemy_ai = EnemyAI(self.enemy, self.wall_list)
                    self.enemy.ai = enemy_ai
                    self.enemy_ai_list.append(enemy_ai)
                    self.enemy_list.append(self.enemy)
                elif pix[x,y] == (0,0,255,255):
                    # blue, place the player
                    self.player = arcade.Sprite('Images\player\playerRight1.png')
                    self.player.bottom = y * 75
                    self.player.left = x * 75
                    self.player.facing_left = False
                    # load all the player textures
                    self.player.append_texture(arcade.load_texture('Images\player\playerRight2.png'))
                    self.player.append_texture(arcade.load_texture('Images\player\playerRight3.png'))
                    self.player.append_texture(arcade.load_texture('Images\player\playerLeft1.png'))
                    self.player.append_texture(arcade.load_texture('Images\player\playerLeft2.png'))
                    self.player.append_texture(arcade.load_texture('Images\player\playerLeft3.png'))
                    self.player.append_texture(arcade.load_texture('Images\player\playerRunRight1.png'))
                    self.player.append_texture(arcade.load_texture('Images\player\playerRunRight2.png'))
                    self.player.append_texture(arcade.load_texture('Images\player\playerRunRight3.png'))
                    self.player.append_texture(arcade.load_texture('Images\player\playerRunLeft1.png'))
                    self.player.append_texture(arcade.load_texture('Images\player\playerRunLeft2.png'))
                    self.player.append_texture(arcade.load_texture('Images\player\playerRunLeft3.png'))
                    self.player.append_texture(arcade.load_texture('Images\player\playerJumpRight.png'))
                    self.player.append_texture(arcade.load_texture('Images\player\playerJumpLeft.png'))
                    self.player_list.append(self.player)
                elif pix[x,y] == (0,255,0,255):
                    # green, place the relic
                    self.relic = arcade.Sprite('Images/relic.png')
                    self.relic.bottom = y * 75
                    self.relic.left = x * 75
                    self.relic_list.append(self.relic)

    def on_draw(self):
        """ Render the screen. """

        arcade.start_render()

        # render all the sprites in each sprite list
        for spriteList in self.list_of_sprite_lists:
            spriteList.draw()

        # render the monster's health text above their heads
        for enemy in self.enemy_list:
            arcade.draw_text(f'{round(enemy.health)}', enemy.left + 15, enemy.top + 5, arcade.csscolor.PALE_GREEN, 18)

        #render the players health bar
        player_health_bars = '|'*round(self.player_health / 3)
        player_health_text = f'Health: {player_health_bars}'
        arcade.draw_text(player_health_text, 10, SCREEN_HEIGHT -30, arcade.csscolor.ORANGE_RED, 18)
        
    def on_key_press(self, key, modifiers):
        """ User control """
        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = True
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = True
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = True
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = True

    def on_key_release(self, key, mods):
        """ User control """
        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = False
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = False
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = False
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = False

    def on_mouse_motion(self, x, y, dy, dx):
        """ get the mouse x and y coordinates """
        self.cursor_x = x
        self.cursor_y = y

    def on_mouse_press(self, x, y, btn, mods):
        """ launch grenades when mouse button is pressed """
        if btn == 1:
            if len(self.projectile_list) < 3: # only 3 grenades out at a time
                # launch a grenade
                arcade.play_sound(self.sound_launch)
                self.grenade = arcade.Sprite('Images\grenade.png')
                self.grenade.center_x = self.player.center_x
                self.grenade.center_y = self.player.center_y
                self.grenade.ticker = 120
                deltaCursor = math.sqrt((self.cursor_x - self.player.center_x)**2 + (self.cursor_y - self.player.center_y)**2)
                initVelocity = [((self.cursor_x - self.player.center_x) / deltaCursor) * INITIAL_GRENADE_SPEED_X, ((self.cursor_y - self.player.center_y) / deltaCursor) * INITIAL_GRENADE_SPEED_Y]
                #start the physics engine for the grenade
                self.grenade_physics = MyPhysicsEngine(self.grenade, self.wall_list, GRAVITY, initVelocity, False)
                self.grenade.physics = self.grenade_physics
                self.physics_engine_list.append(self.grenade_physics)
                self.projectile_list.append(self.grenade)
            else:
                # play click sound effect
                arcade.play_sound(self.sound_click)

    def on_update(self, delta_time):
        """ Movement and game logic """

        # update the positions of any grenade particles
        self.explosions_list.update()

        # advance the animation timer
        self.timer -= 1

        # if the end of the song is reached, start it over
        if self.music.get_stream_position(self.music_player) == 0.0:
            self.music = arcade.Sound('sounds\DemonSlayer.mp3', streaming=True)
            self.music_player = self.music.play(1)
            time.sleep(0.03)
        
        # Calculate speed based on the keys pressed
        self.player.change_x = 0
        self.player.change_y = 0
        if self.up_pressed and not self.down_pressed:
            if self.physics_engine.can_jump:
                self.player.change_y = PLAYER_JUMP_SPEED
        if self.left_pressed and not self.right_pressed:
            self.player.change_x = -PLAYER_MOVEMENT_SPEED
        elif self.right_pressed and not self.left_pressed:
            self.player.change_x = PLAYER_MOVEMENT_SPEED

        # place the launcher ath the players previous position
        # (we want some movement relative to the player, so we do this before updating the player's position)
        self.launcher.center_x = self.player.center_x
        self.launcher.center_y = self.player.center_y

        # lava block animation
        for lava_block in self.hazard_list:
            if self.timer == 25:
                lava_block.set_texture(1)
            if self.timer == 0:
                lava_block.set_texture(0)

        # update each grenade's ticker, if ready to explode calculate any damage done
        for grenade in self.projectile_list:
            grenade.ticker -= 1
            if grenade.ticker == 0: # ready to explode
                arcade.play_sound(self.sound_explosion)
                self.projectile_list.remove(grenade)
                self.physics_engine_list.remove(grenade.physics)
                distance_to_player = math.sqrt((grenade.center_x - self.player.center_x)**2 + (grenade.center_y - self.player.center_y)**2) + 1
                if distance_to_player < 200: # damage the player
                    self.player_health -= 5000 / distance_to_player
                for enemy in self.enemy_list: # damage enemies
                    distance_to_enemy = math.sqrt((grenade.center_x - enemy.center_x)**2 + (grenade.center_y - enemy.center_y)**2) + 1
                    if distance_to_enemy < 200:
                        enemy.health -= 5000 / distance_to_enemy
                        if enemy.health <= 0:
                            arcade.play_sound(self.sound_enemy_death)
                            self.enemy_ai_list.remove(enemy.ai)
                            self.enemy_list.remove(enemy)
                for i in range(20): # start explosion animation
                    particle = Particle(self.explosions_list)
                    particle.position = grenade.position
                    self.explosions_list.append(particle)

        # update monster AI engines
        for AI in self.enemy_ai_list:
            AI.update()

        # only do these things if the game isnt over
        if not self.game_over:

            # aim the launcher
            if self.cursor_x > self.player.center_x:
                self.player.facing_left = False
                angle = math.degrees(math.atan((self.cursor_y - self.player.center_y) / (self.cursor_x - self.player.center_x)))
                self.launcher.angle = angle
                self.launcher.set_texture(0)
            elif self.cursor_x < self.player.center_x:
                self.player.facing_left = True
                angle = math.degrees(math.atan((self.cursor_y - self.player.center_y) / (self.cursor_x - self.player.center_x))) + 180
                self.launcher.angle = angle
                self.launcher.set_texture(1)

            # player animations
            if self.player.facing_left:
                if self.physics_engine.can_jump:
                    if abs(self.player.change_x) > 0:
                        if self.timer == 35:
                            self.player.set_texture(9)
                        elif self.timer == 15:
                            self.player.set_texture(10)
                        elif self.timer == 0:
                            self.player.set_texture(11)
                    else:
                        if self.timer == 35:
                            self.player.set_texture(3)
                        elif self.timer == 15:
                            self.player.set_texture(4)
                        elif self.timer == 0:
                            self.player.set_texture(5)
                else:
                    self.player.set_texture(13)
            else:
                if self.physics_engine.can_jump:
                    if abs(self.player.change_x) > 0:
                        if self.timer == 35:
                            self.player.set_texture(6)
                        elif self.timer == 15:
                            self.player.set_texture(7)
                        elif self.timer == 0:
                            self.player.set_texture(8)
                    else:
                        if self.timer == 35:
                            self.player.set_texture(0)
                        elif self.timer == 15:
                            self.player.set_texture(1)
                        elif self.timer == 0:
                            self.player.set_texture(2)
                else:
                    self.player.set_texture(12)

            # damage the player if they get to close to monsters
            for enemy in self.enemy_list:
                distance_to_enemy = math.sqrt((self.player.center_x - enemy.center_x)**2 + (self.player.center_y - enemy.center_y)**2)
                if distance_to_enemy < 100:
                    self.player_health -= 3

            # check for player death
            if self.player_health <= 0:
                # game over
                arcade.play_sound(self.sound_player_death)
                self.game_over = True

            # check for player fall
            if self.player.center_y < 0:
                self.player_health = 0

            # move the viewport to keep player centered
            self.move_frame()

            # update physics engines
            for engine in self.physics_engine_list:
                engine.update()
        else: # when player dies wait 2 seconds, then proceed to game-over view
            time.sleep(2)
            self.music.stop(self.music_player)
            game_over = GameOverView()
            self.window.show_view(game_over)

        # check to see if player found the relic
        distance_to_relic = math.sqrt((self.player.center_x - self.relic.center_x)**2 + (self.player.center_y - self.relic.center_y)**2)
        if distance_to_relic < 60: # victory
            time.sleep(2)
            victory = VictoryView(self.music, self.music_player)
            self.window.show_view(victory)

        # reset the animation timer when it hits 0
        if self.timer == 0:
            self.timer = 50

    def move_frame(self):
        """ move the frame based on player position """
        if self.player.center_x > 500:
            for spriteList in self.list_of_sprite_lists:
                for sprite in spriteList.sprite_list:
                    sprite.center_x -= (self.player.center_x - 500) / 3
        elif self.player.center_x < 300:
            for spriteList in self.list_of_sprite_lists:
                for sprite in spriteList.sprite_list:
                    sprite.center_x += abs(self.player.center_x - 300) * math.sqrt(3)
   
class MyPhysicsEngine():
    """ Physics engine I created for player and grenades """
    def __init__(self, player, walls, gravity_constant, initial_velocity=[0,0], is_player=True):
        self.player = player
        self.walls = walls
        self.gravity_constant = gravity_constant
        self.playerVelocity = initial_velocity
        self.can_jump = False
        self.is_player = is_player

    def update(self):
        # check for floors
        self.check_for_floors()
        
        if not self.can_jump: # player in free fall
            self.playerVelocity[0] = self.playerVelocity[0] / AIR_FRICTION # calculate change in velocity for air resistance
            self.playerVelocity[1] += self.gravity_constant # calculate change in velocity for gravity
        else: # player on ground
            self.playerVelocity[0] = self.playerVelocity[0] / GROUND_FRICTION # calculate friction
            self.playerVelocity[1] = self.player.change_y # player jump

        # movement in x direction
        self.playerVelocity[0] += self.player.change_x
        
        #check for walls
        self.check_for_walls()

        # maximum movement speed calculation
        if self.is_player:
            if self.playerVelocity[0] > PLAYER_MAX_MOVEMENT_SPEED:
                self.playerVelocity[0] = PLAYER_MAX_MOVEMENT_SPEED
            elif abs(self.playerVelocity[0]) > PLAYER_MAX_MOVEMENT_SPEED:
                self.playerVelocity[0] = -PLAYER_MAX_MOVEMENT_SPEED

        # change position based on the calculated velocity
        self.player.center_x += self.playerVelocity[0]
        self.player.center_y += self.playerVelocity[1]

    def check_for_walls(self):
        """ check for collisions with walls """
        for wall in self.walls.sprite_list:           
            if ((self.player.top - 10) > wall.bottom) and ((self.player.bottom + 10) < wall.top) and ((wall.left - self.player.right) <= 0) and ((wall.left - self.player.right) > -60):
                print('left')
                self.player.right = wall.left
                self.playerVelocity[0] = self.playerVelocity[0] * -0.5
            if ((self.player.top - 10) > wall.bottom) and ((self.player.bottom + 10) < wall.top) and ((self.player.left - wall.right) <= 0) and ((self.player.left - wall.right) > -60):
                print('right')
                self.player.left = wall.right
                self.playerVelocity[0] = self.playerVelocity[0] * -0.5

    def check_for_floors(self):
        """ Check for collisions with floors and ceilings """
        for wall in self.walls.sprite_list:
            if (self.player.right > wall.left) and (self.player.left < wall.right) and ((wall.bottom - self.player.top) <= 0) and ((wall.bottom - self.player.top) > -60):
                self.playerVelocity[1] = self.playerVelocity[1] * (-0.4)
            else:
                self.can_jump = False
            if (self.player.right > wall.left) and (self.player.left < wall.right) and ((self.player.bottom - wall.top) <= 0) and ((self.player.bottom - wall.top) > -60):
                self.player.bottom = wall.top
                self.playerVelocity[1]
                self.can_jump = True
                break


class EnemyAI():
    """ monster movement, animation, and collision detection """
    def __init__(self, enemy, walls):
        self.me_an_enemy = enemy
        self.x_velocity = -3
        self.walls = walls
        self.counter = 40

    def update(self):
        # animation
        self.counter -= 1
        if self.counter == 30:
            self.me_an_enemy.set_texture(1)
        elif self.counter == 20:
            self.me_an_enemy.set_texture(0)
        elif self.counter == 10:
            self.me_an_enemy.set_texture(2)
        elif self.counter == 0:
            self.me_an_enemy.set_texture(0)
            self.counter = 40

        # change position based on velocity
        self.me_an_enemy.center_x += self.x_velocity

        # check to see if monster needs to turn around
        turn_around = True
        for wall in self.walls:
            if (self.me_an_enemy.top - 10 > wall.bottom) and (self.me_an_enemy.bottom + 10 < wall.top) and ((((self.me_an_enemy.left - wall.right) <= 0) and ((self.me_an_enemy.left - wall.right) > -60)) or ((wall.left - self.me_an_enemy.right) <= 0) and ((wall.left - self.me_an_enemy.right) > -60)):
                turn_around = True
                break
            if (self.me_an_enemy.center_x >= wall.left) and (self.me_an_enemy.center_x <= wall.right) and (abs(self.me_an_enemy.bottom - wall.top) < 5):
                turn_around = False
        if turn_around:
            self.x_velocity = self.x_velocity * -1



def main():
    """ Main method """

    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    start_view = InstructionMenuView()
    window.show_view(start_view)
    arcade.run()


if __name__ == "__main__":
    main()