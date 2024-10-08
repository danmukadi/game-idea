## game making with Josh 
## main page 1 

import arcade
from pyglet.gl import glTexParameteri, GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_TEXTURE_MAG_FILTER, GL_NEAREST
import time

# our constants 
SPRITE_SCALING = 2.5
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600 
SCREEN_TITLE = "Mythril"
MOVEMENT_SPEED = 2 
SPRITE_SCALING_ENEMY = 0.5
MINIMAP_SCALE = 0.2
MUSIC_VOLUME = 0.1

class BGMusicPlayer():
    def __init__(self):
        super().__init__()

        self.music_list = []
        self.current_song_index = 0
        self.current_player = None
        self.music = None

    def advance_song(self):
        # advances pointer to the next song only 
        self.current_song_index += 1
        # this will loop it if it gets out of bounds
        if self.current_song_index >= len(self.music_list):
            self.current_song_index = 0

    def play_song(self):
        # this fiunction plays the song
        if self.music:
            self.music.stop()

        # plays the next song
        self.music = arcade.Sound(self.music_list[self.current_song_index], streaming=True)
        self.current_player = self.music.play(MUSIC_VOLUME, 0, True)
        # need a quick delay otherwise elapsed time is 0.0
        time.sleep(0.03)

    def setup(self):
        # our list of music 
        self.music_list = ['bg/bistro-pierre-bg.wav']
        self.current_song_index = 0
        self.play_song()

    def on_update(self, dt):
       if self.music and self.current_player:
            position = self.music.get_stream_position(self.current_player)
            # Reset pointer to 0 after song finishes
            if position == 0.0:
                self.advance_song()
                self.play_song()


