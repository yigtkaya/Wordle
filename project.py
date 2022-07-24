from pickle import TRUE
import readline
from tkinter import CENTER

from sympy import li
from words import WORDS
import pygame
import random


pygame.init()

FPS = 60
WIDTH, HEIGHT = 700, 750
WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = "#6aaa64"
YELLOW = "#c9b458"
GREY = "#787c7e"
OUTLINE = "#d3d6da"
FILLED_OUTLINE = "#878a8c"
text_font = pygame.font.Font('freesansbold.ttf', 56)
small_text_font = pygame.font.Font('freesansbold.ttf', 16)

scores = []
game_over = False
win = False
turn_avtive = True
secret_word = random.choice(WORDS)
print(secret_word)

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("CS50P Final Project -- Wordle Game")


score = 0
turn = 0
letters = 0
board = [
    [" ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " "]
    ]    

def game_board():
    for col in range(5):
        for row in range(5):
            pygame.draw.rect(SCREEN, BLACK, [col * 100 + 105, row * 100 + 25, 75, 75], 3, 5)
            place_text = text_font.render(board[row][col], True, BLACK)
            SCREEN.blit(place_text, (col * 100 + 125, row * 100 + 38))
def get_highest_score():
    global scores
    with open("scores.txt", "r") as f:
        lines = f.readlines()
        for line in lines:
            scores.append(int(line.strip()))
    return max(scores)
def check_words():
    global turn
    global board
    global secret_word
    for col in range(5):
        for row in range(5):
            if secret_word[col] == board[row][col] and turn > row:
                pygame.draw.rect(SCREEN, GREEN, [col * 100 + 105, row * 100 + 25, 75, 75], 0, 5)
            elif board[row][col] in secret_word and turn > row:
                pygame.draw.rect(SCREEN, YELLOW, [col * 100 + 105, row * 100 + 25, 75, 75], 0, 5)
            else:
                pygame.draw.rect(SCREEN, GREY, [col * 100 + 105, row * 100 + 25, 75, 75], 0, 5)
def save_score(s):
    with open("scores.txt", "a") as f:
        f.write("\n" + str(s))
def scoreboard():
    global score
    highest_score = get_highest_score()
    pygame.draw.rect(SCREEN, BLACK,[450, 630, 200, 50], 3)
    pygame.draw.rect(SCREEN, BLACK,[450, 680, 200, 50], 3)
    high_score_text = small_text_font.render(f"Highest Score: {highest_score}", True, BLACK)
    SCREEN.blit(high_score_text, (475, 695))
    score_text = small_text_font.render(f"Current Score: {score}", True, BLACK)
    SCREEN.blit(score_text, (475, 655))

def main():
    global board
    global letters
    global turn
    global game_over
    global win
    global secret_word
    global score
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        SCREEN.fill("white")
        check_words()
        game_board()
        scoreboard()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                max_score = get_highest_score 
                if score > max_score:
                    save_score(score)
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE and letters > 0:
                    board[turn][letters - 1] = ' '
                    letters -=1
                if event.key == pygame.K_RETURN and not game_over and letters == 5:
                    turn +=1
                    letters = 0
                if event.key == pygame.K_RETURN and game_over:
                    save_score(score)
                    score = 0
                    turn = 0
                    letters = 0
                    game_over = False
                    secret_word = random.choice(WORDS)
                    print(secret_word)
                    board = [[" ", " ", " ", " ", " "],
                            [" ", " ", " ", " ", " "],
                            [" ", " ", " ", " ", " "],
                            [" ", " ", " ", " ", " "],
                            [" ", " ", " ", " ", " "],
                            [" ", " ", " ", " ", " "]]
                
                if event.key == pygame.K_RETURN and win:
                    if turn == 1:
                        score += 50
                    if turn == 2:
                        score += 40
                    if turn == 3:
                        score += 30
                    if turn == 4:
                        score += 20
                    if turn == 5:
                        score += 10
                    
                    turn = 0
                    letters = 0
                    game_over = False
                    win = False
                    secret_word = random.choice(WORDS)
                    print(secret_word)
                    board = [[" ", " ", " ", " ", " "],
                            [" ", " ", " ", " ", " "],
                            [" ", " ", " ", " ", " "],
                            [" ", " ", " ", " ", " "],
                            [" ", " ", " ", " ", " "],
                            [" ", " ", " ", " ", " "]]
            
            if event.type == pygame.TEXTINPUT and turn_active and not game_over:
                entry = event.__getattribute__("text")
                if entry != " ":
                    board[turn][letters] = entry
                    letters +=1
                
        
        if letters == 5:
            turn_active = False
        if letters < 5:
            turn_active = True

        for row in range(5):
            guess = board[row][0] + board[row][1] + board[row][2] + board[row][3] + board[row][4]
            if guess == secret_word and row < turn: 
                win = True

        if win and turn < 6: 
            win_text = text_font.render("WIN!", True, BLACK)
            SCREEN.blit(win_text, (270, 530))
            try_again_text = small_text_font.render("Press enter to play again with new word!", True, BLACK)
            SCREEN.blit(try_again_text, (180, 600))

            
        if turn == 5 and not win:
            game_over_text = text_font.render("GAME OVER !!", True, BLACK)
            SCREEN.blit(game_over_text, (170, 530))
            try_again_text = small_text_font.render("Press enter to play again with new word!", True, BLACK)
            SCREEN.blit(try_again_text, (180, 600))
            game_over = True


        pygame.display.flip()

    pygame.quit()



if __name__ == "__main__":
    main()