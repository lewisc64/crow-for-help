import math

from .state import *
from .entities import *

class Editor(Base):

    GRAB_RADIUS = 7

    def __init__(self, surface):
        super().__init__(surface, scale=1)

        self.drag = None
        self.clipboard_data = None
        self.clipboard_class = None

        self.terrain_drag = None

    def update(self, **kwargs):
        super().update(**kwargs)

    def point_in_rect(self, point, rect):
        return point[0] > rect[0] and point[0] < rect[0] + rect[2] and point[1] > rect[1] and point[1] < rect[1] + rect[3]

    def point_in_circle(self, point, circle):
        return math.sqrt((point[0] - circle[0]) ** 2 + (point[1] - circle[1]) ** 2) < circle[2]

    def get_all_things(self):
        return self.images_background + self.images_foreground + self.entities

    def get_all_things_at(self, point, action=lambda l, t: None):

        things = []
        
        for image in self.images_background[:]:
            if self.point_in_circle(point, (image.x, image.y, Editor.GRAB_RADIUS)):
                things.append(image)
                action(self.images_background, image)
                
        for image in self.images_foreground[:]:
            if self.point_in_circle(point, (image.x, image.y, Editor.GRAB_RADIUS)):
                things.append(image)
                action(self.images_foreground, image)

        for entity in self.entities[:]:
            if self.point_in_circle(point, (entity.x, entity.y, Editor.GRAB_RADIUS)):
                things.append(entity)
                action(self.entities, entity)

        for collider in self.terrain[:]:
            if self.point_in_circle(point, ((collider.x1 + collider.x2) / 2, (collider.y1 + collider.y2) / 2, Editor.GRAB_RADIUS)):
                things.append(collider)
                action(self.terrain, collider)

        return things

    def handle_event(self, event, **kwargs):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.camera.target_object.x -= 50
            elif event.key == pygame.K_RIGHT:
                self.camera.target_object.x += 50
            elif event.key == pygame.K_UP:
                self.camera.target_object.y -= 50
            elif event.key == pygame.K_DOWN:
                self.camera.target_object.y += 50
                
            elif event.key == pygame.K_i:
                key = input("image: ")
                image = Image(self.mouse_x, self.mouse_y, key)
                self.images_background.append(image)
                
            elif event.key == pygame.K_o:
                key = input("image: ")
                image = Image(self.mouse_x, self.mouse_y, key)
                self.images_foreground.append(image)

            elif event.key == pygame.K_e:
                name = input(f"entity name ({','.join(get_entity_types())}): ")
                entity = create_entity(name)
                entity.move_to(self.mouse_x, self.mouse_y)
                self.entities.append(entity)
                
            elif event.key == pygame.K_r:
                if self.drag is not None:
                    self.drag.angle += math.pi / 8

            elif event.key == pygame.K_s:
                self.save_as(input("level name: "))
            elif event.key == pygame.K_l:
                self.load_by_name(input("level name: "))
            
            elif event.key == pygame.K_c:
                if self.drag is not None:
                    self.clipboard = self.drag.dump()
                    self.clipboard_class = self.drag.__class__
            elif event.key == pygame.K_v:
                if self.drag is None:
                    thing = self.clipboard_class()
                    thing.load(self.clipboard)
                    self.images_foreground.append(thing)

            elif event.key == pygame.K_DELETE:
                self.get_all_things_at((self.mouse_x, self.mouse_y), lambda l, t: l.remove(t))

            elif event.key == pygame.K_0:
                self.get_all_things_at((self.mouse_x, self.mouse_y), lambda l, t: l.insert(0, l.pop(l.index(t))))
            elif event.key == pygame.K_9:
                self.get_all_things_at((self.mouse_x, self.mouse_y), lambda l, t: l.append(l.pop(l.index(t))))
                
        elif event.type == pygame.MOUSEMOTION:
            self.mouse_x, self.mouse_y = self.camera.shift_point_to_camera(event.pos)
            if self.drag is not None:
                self.drag.move_to(self.mouse_x, self.mouse_y)
            if self.terrain_drag is not None:
                self.terrain_drag.x2 = self.mouse_x
                self.terrain_drag.y2 = self.mouse_y
                self.terrain_drag.recalculate_normal()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.mouse_x, self.mouse_y = self.camera.shift_point_to_camera(event.pos)
                things = self.get_all_things_at((self.mouse_x, self.mouse_y))
                if things:
                    self.drag = things[-1]
                    
            elif event.button == 3:
                if self.terrain_drag is None:
                    self.terrain_drag = Collider(self.mouse_x, self.mouse_y, self.mouse_x, self.mouse_y)
                    self.terrain.append(self.terrain_drag)

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.drag = None
            elif event.button == 3:
                self.terrain_drag = None
            elif event.button == 4:
                if self.drag is not None and hasattr(self.drag, "z"):
                    self.drag.z += 1
            elif event.button == 5:
                if self.drag is not None and hasattr(self.drag, "z"):
                    self.drag.z = max(self.drag.z - 1, 1)
            

    def draw(self, surface, **kwargs):
        super().draw(surface, **kwargs)

        for thing in self.get_all_things():
            pygame.draw.circle(self.surface, (255, 0, 255), self.camera.shift_point((thing.x, thing.y)), Editor.GRAB_RADIUS, 1)

        for collider in self.terrain:
            collider.debug_draw(self.surface, self.camera)
