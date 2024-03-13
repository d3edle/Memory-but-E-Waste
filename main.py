#Pygame start
#Uses VR menu code

import pygame
import random
pygame.init()
SIZE = (width,height) = (800,500)
screen = pygame.display.set_mode(SIZE)
GREEN = (0,255,0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0,0,0)
WHITE = (255, 255, 255)
GREY = (100, 100, 100)

STATE_MAIN = 0
STATE_PLAY = 1
STATE_INSTRUCTIONS = 2
STATE_EXIT = 3
STATE_DONE = 4

font = pygame.font.SysFont("Times New Roman",30)  # done once

#centers text in a box
def centertext(string, size, rect):
  font = pygame.font.SysFont("Times New Roman",size)
  textWidth, textHeight = font.size(string)
  offX = rect[0] + (rect[2] - textWidth)//2
  offY = rect[1] + (rect[3] - textHeight)//2
  textRect = pygame.Rect(offX, offY, textWidth, textHeight)
  text = font.render(string , 1, (0, 0, 0))
  screen.blit(text, textRect)
  
#Center & draw text but without y coordinate
def xCenteredText(string, size, rect, color, y):
  font = pygame.font.SysFont("Times New Roman",size)
  textWidth, textHeight = font.size(string)
  centerx = (rect[2] - textWidth)//2
  centery = (rect[3] - textHeight)//2
  text = font.render(string, 1, color)
  screen.blit(text, [centerx,y])

 # clear the screen, draw off screen and then display
def drawMenu(mx, my, button, currentState):
  #Based off of VR's menu code
  global screenrect
  stateList = [STATE_PLAY, STATE_INSTRUCTIONS, STATE_EXIT]
  titleList = ["Play Game", "Instructions", "Exit"]
  widthX = 800//5
  heightY = 500//20
  startY = heightY + 200
  screen.blit(brainPic, (0,0,500,800))
  xCenteredText('Memory', 45, screenrect, (0,100,255), 75) 
  xCenteredText('The game for making dumb people feel dumber (me)', 25, screenrect, (0,0,0), 150) 
  for i in range(3):
    currentRect = pygame.Rect(widthX, startY, 3*widthX, 2*heightY)
#Checks for collision
    if currentRect.collidepoint(mx, my) == True:
      pygame.draw.rect(screen, (255,0,0), currentRect)

      #Checks if the user left-clicks on a card
      if button == 1:
        currentState = stateList[i]
    else:

      #IF there wasn't a collision
      pygame.draw.rect(screen, (0,100,255), currentRect)
    centertext(titleList[i], 30, currentRect)

    startY += 3*heightY
  return currentState     

#Takes how many cards are left and returns how many seconds the game should have per turn
def timerchange(list):

  #Takes the length of the list (how many cards are left) and compares to decreasing increments: this is how the game gets more diificult 
  if len(list) <= 32:
    secondsleft = 10
  if len(list) == 30:
    secondsleft = 9
  if len(list) <= 26:
    secondsleft = 8
  if len(list) <= 22:
    secondsleft = 7
  if len(list) <= 20:
    secondsleft = 6
  if len(list) <= 16:
    secondsleft = 5
  if len(list) <= 14:
    secondsleft = 4
  if len(list) <= 12:
    secondsleft = 3
  if len(list) <= 10:
    secondsleft = 2
  return secondsleft

#Finds what image is supposed to be displayed
def chooseimage(card):
  image = ''

  #Checks if the name of the card is eye strain, or whichever card it is - then makes image its correponding picture
  if card == 'Eye strain':
    image = eye
  if card == 'Loss of privacy':
    image = privacy
  if card == 'Damages nature':
    image = nature
  if card == 'Social Isolation':
    image = social
  if card == 'Depression':
    image = depression
  if card == 'Distracting':
    image = distracting
  if card == 'Carpal tunnel':
    image = carpal
  if card == 'Cyberbullying':
    image = cyberbullying
  if card == 'Doxxing':
    image = doxxing
  if card == 'Toxic Groups':
    image = toxic
  if card == 'Spinal Rounding':
    image = spinal
  if card == 'Lower Attention':
    image = attention
  if card == 'Parasocial Relations':
    image = parasocial
  if card == 'Stalking':
    image = stalking
  if card == 'Viruses':
    image = virus
  if card == 'Misinformation':
    image = misinfo

  #For if the time ran out; a blank card that blends into the time's up screen
  if card == '':
    image = white
  return image


