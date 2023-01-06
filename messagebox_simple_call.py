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
                    # NOTE: Most basic, self contained MessageBox instance possible:
                    mb = ui.MessageBox(
                        window=window, 
                        event_list=pygame.event.get()
                    )

                    # NOTE: Act upoon if the MessageBox was canceled, if not can act upon the .clicked() value.:
                    if not mb.canceled():
                        print(mb.clicked())
                    else:
                        print("You canceled the MessageBox instance.")
                    
                    window.fill((0,0,0)) # NOTE: Simple clear of screen. Would have draw() logic, blit() in real game.

                    # NOTE: Still basic MessageBox but passing in Title and Message to display:
                    mb = ui.MessageBox(
                        window=window,
                        title="Simple Title",
                        message_text="Some simple text message",
                        event_list=pygame.event.get()
                    )
                    print(mb.clicked())

                    window.fill((0,0,0))
            
        pygame.display.update()

if __name__ == '__main__':
    run()
    pygame.quit()
    exit()