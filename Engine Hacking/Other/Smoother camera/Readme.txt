replace get_camera_position() in unit_path_movement_component.py with:
Made by Starlow




    def get_camera_position(self):
        if not self.event or not self.unit.position:
            return self.unit.position

        return (
            self.unit.position[0] + self.unit.sprite.offset[0] / TILEWIDTH,
            self.unit.position[1] + self.unit.sprite.offset[1] / TILEHEIGHT)