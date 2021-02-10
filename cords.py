from math import cos, sin, radians, floor
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure


class Cords:
    def __init__(self, x: list[float], y: list[float]) -> None:
        if len(x) != len(y):
            raise ValueError('x should be as long as y')
        x.append(x[0])
        y.append(y[0])
        self.x = x 
        self.y = y

    def scale(self, scale_x: float = 1, scale_y: float = 1) -> None:
        if scale_x < 0 or scale_y < 0:
            raise ValueError('Scaling index cannot be less than 0')

        self.x = [x1 * scale_x for x1 in self.x]
        self.y = [y1 * scale_y for y1 in self.y]

    def rotate(self, angle: int) -> None:
        angle = radians(angle)
    
        for i in range(len(self.x)):
            self.x[i] = floor(self.x[i] * cos(angle) - self.y[i] * sin(angle))
            self.y[i] = floor(self.x[i] * sin(angle) + self.y[i] * cos(angle))

        self.x = self._scale_coords(self.x)
        self.y = self._scale_coords(self.y)

    def move(self, move_x: float = 0, move_y: float = 0) -> None:
        self.x = [x1 + move_x for x1 in self.x]
        self.y = [y1 + move_y for y1 in self.y]

        self.x = self._scale_coords(self.x)
        self.y = self._scale_coords(self.y)
    
    def _scale_coords(self, cords: list[float]) -> list[float]:
        if not all(i > 0 for i in cords):
            m = abs(min(cords))
            cords = [xi + m for xi in cords]
        return cords
    
    def to_plot(self, filename: str = 'output.png') -> None:
        fig = Figure()
        plot = fig.add_subplot(111)
        plot.plot(self.x, self.y, 'b')
        plot.set_title('transformation')
        plot.set_ylim(ymin=-1, ymax=max(self.y) + 1)
        plot.set_xlim(xmin=-1, xmax=max(self.x) + 1)
        canvas = FigureCanvas(fig)
        canvas.print_figure(filename)