class PauseView(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view

    def on_show_view(self):
        arcade.set_background_color(arcade.color.ORANGE)

    

    def on_draw(self):
        self.clear()
        #Draw player, for effect, on pause screen
        #The previous View (gameview) was passed in
        #and saved in self.game_view
        player_sprite = self.game_view.player_sprite
        player_sprite.draw()
        #draw orange filter over him
        arcade.draw_lrtb_rectangle_filled(left=player_sprite.left, right=player_sprite.right, top=player_sprite.top, bottom=player_sprite.bottom, color=arcade.color.ORANGE+(200,))
        
        arcade.draw_text("Press ESC to return", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, arcade.color.BLACK, font_size = 20, anchor_x="center")
        
        arcade.draw_text("Press Enter to reset", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 30, arcade.color.BLACK, font_size = 20, anchor_x="center")
    
    def on_key_press(self, key, _modifiers):
        if key == arcade.key.ESCAPE: #resume game
            self.window.show_view(self.game_view)
        elif key == arcade.key.ENTER:
            game = GameView()
            self.window.show_view(game)



class GameView(arcade.View):
    """
    Main application
    """

    def __init__(self):
        #call parent class initializer 
        super().__init__()

        #variables that hold sprites 
        self.player_list = None

        self.music_player = BGMusicPlayer()

        #player info
        self.player_sprite = None
        self.npc_sprite = None

        #set background color
        arcade.set_background_color(arcade.color.BUD_GREEN)
        self.dialogue_active = False

        ''' 
        set up game, init variables 
        '''

        self.music_player.setup()

        # Sprite Lists
        self.player_list = arcade.SpriteList()
        self.npc_list = arcade.SpriteList()

        #set up player 
        self.player_sprite = arcade.AnimatedTimeBasedSprite(scale=SPRITE_SCALING)
        self.player_sprite.frames = []

        for i in range(4): 
            texture = arcade.load_texture("sprites/MC1.png", x=i*32, y=0, width=32, height=32)
            texture.image = texture.image.convert("RGBA")
            anim = arcade.AnimationKeyframe(i, 180, texture)
            self.player_sprite.frames.append(anim)


        # Set initial texture
        self.player_sprite.texture = self.player_sprite.frames[0].texture


          # Create the enemy
        self.enemy = arcade.Sprite("sprites/MC2-EX2.png", SPRITE_SCALING )
        
        self.enemy.center_y = 400
        self.enemy.center_x = 700
        self.npc_list.append(self.enemy)

        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 50
        self.player_list.append(self.player_sprite) 
        
        ''' set up game, init variables '''

        # Sprite Lists
        self.player_list = arcade.SpriteList()
        self.npc_list = arcade.SpriteList()

       

        #set up player 
        self.player_sprite = arcade.AnimatedTimeBasedSprite(scale=SPRITE_SCALING)
        self.player_sprite.frames = []

        
        for i in range(4): 
            texture = arcade.load_texture("sprites/MC1.png", x=i*32, y=0, width=32, height=32)
            anim = arcade.AnimationKeyframe(i, 180, texture)
            self.player_sprite.frames.append(anim)

        if self.player_sprite.change_x < 0:
            for i in range(4): 
                texture = arcade.load_texture("sprites/MC-1-final.png", x=i*32, y=2*32, width=32, height=32)
                anim = arcade.AnimationKeyframe(i+8, 180, texture)
                self.player_sprite.frames.append(anim)

            self.player_sprite.texture = self.player_sprite.frames[8].texture



        # Set initial texture
        self.player_sprite.texture = self.player_sprite.frames[0].texture


          # Create the enemy
        self.enemy = arcade.Sprite("sprites/MC2-EX2.png", SPRITE_SCALING )
        
        self.enemy.center_y = 400
        self.enemy.center_x = 700
        self.npc_list.append(self.enemy)

        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 50
        self.player_list.append(self.player_sprite)
  
       

    def on_draw(self):
        """ rendering """ 
       

        """ this line need to be here before any rendering happens """
        self.clear()

       

        # now we can draw the sprites
        # we only have 1 sprite so thats all we can draw rn 
        self.npc_list.draw()
        self.player_list.draw()  
          
        if self.dialogue_active:
         self.draw_dialogue_box()                         

    def on_update(self, delta_time):
        """ updates game logic"""
        if self.check_enemy_collision():
            self.dialogue_active = True

        self.player_sprite.center_x += self.player_sprite.change_x
        self.player_sprite.center_y += self.player_sprite.change_y

        #checking for OOB
        if self.player_sprite.left < 0:
            self.player_sprite.left = 0
        elif self.player_sprite.right > SCREEN_WIDTH - 1:
            self.player_sprite.right = SCREEN_WIDTH - 1

        if self.player_sprite.bottom < 0:
            self.player_sprite.bottom = 0
        elif self.player_sprite.top > SCREEN_HEIGHT - 1:
            self.player_sprite.top = SCREEN_HEIGHT - 1

        self.music_player.on_update(delta_time)

        # updates player animation 
        self.player_list.update_animation()

        #updates player movement 
        self.player_list.update()



    ''' 
    We need this because the screen isnt adjusted to sprites with lesser pixels, forcing us to scale the pixels up 
    we lose resolution doing this and they come out blurry. We need to create a minimap that allows us to display 
    32x32 or bigger in better resolution than the deafult 
    '''
    def draw_minimap(self):
      pass


    def on_key_press(self, key, mods):
        """ this function is called whenever a key is pressed """

        # if player presses key, its speed is updated 
        # its not the position thats changed but its movement speed, i.e. change in y or x 
        if key == arcade.key.UP:
            self.player_sprite.change_y = MOVEMENT_SPEED
        elif key == arcade.key.DOWN:
            self.player_sprite.change_y = -MOVEMENT_SPEED
        elif key == arcade.key.LEFT:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = MOVEMENT_SPEED
        elif key == arcade.key.ESCAPE:
            pause = PauseView(self)
            self.window.show_view(pause)

    def on_key_release(self, key, mods):
        """ callled when key is released from being pressed """ 

        # Note: doesnt work well if more than 1 key is pressed at same time 
        # thers a better movement ex for this, add later 
        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0

    def check_enemy_collision(self):
        player_radius = 25
        distance_x = abs(self.player_sprite.center_x - self.enemy.center_x)
        distance_y = abs(self.player_sprite.center_y - self.enemy.center_y)
        combined_radius = player_radius + 25

        if distance_x < combined_radius and distance_y < combined_radius:
            return True
        else:
            return False
        
    def draw_dialogue_box(self):
        text = "Music finally works, now to just work on sprites..."

        arcade.draw_rectangle_filled(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 500, 200, arcade.color.WHITE)
        arcade.draw_text(text, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2+ 20, arcade.color.BLACK, font_size=16, anchor_x="center", anchor_y="center")

""" main function """
def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game = GameView()
    window.show_view(game)
    arcade.run()

if __name__ == '__main__':
    main()

    # end