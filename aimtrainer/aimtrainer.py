import pygame
import random
from pygame import mixer
import tweepy
import keys

#Initialize
pygame.init()

#screen creation
#win = pygame.display.set_mode((500, 500)) this was the original screen size
win = pygame.display.set_mode((1000, 750))

#set window name
pygame.display.set_caption("Aim Trainer")

light_gray = (180, 180, 180)
#rand1 = random.randint(50, 450) og
#rand2 = random.randint(50, 450) og
rand1 = random.randint(50, 700)
rand2 = random.randint(50, 700)
width = 20
height = 20

#timer
clock = pygame.time.Clock()
start = 5500

#missed shots
whiffs = 0

#music
mixer.music.load('stress.wav')
mixer.music.play(0)

#enemy and player
def enemy():
    enem = pygame.draw.rect(win, (0, 0, 0), (rand1, rand2, width, height))
    return enem

def player():
    play = pygame.draw.ellipse(win, (255, 255 , 255), (x, y, width/2, height/2))
    return play

#show score
score_val = 0
overall_score = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

#Keys for twitter
consumer_key = keys.consumer_key
consumer_secret = keys.consumer_secret
access_token = keys.access_token
access_token_secret = keys.access_token_secret

#Twitter Authentication
def OAuth():
    try:
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        return auth

    except Exception as e:
        return None

def show_score(x, y):
    score = font.render("Score: " + str(overall_score), True, (0, 0, 0))
    win.blit(score, (x, y))

#time
def show_time(x):
    print(x)

pygame.mouse.set_cursor((8, 8),(0, 0),(0, 0, 0, 0, 0, 0 ,0 ,0), (0, 0, 0, 0, 0, 0, 0, 0))

#indicates that its running
run = True
#indicates that the actual game itself is running, not the entire application
game_run = True

def game():
    win.fill((light_gray))
    player()
    enemy()
    show_score(textX, textY)

#game loop
#timer that will change the screen to its endgame 
while start >= 0:
    x, y = pygame.mouse.get_pos()
    #create a time delay
    pygame.time.delay(10)
    #collision detection
    if player().colliderect(enemy()):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                rand1 = random.randint(50, 700)
                rand2 = random.randint(50, 700)
                score_val += 1
                overall_score += 1
                print("Your score:", str(score_val))
    else:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                whiffs += 1
                overall_score -= 1
                print("You've whiffed: ", str(whiffs))
    
    start -= 1

    #iterate over the list of event objects
    #that was returned by pygame.event.get() method.
    for event in pygame.event.get():
        #is user pressing X
        if event.type == pygame.QUIT:
            #exit program
            run = False
    game()
    pygame.display.update()
#the end screen
else:
    win.fill((light_gray))
    endText = font.render("You've Finished!", True, (0, 0, 0))
    win.blit(endText, (350, 375))

    if overall_score >= 70:
        end_text = "You've done good! No tweet will be posted!"
    else:
        end_text = "You've failed, the tweet has been posted."
        
        #Twitter Poster
        oauth = OAuth()
        api = tweepy.API(oauth)
        api.update_status("i smell bad")
    
    ending = font.render(end_text, True, (0, 0, 0))
    win.blit(ending, (200, 425))

    #final_score = score_val-whiffs
    #final_score = round(final_score, 2)
    final_screen = font.render("You're final score is " + str(overall_score), True, (0, 0, 0))
    win.blit(final_screen, (textX, textY))

    final_val = font.render("You hit " + str(score_val) + (" shots"), True, (0, 0, 0))
    win.blit(final_val, (10, 50))

    final_whiffs = font.render(("You missed ") +str(whiffs) +(" shots"), True, (0, 0, 0))
    win.blit(final_whiffs, (10, 90))
    pygame.display.update()
