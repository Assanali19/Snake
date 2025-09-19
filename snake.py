import pygame
import random
import sys

#------------------ Constants ------------------
width, height = 600, 400
cell_size = 20
flash_interval = 500
snake = [(100,100),(80,100),(60,100)]
speed = 10


class Snake:
    def __init__(self):
        self.body = list(snake)
        self.direction = (cell_size,0)
        self.next_direction = self.direction
    
    def move(self):
        head = (self.body[0][0] + self.direction[0], self.body[0][1] + self.direction[1])
        self.body.insert(0,head)
        return head
    
    def trim_tail(self):
        self.body.pop()

    def change_direction(self,new_dir):
        if (self.direction[0] + new_dir[0] != 0) or (self.direction[1] + new_dir[1] != 0):
            self.next_direction = new_dir
        
    def update_direction(self):
        self.direction = self.next_direction

    def draw(self,surface):
        for i, (x,y) in enumerate(self.body):
            pygame.draw.rect(surface, (0,200,0), (x,y,cell_size,cell_size))
            pygame.draw.rect(surface, (0,150,0), (x,y,cell_size,cell_size),2)
            if i == 0:
                pygame.draw.circle(surface,(255,255,255), (x+5,y+5),3)
                pygame.draw.circle(surface,(255,255,255), (x+15,y+5),3)

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((width,height))
        pygame.display.set_caption("Snake game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial",25, bold=True)

        pygame.mixer.init()
        try:
            self.eat_sound = pygame.mixer.Sound("eat.mp3")
            self.game_over_sound = pygame.mixer.Sound("game_over.mp3")
            pygame.mixer.music.load("music.mp3")
            pygame.mixer.music.stop()
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(0.1)
        except:
            print("No sounds file were located")
        
        self.snake = Snake()
        self.apple = self.place_apple()
        self.food_flash = True
        self.last_flash = pygame.time.get_ticks()
        self.score = 0
        self.speed = speed
        self.game_over = False

    def place_apple(self):
        while True:
            pos = (random.randrange(0,width,cell_size),random.randrange(0,height,cell_size))
            if pos not in self.snake.body:
                return pos
    
    def inputs(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if not self.game_over:
                    if event.key == pygame.K_UP and self.snake.direction != (0,cell_size):
                        self.snake.change_direction((0,-cell_size))
                    elif event.key == pygame.K_DOWN and self.snake.direction != (0,-cell_size):
                        self.snake.change_direction((0,cell_size))
                    elif event.key == pygame.K_RIGHT and self.snake.direction != (-cell_size,0):
                        self.snake.change_direction((cell_size,0))
                    elif event.key == pygame.K_LEFT and self.snake.direction != (cell_size,0):
                        self.snake.change_direction((-cell_size,0))
                else:
                    if event.key == pygame.K_r:
                        self.reset_game()
    def reset_game(self):
        self.snake = Snake()
        self.apple = self.place_apple()
        self.score = 0
        self.speed = speed
        self.game_over = False
        pygame.mixer.music.play(-1)
    
    def update(self):
        if self.game_over:
            return
        self.snake.update_direction()
        new_head = self.snake.move()
    
        if new_head == self.apple:
            self.score += 1
            self.speed += 2
            self.apple = self.place_apple()
            try:
                self.eat_sound.play()
            except:
                pass
        else:
            self.snake.trim_tail()
        
        if(new_head[0] < 0 or new_head[0] >= width or new_head[1] < 0 or new_head[1] >= height or new_head in self.snake.body[1:]):
            self.game_over = True
            pygame.mixer.music.stop()
            try:
                self.game_over_sound.play()
            except:
                pass
    
    def draw(self):
        self.screen.fill((0,0,0))

        now = pygame.time.get_ticks()
        if now- self.last_flash > flash_interval:
            self.food_flash = not self.food_flash
            self.last_flash = now
        if self.food_flash:
            color = (200,0,0)
        else:
            color = (255,215,0)
        pygame.draw.rect(self.screen,color,(*self.apple, cell_size,cell_size))

        self.snake.draw(self.screen)

        score_text = self.font.render(("Score: " + str(self.score)),True,(255,255,255))
        self.screen.blit(score_text,(10,10))

        if self.game_over:
            self.show_game_over()
        
        pygame.display.flip()
    
    def show_game_over(self):
        font_large = pygame.font.SysFont("Arial",48,bold=True)
        font_medium = pygame.font.SysFont("Arial",32,bold=True)
        font_small = pygame.font.SysFont("Arial",28,bold=True)

        over_text = font_large.render("GAME OVER",True, (200,0,0))
        score_text = font_large.render(("Score: " + str(self.score)),True, (200,0,0))
        restart_text = font_large.render("Press R to Restart",True, (255,215,0))

        self.screen.blit(over_text, over_text.get_rect(center=(width//2,height//2 - 50)))
        self.screen.blit(score_text, score_text.get_rect(center=(width//2,height//2)))
        self.screen.blit(restart_text, restart_text.get_rect(center=(width//2,height//2 + 50)))


def main():
    game = Game()
    while True:
        game.inputs()
        game.update()
        game.draw()
        game.clock.tick(game.speed)

if __name__ == "__main__":
    main()