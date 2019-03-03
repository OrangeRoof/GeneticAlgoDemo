__GROUND = 350
__GROUND_VELOCITY = PVector(0, 0.2)
class PhysicSim:
    # contains references to all physics objects, as well as simulation code
    def __init__(self):
        self.objs = []
        self.iobjs = []

    def addBall(self, p_x, p_y, v_x, v_y, r=255, g=255, b=255):
        self.objs.append(PhysicsBall(p_x, p_y, v_x, v_y, r, g, b))
        self.iobjs.append(PhysicsBall(p_x, p_y, v_x, v_y, r, g, b))

    def delBalls(self):
        del self.objs[:]
        del self.iobjs[:]

    def simulateTick(self):
        for b in self.objs:
            b.advance()

    def draw(self):
        for b in self.objs:
            b.draw()

class PhysicsBall:
    def __repr__(self):
        return '({}, {}, {}, {})'.format(self.p.x, self.p.y, self.v.x, self.v.y)
    # represents a ball
    def __init__(self, p_x, p_y, v_x, v_y, r, g, b):
        # initalize the ball with [p]osition and [velocity
        self.p = PVector(p_x, p_y)
        self.v = PVector(v_x, v_y)
        self.r = r
        self.g = g
        self.b = b
        self.bounce = 0

    def advance(self):
        self.bounce = 0
        # change position by velocity
        self.p.add(self.v)
        # change velocity by gravity
        self.v.add(__GROUND_VELOCITY)
        # short circuit flip x dir bounce off walls
        if self.p.x < 0 or self.p.x > width:
            if self.p.x < 0:
                self.bounce = 1 # LEFT WALL
            else:
                self.bounce = 2 # RIGHT WALL
            self.v.x = -self.v.x
        # no penalty for hitting ceiling
        if self.p.y < 0:
            self.bounce = 4
            self.v.y = abs(self.v.y)
            self.p.y = 0
        # bleed off velocity when hitting ground
        if self.p.y > __GROUND:
            self.v.y = self.v.y * -0.65
            self.v.x = self.v.x * 0.95
            self.p.y = __GROUND
            if abs(self.v.y) < 1:
                self.v.y = 0
        return

    def draw(self):
        fill(0)
        stroke(self.r, self.g, self.b)
        ellipse(self.p.x, self.p.y, 50, 50)
        return
