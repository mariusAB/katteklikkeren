[level]

tileset = 15x15.png


map =  ++++++++++++++++++++++++++++++
       +*+........!+!...+!.....!+..!+
       +...+.+++++++++..+.+.!+.++.+.+
       +++++.+!........++!+.++....+.+
       +!+!+.+++++++++..+++!++++..+.+
       +..................+++.!+..+.+
       ++++++++++++++++.......++.!+.+
       +!+!...........+!+........++.+
       +.+.+.+.+.+.++.+.++++++++++..+
       +.+.+.+.+.+.+!.+.+...+...+..++
       +.+.+.+.+.+.++.+++.+.+.+.++.!+
       +.+!+.+!+.+!+!.+...+...+....++
       +.+++!+++.++++.+.+++++++++++++
       +...........................!+
       ++++++++++++++++++++++++++++++


[.]
name = floor
tile = 0,0

[+]
name = wall
tile = 1,0
wall = true
block = true

[!]
name = redbutton
tile = 2,0
redpress = true

[z]
name = greenbutton
tile = 3,0
redpress = false

[?]
name = sea
tile = 8,0
wall = true
block = true

[,]
name = invisiblesea
tile = 8,0

[*]
name = portalblocked
tile = 5,0
cannotenter = true

[p]
name = portal
tile = 4,0
canenter = true

[-]
name = shore
tile = 4,0

[=]
name = shorebush
tile = 4,0
block = true
wall = true