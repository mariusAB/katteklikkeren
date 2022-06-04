[level]

tileset = 15x15.png


map =  ...............................
       ++++++++++++++.eqqqqqqqqqqqqqqt
       ++++++!++++++..svvvvvvgvvvvvvgg
       +.!++...!++!..+svggvvggggvvgggv
       +.++!.+.+!+++..svgvvggvgvgvvvgg
       +.!++.+.+.....+svggvvgvgvgggggv
       +.++!.+!+++++..svgvvggvgvvvvvgg
       +.!++.++!...++.svggvvgvvggggvvg
       +.+++.+++.+....svgvvvgvvvgvgggg
       +...+.++!.+++++svgggvgvvggvvvvv
       +.+.+.+++......svgvgvgvvvgggggg
       +.+.+.+++!+!++.svgvgvgvvvgvgvvg
       +.+......++++..svgvggggggvvvvgg
       +.++++++.++++.+/-o-----=o----o-
       *......+.......+.......+.......


[.]
name = floor
tile = 0,0

[+]
name = wall
tile = 1,0
wall = true
block = true

[p]
name = portal
tile = 4,0
canenter = true

[z]
name = greenbutton
tile = 7,0
redpress = false

[o]
name = shoreupgo
tile = 9,0

[!]
name = redbutton
tile = 6,0
redpress = true

[v]
name = sea
tile = 8,0
wall = true
block = true

[g]
name = invisiblesea
tile = 8,0

[*]
name = exitblocked
tile = 5,0
cannotenter = true

[-]
name = shoreup
tile = 9,0
wall = true
block = true

[s]
name = shoreleft
tile = 10,0
block = true
wall = true

[=]
name = shoreblockup
tile = 9,0
block = true
wall = true

[t]
name = shoreblockdown
tile = 12,0

[/]
name = shoreedgeup
tile = 11,0
block = true
wall = true

[q]
name = shoredown
tile = 12,0
block = true
wall = true

[e]
name = shoreedgedown
tile = 13,0
block = true
wall = true