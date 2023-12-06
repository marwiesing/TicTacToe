class Gameboard:
    def __init__(self, x, y, width, height, rows, columns):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rows = rows
        self.columns = columns
        self.row_spacing = height / rows
        self.col_spacing = width / columns

    def get_field_number(self, click_x, click_y):
        for row in range(self.rows):
            for col in range(self.columns):
                x1 = self.x + col * self.col_spacing
                x2 = x1 + self.col_spacing
                y1 = self.y + row * self.row_spacing
                y2 = y1 + self.row_spacing

                if x1 <= click_x <= x2 and y1 <= click_y <= y2:
                    return row * self.columns + col + 1
        return None