# Overview

## Description
Underworld Heist is a simple platformer made with the python language and the arcade library. In the game the player uses a grenade launcher to fight his/her way through a horde of tentacle monsters in search of the ancient golden eye relic.
## Purpose
My first purpose in making this game is to understand how video games are made. I have learned how the flow of the game works, as well as how to use object classes and list of object classes to update and render sprites. My second purpose in making this game is to learn how to implement mathmatics, physics, and other real world concepts into software development. 
## How To Play
When the game first loads you will see a title screen with the prompt "click to continue". The next screen gives a tutorial on the controls, and the objective of the game. When the player clicks out of the tutorial the game begins. Your character can be moved left to right using the sideways arrow keys (or A and D), and can jump using the up arrow key (or W). When the mouse is moved across the screen the player aims the grenade launcher at the cursor, then when the left mouse button is clicked a grenade is shot tword the cursor. Across the map there are tentacle monsters moving back and forth on their platforms, you must blow them up with your grenades, or attempt to evade them to reach the objective at the end of the map. When you touch a monster or stand too close to an exploding grenade you take damage, take too much and you'll be sent to a game over screen. If you fall in lava your health will instantly fall to 0. Touch the golden relic at the end of the map to win.
## Physics Engine
While creating the game I found that the physics engines included with the arcade library were very underwhelming, so I made my own. The physics engine in Underworld Heist uses principles from real life physics, not just gravity, but also collisions, friction and air resistance. While the air resistance is mostly negligible, the ground friction adds a new dimention to the game. When a collision is detected with a wall the object doesn't simply stop, it bounces off the wall with a small decrease in speed. The grenade projectiles that the player shoots are subject to the same physics as the player, making combat more complicated.
## Map Making
Underworld Heist loads it's levels from a png image. Each pixel of the png image represents a block in the game, and the game will render different objects based on the RGB value of each pixel. The game is able to render every sprite into the game this way; barrier blocks, hazard blocks, tenticle monsters, the relic, and the player. This makes for very easy level building. Below is the tutorial level made using ms paint.
![map1.png](Images\map1Documentation.png)
As you might have noticed, the map is upside down. This is because the x axis for the image starts at the top, while the x axis for the game window starts at the bottom. If this bothers you to create levels upside down you could just create one normally then flip it in MS Paint. Anyone can make a level using MS Paint, once one is created just name it `map1.png` and replace the one in the images folder.
### RGB values for each sprite
* Platform: (0,0,0)
* Lava:     (255,255,0)
* Monster:  (255,0,0)
* Relic:    (0,255,0)
* Player:   (0,0,255)
* Nothing:  (255,255,255)
## Textures
Each texture used in the game was made by me using Microsoft Paint.
## Music and Sound Effects
The music and sound effects used in game are royalty free / non copyrighted.

# Demonstration Video

[Youtube - Demo Video](https://youtu.be/vnJKtz0pi2c)

# Development Environment

The IDE I used was VS Code, and I wrote the game using the Python language. The library that I used to manage the flow of the game, image rendering, and sprite objects was Arcade.

# Useful Websites

* [Arcade Academy](https://arcade.academy/tutorials)
* [W3schools RGB Color Picker](https://www.w3schools.com/colors/colors_picker.asp)
* [Online png Transparency Tool](https://onlinepngtools.com/create-transparent-png)
* [NemoQuiz: loop through pixel tutorial](http://www.nemoquiz.com/python/loop-through-pixel-data/#:~:text=You%20can%20use%20Python%20Image,pixel%20data%20as%20an%20array.)
* [Zapsplat - Royalty-free sound effects](https://www.zapsplat.com/)
* [Youtube - Demon Slayer(song) Royalty-free](https://www.youtube.com/watch?v=BYjVICisNEc)
* [StackOverflow](https://stackoverflow.com/)


# Future Work
* Create more levels
* Add ability for user to import custom levels
* Speed improvements
* Asthetic improvements