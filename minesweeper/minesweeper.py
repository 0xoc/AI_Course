import itertools
import random
import copy

class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __hash__(self):
        return hash(tuple(self.cells))
    
    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if len(self.cells) == self.count:
            return copy.deepcopy(self.cells)
        
        return ()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        
        if self.count == 0:
            return copy.deepcopy(self.cells)

        return ()


    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = set()
    
    def get_neighbors(self, cell):
        """
        return the neighboring cells
        """
        n = []
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    n.append((i,j))
        return n

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """

        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        e = Sentence([],0)
        self.moves_made.add(cell)
        self.mark_safe(cell)
        
        new_sentences = set()
        new_sentences.add(Sentence(self.get_neighbors(cell), count))

        while len(new_sentences):
            # add them to AI knowlage
            self.knowledge.update(new_sentences)

            # clear
            new_sentences = set()

            # pass 0: Let me tell you what I know to be safe or mine
            for safe in self.safes:
                for sentence in self.knowledge:
                    sentence.mark_safe(safe)
            for mine in self.mines:
                for sentence in self.knowledge:
                    sentence.mark_mine(safe)

            # pass 1: Given what you all know now, is there anything you could tell us for sure
            need_change = True
            while need_change:
                need_change = False
                for sentence in self.knowledge:
                    
                    safes = sentence.known_safes()
                    mines = sentence.known_mines()
                    for safe in safes:
                        if safe not in self.safes:
                            self.mark_safe(safe)
                            need_change = True
                    
                    for mine in mines:
                        if mine not in self.mines:
                            self.mark_mine(mine)
                            need_change = True
            
            # pass 2: Let's see if toghether we can deduce some more information
            for sentence in self.knowledge:
                for other_sentence in self.knowledge:
                    if sentence == other_sentence:
                        continue
                    if sentence.cells.issubset(other_sentence.cells):
                        new_cells = other_sentence.cells - sentence.cells
                        s = Sentence(list(new_cells),other_sentence.count - sentence.count )

                        if s in self.knowledge:
                            continue

                        new_sentences.add(s)


    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        for safe in self.safes:
            if safe not in self.moves_made:
                return safe
        
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        move = random.randrange(self.width), random.randrange(self.height)

        if self.width * self.height == len(self.moves_made) + len(self.mines):
            return None

        while move in self.moves_made or move in self.mines:
            move = random.randrange(self.width), random.randrange(self.height)
        
        return move

