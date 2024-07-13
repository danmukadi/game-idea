## game making with Josh 
## main page 1 

import arcade

# our constants 
SPRITE_SCALING = 0.5
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600 
SCREEN_TITLE = "Meribia"
MOVEMENT_SPEED = 5 
SPRITE_SCALING_ENEMY = 0.5

class Player(arcade.Sprite):
    '''Player Class'''

    def update(self):
        '''Move player'''
        # add physics engine later 
        self.center_x += self.change_x
        self.center_y += self.change_y

        #checking for OOB
        if self.left < 0:
            self.left = 0
        elif self.right > SCREEN_WIDTH - 1:
            self.right = SCREEN_WIDTH - 1

        if self.bottom < 0:
            self.bottom = 0
        elif self.top > SCREEN_HEIGHT - 1:
            self.top = SCREEN_HEIGHT - 1




class MyGame(arcade.Window):
    """
    Main application
    """

    def __init__(self, width, height, title):
        #call parent class initializer 
        super().__init__(width, height, title)

        #variables that hold sprites 
        self.player_list = None

        #player info
        self.player_sprite = None
        self.npc_sprite = None

        #set background color
        arcade.set_background_color(arcade.color.AMAZON)
        self.dialogue_active = False
  
        
    def setup(self):
        ''' set up game, init variables '''

        # Sprite Lists
        self.player_list = arcade.SpriteList()
        self.npc_list = arcade.SpriteList()

        #set up player 
        self.player_sprite = Player(":resources:images/animated_characters/female_person/femalePerson_idle.png", SPRITE_SCALING)

          # Create the enemy
        self.enemy = arcade.Sprite(":resources:images/animated_characters/robot/robot_idle.png", SPRITE_SCALING_ENEMY )
        
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

        # updates player movement
        self.player_list.update()

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
        text = "test"

        arcade.draw_rectangle_filled(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 500, 200, arcade.color.WHITE)
        arcade.draw_text(text, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2+ 20, arcade.color.BLACK, font_size=16, anchor_x="center", anchor_y="center")

""" main function """
def main():
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()

if __name__ == '__main__':
    main()

    # end