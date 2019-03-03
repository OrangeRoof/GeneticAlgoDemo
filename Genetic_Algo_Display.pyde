import genetics
import physics
def setup():
    size(800, 500)
    global f
    frameRate(60)
    global g
    g = genetics.World(10, 7)
    
def draw():
    if keyPressed:
        if key == 's':
            frameRate(frameRate + 10)
        if key == 'w':
             frameRate(frameRate - 10)
            
    background(50)
    g.eval_tick()
    stroke(255)
    
    # BASKET CODE
    strokeWeight(3)
    line(0, physics.__GROUND + 25, width, physics.__GROUND + 25)
    quad(width-90, height/2, width-80, height/2 + 50, width-30, height/2 + 50, width-20, height/2)
    strokeWeight(1)
