import numpy as np

class Grid(object):
    """ Finds the number of times one must apply the function,
        f(a, b) = a * a + b, to each point before the result exceeds
        Grid.threshold.

        If Grid.elementwise equals True, Grid.fill() uses a straight-forward,
        ineffecient method, one element at a time:
            for every point, x, on the horizontal axis
                for every point, y, on the vertical axis
                    find the number of times one must apply the function

        If Grid.elementwise equals False, Grid.fill() uses a faster array
        method instead
    """

    DEFAULT_THRESHOLD       = 4.0
    DEFAULT_MAX_ITERATIONS  = 255
    DEFAULT_SCALE           = 3.0
    MAGNIFICATION_PER_CLICK = 0.5
    MANDLEBROT              = lambda x, y: x ** 2 + y
    TOWER                   = lambda x, y: x ** x + y

    def __init__(self, width, height, elementwise=False, centre=complex(0, 0),
                 scale=DEFAULT_SCALE, threshold=DEFAULT_THRESHOLD,
                 iterations=DEFAULT_MAX_ITERATIONS, funct=MANDLEBROT):
        self.centre, self.scale           = centre, scale
        self.elementwise, self.threshold  = elementwise, threshold
        self.width, self.height           = width, height
        self.funct                        = funct
        self.halfwidth, self.halfheight   = width // 2, height // 2
        self.widthrange, self.heightrange = range(width), range(height)
        self.iterations                   = range(1, iterations)
        self.aspectratio                  = height / width if width > 0 else 0

    def checknum(self, number):
        newval = number
        for iteration in self.iterations:
            newval = self.funct(newval, number)
            if abs(newval) > self.threshold:
                return iteration
        return False

    def zoom(self, pixelposition, magnification=MAGNIFICATION_PER_CLICK):
        self.centre = complex(grid.fetchreal(pixelposition[0]),
                              grid.fetchimaginary(pixelposition[1]))
        self.scale *= magnification

    def fill(self, displaysurface=None):
        if self.elementwise:
            try:
                result = 0
                for xpixel in self.widthrange:
                    x = self.fetchreal(xpixel)
                    for ypixel in self.heightrange:
                        y = self.fetchimaginary(ypixel)
                        exclusion = self.checknum(complex(x, y))
                        if exclusion:
                            if displaysurface:
                                redandgreen = 256 - exclusion
                                displaysurface.set_at((xpixel, ypixel),
                                                      (redandgreen, redandgreen, 255))
                            else:
                                result += exclusion
                return result
            except ZeroDivisionError:
                raise RuntimeError("Grid too small to fill") from ZeroDivisionError
        elif displaysurface:
            complexvals     = (np.linspace(self.fetchreal(), self.fetchreal(self.width),
                                           self.width).reshape((self.width, 1)) + 1j *
                               np.linspace(self.fetchimaginary(),
                                           self.fetchimaginary(self.height),
                                           self.height).reshape((1, self.height)))
            stillchecking   = np.full(complexvals.shape, True, dtype=bool)
            newvalues       = np.zeros(complexvals.shape, dtype=np.complex128)
            iterationcounts = np.zeros(newvalues.shape, dtype=int)
            for iteration in self.iterations:
                newvalues[stillchecking] = self.funct(newvalues[stillchecking],
                                                      complexvals[stillchecking])
                iterationcounts[np.greater(np.abs(newvalues), self.threshold,
                                           out=np.full(complexvals.shape, False),
                                           where=stillchecking)] = iteration
                stillchecking[np.abs(newvalues) > self.threshold] = False
            displaysurface.blit(pygame.surfarray.make_surface(iterationcounts), (0, 0))
            pygame.display.update()

    def fetchreal(self, abscissa=0):
        return (self.centre.real + self.scale * (abscissa - self.halfwidth) /
               self.halfwidth)

    def fetchimaginary(self, ordinate=0):
        return (self.centre.imag + self.aspectratio * self.scale *
            (ordinate - self.halfheight) / self.halfheight)


if __name__ == '__main__':
    ELEMENTWISE = False

    import pygame

    screen = pygame.display.set_mode((200, 150), 24)
    grid = Grid(200, 150, ELEMENTWISE, funct=Grid.MANDLEBROT)
    grid.fill(screen)
    pygame.display.flip()
    show, buttonClear = True, True
    while show:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                buttonClear = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if buttonClear:
                    grid.zoom(pygame.mouse.get_pos())
                    buttonClear = False
                    screen.fill((0, 0, 0),)
                    pygame.display.flip()
                    grid.fill(screen)
                    pygame.display.flip()
            if (event.type == pygame.KEYDOWN) or (event.type == pygame.QUIT):
                show = False
