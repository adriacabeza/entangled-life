[![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/adriacabeza/entangled-life)

<div align="center">
<img src="docs/entangled_life.png" width="480"/>
</div>

This game was inspired by the fascinating world of mushrooms and their complex interactions, as explored in the book 
<a href="https://www.merlinsheldrake.com/entangled-life">"Entangled Life</a>." Get ready to embark on a ferocious 
battle through mycelial networks while honing your coding skills. Players take on the roles of myceliums trying to look for food and expand by traversing a map with other rival players. 


## Coding Challenges
The coding challenges in Entangled Life will include: 

- Implementing algorithms to make your mycelial growth and nutrient distribution.
- Block your rivals possibilities by limiting their reachable zone. 

## Game overview 
In this game, N players take on the role of mushrooms placed randomly on a grid, all looking for limited resources scattered across the terrain. The main objective is to use strategic algorithms to reach these resources before your 
rivals do. Each player's success is measured by the amount of food they manage to consume throughout the game. Just like in real life, just like a mushroom, you will control the mycelial growth looking for resources: 
<div align="center">
<img src="docs/mycelial-networks.png" width="480"/>

Figure of *Phanerochaete velutina* growing towards pieces of wood.
Source: <a href="https://www.researchgate.net/figure/Effects-of-resource-addition-and-grazing-on-mycelial-networks-Mycelial-cord-systems-99_fig2_317122457"> The Mycelium as a network</a>
</div>

The grid contains food placed at various locations, and players must navigate their way to these spots to obtain the food units. Once a player reaches a cell with food, they must remain there to consume it. However, it's important to note that each round of the game spent on a food cell depletes one unit of food from that cell. To add an additional layer of strategy and rivalry, players have the unique ability to leave toxic spores in their wake as they move across the grid. These spores act as barriers that block their opponents' movements, effectively creating obstacles and controlling zones on the map. Players can augment their mushroom presence by reaching a score of five points or more. At this point, they have the option to spend five points to branch themselves into two mushroom units. This decision enables them to access more resources and effectively hinder their opponents' progress. However, this option should be carefully weighed, as it can be a powerful move with significant implications for the overall game strategy.

## Adding your player

To create a new player with, say, name KelsierPlayer, copy PlayerTemplate to a new file and create the class 
KelsierPlayer. 
Then edit the new file, 
this will 
be the file that you will have to upload. The name you choose for your player must be unique, non-offensive and less 
than 12 letters long. The name will be shown as well when viewing the matches on the website. 

Now you can start implementing the method `play()`. This method will be called every round and is where your player 
should decide what to do, and do it. Of course, you can define auxiliary methods and variables inside your player 
class, but the entry point of your code will always be the play method. 

## Requirements
To participate in Entangled Life, you will need:

- Google Account (to sign in)
- A device that runs a browser.
- Basic coding knowledge and familiarity with Python 
- Enthusiasm for learning about mushrooms and mycology (NOT REALLY LOL)


## Want to collaborate?  
### Backend
- [ ] Add debug logs and CLI to run main.py 
- [ ] Add mushroom blocking paths
- [ ] Add branching factor
- [ ] Add Observability: Datadog traces and metrics
- [ ] Add unit tests
- [ ] Generate output of a match to later visualize

### Frontend
- [ ] Create Sign In page 
- [ ] Create way to push your code (+ find a way to see users code actually can be interpreted?)
- [ ] Create editing code page with Monaco
- [ ] Create visualization of a run