# Using an Arduino with Python LESSON 15: Model of Bouncing Marble in 3D Room.
# https://www.youtube.com/watch?v=1qNnMjw_KxM
# https://toptechboy.com/

# Internet References:
# https://www.glowscript.org/docs/VPythonDocs/index.html

from vpython import *
import numpy as np

# vPython refresh rate.
vPythonRefreshRate = 100

# A place on which to put our things...
canvas(title = "<b><i>Arduino with Python - Many connected boxes and a bouncing ball!</i></b>", background = color.cyan, width = 800, height = 600)

# A function to draw an arena box.
def buildBox(rPos = vector(0, 0, 0), boxSize = 1):
    boxX = boxSize * 3  # Width.
    boxY = boxSize      # Height.
    boxZ = boxSize * 2  # Depth.
    wallThickness = (boxZ + boxX + boxY) / 200
    wallLeft   = box(color = color.gray(0.5), opacity = 0.5, pos = vector(-boxX / 2,  0, 0) + rPos, size = vector(wallThickness, boxY, boxZ + wallThickness))
    wallRight  = box(color = color.gray(0.5), opacity = 0.5, pos = vector( boxX / 2,  0, 0) + rPos, size = vector(wallThickness, boxY, boxZ + wallThickness))
    wallTop    = box(color = color.gray(0.5), opacity = 0.5, pos = vector( 0,  boxY / 2, 0) + rPos, size = vector(boxX, wallThickness, boxZ + wallThickness))
    wallBottom = box(color = color.gray(0.5), opacity = 0.5, pos = vector( 0, -boxY / 2, 0) + rPos, size = vector(boxX, wallThickness, boxZ + wallThickness))
    wallRear   = box(color = color.gray(0.5), opacity = 0.5, pos = vector( 0, 0, -boxZ / 2) + rPos, size = vector(boxX, boxY, wallThickness))
    wallFront  = box(color = color.gray(0.5), opacity = 0.10, pos = vector( 0, 0,  boxZ / 2) + rPos, size = vector(boxX, boxY, wallThickness))
    topleftCornerTrim     = cylinder (color = color.gray(0.5), opacity = 0.5, radius = wallThickness / 2, pos = vector(-boxX / 2,  boxY / 2, -(boxZ + wallThickness) / 2) + rPos, axis = vector(0, 0, boxZ + wallThickness))
    toprightCornerTrim    = cylinder (color = color.gray(0.5), opacity = 0.5, radius = wallThickness / 2, pos = vector( boxX / 2,  boxY / 2, -(boxZ + wallThickness) / 2) + rPos, axis = vector(0, 0, boxZ + wallThickness))
    bottomleftCornerTrim  = cylinder (color = color.gray(0.5), opacity = 0.5, radius = wallThickness / 2, pos = vector(-boxX / 2, -boxY / 2, -(boxZ + wallThickness) / 2) + rPos, axis = vector(0, 0, boxZ + wallThickness))
    bottomrightCornerTrim = cylinder (color = color.gray(0.5), opacity = 0.5, radius = wallThickness / 2, pos = vector( boxX / 2, -boxY / 2, -(boxZ + wallThickness) / 2) + rPos, axis = vector(0, 0, boxZ + wallThickness))
    # Return the box boundaries -> [x-left, x-right, y-bottom, y-top, z-back, z-front].
    return([(-boxX / 2 + wallThickness / 2 + rPos.x), (boxX / 2 - wallThickness / 2 + rPos.x),
            (-boxY / 2 + wallThickness / 2 + rPos.y), (boxY / 2 - wallThickness / 2 + rPos.y),
            (-boxZ / 2 + wallThickness / 2 + rPos.z), (boxZ / 2 - wallThickness / 2 + rPos.z)])

