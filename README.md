# affective_computing

The goal of this project was, to investigate, how stress and especially how frustration of humans can be measured with innovative measuring devices outside a lab. We decided to implement a simple stress and frustration inducing game and perform a small user study. In this pilot study a few participants (n=8) played this game and the devices monitored their physiological data while playing. Afterwards we interpreted the measured data in comparison to how the participants felt while playing. The latter they had to tell us with a little questionnaire after each level of the game. For the purpose of measuring the physiological data we used a mouse "MIONIX NAOS QG" and a keyboard "ROCCAT Isku+ Force FX" with integrated sensors. The mouse has a skin conductance and a heart rate sensor while the keyboard has a pressure-sensitive key zone.

### Start the Game

    python3 main.py <NAME> <PARAMETER>
    
Here, `<NAME>` is the actual name of the created measurement files. The `<PARAMETER>` is optional. This parameter indicates whether the manipulation mode for "frustrating - effects" is enabled with E or not. 
    
### default setting: 
Manipulating factors (lagging and freezing) are DISABLED. There is no need to define `<PARAMETER>` by not using the manipulation mode.
### to enable the manipulation type 

    python3 main.py <NAME> E

### Background music: 
“Foggy Forest”, from https://PlayOnLoop.com \
Licensed under Creative Commons by Attribution 4.0 

### Sound Effects: 
“Large Fireball”, from https://soundbible.com \
Licensed under Creative Commons by Attribution 3.0 

“Explosion”, from https://github.com/attreyabhatt/Space-Invaders-Pygame 
