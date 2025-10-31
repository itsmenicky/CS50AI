import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        # Nesta função eu devo mapear todas as variáveis do domínio e verificar
        # o tamanho da mesma, para assim comparar se as palavras disponíveis 
        # são consistentes com a variável.
        for var in self.domains:
            self.domains[var] = {
                word for word in self.domains[var]
                if len(word) == var.length
            }

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        # Inicializando variável de revisão
        revised = False
        # Verificando se há sobreposição entre as variáveis
        overlap = self.crossword.overlaps.get((x, y))
        if overlap == None:
            return revised
        # Em caso de existir sobreposição, capturamos as coordenadas
        i, j = overlap
        # Inicializamos um set onde iremos armazenar as palavras a eliminar
        # do domínio de x
        to_remove = set()
        # Percorremos o domínio de x e y verificando se cada palavra em x tem 
        # pelo menos compatibilidade com alguma em y
        for word_x in self.domains[x]:
            compatible = False
            for word_y in self.domains[y]:
                if word_x[i] == word_y[j]:
                    compatible = True
                    break
            if not compatible:
                to_remove.add(word_x)
                
        # Verificando as palavras a remover e retornando o revised
        if to_remove:
            self.domains[x] -= to_remove
            revised = True
            return revised
        
    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        # Inicializando fila de arcos
        if arcs is None:
            queue = [
                (x, y)
                for x in self.crossword.variables
                for y in self.crossword.neighbors(x)
            ]
        else:
            queue = list(arcs)
            
        # Processando a fila
        
        while queue:
            x, y = queue.pop(0)
            # Aplicando o algoritmo de revisão
            if self.revise(x, y):
                # Se o domínio de x ficou vazio, o problema é insolúvel
                if not self.domains[x]:
                    return False
                # Adiciona todos os vizinhos de x (exceto y) de volta na fila
                for z in self.crossword.neighbors(x):
                    if z != y:
                        queue.append((z, x))
                        
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        # Retorna se todas as variáveis do problema estão presentes no assignment
        if set(assignment.keys()) == set(self.crossword.variables):
            return True
        else:
            return False

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        # Verifica a unicidade das palavras
        if len(set(assignment.values())) < len(assignment):
            return False
        for x in assignment:
            word_x = assignment[x]
            # Verifica se o comprimento da palavra corresponde à variável
            if len(word_x) != x.length:
                return False
            for y in assignment:
                if x == y:
                    continue
                overlap = self.crossword.overlaps.get((x, y))
                if overlap:
                    i, j = overlap
                    word_y = assignment[y]
                    if word_x[i] != word_y[j]:
                        return False
        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        def count_conflicts(value):
            count = 0
            for neighbor in self.crossword.neighbors(var):
                if neighbor in assignment:
                    continue
                overlap = self.crossword.overlaps.get((var, neighbor))
                if overlap:
                    i, j = overlap
                    for neighbor_value in self.domains[neighbor]:
                        if value[i] != neighbor_value[j]:
                            count += 1
            return count

        return sorted(self.domains[var], key=count_conflicts)

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        unassigned = [
            var for var in self.crossword.variables
            if var not in assignment
        ]

        # Ordena por número de valores no domínio (MRV), depois por grau (número de vizinhos)
        return min(
            unassigned,
            key=lambda var: (len(self.domains[var]), -len(self.crossword.neighbors(var)))
        )

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        # Verifica se a atribuição está completa
        if self.assignment_complete(assignment):
            return assignment

        # Seleciona uma variável não atribuída
        var = self.select_unassigned_variable(assignment)

        # Tenta cada valor do domínio, ordenado pela heurística de menor restrição
        for value in self.order_domain_values(var, assignment):
            # Cria uma cópia da atribuição atual
            new_assignment = assignment.copy()
            new_assignment[var] = value

            # Verifica se a nova atribuição é consistente
            if self.consistent(new_assignment):
                # Opcional: aplica inferência com AC-3
                domains_backup = self.domains.copy()
                self.domains[var] = {value}
                if self.ac3(arcs=[
                    (neighbor, var)
                    for neighbor in self.crossword.neighbors(var)
                    if neighbor not in new_assignment
                ]):
                    result = self.backtrack(new_assignment)
                    if result is not None:
                        return result
                # Restaura os domínios se a inferência falhar
                self.domains = domains_backup

        # Se nenhum valor funcionar, retorna None
        return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
