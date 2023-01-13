# PyGames-pyguix (PYGame User Interface eXtreme (PYGUIX))
By: J. Brandon George | darth.data410@gmail.com | twitter: @PyFryDay | medium.com: https://darth-data410.medium.com/
license found @: PyGames-pyguix/LICENSE (Apache License Version 2.0 Janurary 2004)

# demo details:
A quick demo to see all current active pyguix.ui.elements in action can be found in the root for pyguix folder, named __ui_elements_demo_all1.py__ 

Futher you can find an introduction article for this project on medium, located here: <a href="https://darth-data410.medium.com/how-to-easily-create-pygame-user-interface-and-heads-up-display-elements-3b1bf424a2c8">How-To: Easily Create PyGame User Interface and Heads Up Display Elements</a>

# pyguix.ui.elements.MessageBox:
1. pyguix.ui.elements.MessageBox(pygame.sprite.Sprite) pygame message box user interface class. 
    
    1. Simple implementation:

        import pygame
        import pyguix.ui.elements as ui

        ui.MessageBox(
            window = self.window,
            event_list=pygame.event.get()
        )

        #NOTE: above simple example generates with all defaults for title, buttons, etc. (ie: 'OK')

    2. Respond to msgbox.canceled() | msgbox.clicked() button implementation:

        import pygame #<---NOTE: must import pygame
        import pyguix.ui.elements as ui #<---NOTE: assumes deployment as subdirectory of main module *.py file

        #NOTE: pygame init code and game loop logic here...

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

    3. MessageBox class init variable details:
        1. window = pygame.display(Surface)[REQUIRED]
        2. message_text = (str) [default=ut.MSGBOX_TXT]
        3. title = (str) [default=ut.MSGBOX_TXT]
        4. buttons = (tuple(str,)) [default=(ut.MSGBOX_TXT,)]
        5. width = (int) [default=ut.MSGBOX_WIDTH]
        6. height = (int) [default=ut.MSGBOX_HEIGHT]
        7. event_list = (list[pygame.event.Event]) [default=None]
        8. theme = (str) [default=ut.DEFAULT_JSONTHEME]
        9. rg = (pygame.sprite.RenderUpdates()) [default=None] 
            *NOTE: if passed in value is of type(pygame.sprite.RenderUpdates()) is detected then this is used for rendering MessageBox to display. Otherwise will create and use an intrenal pygame.sprite.RenderUpdates() group.
     
    4. pyguix.ui.elements.py = location of MessageBox class def
    
    5. pyguix. _ _ utils _ _ . _ _ help _ _ .py = all constants, dataclasses, theme classes, theme base class, utility source code / class used as 'helper' to elements.py
    
    6. Further example implementions found in pygames-pyguix/messagebox_simple_call.py
    
    7. More detailed examples and testing found in pygames-pyguix/messagebox_examples_wnotesa.py

    8. Detailed examples when keeping a MessageBox instance active during a game loop, and intracting with the MessageBox while the game continues to run can be found at pygames-pyguix/messagebox_examples_wnotesb_gameloop.py

