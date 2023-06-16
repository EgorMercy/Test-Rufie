from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt5.QtGui import QPainter, QColor
import sys
from random import randint, choice
 
 
WIDTH = 600
HEIGHT = 600
 
BLACK = QColor(0, 0, 0)
WHITE = QColor(255, 255, 255)
GREEN = QColor(0, 255, 0)
RED = QColor(255, 0, 0)
 
 
class Snake:
    def __init__(self):
        self.size = 1
        self.positions = [(WIDTH // 2, HEIGHT // 2)]
        self.direction = choice([Qt.Key_W, Qt.Key_S, Qt.Key_A, Qt.Key_D])
        self.timer = QTimer()
        self.timer.timeout.connect(self.move)
        self.timer.start(30)
 
    def get_head_position(self):
        return self.positions[0]
 
    def move(self):
        x, y = self.get_head_position()
        if self.direction == Qt.Key_W:
            y -= 10
        elif self.direction == Qt.Key_S:
            y += 10
        elif self.direction == Qt.Key_A:
            x -= 10
        elif self.direction == Qt.Key_D:
            x += 10
 
        self.positions.insert(0, (x, y))
        if len(self.positions) > self.size:
            self.positions.pop()
 
    def draw(self, painter):
        for position in self.positions:
            painter.fillRect(position[0], position[1], 10, 10, GREEN)
 
    def check_collision_self(self):
        head = self.get_head_position()
        for position in self.positions[1:]:
            if head == position:
                return True
        return False
 
    def check_collision(self):
        head = self.get_head_position()
        if (head[0] < 0 or head[0] >= WIDTH 
                or head[1] >= HEIGHT or head[1] < 0 
                or self.check_collision_self()):
            return True
        return False
 
    def inc_size(self):
        self.size += 1
    
    def inc_score(self):
        self.score += 1
 
class Fruit:
    def __init__(self):
        self.position = (0, 0)
        self.spawn()
 
    def spawn(self):
        x = randint(0, WIDTH // 10 - 1) * 10
        y = randint(0, HEIGHT // 10 - 1) * 10
        self.position = (x, y)
 
    def draw(self, painter):
        painter.fillRect(self.position[0], self.position[1], 10, 10, RED)
 
 
class SnakeGame(QMainWindow):
    def __init__(self):
        super().__init__()
 
        self.setWindowTitle("Змейка")
        self.setGeometry(100, 100, WIDTH, HEIGHT)
 
        self.btn_start = QPushButton("Начать игру", self)
        self.btn_start.setGeometry(250, 250, 100, 50)
        self.btn_start.clicked.connect(self.start_game)
 
        self.btn_reset = QPushButton("Рестарт", self)
        self.btn_reset.setGeometry(250, 300, 100, 50)
        self.btn_reset.clicked.connect(self.reset_game)
        self.btn_reset.hide() 
 
        self.btn_exit = QPushButton("Выход", self)
        self.btn_exit.setGeometry(250, 350, 100, 50)
        self.btn_exit.clicked.connect(QApplication.instance().quit)
 
        self.snake = Snake()
        self.fruit = Fruit()
        self.run = False
 
    def reset_game(self):
        self.snake = Snake()
        self.fruit = Fruit()
        self.run = True
        self.btn_start.hide()
        self.btn_exit.hide()
        self.btn_reset.hide()
 
    def start_game(self):
        self.run = True
        self.btn_start.setDisabled(True)
        self.btn_start.hide()
        self.btn_exit.hide() 
 
    def keyPressEvent(self, event):
        if self.run:
            if event.key() == Qt.Key_W and self.snake.direction != Qt.Key_S:
                self.snake.direction = Qt.Key_W
            elif event.key() == Qt.Key_S and self.snake.direction != Qt.Key_W:
                self.snake.direction = Qt.Key_S
            elif event.key() == Qt.Key_A and self.snake.direction != Qt.Key_D:
                self.snake.direction = Qt.Key_A
            elif event.key() == Qt.Key_D and self.snake.direction != Qt.Key_A:
                self.snake.direction = Qt.Key_D
 
    def paintEvent(self, event):
        if self.run:
            if self.snake.get_head_position() == self.fruit.position:
                self.snake.inc_size()
                self.fruit.spawn()
 
            if self.snake.check_collision():
                self.run = False
                self.btn_start.setDisabled(False)
                # self.btn_start.show()
                self.btn_exit.show()
                self.btn_reset.show()
 
            painter = QPainter(self)
            painter.setPen(Qt.NoPen)
            painter.setBrush(BLACK)
            painter.drawRect(0, 0, WIDTH, HEIGHT)
            painter.setPen(WHITE)
            painter.drawText(10, 20, f'Score', )
 
            self.snake.draw(painter)
            self.fruit.draw(painter)
 
            painter.end()
            self.update()
 
app = QApplication([])
window = SnakeGame()
window.show()
sys.exit(app.exec_())