import board_data
from pieces import *

pg.init()
fnt_num = pg.font.Font(FNT_PATH, FNT_SIZE)


class playboard:
    def __init__(self, parent_surface: pg.Surface, cell_qty: int = CELL_QTY, cell_size: int = CELL_SIZE):
        self.__screen = parent_surface
        self.__table = board_data.board
        self.__qty = cell_qty
        self.__size = cell_size
        self.__pieces_types = PIECES_TYPES
        self.__all_cells = pg.sprite.Group()
        self.__all_pieces = pg.sprite.Group()
        self.__all_areas = pg.sprite.Group()
        self.__pressed_cell = None
        self.__picked_piece = None
        self.__prepare_screen()
        self.__draw_playboard()
        self.__draw_all_pieces()
        pg.display.update()


    def __prepare_screen(self):
        back_img = pg.image.load(IMG_PATH + WIN_BG_IMG)
        back_img = pg.transform.scale(back_img, WINDOW_SIZE)
        self.__screen.blit(back_img, (0, 0))


    def __draw_playboard(self):
        total_width = self.__qty * self.__size
        num_fields = self.__create_num_fields()
        self.__all_cells = self.__create_all_cells()
        num_fields_depth = num_fields[0].get_width()
        playboard_view = pg.Surface((
            2 * num_fields_depth + total_width,
            2 * num_fields_depth + total_width
        ))

        playboard_view.blit(num_fields[0],
            (0, num_fields_depth))

        playboard_view.blit(num_fields[0],
            (num_fields_depth + total_width, num_fields_depth))

        playboard_view.blit(num_fields[1],
            (num_fields_depth, 0))

        playboard_view.blit(num_fields[1],
            (num_fields_depth, num_fields_depth + total_width))

        playboard_rect = playboard_view.get_rect()
        playboard_rect.x += (self.__screen.get_width() - playboard_rect.width) // 2
        playboard_rect.y += (self.__screen.get_height() - playboard_rect.height) // 2
        self.__screen.blit(playboard_view, playboard_rect)
        cells_offset = (
            playboard_rect.x + num_fields_depth,
            playboard_rect.y + num_fields_depth,
        )
        self.__draw_cells_on_playboard(cells_offset)


    def __create_num_fields(self):
        n_lines = pg.Surface((self.__qty * self.__size, self.__size // 3))
        n_rows = pg.Surface((self.__size // 3, self.__qty * self.__size))
        for i in range(0, self.__qty):
            letter = fnt_num.render(LTRS[i], True, WHITE)
            number = fnt_num.render(str(CELL_QTY - i), True, WHITE)
            n_lines.blit(letter, (
                i * CELL_SIZE + (CELL_SIZE - letter.get_rect().width) // 2,  # X
                (n_lines.get_height() - letter.get_rect().height) // 2  # Y
            )
                         )
            n_rows.blit(number, (
                (n_rows.get_width() - letter.get_rect().width) // 2,  # X
                i * CELL_SIZE + (CELL_SIZE - number.get_rect().height) // 2  # Y
            )
                        )
        return n_rows, n_lines


    def __create_all_cells(self):
        group = pg.sprite.Group()
        is_even_qty = (self.__qty % 2 == 0)
        cell_color_index = 1 if is_even_qty else 0
        for y in range(self.__qty):
            for x in range(self.__qty):
                cell = Cell(
                    cell_color_index,
                    self.__size,
                    (x, y),
                    LTRS[x] + str(self.__qty - y)
                )
                group.add(cell)
                cell_color_index ^= True
            cell_color_index = cell_color_index ^ True if is_even_qty else cell_color_index
        return group


    def __draw_cells_on_playboard(self, offset):
        for cell in self.__all_cells:
            cell.rect.x += offset[0]
            cell.rect.y += offset[1]
        self.__all_cells.draw(self.__screen)


    def __draw_all_pieces(self):
        self.__setup_board()
        self.__all_pieces.draw(self.__screen)


    def __setup_board(self):
        for j, row in enumerate(self.__table):
            for i, field_value in enumerate(row):
                if field_value != '0':
                    piece = self.__create_piece(field_value, (j, i))
                    self.__all_pieces.add(piece)
            for piece in self.__all_pieces:
                for cell in self.__all_cells:
                    if piece.field_name == cell.field_name:
                        piece.rect = cell.rect


    def __create_piece(self, piece_symbol: str, table_coord: tuple):
        field_name = self.__to_field_name(table_coord)
        piece_tuple = self.__pieces_types[piece_symbol]
        classname = globals()[piece_tuple[0]]
        return classname(self.__size, piece_tuple[1], field_name)


    def __to_field_name(self, table_coord: tuple):
        return LTRS[table_coord[1]] + str(self.__qty - table_coord[0])


    def __get_piece(self, position: tuple):
        for piece in self.__all_pieces:
            if piece.rect.collidepoint(position):
                return piece
        return None


    def __get_cell(self, position: tuple):
        for cell in self.__all_cells:
            if cell.rect.collidepoint(position):
                return cell
        return None


    def btn_down(self, button_type: int, position: tuple):
        self.__pressed_cell = self.__get_cell(position)


    def btn_up(self, button_type: int, position: tuple):
        released_cell = self.__get_cell(position)
        if (released_cell is not None) and (released_cell == self.__pressed_cell):
            if button_type == 3:
                self.__mark_cell(released_cell)
            if button_type == 1:
                self.__pick_cell(released_cell)
        self.__grand_update()

    def __mark_cell(self, cell):
        if not cell.mark:
            mark = Area(cell)
            self.__all_areas.add(mark)
        else:
            for area in self.__all_areas:
                if area.field_name == cell.field_name:
                    area.kill()
                    break
        cell.mark ^= True


    def __pick_cell(self, cell):
        self.__unmark_all_cells()
        if self.__picked_piece is None:
            for piece in self.__all_pieces:
                if piece.field_name == cell.field_name:
                    pick = Area(cell, False)
                    self.__all_areas.add(pick)
                    self.__picked_piece = piece
                    break
        else:
            self.__picked_piece.rect = cell.rect
            self.__picked_piece.field_name = cell.field_name
            self.__picked_piece = None

    def __unmark_all_cells(self):
        self.__all_areas.empty()
        for cell in self.__all_cells:
            cell.mark = False

    def __grand_update(self):
        self.__all_cells.draw(self.__screen)
        self.__all_areas.draw(self.__screen)
        self.__all_pieces.draw(self.__screen)
        pg.display.update()




class Cell(pg.sprite.Sprite):
    def __init__(self, color_index: int, size: int, coords: tuple, name: str):
        super().__init__()
        x, y = coords
        self.color = color_index
        self.field_name = name
        self.image = pg.image.load(IMG_PATH + COLORS[color_index])
        self.image = pg.transform.scale(self.image, (size, size))
        self.rect = pg.Rect(x * size, y * size, size, size)
        self.mark = False

class Area(pg.sprite.Sprite):
    def __init__(self, cell: Cell, type_of_area: bool = True):
        super().__init__()
        coords = (cell.rect.x, cell.rect.y)
        area_size = (cell.rect.width, cell.rect.height)
        if type_of_area:
            picture = pg.image.load(IMG_PATH + 'select_circle.png')
            self.image = pg.transform.scale(picture, area_size)
        else:
            self.image = pg.Surface(area_size).convert_alpha()
            self.image.fill(ACTIVE_CELL_COLOR)
        self.rect = pg.Rect(coords, area_size)
        self.field_name = cell.field_name








