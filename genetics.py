import struct
import physics
import random
import math
import copy

class World:
    def __init__(self, _mutation_rate, _gen_size):
        random.seed()
        self.mutation_rate = _mutation_rate
        self.gen_size = _gen_size
        self.gen_tick = 1 # reset to 0; already pass init_gen here
        self.generation = 0
        self.p = physics.PhysicSim()
        # TUPLES: (fitness, bounce)
        # the way bounce works: left wall is 1, right wall is 2
        # ceiling is 4, ground is 0, anything outside 0-7 is dead
        self.fitness = []
        for _ in range(0, _gen_size):
            self.p.addBall(random.uniform(200, 500), random.uniform(150, 350),\
                random.uniform(-10, 10), random.uniform(-10, 10),\
                random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
            self.fitness.append((0, 0))
        return

    def init_generation(self):
        # mutate with the best PhysicsBall
        self.generation += 1
        self.gen_tick = 1
        print(max(self.fitness, key=lambda i:i[0])[0])
        if(max(self.fitness, key=lambda i:i[0])[0] > 100):
            b = self.p.iobjs[self.fitness.index(max(self.fitness, key=lambda i:i[0]))]
            x, y, v_x, v_y = b.p.x, b.p.y, b.v.x, b.v.y
            self.p.delBalls()
            self.p.addBall(x, y, v_x, v_y, 255, 255, 255)
            self.fitness = [(1000, 0)]
            return
            
        self.mutate(self.p.iobjs[self.fitness.index(max(self.fitness, key=lambda i:i[0]))])
        self.fitness = [(0, 0)] * self.gen_size
        for i, ball in enumerate(self.p.objs):
            if ball.p.x not in range(200, 500) or ball.p.y not in range(0, 350):
                self.fitness[i] = (-100, 0)
        return

    def eval_tick(self):
        if self.gen_tick < 0:
            self.init_generation()
        # move the balls
        self.p.simulateTick()
        # evaluate fitness: copy bounce times into new list
        for i, ball in enumerate(self.p.objs):
            b = self.fitness[i][1]
            f = 0
            if b == 0:
                # no bounces yet
                f = 1 - min(ball.p.x/800, 1 - (ball.p.x/800), ball.p.y/500)
                if ball.bounce:
                    b = ball.bounce
            elif b == 1:
                # after one bounce on left wall
                f = 2 - min(1 - (ball.p.x/800), ball.p.y/500)
                if ball.bounce:
                    b += ball.bounce
            elif b == 2:
                # after one bounce off right wall
                f = 2 - min(ball.p.x/800, ball.p.y/500)
                if ball.bounce:
                    b += ball.bounce
            elif b == 4:
                # after one bounce off ceiling
                f = 2 - min(ball.p.x/800, 1 - (ball.p.x/800))
                if ball.bounce:
                    b += ball.bounce
            elif b in range(0, 7):
                # two bounces, heading to goal
                f = 2 + 1/(math.sqrt((ball.p.x - 745)**2 + (ball.p.y - 300)**2)/800)
                if f > 70:
                    if not (ball.p.y < 320 and ball.v.y > 0):
                        f = -100
                if ball.bounce or self.fitness[i][0] == -100:
                    # stay dead
                    f = -100
            else:
                # dead
                f = -100
            self.fitness[i] = (-100 if f == -100 else max(f, self.fitness[i][0]), b)

        if not [ball for ball in self.p.objs if math.sqrt(ball.v.x**2 + ball.v.y**2) > 0.5]\
                or not [f for f, _ in self.fitness if f!= -100]:
                    self.gen_tick = -1
        self.p.draw()
        return

    def mutate(self, best):
        x, y, v_x, v_y = float(best.p.x), float(best.p.y), float(best.v.x), float(best.v.y)
        self.p.delBalls()
        self.p.addBall(x, y, v_x, v_y, 255, 0, 0)
        for _ in range(0, self.gen_size - 2):
            self.p.addBall(\
                x + random.uniform(-(self.mutation_rate*3), self.mutation_rate*3),\
                y + random.uniform(-(self.mutation_rate*3), self.mutation_rate*3),\
                v_x + random.uniform(-self.mutation_rate, self.mutation_rate),\
                v_y + random.uniform(-self.mutation_rate, self.mutation_rate),\
                random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
        # unicorn
        self.p.addBall(random.uniform(200, 500), random.uniform(150, 350),\
             random.uniform(-10, 10), random.uniform(-10, 10),\
             random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
        return

#    def mutate(self, best):
#        x, y, v_x, v_y = float(best.p.x), float(best.p.y), float(best.v.x), float(best.v.y)
#        del(self.p)
#        self.p = physics.PhysicSim()
#        base = list(bytearray(struct.pack('4f', x, y, v_x, v_y)))
#        for _ in range(0, self.gen_size):
#            m = base[:]
#            print(m)
#            print(base)
#            for _ in range(0, self.mutation_rate):
#                m[random.randint(0, len(m) - 1)] = random.randint(0, 255)
#                s = str(bytearray(m))
#            ix, iy, ivx, ivy = struct.unpack('4f', s)
#            self.p.addBall(ix, iy, ivx, ivy, \
#                random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
#        return
