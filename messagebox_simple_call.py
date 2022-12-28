# PyGames-pyguix
# made with: pygame 2.1.2 (SDL 2.0.16, Python 3.10.6)
# using: vscode ide
# By: J. Brandon George | darth.data410@gmail.com | twitter: @PyFryDay
# Copyright 2022 J. Brandon george
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

    window.fill((0,0,0))

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
                        title="Simple"
                    )

                    # Operate upon MessageBox.wait() and perform some logic while waiting.:
                    while msgbox.wait(event_list):
                        event_list = pygame.event.get()

                    print(msgbox.clicked())
                    
                    if msgbox.canceled():
                        print("MessageBox instance was canceled.")

                    window.fill((0,0,0))               
                    #########################################

                    #########################################
                    # NOTE: Simple MessageBox example code, in 'self-contained' mode, 
                    # passing event_list in at init() of instance.
                    msgbox = ui.MessageBox(
                        window=window,
                        message_text="Simple contained example MessageBox",
                        title="Simple Self Contained",
                        width=300, # Expand width to show full message for example.
                        event_list=pygame.event.get(),
                        theme="MessageBox_orange.json" #<-NOTE: passing in custom JSON theme named: MessageBox_orange.json
                    )

                    if msgbox.canceled():
                        print("MessageBox instance was canceled. (self-contained mode example)")
                    else:
                        print(msgbox.clicked())
                    
                    window.fill((0,0,0))
                    ##########################################

        pygame.display.update()

if __name__ == '__main__':
    run()
    pygame.quit()
    exit()