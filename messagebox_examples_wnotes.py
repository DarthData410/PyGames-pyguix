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

import pygame
import pyguix.ui.elements as ui 

def run():
    pygame.init()
    window = pygame.display.set_mode((600,400))
    clock = pygame.time.Clock()
    run = True

    all = pygame.sprite.RenderUpdates()

    while run:
        pygame.display.update()
        clock.tick(40)
        event_list = pygame.event.get()
        
        window.fill((0,0,0)) # clear test window
        all.draw(window)

        for event in event_list:
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m: # <- NOTE: Press 'M' key to launch message.
                    
                    #####################################
                    # NOTE: Implementation: 
                    # Upon pressing KEYDOWN event.type for key 'm' create an instance
                    # of the pyguix.ui.elements.MessageBox class. (pygame.sprite.Sprite)
                    msgbox = ui.MessageBox(
                        window=window, # pygame active display window
                        message_text="Are you sure? ABCDEFGHIJKLMNOPQRSTUVWXYZ", # message text to appear. (will trim for safe render)
                        title="Infomation (Yes/No/?)", # title of message box
                        buttons=("Yes","No","?"), # number of buttons and string values
                        # NOTE: You can set the width and height of the MessageBox or accept the defaults.
                        width=340, # width 
                        height=180 # height
                    )

                    # NOTE: Call to active MessageBox instance .wait(event_list) function. 
                    # Will return True until a button is clicked. Then it will return False.
                    # True = (yes).wait(), False (no don't).wait()
                    while msgbox.wait(event_list):
                        # NOTE: Update event_list sent in:
                        event_list = pygame.event.get()

                    # NOTE: Simple print() of the msgbox.get_clicked() function.
                    # This will return the button that was clicked from the active MessageBox
                    # instance. 
                    print(msgbox.clicked())
                    
                    # NOTE: MessageBox.canceled() allows post user interaction to determine if MessageBox was simply closed
                    # without choice of buttons sent for user to select from.:
                    if msgbox.canceled():
                        print("You canceled the MessageBox instance.")
                    

                    window.fill((0,0,0)) # Clear test screen
                    
                    pygame.time.delay(200) # Slight delay for demo purposes.

                    # NOTE: Next MessageBox using .clicked() value of previous MessageBox, accepting more defaults.
                    # Includes sending in event_list which will turn on 'self-contained' mode and expect caller to
                    # operate on MessageBox.canceled()[bool] and MessageBox.clicked()[str] values, post user interaction. 
                    msgbox2 = ui.MessageBox(
                        window=window,
                        message_text=("You clicked: %s" % msgbox.clicked()),
                        title="information",
                        event_list=pygame.event.get(),
                        theme="MessageBox_orange.json", #<-NOTE: using custom JSON theme file named MessageBox_orange.json
                        rg=all #<-NOTE: pygame.sprite.RenderUpdates() group passed in for usage, vs. instance within class.
                    )
                    # NOTE: Remove instance of MessageBox class from all sprite groups.
                    # comment out the following and the MessageBox sprite will stay actively drawn as part of the
                    # game loop.:
                    msgbox2.remove(all) 
                        
                    # NOTE: Simple print() of the msgbox.get_clicked() function.
                    # This will return the button that was clicked from the active MessageBox
                    # instance. 
                    print(msgbox2.clicked())
                    if msgbox2.canceled():
                        # NOTE: Do some logic based on MessageBox.canceled()[bool] = True:
                        print("You canceled the 2nd MessageBox instance.")
                    window.fill((0,0,0)) # Clear test screen

                    # NOTE: Next MessageBox shows off another JSON theme file.
                    msgbox = ui.MessageBox(
                        window=window,
                        message_text=("You clicked: %s" % msgbox2.clicked()),
                        title="information",
                        event_list=pygame.event.get(),
                        theme="MessageBox_blue.json" #<-NOTE: using custom JSON theme file named MessageBox_blue.json
                    )
                        
                    # NOTE: Simple print() of the msgbox.get_clicked() function.
                    # This will return the button that was clicked from the active MessageBox
                    # instance. 
                    print(msgbox.clicked())
                    if msgbox.canceled():
                        # NOTE: Do some logic based on MessageBox.canceled()[bool] = True:
                        print("You canceled the 3nd MessageBox instance.")
                    window.fill((0,0,0)) # Clear test screen

                    # NOTE: Next MessageBox shows off another JSON theme file.
                    msgbox = ui.MessageBox(
                        window=window,
                        message_text=("You clicked: %s" % msgbox.clicked()),
                        title="information",
                        event_list=pygame.event.get(),
                        theme="MessageBox_red.json" #<-NOTE: using custom JSON theme file named MessageBox_blue.json
                    )
                        
                    # NOTE: Simple print() of the msgbox.get_clicked() function.
                    # This will return the button that was clicked from the active MessageBox
                    # instance. 
                    print(msgbox.clicked())
                    if msgbox.canceled():
                        # NOTE: Do some logic based on MessageBox.canceled()[bool] = True:
                        print("You canceled the 4nd MessageBox instance.")
                    window.fill((0,0,0)) # Clear test screen

                    # NOTE: Next MessageBox shows off another JSON theme file.
                    msgbox = ui.MessageBox(
                        window=window,
                        message_text=("You clicked: %s" % msgbox.clicked()),
                        title="information",
                        event_list=pygame.event.get(),
                        theme="MessageBox_green.json" #<-NOTE: using custom JSON theme file named MessageBox_blue.json
                    )
                        
                    # NOTE: Simple print() of the msgbox.get_clicked() function.
                    # This will return the button that was clicked from the active MessageBox
                    # instance. 
                    print(msgbox.clicked())
                    if msgbox.canceled():
                        # NOTE: Do some logic based on MessageBox.canceled()[bool] = True:
                        print("You canceled the 5nd MessageBox instance.")


                window.fill((0,0,0)) # Clear test screen          
                    
        pygame.display.update()

if __name__ == '__main__':
    run()
    pygame.quit()
    exit()