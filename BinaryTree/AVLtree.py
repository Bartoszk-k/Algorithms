from PIL import Image, ImageDraw, ImageFont
import math


class BinaryNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 0

    def height_difference(self):
        left_height = self.left.height if self.left else -1
        right_height = self.right.height if self.right else -1
        return left_height - right_height

    def compute_height(self):
        left_height = self.left.height if self.left else -1
        right_height = self.right.height if self.right else -1
        self.height = 1 + max(left_height, right_height)


class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, key):
        self.root =  self._insert(self.root, key)

    def _insert(self, current, key):
        if current is None:
            return BinaryNode(key)
        if key < current.key:
            current.left = self._insert(current.left, key)
            current = self.resolve_left_leaning(current)
        else:
            current.right = self._insert(current.right, key)
            current = self.resolve_right_leaning(current)

        current.compute_height()
        return current

    def resolve_left_leaning(self, node):
        if node.height_difference() == 2:
            if  node.left.height_difference() >= 0:
                node = self.rotate_right(node)
            else:
                node = self.rotate_left_right(node)
        return node

    def resolve_right_leaning(self, node):
        if node.height_difference() == -2:
            if  node.right.height_difference() <= 0:
                node = self.rotate_left(node)
            else:
                node = self.rotate_right_left(node)
        return node

    @staticmethod
    def rotate_left_right(node):
        child = node.left
        new_node = child.right

        child.right = new_node.left
        node.left = new_node.right

        new_node.left = node
        new_node.right = child

        node.compute_height()
        child.compute_height()
        return new_node

    @staticmethod
    def rotate_right_left(node):
        child = node.right
        new_node = child.left

        child.right = new_node.left
        node.left = new_node.right

        new_node.right = node
        new_node.left = child

        node.compute_height()
        child.compute_height()
        return new_node

    @staticmethod
    def rotate_left(node):
        child = node.right

        node.right = child.left
        child.left = node

        node.compute_height()
        child.compute_height()
        print('left')
        return child

    @staticmethod
    def rotate_right(node):
        child = node.left

        node.left = child.right
        child.right = node

        node.compute_height()
        child.compute_height()
        print('right')
        return child

    def inorder(self, node):
        if node is not None:
            self.inorder(node.left)
            print(node.key, end=" ")
            self.inorder(node.right)


    def compute_height(self, current=None):
        if current is None:
            return -1
        left_height = self.compute_height(current.left)
        right_height = self.compute_height(current.right)
        return max(left_height, right_height) + 1

    def draw_tree(self):
        width, height = 800, 600
        image = Image.new("RGB", (width, height), "white")
        draw = ImageDraw.Draw(image)

        self._draw_tree_recursive(self.root, image, draw, x=int(width / 2), y=100, level=0, width=self.compute_height(self.root) * 80)

        # Wyświetlanie obrazu
        image.show()

    def _draw_tree_recursive(self, current, image, draw, x, y, level, width):
        """
        Rysowanie drzewa:
        x - współrzędna x środka okręgu aktualnego węzła
        y - współrzędna y środka okręgu aktualnego węzła
        level - wysokość liczona od góry
        width - długość linii łączącej węzły
        """

        if current is None:
            return

        height = self.compute_height(self.root)  # wysokość drzewa

        radius = int((1 / (height + 1)) * 150)
        font_size = int((1 / (height + 1)) * 150) - 10
        font = ImageFont.truetype("arial.ttf", font_size)

        # Obliczanie wymiarów tekstu
        bbox = draw.textbbox((x - radius, y - radius), str(current.key), font=font)
        text_width = bbox[2] - bbox[0]
        text_height = (bbox[3] - bbox[1]) + 7

        # Rysowanie węzła
        draw.ellipse((x - radius, y - radius, x + radius, y + radius), outline="black", width=3)

        # Rysowanie tekstu
        draw.text((x - text_width / 2, y - text_height / 2), str(current.key), font=font, fill="black")

        # Rysowanie połączeń
        if current.left:
            # Obliczanie środka lewego węzła
            left_child_x = x - width
            left_child_y = y + 3 * radius

            # Obliczanie punktów na obwodzie
            dx = left_child_x - x
            dy = left_child_y - y
            distance = math.sqrt(dx ** 2 + dy ** 2)
            parent_x = x + radius * dx / distance
            parent_y = y + radius * dy / distance
            child_x = left_child_x - radius * dx / distance
            child_y = left_child_y - radius * dy / distance

            # Rysowanie linii
            draw.line([parent_x, parent_y, child_x, child_y], fill="black", width=3)

            # Przejście do lewego poddrzewa
            self._draw_tree_recursive(current.left, image, draw, left_child_x, left_child_y, level + 1, width / 2)

        if current.right:
            # Obliczanie środka prawego węzła
            right_child_x = x + width
            right_child_y = y + 3 * radius

            # Obliczanie punktów na obwodzie
            dx = right_child_x - x
            dy = right_child_y - y
            distance = math.sqrt(dx ** 2 + dy ** 2)
            parent_x = x + radius * dx / distance
            parent_y = y + radius * dy / distance
            child_x = right_child_x - radius * dx / distance
            child_y = right_child_y - radius * dy / distance

            # Rysowanie linii
            draw.line([parent_x, parent_y, child_x, child_y], fill="black", width=3)

            self._draw_tree_recursive(current.right, image, draw, right_child_x, right_child_y, level + 1, width / 2)


# Przykład użycia
tree = BinarySearchTree()
tab = [10,5,15,3,4,6,8]
for item in tab:
    tree.insert(item)

tree.inorder(tree.root)

print(tree.compute_height(tree.root))
tree.draw_tree()