#Actual game function
def drawPlay(mx, my, button, currentState):
  global cardrectlist, cardnamelist, button_val, flipped_val, pressed_amount, card1, card2, card1rect, card2rect, card1value, card2value, numcards, p1scorerect, p2scorerect, p1scoretitlerect, p2scoretitlerect, p1score, p2score, card1textrect, card1titlerect, card2textrect, card2titlerect, playerturnrect, playerturn, amountflip, amountreverseflip, flipTimer, flippedrect, reverseflippedrect, timeleft, timeleftrect, secondsleft, beginningtimeramount, timesuptimer, timelefttimer, timerdone, turndonetimer, flipdone, previousturndone, image, secimage
  
  #Checks if the time is up
  if timeleft == 0 or timeleft == -1 or timeleft == -2:
    card1 = ''
    card2 = ''
    card1rect = pygame.Rect(0,0,0,0)
    card2rect = pygame.Rect(0,0,0,0)
    timerdone = False
    screen.fill((255,255,255))
    centertext('Time\'s up!', 25, screenrect)
    
  #Changes the turn once the timer reaches 0, resets the card values
  if timeleft == 0:

    #Checks which player's turn it is, then changes the turn to the other player
    if playerturn == 1:
      playerturn = 2
    else:
      playerturn = 1
    card1 = ''
    card2 = ''
    
    #Resets the timer 
  if timeleft == -2:
    timerdone = True
    timelefttimer = pygame.time.get_ticks() 
    secondsleft = timerchange(cardnamelist)
    timeleft = secondsleft
    pressed_amount = 0
    
  #Timer used at the very beginning; not needed after first turn is done
  if beginningtimeramount == 0:
    secondsleft = timerchange(cardnamelist)
    timeleft = secondsleft
    timelefttimer = pygame.time.get_ticks()
    beginningtimeramount += 1
    
  #Turn up timer: decreases by 1 every second
  if pygame.time.get_ticks() - timelefttimer >= 1000:
    timeleft -= 1
    timelefttimer = pygame.time.get_ticks()
    
  #Plays the game if the time isn't up
  if timeleft > 0:

    #checks if all the cards are done. If they are, goes to the game end screen
    if len(cardnamelist) == 0:
      currentState = STATE_DONE 

    #Redraws the screen, draws the score, card numbers, and the timer
    screen.fill((92, 72, 18))
    pygame.draw.rect(screen, (0,0,0), p1scorerect, 3)
    pygame.draw.rect(screen, (0,0,0), p2scorerect, 3)
    centertext('P1 Score:', 12, p1scoretitlerect)
    centertext('P2 Score:', 12, p2scoretitlerect)
    centertext(str(p1score), 20, p1scorerect)
    centertext(str(p2score), 20, p2scorerect)
    centertext('It\'s player ' + str(playerturn) + '\'s turn', 16, playerturnrect)
    centertext('Time left: ' + str(timeleft), 20, timeleftrect)
    pygame.draw.rect(screen, (92, 72, 18), (145, 400, 320, 100))
    centertext('Card 1:', 20, card1textrect)
    centertext(card1, 15, card1titlerect)
    centertext('Card 2:', 20, card2textrect)
    centertext(card2, 15, card2titlerect)

    #For dealing with the cards themselves, goes through each one individually
    for i in range(len(cardnamelist)):

      #Stops the program if it goes to a card index that doesn't exist: deleting can't change how many tiems the program loops when halfway through
      if i == len(cardnamelist):
        break

      #Deals with the cards 1 at a time, checks for collision and being clicked on
      currentrect = cardrectlist[i]
      if currentrect.collidepoint(mx, my) == True:

        #For showing if the mouse hovers over a card 
        if currentrect != card1rect and currentrect != card2rect:
          pygame.draw.rect(screen, (0,255,255), currentrect)
        if button == 1:
          #Sets animation values to zero so animation can start
          amountflip = 0
          amountreverseflip = 0
          flipTimer = pygame.time.get_ticks()

          #for setting values for the first card clicked on
          if pressed_amount == 0:

            #Checks for the display of the previous turn is done
            if previousturndone == True:
              pygame.draw.rect(screen, (92, 72, 18), (145, 400, 320, 100))
              card1 = cardnamelist[i]
              card1rect = currentrect
              card1value = i
              card2 = ''
              flipdone[0] = False
              
              # This is just for easier playing of the game during testing: displays what position the mathcing card is in
              # for j in range(len(cardnamelist)):
              #   if card1 == cardnamelist[j] and card1value != j:
              #     print(j)

          #For setting values of the second card
          if pressed_amount == 1:
            
            #Checks for dupilcates
            if card1value != i:
              if previousturndone == True:
                card2 = cardnamelist[i]
                card2rect = cardrectlist[i]
                card2value = i
                turndonetimer = pygame.time.get_ticks()
                flipdone[1] = False
                pygame.draw.rect(screen, (92, 72, 18), (145, 400, 350, 100))
                centertext('Card 1:', 20, card1textrect)
                centertext('Card 2:', 20, card2textrect)
                centertext(card1, 15, card1titlerect)
                centertext(card2, 15, card2titlerect)

          #Makes sure turn is done before allowing the button-related code to trigger
          if previousturndone == True and flipdone:
            pressed_amount += 1
            flipped_val[i] = True

      #If card wasn't hovered over
      else:

        #Draws the cards white if not hovered over or are not the ones being animated
        if currentrect != card1rect and currentrect != card2rect:
          pygame.draw.rect(screen, (255,255,255), currentrect)

      #Checks if the card shoudl be flipped, and animtes it if it is
      if flipped_val[i] == True:

        #Shortens the rect until 40 has been taken away from both sides
        if amountflip < 40:

          #Changes the amount shortened by 8 every tick (every 60 ticks becuase of the clock.tick(60), though)
          if pygame.time.get_ticks() - flipTimer >= 1:
            amountflip += 8

            #Shortens the rect to animate it
            flippedrect = pygame.Rect(currentrect[0]+amountflip, currentrect[1], currentrect[2]-amountflip*2, currentrect[3])
            pygame.draw.rect(screen, (92, 72, 18), currentrect)
            pygame.draw.rect(screen, (255,255,255), flippedrect)

            #Resets the timer for the animation to occur again when anotehr card is clicked
            flipTimer = pygame.time.get_ticks()
          else:

            #Draws the rect when not beiing changed so it doesn't flicker
            flippedrect = pygame.Rect(currentrect[0]+amountflip, currentrect[1], currentrect[2]-amountflip*2, currentrect[3])
            pygame.draw.rect(screen, (255,255,255), flippedrect)
        else:

          #Does second half of animation once the first half is done, same thing but now the card's being extended
          if amountreverseflip < 40:
            if pygame.time.get_ticks() - flipTimer >= 1:
              amountreverseflip += 8
              reverseflippedrect = pygame.Rect(flippedrect[0]-amountreverseflip, flippedrect[1], flippedrect[2]+amountreverseflip*2, flippedrect[3])
              pygame.draw.rect(screen, (92, 72, 18), currentrect)
              pygame.draw.rect(screen, (255,255,255), reverseflippedrect)
              flipTimer = pygame.time.get_ticks()
            else:
              reverseflippedrect = pygame.Rect(flippedrect[0]-amountreverseflip, flippedrect[1], flippedrect[2]+amountreverseflip*2, flippedrect[3])
              pygame.draw.rect(screen, (255,255,255), reverseflippedrect)
          else:
            
            #Sets the flipped value to false once it's finished animating
            flipped_val[i] = False
            pygame.draw.rect(screen, (255,255,255), currentrect)

            #Once done, says if the flip is done for the first card 
            # Sets the flipdone value to True corresponding to which card was clicked on
            if pressed_amount == 1:
              flipdone[0] = True
              pygame.draw.rect(screen, (92, 72, 18), (145, 400, 300, 100))

            #Draws the card header and the name of the card
              centertext('Card 1:', 20, card1textrect)
              centertext(card1, 15, card1titlerect)
            if pressed_amount == 2:
              flipdone[1] = True
              pygame.draw.rect(screen, (92, 72, 18), (145, 400, 300, 100))
              centertext('Card 1:', 20, card1textrect)
              centertext(card1, 15, card1titlerect)
              centertext('Card 2:', 20, card2textrect)
              centertext(card2, 15, card2titlerect)

              #checks if the cards match - if they do, deletes those cards' values from their respective lists
              if card1 == card2 and card1rect != card2rect:
                del cardrectlist[card1value]
                del cardnamelist[card1value]
                del flipped_val[card1value]
                
                #List becomes 1 shorter when deleted, so to delete the second value -1 is needed but only if the first card clicked is before the second one
                if card1value < card2value:
                  del cardrectlist[card2value-1]
                  del cardnamelist[card2value-1]
                  del flipped_val[card2value-1]
                else:
                  del cardrectlist[card2value]
                  del cardnamelist[card2value]
                  del flipped_val[card2value]

                #Increases the score
                if playerturn == 1:
                  p1score += 1
                else:
                  p2score += 1
              else:

                #Changes the turn if the player didn't score
                if playerturn == 1:
                  playerturn = 2
                else:
                  playerturn = 1
              beginningtimeramount = 0
      else:
        pygame.draw.rect(screen, (255,255,255), currentrect)

      #For drawing the images on the cards
      #Draws the first card's image if there's been one pressed
      if pressed_amount == 1:
  
        #Draws the card's image only if the animation is finished
        if flipdone[0] == True:

          #Displays the image if the time's not up
          if timeleft > 0:
            image = chooseimage(card1)
            screen.blit(image, card1rect)

      #For displayig the second card's image
      if pressed_amount == 2:

        #Sets previousturndone to false: this ensures one can't click on cards until the im disappear
        previousturndone = False
        if flipdone[1] == True:
          if timeleft > 0:
            secimage = chooseimage(card2)
            screen.blit(secimage, card2rect)

        #Resets values after 3 seconds have passed, allows players to click on cards again 
        if pygame.time.get_ticks() - turndonetimer >= 2000:
          card1rect = pygame.Rect(0,0,0,0)
          card2rect = pygame.Rect(0,0,0,0)
          pressed_amount = 0
          previousturndone = True
          image = ''
          secimage = ''
          for i in flipdone:
            i = False
        else:

          #Draws the image if their respective cards have finished animating for 2 seconds
          if flipdone[0] == True:
            screen.blit(image, card1rect)
          if flipdone[1] == True:
            screen.blit(secimage, card2rect)
        #Where the game code ends

    #Button for qutting 
    exitrect = pygame.Rect(20, 430, 100, 50)

    #Checks for cursor collision with the quit button
    if exitrect.collidepoint(mx, my) == True:
      pygame.draw.rect(screen, (255,0,0), exitrect)

      #Checks if the button has been left clicked
      if button == 1:
        currentState = STATE_MAIN
    else:
      pygame.draw.rect(screen, (0,100,255), exitrect)
    centertext('Quit', 20, exitrect)
  return currentState

