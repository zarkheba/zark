from random import shuffle
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Paragraph, Table, TableStyle, Spacer


class WordSearch:
    def __init__(self, words, size=15, backward_chance=0.1):
        self.words = words
        self.size = size
        self.backward_chance = backward_chance
        self.grid = [[' ' for _ in range(size)] for _ in range(size)]
        self.populate_grid()
        
    def populate_grid(self):
        # Place words randomly on the grid
        for word in self.words:
            placed = False
            while not placed:
                direction = self.get_random_direction()
                row, col = self.get_random_position()
                if self.can_place_word(word, row, col, direction):
                    self.place_word(word, row, col, direction)
                    placed = True

        # Fill empty spaces with random letters
        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i][j] == ' ':
                    self.grid[i][j] = self.get_random_letter()
                    
    def get_random_direction(self):
        # Choose a random direction (horizontal, vertical, or diagonal)
        directions = ['H', 'V', 'D']
        return shuffle(directions)[0]
    
    def get_random_position(self):
        # Choose a random position on the grid
        return (random.randint(0, self.size - 1), random.randint(0, self.size - 1))
    
    def can_place_word(self, word, row, col, direction):
        # Check if the word can be placed at the given position and direction
        if direction == 'H':
            return col + len(word) <= self.size
        elif direction == 'V':
            return row + len(word) <= self.size
        elif direction == 'D':
            return col + len(word) <= self.size and row + len(word) <= self.size
    
    def place_word(self, word, row, col, direction):
        # Place the word on the grid
        for i, letter in enumerate(word):
            if direction == 'H':
                self.grid[row][col + i] = letter
            elif direction == 'V':
                self.grid[row + i][col] = letter
            elif direction == 'D':
                self.grid[row + i][col + i] = letter
    
    def get_random_letter(self):
        # Choose a random letter from the alphabet
        return chr(ord('A') + random.randint(0, 25))
    
    def draw_puzzle(self, canvas):
        # Draw the puzzle on the canvas
        for i in range(self.size):
            for j in range(self.size):
                canvas.drawString(j * 0.5 * inch, (self.size - i - 1) * 0.5 * inch, self.grid[i][j])
    
    def draw_solution(self, canvas):
        # Draw the solution on the canvas
        for word in self.words:
            for i in range(self.size):
                for j in range(self.size):
                    if self.grid[i][j] == word[0]:
                        if self.check_word(word, i, j, 'H'):
                            self.draw_word(canvas, word, i, j, 'H')
                        elif self.check_word(word, i, j, 'V'):
                            self.draw_word(canvas, word, i, j, 'V')
                        elif self.check_word(word, i, j, 'D'):
                            self.draw_word(canvas, word, i, j, 'D')
    
    def check_word(self, word, row, col, direction):
        # Check if the word can be found starting at the given position and direction
        if direction == 'H':
            if col + len(word) > self.size:
                return False
            for i, letter in enumerate(word):
                if self.grid[row][col + i] != letter:
                    return False
            return True
        elif direction == 'V':
            if row + len(word) > self.size:
                return False
            for i, letter in enumerate(word):
                if self.grid[row + i][col] != letter:
                    return False
            return True
        elif direction == 'D':
            if col + len(word) > self.size or row + len(word) > self.size:
                return False
            for i, letter in enumerate(word):
                if self.grid[row + i][col + i] != letter:
                    return False
            return True
    
    def draw_word(self, canvas, word, row, col, direction):
        # Draw the word on the canvas
        for i, letter in enumerate(word):
            if direction == 'H':
                canvas.drawString(col * 0.5 * inch, (self.size - row - 1) * 0.5 * inch, letter)
            elif direction == 'V':
                canvas.drawString(col * 0.5 * inch, (self.size - row - i - 1) * 0.5 * inch, letter)
            elif direction == 'D':
                canvas.drawString((col + i) * 0.5 * inch, (self.size - row - i - 1) * 0.5 * inch, letter)
    
    def draw_legend(self, canvas):
        # Draw the legend on the canvas
        styles = getSampleStyleSheet()
        style = styles['Normal']
        words = []
        for word in self.words:
            words.append((word, ''))
        table = Table(words, style=[('ALIGNMENT', (1,1), (-1,-1), 'RIGHT')])
        table.wrapOn(canvas, 0.5 * inch, 0.5 * inch)
        table.drawOn(canvas, 0.5 * inch, 0.5 * inch)
    

def create_word_search_puzzle(words, filename):
    # Create a word search puzzle and save it to a PDF file
    puzzle = WordSearch(words)
    canvas = Canvas(filename, pagesize=letter)
    puzzle.draw_puzzle(canvas)
    canvas.showPage()
    puzzle.draw_solution(canvas)
    puzzle.draw_legend(canvas)
    canvas.save()

if __name__ == '__main__':
    words = ['HELLO', 'WORLD', 'PYTHON', 'PROGRAMMING']
    create_word_search_puzzle(words, 'word_search.pdf')
