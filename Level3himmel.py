[level]

tileset = 15x15.png


map =  ...............................
       ...............................
       ...............................
       ...............................
       ...............................
       ...............................
       ...............................
       ...............................
       ...............................
       ...............................
       ...............................
       ...............................
       ...............................
       ...............................
       ...............................


[.]
name = floor
tile = 14,0

[+]
name = wall
tile = 1,0
wall = true
block = true

[l]
name = sky
tile = 14,0

[j]
name = regnsky
tile = 16,0
wall = true
block = true

[!]
name = redbutton
tile = 2,0
redpress = true

[?]
name = sea
tile = 8,0
wall = true
block = true

[,]
name = invisiblesea
tile = 8,0

[*]
name = exitblocked
tile = 5,0
cannotenter = true

[-]
name = shoreup
tile = 9,0

[_]
name = shoreleft
tile = 10,0
block = true
wall = true

[=]
name = shoreblockup
tile = 9,0
block = true
wall = true

[&]
name = shoreblockdown
tile = 12,0

[/]
name = shoreedgeup
tile = 11,0
block = true
wall = true

[<]
name = shoredown
tile = 12,0
block = true
wall = true

[>]
name = shoreedgedown
tile = 13,0
block = true
wall = true