#For drawing the instructions
def drawInstructions(mx, my, button, currentState):
  global screenrect
  screen.fill(WHITE)
  xCenteredText('Welcome to the game of memory!', 35, screenrect, (0,100,255), 50)
  xCenteredText('This game works like the classic card game memory, ', 20, screenrect, (0,0,0), 100)
  xCenteredText('which you may be familliar with.', 20, screenrect, (0,0,0), 125)
  xCenteredText('Click two cards to flip them over, ', 20, screenrect, (0,0,0), 150)
  xCenteredText('and try matching the symbols on the back of them.', 20, screenrect, (0,0,0), 175)
  xCenteredText('If they match, the cards disappear, you get a point, and you go again.', 20, screenrect, (0,0,0), 200)
  xCenteredText('If they don\'t, your oponent goes.', 20, screenrect, (0,0,0), 225)
  xCenteredText('Keep going until the cards run out.', 20, screenrect, (0,0,0), 250)
  xCenteredText('You get ten seconds per turn, but it\'ll decrease as the game goes on.', 20, screenrect, (0,0,0), 275)
  xCenteredText('Spooky, I know.', 20, screenrect, (0,0,0), 300)
  xCenteredText('Have fun! (hopefully)', 20, screenrect, (0,0,0), 325)
  xCenteredText('(Also, make sure to wait until the images disappear to click on cards again.', 20, screenrect, (0,0,0), 350)
  xCenteredText('Be respectful of the cards, yeah?)', 20, screenrect, (0,0,0), 375)

  #Draws a photo of the card game memory
  screen.blit(memory, (250, 410,0,0))
  
  #Back button
  exitrect = pygame.Rect(20, 430, 100, 50)
  if exitrect.collidepoint(mx, my) == True:
    pygame.draw.rect(screen, (255,0,0), exitrect)
    if button == 1:
      currentState = STATE_MAIN
  else:
    pygame.draw.rect(screen, (0,100,255), exitrect)
  centertext('<- Back', 20, exitrect)
  return currentState

