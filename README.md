# Game of Life Project
![Alt Text](https://gitup.uni-potsdam.de/pichottka/game-of-life/raw/master/example.gif)
Useage: python GoL.py [input txt-file] [number of generations] [animation delay in ms]    
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;e.g. python GoL.py example1.txt 20 800  
  
input txt-file mandatory structure:    
1: [number of matrix rows],[number of matrix columns]  
2: [boundary condition: toroidal or death_edge]  
3: [rule string]  
4: [matrix with comma delimiter + line breaks for rows]  

Used Modules: pil, gtk, matplotlib, numpy, itertools, time, sys 
