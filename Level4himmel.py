[level]

tileset = 15x15.png


map =  .g.r..b........................
       r..r...grgbrgbrgbrgbrgbgrgrbbgb
       .b.b...g....r...b....r.........
       ..r....brrgbg.....r.....b...rgb
       r.brgbrg.......................
       .g.......b.......b...grgb....gr
       .....r..........g.grb....rrgb..
       ................r..............
       g.b.g.b.r.b.g.r.r.b.g.b.r.g.b.r
       rgbhgbrgbrgbgrgbrgbdrbgrbgbgb.b
       .g....g.r.r....r......r.....b..
       ..g.....g.g.b.....g...g..r.....
       .b......b.b....g......b.......b
       ....b...g.r..b......r.r..g..r..
       .r....r.r.g.....r.....g........


[.]
name = floor
tile = 14,0

[d]
name = rballonggjennom
tile = 16,0

[h]
name = bballonggjennom
tile = 17,0

[t]
name = gballonggjennom
tile = 18,0

[r]
name = rballong
tile = 16,0
wall = true
block = true

[b]
name = bballong
tile = 17,0
wall = true
block = true

[g]
name = gballong
tile = 18,0
wall = true
block = true

[+]
name = wall
tile = 1,0
wall = true
block = true

[l]
name = sky
tile = 14,0



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