#Draws the endscreen, triggers once all the cards are gone
def drawDoneGame(mx, my, button, currentState):

  #Resets all teh game values so the game can be played again
  values()

  #Checks who won, the endscreen displays text depending
  if p1score > p2score:
    winningtext = 'Congratulations player 1! You win!'
  elif p2score > p1score:
    winningtext = 'Congratulations player 2! You win!'
  else:

    #I will be geninely impressed if anyone ever gets this screen
    winningtext = 'Uh...I guess you tie. Good job?'

  #Draws the actual screen
  screen.fill((255,255,255))
  xCenteredText('Game over', 35, screenrect, (0,0,0), 200)
  xCenteredText(winningtext, 25, screenrect, (0,0,0), 300)

  #Givers player option to play again or go back to the main menu
  playagainrect = pygame.Rect(200, 350, 400, 40)
  exitrect = pygame.Rect(200, 400, 400, 40)

  #Draws the two buttons
  buttonrectlist = [playagainrect, exitrect]
  for i in range(2):
    currentrect = buttonrectlist[i]

    #For highlighting upon hover
    if currentrect.collidepoint(mx, my) == True:
      pygame.draw.rect(screen, (255,0,0), currentrect)
      if button == 1:
        if currentrect == playagainrect:
          currentState = STATE_PLAY
        else:
          currentState = STATE_MAIN
    else:

      #For if there's no cursor on the currentrect
      pygame.draw.rect(screen, (0,100,255), currentrect)

  #Draws options on the buttons
  centertext('Play Again', 20, playagainrect)
  centertext('Main Menu', 20, exitrect)
  
  return currentState

