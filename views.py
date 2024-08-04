import arcade 
from main import GameView

WIDTH = 800
HEIGHT = 600
SPRITE_SCALING = 0.5

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
        
        arcade.draw_text("Press ESC to return", WIDTH / 2, HEIGHT / 2, arcade.color.BLACK, font_size = 20, anchor_x="center")
        
        arcade.draw_text("Press Enter to reset", WIDTH / 2, HEIGHT / 2 - 30, arcade.color.BLACK, font_size = 20, anchor_x="center")
    
    def on_key_press(self, key, _modifiers):
        if key == arcade.key.ESCAPE: #resume game
            self.window.show_view(self.game_view)
        elif key == arcade.key.ENTER:
            game = GameView()
            self.window.show_view(game)