# pyguix.ui.elements.PopupMenu:
2. pyguix.ui.elements.PopupMenu(pygame.sprite.Sprite) pygame message box user interface class.
    
    1. Implementation steps can be found in __popup_simple_call.py__ with greater details and more advanced examples found in __popup_examples_wnotes.py__.
        
        1. Finally you can also find a break down of steps as follows.   

            1. __STEP1:__ Define the PopupMenuActions inherited class(es).
            
            2. __STEP2:__ Create context JSON file. (pyguix.ui.context location)

                1. <b>(reference pyguix.ui.context section below)</b> 

            3. __STEP3:__ Initialize __*ANY*__ PopupMenuAction class(es).
                
                1. ClassName(window,render_group) *NOTE: Create new instance is that is required. Stored in dict() variables within pyguix.ui.elements and used properly via mapping supplied in JSON context file, relating to contextof targeted Sprite classes.  
                 
            4. __STEP4:__ Detect type=pygame.event.MOUSEBUTTONDOWN / button=pygame.BUTTON_RIGHT
                1. Sample code for pygame.BUTTON_RIGHT:
                    
                    ui.PopupMenu.clearall(pu)
                    #Create new instance of ui.PopupMenu:
                    #NOTE: Using theme/default.json for theme color scheme:
                    pu = ui.PopupMenu(
                        window=window,
                        target_mouse_pos=pygame.mouse.get_pos(),
                        rg=all
                    )

                    #--------------
                    #NOTE: The above instance only needs to be delcared once, even when multiple PopupMenus are used. 
                    #Based on context mapping found in the contet JSON file is how the pyguix.ui.elements.PopupMenu 
                    #instance determines contextof for specific collided Sprite class. 
                    #If nothing can be found, then by default no PopupMenu will be shown.
                    #--------------
                
            5. __STEP5:__ Detect type=pygame.event.MOUSEBUTTONDWON / button=pygame.BUTTON_LEFT
                1. Sample code for button=pygame.BUTTON_LEFT:

                    if event.button == pygame.BUTTON_LEFT:
                    
                    #NOTE: STEP5: If PopupMenu instance active then call 
                    #PopupMenu.clicked() passing in event_list:
                    if isinstance(pu,ui.PopupMenu):
                        pu.clicked(event_list) 
            
            6. __STEP6:__ Check if 'PopupMenu' variable isinstance() of ui.PopupMenu and if so call .update()
                1. Sample code for isinstance() check:
                
                    if isinstance(pu,ui.PopupMenu):
                        pu.update()
    
    2. Custom pyguix.ui.context.*.json context files to define PopupMenu's, MenuItems and Actions. ('_ _ utils _ _ . _ _ help _ _.PopupMenuContext(context)') 

    3. pyguix.ui.elements.PopupMenuItem(pygame.Surface) is a class used to build PopupMenu items generated for contextof targets for PopupMenu(s).

    4. pyguix.ui.elements.PopupMenuActons(object) is a base class meant to have inherited classes derived from it. These classes should map to pyguix.ui.context.(name).json context file. These classes contain functions that PopupMenuItem actions are mapped 1:1 with.  

# pyguix.ui.elements.SnapHUD:
3. pyguix.ui.elements.SnapHUD(pygame.sprite.Sprite) is a heads up display (HUD) ui element, designed to 'snap' open or close by a single click.

    1. Location determined by pyguix.ui.settings.(settings_file).json. The initial default settings file for SnapHUD elements is named SnapHUD.json. This element used several sub-classes, that allow for easy setup of multiple display parts (SnapHUDPart inherited classes. ie: SnapHUDPartText) for showing in-game information to a player. 
    
    This interaction is handled by mapping display parts, to functions of a SnapHUDPartInfo inherited class/object instance. A class created and inherited from SnapHUDPartInfo with bound functions created to allow for SnapHUDParts the ability to 'listen' for updates to display to user. Using the defaults, you can easily have a heads up display that can be 'Open' or 'Closed', showing important game updates. 
    
    Like all other pyguix ui elements, SnapHUD uses the theme concept, allowing for a ui.globaltheme() to be set and all ui elements implemented in a game instance will take advantage of suppied theme. 

    2. There are still several items in development for SnapHUD.
        1. Alignment to Left or Right side. Right now, only Right side alignment
        2. Adding more part types other than just Text
        3. Finalize code placement within self-contained bound functions. (ie: some clean up in .update())
    
    3. You can find example implementation, with NOTE(s) and steps for this ui element in the pyguix root folder, named: __snaphud_example_wnotes.py__

    4. The following are defaults supplied as part of this ui element.:
        1. pyguix.ui.context.SnapHUD_default.json - Mapping file for example SnapHUD example. Note the infoclass, and function. If you add/remove parts then that is reflected in the SnapHUD element in game found in the supplied snaphud_example_wnotes.py
        2. pyguix.ui.settings.SnapHUD.json - Default settings file for SnapHUD element usage in game. 