#Sets all the various values needed in the game, makes them global variables - I might pass out if I had to label all of them but the names hsoudl be self-explanatory - the reason tehere's so amny rects is that I prefer to have centered text over just randomly drawing the question
def values():
  global cardrectlist, cardnamelist, xcoordlist, ycoordlist, cardnamelist, button_val, flipped_val, pressed_amount, card1, card2, card1rect, card2rect, numcards, timeleft, timeleftrect, p1scorerect, p2scorerect, p1scoretitlerect, p2scoretitlerect, p1score, p2score, card1textrect, card1titlerect, card2textrect, card2titlerect, playerturnrect, playerturn, screenrect, amountflip, flipTimer, flippedrect, amountreverseflip, reverseflippedrect, timeleft, timeleftrect, secondsleft, beginningtimeramount, timerdone, timelefttimer, turndonetimer, flipdone, previousturndone, image, secimage
  xcoordlist = []
  ycoordlist = []
  coordlist =[]
  cardnamelist = []
  cardrectlist = []
  button_val = False
  flipped_val = []
  pressed_amount = 0
  card1 = ''
  card2 = ''
  numcards = 32
  p1scorerect = pygame.Rect(660, 440, 60, 60)
  p2scorerect = pygame.Rect(730, 440, 60, 60)
  p1scoretitlerect = pygame.Rect(660, 420, 60, 20)
  p2scoretitlerect = pygame.Rect(730, 420, 60, 20)
  p1score = 0
  p2score = 0
  card1textrect = pygame.Rect(170, 400, 125, 50)
  card1titlerect = pygame.Rect(170, 430, 125, 50)
  card2textrect = pygame.Rect(330, 400, 125, 50)
  card2titlerect = pygame.Rect(330, 430, 125, 50)
  playerturnrect = pygame.Rect(505, 400, 125, 50)
  timeleftrect = pygame.Rect(530, 440, 65, 50)
  secondsleft = 10
  timelefttimer = 0
  playerturn = 1
  screenrect = pygame.Rect(0,0,800,500)
  amountflip = 0
  amountreverseflip = 0
  flipTimer = 0
  timesuptimer = 0
  card1rect = pygame.Rect(0,0,0,0)
  card2rect = pygame.Rect(0,0,0,0)
  flippedrect = ''
  reverseflippedrect = ''
  beginningtimeramount = 0
  timelefttimer = 0
  timeleft = secondsleft
  timerdone = False
  turndonetimer = 0
  previousturndone = True
  flipdone = [True, True]
  image = ''
  secimage = ''
  #Loads all the images
  
  #List of all the text for the cards
  cardnamelist = ['Eye strain', 'Eye strain', 'Damages nature', 'Damages nature', 'Social Isolation', 'Social Isolation', 'Depression', 'Depression', 'Carpal tunnel', 'Carpal tunnel', 'Misinformation', 'Misinformation', 'Loss of privacy', 'Loss of privacy', 'Distracting', 'Distracting', 'Cyberbullying', 'Cyberbullying', 'Doxxing', 'Doxxing', 'Toxic Groups', 'Toxic Groups', 'Spinal Rounding', 'Spinal Rounding', 'Lower Attention', 'Lower Attention', 'Parasocial Relations', 'Parasocial Relations', 'Stalking', 'Stalking', 'Viruses', 'Viruses']
  random.shuffle(cardnamelist)
  #Gets all the coordinates for the various cards
  for i in range(20, 780, 95):
    xcoordlist.append(i)
  for i in range(20, 400, 100):
    ycoordlist.append(i)
  for i in range(len(cardnamelist)):
    flipped_val.append(False)
  #Creates a new list of coordinates in an 8x4 grid
  for i in range(len(ycoordlist)):
    for j in range(len(xcoordlist)):
      cardrectlist.append(pygame.Rect(xcoordlist[j], ycoordlist[i], 80, 70))
      
