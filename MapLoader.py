import xml.etree.ElementTree as ET


# Парсер файла карты
class MapLoader:
    def map_load(self, name):
        tree = ET.parse(name)
        root = tree.getroot()
        # Парсинг атрибутов ширины и высоты
        width, height = int(root.attrib['width']), int(root.attrib['height'])
        # Количество слоев
        layers = len(tree.findall('layer'))
        # Трехмерный массив, отвечающий за координаты тайлов
        res = [[[0 for _ in range(width)] for _ in range(height)] for _ in range(layers)]

        # Счетчик слоев
        z = 0
        for xml_string in root.iter('data'):
            data = xml_string.text.split(',')
            for y in range(height):
                for x in range(width):
                    tile_id = int(data[y * height + x])
                    res[z][y][x] = tile_id
            z += 1
        return res, width, height, layers