# A function to draw a tunnel box.
def buildTunnel(rPos = vector(0, 0, 0), tunnelSize = 1, axis = "X"):
    tunnelX = tunnelSize    # Width.
    tunnelY = tunnelSize    # Height.
    tunnelZ = tunnelSize    # Depth.
    wallThickness = (tunnelX + tunnelY + tunnelZ) / 200
    wallThicknessX = wallThicknessY = wallThicknessZ = 0
    if (axis.upper() != "X"):
        wallLeft   = box(color = color.gray(0.5), opacity = 0.2, pos = vector(-tunnelX / 2,  0, 0) + rPos, size = vector(wallThickness, tunnelY, tunnelZ))
        wallRight  = box(color = color.gray(0.5), opacity = 0.2, pos = vector( tunnelX / 2,  0, 0) + rPos, size = vector(wallThickness, tunnelY, tunnelZ))
        wallThicknessX = wallThickness
    if (axis.upper() != "Y"):
        wallBottom = box(color = color.gray(0.5), opacity = 0.2, pos = vector( 0, -tunnelY / 2, 0) + rPos, size = vector(tunnelX, wallThickness, tunnelZ))
        wallTop    = box(color = color.gray(0.5), opacity = 0.2, pos = vector( 0,  tunnelY / 2, 0) + rPos, size = vector(tunnelX, wallThickness, tunnelZ))
        wallThicknessY = wallThickness
    if (axis.upper() != "Z"):
        wallRear   = box(color = color.gray(0.5), opacity = 0.2, pos = vector( 0, 0, -tunnelZ / 2) + rPos, size = vector(tunnelX, tunnelY, wallThickness))
        wallFront  = box(color = color.gray(0.5), opacity = 0.2, pos = vector( 0, 0,  tunnelZ / 2) + rPos, size = vector(tunnelX, tunnelY, wallThickness))
        wallThicknessZ = wallThickness
    # Return the box boundaries -> [x-left, x-right, y-bottom, y-top, z-back, z-front].
    return([(-tunnelX / 2 + wallThicknessX / 2 + rPos.x), (tunnelX / 2 - wallThicknessX / 2 + rPos.x),
            (-tunnelY / 2 + wallThicknessY / 2 + rPos.y), (tunnelY / 2 - wallThicknessY / 2 + rPos.y),
            (-tunnelZ / 2 + wallThicknessZ / 2 + rPos.z), (tunnelZ / 2 - wallThicknessZ / 2 + rPos.z)])

# Arena sizes.
arena1Size = 10         # Left, top, front.
arena2Size = 15         # Left, bottom, front.
arena3Size = arena2Size # Right, top, front.
arena4Size = arena1Size # Left, bottom, back.

# Arena 1 - Left, top, front..
arena1Centre = vector(-(arena1Size + arena2Size), arena1Size, 0)
arena1 = buildBox(arena1Centre, arena1Size)
# Arena 2 - Left, bottom, front.
arena2Centre = vector(-(arena1Size + arena2Size), -arena2Size, 0)
arena2 = buildBox(arena2Centre, arena2Size)
# Arena 3 - Right, top, front.
arena3Centre = vector((arena1Size + arena2Size) / 1.25, arena1Size, 0)
arena3 = buildBox(arena3Centre, arena3Size)
# Arena 4 - Left, bottom, back.
arena4Centre = vector(-(arena1Size + arena2Size), -arena2Size, -1.25 * (arena1Size + arena2Size))
arena4 = buildBox(arena4Centre, arena4Size)

# Linking X tunnel between Arena 1 and Arena 3.
xTunnelSize =  arena3[0] - arena1[1]# Related to the arenas, larger - smaller.
xTunnelCentre = vector((arena1[1] + arena3[0]) / 2, arena1Size, 0)
xTunnel = buildTunnel(xTunnelCentre, xTunnelSize, "X")
# Linking Y tunnel between Arena 1 and Arena 2.
yTunnelSize = arena1[2] - arena2[3] # Related to the arenas, larger - smaller.
yTunnelCentre = vector(-(arena1Size + arena2Size), (arena1[2] + arena2[3]) / 2, 0)
yTunnel = buildTunnel(yTunnelCentre, yTunnelSize, "Y")
# Linking Z tunnel between Arena 2 and Arena 4.
zTunnelSize = arena2[4] - arena4[5] # Related to the arenas, larger - smaller.
zTunnelCentre = vector(-(arena1Size + arena2Size), -arena2Size, (arena2[4] + arena4[5]) / 2)
zTunnel = buildTunnel(zTunnelCentre, zTunnelSize, "Z")