running = True
myClock = pygame.time.Clock()
currentState = STATE_MAIN
mx = my = button = 0

#Loads in and changes the size of all the images
brainPic = pygame.image.load("brain.jpeg") 
brainPic = pygame.transform.scale(brainPic, (800, 500))
attention = pygame.image.load("attention.jpeg") 
attention = pygame.transform.scale(attention, (80, 70))
eye = pygame.image.load("eyestrain.jpeg") 
eye = pygame.transform.scale(eye, (80, 70))
carpal = pygame.image.load("Carpal tunnel.jpeg") 
carpal = pygame.transform.scale(carpal, (80, 70))
cyberbullying = pygame.image.load("cyberbullying.jpeg") 
cyberbullying = pygame.transform.scale(cyberbullying, (80, 70))
depression = pygame.image.load("depression.png") 
depression = pygame.transform.scale(depression, (80, 70))
distracting = pygame.image.load("distracting.jpeg") 
distracting = pygame.transform.scale(distracting, (80, 70))
doxxing = pygame.image.load("doxxing.jpeg") 
doxxing = pygame.transform.scale(doxxing, (80, 70))
eyestrain = pygame.image.load("eyestrain.jpeg") 
eyestrain = pygame.transform.scale(eyestrain, (80, 70))
misinfo = pygame.image.load("Misinfo.jpeg") 
misinfo = pygame.transform.scale(misinfo, (80, 70))
nature = pygame.image.load("nature damage.jpeg") 
nature = pygame.transform.scale(nature, (80, 70))
parasocial = pygame.image.load("parasocial.jpeg") 
parasocial = pygame.transform.scale(parasocial, (80, 70))
privacy = pygame.image.load("privacy.jpeg") 
privacy = pygame.transform.scale(privacy, (80, 70))
social = pygame.image.load("Social Isolation.jpeg") 
social = pygame.transform.scale(social, (80, 70))
spinal = pygame.image.load("spinal rounding.jpeg") 
spinal = pygame.transform.scale(spinal, (80, 70))
stalking = pygame.image.load("stalking.jpeg") 
stalking = pygame.transform.scale(stalking, (80, 70))
virus = pygame.image.load("virus.jpeg") 
virus = pygame.transform.scale(virus, (80, 70))
memory = pygame.image.load("memory.jpeg") 
memory = pygame.transform.scale(memory, (300, 70))
toxic = pygame.image.load("toxic.jpeg") 
toxic = pygame.transform.scale(toxic, (80, 70))
white = pygame.image.load("white.png") 
white = pygame.transform.scale(white, (80, 70))

#Resets values to default
#Sets the cordinates and card names
values()
while running:   # this is our game loop
  button = 0
  # Check all the events that happen
  for evnt in pygame.event.get():
    # if the user tries to close the window, then raise the "flag"
    if evnt.type == pygame.QUIT:
      running = False
    if evnt.type == pygame.MOUSEBUTTONDOWN:
      mx, my = evnt.pos
      button = evnt.button
    if evnt.type == pygame.MOUSEMOTION:
      mx, my = evnt.pos
    if evnt.type == pygame.KEYDOWN:
      key = evnt.unicode

  if currentState == STATE_MAIN:
    currentState = drawMenu(mx, my, button, currentState)
  elif currentState == STATE_EXIT:
    running = False
  elif currentState == STATE_PLAY:
    currentState = drawPlay(mx, my, button, currentState)
  elif currentState == STATE_INSTRUCTIONS:
    currentState = drawInstructions(mx, my, button, currentState)
  elif currentState == STATE_DONE:
    currentState = drawDoneGame(mx, my, button, currentState)
  # waits long enough to have 60 fps
  pygame.display.flip()
  myClock.tick(60)

pygame.quit()
