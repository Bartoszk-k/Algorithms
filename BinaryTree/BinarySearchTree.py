from PIL import Image, ImageDraw, ImageFont
import math



class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None


class BinarySearchTree:
    def __init__(self):
        self.root = None
        self.height = 0

    def insert(self, key):
        if self.root == None:
            self.root = Node(key)
        else:
            self._insert_recursive(self.root, key)

    def _insert_recursive(self, current, key):
        if key < current.key:
            if current.left == None:
                current.left = Node(key)
            else:
                self._insert_recursive(current.left, key)

        elif key > current.key:
            if current.right == None:
                current.right = Node(key)
            else:
                self._insert_recursive(current.right, key)

    def search(self, current, key):
        if current == None:
            return False
        if current.key == key:
            return True
        if key < current.key:
            return self.search(current.left, key)
        if key > current.key:
            return self.search(current.right, key)

    def inorder(self, node):
        if node is not None:
            self.inorder(node.left)
            print(node.key, end=" ")
            self.inorder(node.right)

    def find_min(self):
        return self._find_min_recursive(self.root)

    def _find_min_recursive(self,current):
        if current.left == None:
            return current.key
        else:
            return self._find_min_recursive(current.left)


    def find_max(self):
        return self._find_max_recursive(self.root)

    def _find_max_recursive(self, current):
        if current.right == None:
            return current.key
        else:
            return self._find_max_recursive(current.right)

    def compute_height(self,current= None):
        if current is None:
            return -1
        left_height = self.compute_height(current.left)
        right_height = self.compute_height(current.right)
        return max(left_height, right_height) + 1

    def draw_tree(self):
         width, height = 800, 600
         image = Image.new("RGB", (width, height), "white")
         draw = ImageDraw.Draw(image)

         self._draw_tree_recursive(self.root, image, draw, x=int(width / 2), y=100, level=0, width=self.compute_height(self.root)*50)

         #wyswietlanie obrazu
         image.show()

    def _draw_tree_recursive(self, current, image, draw, x, y, level, width):

        """
        Rysowanie drzewa:
        x-wspolzedna x srodka okregu aktualnego wezla
        y-wspolzedna y srodka okregu aktualnego wezla
        level - wysokosc liczona od gory
        width - dlugosc lini laczacej wezly
        """

        if current is None:
            return

        height = self.compute_height(self.root) # wysokość drzewa

        radius =  int((1/ (height +1))*150)
        font_size = int((1/(height+1))*150)-10
        font = ImageFont.truetype("arial.ttf", font_size)

        #oblicznie wymiarów tekstu
        bbox = draw.textbbox((x - radius, y - radius), str(current.key), font=font)
        text_width = bbox[2] - bbox[0]
        text_height = (bbox[3] - bbox[1]) +7

        #rysowanie wezla
        draw.ellipse((x - radius, y - radius, x + radius, y + radius), outline="black", width=3)

        # Rysowanie tekstu
        draw.text((x - text_width / 2, y - text_height / 2), str(current.key), font=font, fill="black")

        # Rysowanie połączeń
        if current.left:
            #oblicznie srodka lewego wezla
            left_child_x = x - width
            left_child_y = y + 3 * radius

            #oblicznie punktow na obwodzie
            dx = left_child_x - x
            dy = left_child_y - y
            distance = math.sqrt(dx ** 2 + dy ** 2)
            parent_x = x + radius * dx / distance
            parent_y = y + radius * dy / distance
            child_x = left_child_x - radius * dx / distance
            child_y = left_child_y - radius * dy / distance

            #rysowanie lini
            draw.line([parent_x, parent_y, child_x, child_y], fill="black", width=3)

            # przejście do lewego poddrzewa
            self._draw_tree_recursive(current.left, image, draw, left_child_x, left_child_y, level + 1, width / 2)

        if current.right:
            #oblicznie srodka prawego wezla
            right_child_x = x + width
            right_child_y = y + 3 * radius

            # oblicznie punktow na obwodzie
            dx = right_child_x - x
            dy = right_child_y - y
            distance = math.sqrt(dx ** 2 + dy ** 2)
            parent_x = x + radius * dx / distance
            parent_y = y + radius * dy / distance
            child_x = right_child_x - radius * dx / distance
            child_y = right_child_y - radius * dy / distance

            #rysowanie lini
            draw.line([parent_x, parent_y, child_x, child_y], fill="black", width=3)

            self._draw_tree_recursive(current.right, image, draw, right_child_x, right_child_y, level + 1, width / 2)


tree = BinarySearchTree()
tree.insert(10)
tree.insert(5)
tree.insert(15)
tree.insert(3)
tree.insert(7)
tree.insert(6)

tree.inorder(tree.root)
print(tree.search(tree.root,7))
print(tree.find_min())
print(tree.find_max())
print(tree.compute_height(tree.root))
tree.draw_tree()
