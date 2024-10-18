import numpy as np
from DrawObjects import DrawObject
from pygame import Surface, draw, font


def _get_face_array_length(array: np.array) -> int:
    length = len(array)
    for i in np.arange(length):
        if array[i] == -1:
            return i
    return length


class Camera:
    def __init__(self, screen: Surface) -> None:
        self.x = 0
        self.y = 0
        self.z = 0

        self.__screen = screen
        self.__view_matrix = 0
        self.__projection_matrix = 0

        self.font = font.SysFont(None, 24)

    def set_position(self, x: float, y: float, z: float) -> None:
        self.x = x
        self.y = y
        self.z = z

        translation_matrix = np.asarray([[1, 0, 0, 0],
                                          [0, 1, 0, 0],
                                          [0, 0, 1, 0],
                                          [-self.x, -self.y, -self.z, 1]], dtype='float')

        reflection_matrix = np.asarray([[-1, 0, 0, 0],
                                         [0, 1, 0, 0],
                                         [0, 0, 1, 0],
                                         [0, 0, 0, 0]], dtype='float')

        rotation_matrix_90 = np.asarray([[1, 0, 0, 0],
                                          [0, 0, -1, 0],
                                          [0, 1, 0, 0],
                                          [0, 0, 0, 1]], dtype='float')

        d = np.sqrt(self.x**2 + self.y**2)
        c = s = 0
        if d == 0:
            c = 1
            s = 1
        else:
            c = self.y / d
            s = self.x / d

        rotation_matrix_u = np.asarray([[c, 0, s, 0],
                                         [0, 1, 0, 0],
                                         [-s, 0, c, 0],
                                         [0, 0, 0, 1]], dtype='float')

        l = np.sqrt(d * d + self.z * self.z)

        if l == 0:
            c = 1
            s = 0
        else:
            c = d / l
            s = self.z / l

        rotation_matrix_w = np.asarray([[1, 0, 0, 0],
                                         [0, c, -s, 0],
                                         [0, s, c, 0],
                                         [0, 0, 0, 1]], dtype='float')

        self.__view_matrix = np.dot(
            np.dot(np.dot(np.dot(translation_matrix, reflection_matrix), rotation_matrix_90), rotation_matrix_u), rotation_matrix_w)

    def set_orthographic_projection(self, offset_x: float, offset_y: float, zoom: float) -> None:
        self.__projection_matrix = np.array([[zoom, 0, 0, 0],
                                              [0, -zoom, 0, 0],
                                              [0, 0, 0, 0],
                                              [offset_x, offset_y, 0, 1]])

    def render(self, figure: DrawObject) -> None:
        points_3d = figure.get_draw_points()
        points_3d = np.hstack([points_3d, np.ones((points_3d.shape[0], 1))])
        points = np.dot(np.dot(points_3d, self.__view_matrix), self.__projection_matrix)

        center_point_3d = figure.get_center_points()
        center_point_3d = np.hstack([center_point_3d, np.array([1])])
        center_point = np.dot(np.dot(center_point_3d, self.__view_matrix), self.__projection_matrix)
        draw.circle(self.__screen, (255, 0, 0), center_point[:2], 5, 5)

        for face in figure.faces:
            A, B, C, D = figure.find_flat_coefficients(points_3d[face[0]], points_3d[face[1]], points_3d[face[2]])
            if figure.is_facing(A, B, C, D, self.x, self.y, self.z,
                               center_point_3d[0], center_point_3d[1], center_point_3d[2]):
                face_length = _get_face_array_length(face)

                img1 = self.font.render(str(face[0]), True, (0, 0, 255))
                self.__screen.blit(img1, points[face[0]][:2])

                for i in np.arange(face_length):
                    draw.line(self.__screen, figure.color,
                              points[face[i]][:2], points[face[(i + 1) % face_length]][:2])

    def draw_center(self) -> None:
        x, y = self.__screen.get_size()
        points = [x // 2, y // 2, 0, 1]
        points = np.dot(np.dot(points, self.__view_matrix), self.__projection_matrix)
        draw.circle(self.__screen, (255, 0, 0), points[:2], 5)

    def draw_figure(self, cords: np.array) -> None:
        cords = np.hstack([cords, np.ones([cords.shape[0], 1])])
        cords = np.dot(np.dot(cords, self.__view_matrix), self.__projection_matrix)
        for cord in cords:
            draw.circle(self.__screen, (255, 0, 0), cord[:2], 5)
