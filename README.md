# PyGames-pyguix
# PYGame User Interface eXtreme (PYGUIX)
# By: J. Brandon George | darth.data410@gmail.com | twitter: @PyFryDay
# license found @: PyGames-pyguix/LICENSE (Apache License Version 2.0 Janurary 2004)
# Project started in: 12/2022

# pyguix.ui.elements.MessageBox:
1. pyguix.ui.elements.MessageBox(pygame.sprite.Sprite) pygame message box user interface class. 
    a. Simple implementation:

        import pygame #<---NOTE: must import pygame
        import pyguix.ui.elements as ui #<---NOTE: assumes deployment as subdirectory of main module *.py file

        # NOTE: pygame init code and game loop logic here...

        msgbox = ui.MessageBox(
            window=window, #NOTE: pygame.display (active display surface)
            message_text="Simple MessageBox", #NOTE: text to display on MessageBox
            title="Simple", #NOTE: title of MessageBox
            event_list=event_list #NOTE: current game loop event_list - when passed, while MessageBox.wait(): not needed.
        )

        if msgbox.canceled():
            print("Canceled ui.MessageBox detected")
        else:
            print(msgbox.clicked()) #<---NOTE: will print 'OK' since default button(s) of 'OK' used with above example.
    
    # MessageBox class variable details
    b. MessageBox class implementation variable details:
        1. window = pygame.display(Surface)[REQUIRED]
        2. message_text = (str) [default=ut.MSGBOX_TXT]
        3. title = (str) [default=ut.MSGBOX_TXT]
        4. buttons = (tuple(str,)) [default=(ut.MSGBOX_TXT,)]
        5. width = (int) [default=ut.MSGBOX_WIDTH]
        6. height = (int) [default=ut.MSGBOX_HEIGHT]
        7. event_list = (list[pygame.event.Event]) [default=None]
        8. theme = (str) [default=ut.MSGBOX_DEFAULT_JSONTHEME]
        9. rg = (pygame.sprite.RenderUpdates()) [default=None] 
            *NOTE: if passed in value is of type(pygame.sprite.RenderUpdates()) is detected then this is used for rendering MessageBox to display. Otherwise will create and use an intrenal pygame.sprite.RenderUpdates() group.
     
    c. pyguix.ui.elements.py = location of MessageBox class defition
    d. pyguix.__utils__.__help__.py = all constants, dataclasses, theme classes, theme base class, utility source code / class used as 'helper' to elements.py
    e. Further example implementions found in pygames-pyguix/messagebox_simple_call.py
    f. More detailed examples and testing found in pygames-pyguix/messagebox_examples_wnotes.py

    # Custom MessageBox JSON Theme File Creation:
    g. Custom JSON file themes can be easily created. Select an existing *.json file, copy it, make changes and give it a unique name. Save it in the pyguix.ui.themes folder. (ie: select MessageBox_default.json, make changes and save as MessageBox_(themename).json).
        a. Implementation of new JSON theme is easy, simply pass in as part of creating a new instance of a ui.(element), like ui.MessageBox(theme="MessageBox_blue.json").
        b. If JSON theme file passed in can be found in pyguix.ui.themes and is valid per ui.(element)Theme class, then theme will be applied. [ie: When passed in for ui.MessageBox(theme="MessagBox_blue.json"), the MessageBoxTheme class, found in pyguix.__utils__.__help__.py is employed in loading the pyguix.ui.elements.MessageBox class, and validates the passed in JSON theme. If ANY part of validation fails, the MessageBoxTheme class will notify in terminal, and revert to constant MSGBOX_DEFAULT_JSONTHEME provided value for JSON theme file to load.]

# pyguix.ui.elements.PopupMenu: (IN DEVELOPMENT)
2. pyguix.ui.elements.PopupMenu(pygame.sprite.Sprite) pygame message box user interface class.
    a. This class is currently in DEVELOPMENT, and therefore not ready for use.
    b. Custom pyguix.ui.context.*.json context files to define PopupMenu's, MenuItems and there Actions currently in DEVELOPMENT, and therefore not ready for use. (__utils__.__help__.PopupMenuContext(context))

# pyguix.ui.elements.PopupMenuItem: (IN DEVELOPMENT)
3. pyguix.ui.elements.PopupMenuItem(pygame.Surface) surface interface class used by PopupMenu.
    a. This class is currently in DEVELOPMENT, and therefore not ready for use.

# pyguix.ui.elements.PopupMenuActions: (IN DEVELOPMENT)
4. pyguix.ui.elements.PopupMenuActions(object) class used with PopupMenu and __utils__.__help__.PopupMenuContext to define PopupMenu's, MenuItems and actions from user interaction.
    a. This class is currently in DEVELOPMENT, and therefore not ready for use.

# pyguix current structure:
3. Breakdown of structure:
        PyGames-pyguix:
                -> pyguix
                        -> __utils__
                                -> __help__.py
                        -> ui
                                -> context
                                        -> PopupMenu_default.json
                                        -> PopupMenu_sprites.json
                                -> themes
                                        -> MessageBox_blue.json
                                        -> MessageBox_default.json
                                        -> MessageBox_green.json
                                        -> MessageBox_orange.json
                                        -> MessageBox_red.json
                                -> elements.py
                -> LICENSE
                -> messagebox_examples_wnotes.py
                -> messagebox_simple_call.py
                -> popup_testing.py (IN DEV)
                -> README.md
                -> TreeSprite.gif

# pyguix deployment
4. (NOTE: DEPLOYMENT SECTION AND PIP INSTALL SLATED FOR DEVELOPMENT. CLONE REPO AND USE AS YOU DESIRE AND AT YOUR OWN RISK. REFER TO LICENSE FILE FOR FURTHER DETAILS.) 

# pyguix planned development & notes:
5. Upcoming Development:
    a. General elements / task:
        1. Merge of JSON theme files, to allow single color/font theme across multiple or specific ui class instances.
    b. UI elements slated for development:
        1. PopupMenu(pygame.sprite.Sprite) (IN DEV)
            a. PopupMenuItem(pygame.Surface) (IN DEV)
            b. PopupMenuActions(object) (IN DEV)
        2. GameOptions(pygame.sprite.Sprite)
        3. GameScene(pygame.Surface)
    c. Deployment / install:
        1. Establish a 'pip install' for pyguix, create and test
            a. Test for *nix OS
            b. Test for Win OS
            c. Test for MacOS
