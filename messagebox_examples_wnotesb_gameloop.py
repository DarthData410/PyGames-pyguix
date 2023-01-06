# PyGames-pyguix
# made with: pygame 2.1.2 (SDL 2.0.16, Python 3.10.6)
# using: vscode ide
# By: J. Brandon George | darth.data410@gmail.com | twitter: @PyFryDay
# Copyright 2022 J. Brandon George
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import random
import pygame
import pyguix.ui.elements as ui 

def run():
    pygame.init()
    window = pygame.display.set_mode((600,400))
    clock = pygame.time.Clock()
    run = True

    window.fill((0,0,0))
    msgbox = None
    rg = pygame.sprite.RenderUpdates()

    while run:
        pygame.display.update()
        clock.tick(40)
        event_list = pygame.event.get()
        for event in event_list:
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m: # <- NOTE: Press 'M' key to launch message.
                    
                    #########################################
                    # NOTE: Simple MessageBox example code, using MessageBox_default.json theme
                    msgbox = ui.MessageBox(
                        window=window, 
                        message_text="Simple MessageBox",
                        title="Simple",
                        rg=rg #<-NOTE: Key for NOT generating internal RenderUpdates group.
                    )
            
            if isinstance(msgbox,ui.MessageBox): #<- NOTE: Making sure msgbox variable is type of ui.MessageBox vs. None, etc.
                if not msgbox.wait(event_list): #<- NOTE: If no longer waiting for user input
                    mbclicked= msgbox.clicked() #<- NOTE: Get the clicked() value for which button was clicked. Returned as button text.
                    msgbox.remove(rg)
                    window.fill((0,0,0))

                    #########################################
                    # NOTE: Simple MessageBox example code, in 'self-contained' mode, 
                    # passing event_list in at init() of instance.
                    theme = random.choice(["ex_orange.json","ex_red.json","ex_green.json","ex_blue.json"])
                    msgbox = ui.MessageBox(
                        window=window,
                        message_text=("You clicked the %s button" % mbclicked),
                        title="Previous Click Event",
                        width=350, # Expand width to show full message for example.
                        event_list=pygame.event.get(),
                        theme=theme #<-NOTE: passing in custom, random, JSON theme file name
                    )
                    # NOTE: rg not supplied, therefore MessageBox event loop contained WITHIN MessageBox
                    
                    window.fill((0,0,0))

                    if msgbox.canceled():
                        run = False
                        print("You clicked (X) cancel button, or hit the 'Esc' key. Goodbye!")
                    ##########################################


        pygame.display.update()

if __name__ == '__main__':
    run()
    pygame.quit()
    exit()