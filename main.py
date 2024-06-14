import arcade
import obj


class Game(arcade.Window):
    def __init__(self):
        super().__init__(800, 600)
        self.background_color = arcade.color.WHITE
        self.simulation = obj.Simulation()

    def on_update(self, delta_time):
        pass

    def on_draw(self):
        self.clear()
        self.simulation.draw()



def main():
    game = Game()
    game.run()


if __name__ == '__main__':
    main()