# The ball.
ball1Radius = 0.075 * arena1Size
ball1 = sphere(color = color.green, opacity = 1, radius = ball1Radius, pos = arena3Centre, make_trail = True, retain = arena1Size * 10)
# A random position change vector for the ball.
#ball1Change = vector((np.random.rand() - 0.5) / (arena1Size / 2), (np.random.rand() - 0.5) / (arena1Size / 2), (np.random.rand() - 0.5) / (arena1Size / 2))
ball1Change = vector(-0.0457517, -0.0562431, 0.0517289) # The ball will visit all rooms with this change vector.

# Print all the interesting data to be able to manually check the 3D calculations.
print("Arena 1 :", arena1)
print("Arena 2 :", arena2)
print("Arena 3 :", arena3)
print("Arena 4 :", arena4)
print("X-Tunnel:", xTunnel)
print("Y-Tunnel:", yTunnel)
print("Z-Tunnel:", zTunnel)
print("Ball 1  : P-%s, M-%s, R-%s" % (ball1.pos, ball1Change, ball1Radius))

# An infinite loop: When is True, True? It is always True!
while True:
    rate(vPythonRefreshRate) # The vPython rate command is obligatory in animation loops.

    # We have not yet worked out where ball1 is.
    ball1InArena1 = ball1InArena2 = ball1InArena3 = ball1InArena4 = ball1InXTunnel = ball1InYTunnel = ball1InZTunnel = False
    # Check where ball1 is going, and set the boundaries.
    if (((arena1[0] <= (ball1.pos.x + ball1Radius + ball1Change.x) and (ball1.pos.x + ball1Radius + ball1Change.x) <= arena1[1])
        or (arena1[0] <= (ball1.pos.x - ball1Radius + ball1Change.x) and (ball1.pos.x - ball1Radius + ball1Change.x) <= arena1[1]))
        and ((arena1[2] <= (ball1.pos.y + ball1Radius + ball1Change.y) and (ball1.pos.y + ball1Radius + ball1Change.y) <= arena1[3])
        or (arena1[2] <= (ball1.pos.y - ball1Radius + ball1Change.y) and (ball1.pos.y - ball1Radius + ball1Change.y) <= arena1[3]))
        and ((arena1[4] <= (ball1.pos.z + ball1Radius + ball1Change.z) and (ball1.pos.z + ball1Radius + ball1Change.z) <= arena1[5])
        or (arena1[4] <= (ball1.pos.z - ball1Radius + ball1Change.z) and (ball1.pos.z - ball1Radius + ball1Change.z) <= arena1[5]))):
        bounds1 = arena1
        ball1InArena1 = True
    if (((arena2[0] <= (ball1.pos.x + ball1Radius + ball1Change.x) and (ball1.pos.x + ball1Radius + ball1Change.x) <= arena2[1])
        or (arena2[0] <= (ball1.pos.x - ball1Radius + ball1Change.x) and (ball1.pos.x - ball1Radius + ball1Change.x) <= arena2[1]))
        and ((arena2[2] <= (ball1.pos.y + ball1Radius + ball1Change.y) and (ball1.pos.y + ball1Radius + ball1Change.y) <= arena2[3])
        or (arena2[2] <= (ball1.pos.y - ball1Radius + ball1Change.y) and (ball1.pos.y - ball1Radius + ball1Change.y) <= arena2[3]))
        and ((arena2[4] <= (ball1.pos.z + ball1Radius + ball1Change.z) and (ball1.pos.z + ball1Radius + ball1Change.z) <= arena2[5])
        or (arena2[4] <= (ball1.pos.z - ball1Radius + ball1Change.z) and (ball1.pos.z - ball1Radius + ball1Change.z) <= arena2[5]))):
        bounds1 = arena2
        ball1InArena2 = True
    if (((arena3[0] <= (ball1.pos.x + ball1Radius + ball1Change.x) and (ball1.pos.x + ball1Radius + ball1Change.x) <= arena3[1])
        or (arena3[0] <= (ball1.pos.x - ball1Radius + ball1Change.x) and (ball1.pos.x - ball1Radius + ball1Change.x) <= arena3[1]))
        and ((arena3[2] <= (ball1.pos.y + ball1Radius + ball1Change.y) and (ball1.pos.y + ball1Radius + ball1Change.y) <= arena3[3])
        or (arena3[2] <= (ball1.pos.y - ball1Radius + ball1Change.y) and (ball1.pos.y - ball1Radius + ball1Change.y) <= arena3[3]))
        and ((arena3[4] <= (ball1.pos.z + ball1Radius + ball1Change.z) and (ball1.pos.z + ball1Radius + ball1Change.z) <= arena3[5])
        or (arena3[4] <= (ball1.pos.z - ball1Radius + ball1Change.z) and (ball1.pos.z - ball1Radius + ball1Change.z) <= arena3[5]))):
        bounds1 = arena3
        ball1InArena3 = True
    if (((arena4[0] <= (ball1.pos.x + ball1Radius + ball1Change.x) and (ball1.pos.x + ball1Radius + ball1Change.x) <= arena4[1])
        or (arena4[0] <= (ball1.pos.x - ball1Radius + ball1Change.x) and (ball1.pos.x - ball1Radius + ball1Change.x) <= arena4[1]))
        and ((arena4[2] <= (ball1.pos.y + ball1Radius + ball1Change.y) and (ball1.pos.y + ball1Radius + ball1Change.y) <= arena4[3])
        or (arena4[2] <= (ball1.pos.y - ball1Radius + ball1Change.y) and (ball1.pos.y - ball1Radius + ball1Change.y) <= arena4[3]))
        and ((arena4[4] <= (ball1.pos.z + ball1Radius + ball1Change.z) and (ball1.pos.z + ball1Radius + ball1Change.z) <= arena4[5])
        or (arena4[4] <= (ball1.pos.z - ball1Radius + ball1Change.z) and (ball1.pos.z - ball1Radius + ball1Change.z) <= arena4[5]))):
        bounds1 = arena4
        ball1InArena4 = True
    if (((xTunnel[0] <= (ball1.pos.x + ball1Radius + ball1Change.x) and (ball1.pos.x + ball1Radius + ball1Change.x) <= xTunnel[1])
        or (xTunnel[0] <= (ball1.pos.x - ball1Radius + ball1Change.x) and (ball1.pos.x - ball1Radius + ball1Change.x) <= xTunnel[1]))
        and ((xTunnel[2] <= (ball1.pos.y + ball1Radius + ball1Change.y) and (ball1.pos.y + ball1Radius + ball1Change.y) <= xTunnel[3])
        or (xTunnel[2] <= (ball1.pos.y - ball1Radius + ball1Change.y) and (ball1.pos.y - ball1Radius + ball1Change.y) <= xTunnel[3]))
        and ((xTunnel[4] <= (ball1.pos.z + ball1Radius + ball1Change.z) and (ball1.pos.z + ball1Radius + ball1Change.z) <= xTunnel[5])
        or (xTunnel[4] <= (ball1.pos.z - ball1Radius + ball1Change.z) and (ball1.pos.z - ball1Radius + ball1Change.z) <= xTunnel[5]))):
        bounds1 = xTunnel
        ball1InXTunnel = True
    if (((yTunnel[0] <= (ball1.pos.x + ball1Radius + ball1Change.x) and (ball1.pos.x + ball1Radius + ball1Change.x) <= yTunnel[1])
        or (yTunnel[0] <= (ball1.pos.x - ball1Radius + ball1Change.x) and (ball1.pos.x - ball1Radius + ball1Change.x) <= yTunnel[1]))
        and ((yTunnel[2] <= (ball1.pos.y + ball1Radius + ball1Change.y) and (ball1.pos.y + ball1Radius + ball1Change.y) <= yTunnel[3])
        or (yTunnel[2] <= (ball1.pos.y - ball1Radius + ball1Change.y) and (ball1.pos.y - ball1Radius + ball1Change.y) <= yTunnel[3]))
        and ((yTunnel[4] <= (ball1.pos.z + ball1Radius + ball1Change.z) and (ball1.pos.z + ball1Radius + ball1Change.z) <= yTunnel[5])
        or (yTunnel[4] <= (ball1.pos.z - ball1Radius + ball1Change.z) and (ball1.pos.z - ball1Radius + ball1Change.z) <= yTunnel[5]))):
        bounds1 = yTunnel
        ball1InYTunnel = True
    if (((zTunnel[0] <= (ball1.pos.x + ball1Radius + ball1Change.x) and (ball1.pos.x + ball1Radius + ball1Change.x) <= zTunnel[1])
        or (zTunnel[0] <= (ball1.pos.x - ball1Radius + ball1Change.x) and (ball1.pos.x - ball1Radius + ball1Change.x) <= zTunnel[1]))
        and ((zTunnel[2] <= (ball1.pos.y + ball1Radius + ball1Change.y) and (ball1.pos.y + ball1Radius + ball1Change.y) <= zTunnel[3])
        or (zTunnel[2] <= (ball1.pos.y - ball1Radius + ball1Change.y) and (ball1.pos.y - ball1Radius + ball1Change.y) <= zTunnel[3]))
        and ((zTunnel[4] <= (ball1.pos.z + ball1Radius + ball1Change.z) and (ball1.pos.z + ball1Radius + ball1Change.z) <= zTunnel[5])
        or (zTunnel[4] <= (ball1.pos.z - ball1Radius + ball1Change.z) and (ball1.pos.z - ball1Radius + ball1Change.z) <= zTunnel[5]))):
        bounds1 = zTunnel
        ball1InZTunnel = True

    # A ball with a radius can be in an Arena and in a tunnel, so set the bounds to be where it is travelling to.
    if (ball1InArena1 and ball1InXTunnel):
        if (ball1Change.x < 0):
            bounds1 = arena1
        if (ball1Change.x > 0):
            bounds1 = xTunnel
    if (ball1InArena3 and ball1InXTunnel):
        if (ball1Change.x > 0):
            bounds1 = arena3
        if (ball1Change.x < 0):
            bounds1 = xTunnel
    if (ball1InArena1 and ball1InYTunnel):
        if (ball1Change.y < 0):
            bounds1 = yTunnel
        if (ball1Change.y > 0):
            bounds1 = arena1
    if (ball1InArena2 and ball1InYTunnel):
        if (ball1Change.y > 0):
            bounds1 = yTunnel
        if (ball1Change.y < 0):
            bounds1 = arena2
    if (ball1InArena2 and ball1InZTunnel):
        if (ball1Change.z < 0):
            bounds1 = zTunnel
        if (ball1Change.z > 0):
            bounds1 = arena2
    if (ball1InArena4 and ball1InZTunnel):
        if (ball1Change.z > 0):
            bounds1 = zTunnel
        if (ball1Change.z < 0):
            bounds1 = arena4

    # Move ball1.
    ball1.pos += ball1Change
    # Check if ball1 has hit a boundary, and if it is moving towards that boundary, reverse the direction.
    if (((bounds1[0] + ball1Radius) >= ball1.pos.x and ball1Change.x < 0)
        or (ball1.pos.x >= (bounds1[1] - ball1Radius) and ball1Change.x > 0)):
        ball1Change.x = -ball1Change.x
    if (((bounds1[2] + ball1Radius) >= ball1.pos.y and ball1Change.y < 0)
        or (ball1.pos.y >= (bounds1[3] - ball1Radius) and ball1Change.y > 0)):
        ball1Change.y = -ball1Change.y
    if (((bounds1[4] + ball1Radius) >= ball1.pos.z and ball1Change.z < 0)
        or (ball1.pos.z >= (bounds1[5] - ball1Radius) and ball1Change.z > 0)):
        ball1Change.z = -ball1Change.z

# EOF