# pyguix.ui.themes
4. Custom JSON file themes can be easily created. Select an existing *.json file, copy it, make changes and give it a unique name. Save it in the pyguix.ui.themes folder. (ie: select default.json, make changes and save as (themename).json).
        
    1. Implementation of new JSON themes is an easy task. Simply pass in as part of creating a new instance of a ui.(element), like ui.MessageBox(theme="ex_blue.json") or setting the <b>ui.globaltheme(theme="ex_red.json").</b> <b>NOTE:</b> When ui.globaltheme() value is supplied, then that value overrides any instance specific value supplied.
        
    2. If JSON theme file passed in can be found in pyguix.ui.themes and is valid per ui.ElementTheme class, then theme will be applied. [ie: When passed in for ui.<i>element</i>(theme="ex_blue.json"), the ElementTheme class, found in pyguix._ _ utils _ _ . _ _ help _ _.py is employed in loading the pyguix.ui.elements.* classes, and validates the passed in JSON theme. If ANY part of validation fails, the ElementTheme class will notify in terminal, and revert to constant DEFAULT_JSONTHEME provided value for JSON theme file to load.]

    3. The following list of themes are supplied, as examples, within the themes subfolder: 
        1. default.json
        2. ex_blue.json
        3. ex_green.json
        4. ex_orange.json
        5. ex_red.json

# pyguix.ui.settings
5. The settings JSON files, are pyguix.ui.element(s) specific. There is expected to have ONE per ui element, at least. Multiple can exist, but need to follow the expected settings format of that given ui.(element). Example JSON settings files are provided, which are recommended to keep as a base to copy from. Then you can copy, make your own, and supply the desired (named).JSON settings file.  

    1. The following list are currently shipped settings.JSON files:
        1. MessageBox.json
        2. PopupMenu.json
        3. SnapHUD.json
        4. *IN DEV* EventTopicHUD.json *IN DEV*

# pyguix.ui.context
6. The JSON context files found in pyguix.ui.context are element specific, and are not implemented for all elements. Each element has its specific context format, with some similar attributes. Review provided examples for more details. The important aspect to note about context.json files is how they interact with specific class types, enabling the reflection development concepts to execute defined functions for 'PopupMenu Actions' or for updating SnapHUDPartText values, for example. 

    1. The following is a list of currently shipped context.JSON files:
        1. ex_BoatSprite_menu.json -> Implemented in popup_examples_wnotes.py
        2. ex_Popup_Simple_Call_menu.json -> Implemented in popup_simple_call.py
        3. ex_RiverSprite_menu.json -> Implemented in popup_examples_wnotes.py
        4. ex_TreeSprite_menu.json -> Implemented in popup_examples_wnotes.py & ui_elements_demo_all1.py
        5. PopupMenu_default.json -> (blank no-context menu) implemented by default everywhere
        6. SnapHUD_default.json -> Implemented in snaphud_example_wnotes.py
        7. *IN DEV* EventTopicHUD_default.json -> *IN DEV* 

# pyguix deployment
7. (NOTE: DEPLOYMENT SECTION AND PIP INSTALL SLATED FOR DEVELOPMENT. CLONE REPO AND USE AS YOU DESIRE AND AT YOUR OWN RISK. REFER TO LICENSE FILE FOR FURTHER DETAILS.) 

# pyguix planned development & notes:
8. Upcoming Development:
    1. UI elements slated for development:
        1. EventTopicHUD(pygame.sprite.Sprite(s)/Surface(s)) 
        2. GameOptions(pygame.sprite.Sprite/Surface(s))
        3. GameScene(pygame.Surface)
    2. Deployment / install:
        1. Establish a 'pip install' for pyguix, create and test
            1. Test for *nix OS
            2. Test for Win OS
            3. Test for MacOS