import json

import pygame
import os

from Bazaar.Common.exceptions import BazaarException
from Bazaar.Common.JSON.serializer import BazaarSerializer
from Bazaar.Referee.IObserver import IObserver
from Bazaar.Referee.game_state import GameState
from Bazaar.Referee.game_state_factory import GameStateFactory
from Bazaar.Referee.pygame_rendering import game_state_to_image


class Observer(IObserver):
    """
    A class that represents an observer in Bazaar and creates a display.
    """
    game_state: GameState
    is_game_over: bool
    save_index: int
    display_index: int
    png_directory: str
    image_files: list[str]
    loaded_images: list[pygame.Surface]
    game_state_list: list[GameState]
    json_directory: str

    class Config:
        arbitrary_types_allowed = True

    def __init__(self, game_state: GameState):
        super().__init__(game_state=game_state, png_directory="", image_files=[], loaded_images=[], is_game_over=False,
                         save_index=0, display_index=0, game_state_list=[], json_directory="")

        self.png_directory = "Tmp"
        self.save_state_as_png()

    async def receive_state(self, game_state: GameState) -> None:
        """
        Sets an observer's game_state, appends the GameState to game_state_list, and calls save_state_as_png.
        """
        if self.is_game_over:
            raise BazaarException("Game Over")
        self.game_state = game_state
        self.game_state_list.append(self.game_state)
        self.save_state_as_png()

    async def game_over(self) -> None:
        self.is_game_over = True

    def save_state(self) -> None:
        """
        Saves the current game state as a JSON file in a designated directory.
        """

        # TODO: ask user for location to save

        self.json_directory = "Tmp2"

        os.makedirs(self.json_directory, exist_ok=True)

        json_state = BazaarSerializer.game_state_to_json(self.game_state_list[self.display_index - 1])

        filename = str(self.display_index) + ".json"
        path = os.path.join(self.json_directory, filename)

        with open(path, "w") as outfile:
            if isinstance(json_state, str):
                json_state = json.loads(json_state)

            clean_json = json.dumps(json_state, ensure_ascii=False)
            outfile.write(clean_json)

    def save_state_as_png(self) -> None:
        """
        Converts an observer's game_state to a png file and saves it in png_directory.
        """
        pygame.init()
        width, height = 960, 540

        surface = game_state_to_image(self.game_state, width, height)

        filename = str(self.save_index)+".png"
        self.save_index += 1
        path = os.path.join(self.png_directory, filename)
        pygame.image.save(surface, path)

    def load_all_images(self) -> None:
        """
        Loads all png images contained in self.png_directory for rendering.
        """
        self.loaded_images.clear()
        for filename in sorted(os.listdir(self.png_directory)):
            if filename.endswith(".png"):
                image_path = os.path.join(self.png_directory, filename)
                self.loaded_images.append(pygame.image.load(image_path))

    def display_saved_states(self) -> None:
        """
        Displays the saved PNG game states in a Pygame window, allowing navigation between states.

        Controls:
            - `Left Arrow`: Navigate to the previous saved state.
            - `Right Arrow`: Navigate to the next saved state.
            - `s`: Save the current state to a JSON file.
            - Close the Pygame window to exit the display.
        """
        self.load_all_images()
        pygame.init()
        screen = pygame.display.set_mode((960, 540), pygame.RESIZABLE)
        pygame.display.set_caption("PNG GameStates")
        clock = pygame.time.Clock()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        self.save_state()
                    elif event.key == pygame.K_LEFT:
                        if self.display_index > 0:
                            self.display_index -= 1
                    elif event.key == pygame.K_RIGHT:
                        if self.display_index == self.save_index - 1 or self.is_game_over:
                            self.display_index = self.display_index
                        elif self.display_index < self.save_index:
                            self.display_index += 1

            screen.fill((127, 127, 127))
            if self.loaded_images:
                screen.blit(self.loaded_images[self.display_index], (0, 0))
            pygame.display.flip()
            clock.tick(60)

        pygame.quit()


if __name__ == "__main__":
    ob1 = Observer(GameStateFactory(player_count=3).create())
    ob1.receive_state(GameStateFactory(player_count=4).create())
    ob1.receive_state(GameStateFactory(player_count=2).create())
    ob1.display_saved_states()

