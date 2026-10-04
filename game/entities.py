from .core import *

class Obstacle:

    def __init__(
        self,
        x,
        y,
        width,
        height,
        kind="tree",
        style="default"
    ):

        self.rect = pygame.Rect(
            x,
            y,
            width,
            height
        )

        self.kind = kind
        self.style = style
        # For fairy houses, this identifies the NPC who lives here.
        # It is intentionally stored on the house itself so the visible
        # owner label always follows the correct house after repositioning.
        self.owner = None

    def draw(self, screen, camera):

        rect = self.rect.move(
            -camera.x,
            -camera.y
        )

        if (
            rect.right < 0
            or rect.left > SCREEN_WIDTH
            or rect.bottom < 0
            or rect.top > SCREEN_HEIGHT
        ):
            return

        if self.kind == "tree":

            # --------------------------------------------------------
            # 3D FAIRY TREE
            # --------------------------------------------------------
            # The tree is still drawn with Pygame primitives, but uses
            # layered silhouettes, side shading, highlights, branches,
            # a ground shadow and depth offsets so it reads as a solid
            # 3D object instead of a flat 2D icon.

            # Ground shadow / contact shadow.
            shadow = pygame.Rect(
                rect.left - 8,
                rect.bottom - 13,
                rect.width + 16,
                25
            )
            pygame.draw.ellipse(
                screen,
                (62, 86, 65),
                shadow
            )
            pygame.draw.ellipse(
                screen,
                (48, 72, 52),
                shadow.inflate(-18, -8)
            )

            # Main trunk: dark rear side first.
            trunk_w = 34
            trunk_h = 78
            trunk = pygame.Rect(
                rect.centerx - trunk_w // 2,
                rect.bottom - trunk_h,
                trunk_w,
                trunk_h
            )

            pygame.draw.polygon(
                screen,
                (82, 52, 35),
                [
                    (trunk.left - 4, trunk.bottom),
                    (trunk.left + 1, trunk.top + 9),
                    (trunk.left + 7, trunk.top),
                    (trunk.right + 5, trunk.top + 7),
                    (trunk.right + 8, trunk.bottom),
                ]
            )

            # Warm front face.
            pygame.draw.rect(
                screen,
                (139, 88, 48),
                trunk,
                border_radius=6
            )

            # Bright side plane creates a rounded trunk highlight.
            pygame.draw.polygon(
                screen,
                (180, 116, 63),
                [
                    (trunk.left + 5, trunk.top + 4),
                    (trunk.left + 12, trunk.top + 1),
                    (trunk.left + 11, trunk.bottom - 4),
                    (trunk.left + 4, trunk.bottom),
                ]
            )

            # Dark bark plane on the opposite side.
            pygame.draw.polygon(
                screen,
                (101, 61, 38),
                [
                    (trunk.right - 7, trunk.top + 5),
                    (trunk.right, trunk.top + 9),
                    (trunk.right, trunk.bottom),
                    (trunk.right - 9, trunk.bottom - 3),
                ]
            )

            # Roots spread over the ground, reinforcing the 3D contact.
            pygame.draw.polygon(
                screen,
                (113, 69, 40),
                [
                    (trunk.left + 3, trunk.bottom - 14),
                    (trunk.left - 19, trunk.bottom - 4),
                    (trunk.left - 24, trunk.bottom + 4),
                    (trunk.centerx - 2, trunk.bottom - 2),
                ]
            )
            pygame.draw.polygon(
                screen,
                (95, 57, 36),
                [
                    (trunk.right - 3, trunk.bottom - 14),
                    (trunk.right + 18, trunk.bottom - 3),
                    (trunk.right + 23, trunk.bottom + 5),
                    (trunk.centerx + 3, trunk.bottom - 2),
                ]
            )

            # Branches behind the canopy.
            branch_color = (102, 63, 39)
            branch_hi = (157, 96, 49)

            pygame.draw.polygon(
                screen,
                branch_color,
                [
                    (trunk.centerx - 2, trunk.top + 24),
                    (trunk.left - 22, trunk.top + 2),
                    (trunk.left - 30, trunk.top + 6),
                    (trunk.centerx - 7, trunk.top + 34),
                ]
            )
            pygame.draw.polygon(
                screen,
                branch_color,
                [
                    (trunk.centerx + 3, trunk.top + 27),
                    (trunk.right + 24, trunk.top + 1),
                    (trunk.right + 31, trunk.top + 7),
                    (trunk.centerx + 9, trunk.top + 37),
                ]
            )
            pygame.draw.line(
                screen, branch_hi,
                (trunk.centerx - 2, trunk.top + 24),
                (trunk.left - 20, trunk.top + 5),
                4
            )

            # Canopy rear shadow: large dark volume.
            canopy_shadow = pygame.Rect(
                rect.left - 24,
                rect.top - 30,
                rect.width + 48,
                104
            )
            pygame.draw.ellipse(
                screen,
                (47, 104, 57),
                canopy_shadow.move(7, 11)
            )

            # Main canopy volume.
            canopy = pygame.Rect(
                rect.left - 22,
                rect.top - 34,
                rect.width + 44,
                104
            )
            pygame.draw.ellipse(
                screen,
                (69, 145, 76),
                canopy
            )

            # Lower darker foliage gives the canopy a rounded underside.
            lower = pygame.Rect(
                rect.left - 12,
                rect.top + 10,
                rect.width + 24,
                62
            )
            pygame.draw.ellipse(
                screen,
                (53, 119, 62),
                lower
            )

            # Individual overlapping foliage masses create depth.
            foliage_layers = [
                (rect.left - 2, rect.top + 10, 48, 50, (82, 163, 84)),
                (rect.left + 17, rect.top - 18, 58, 56, (108, 188, 101)),
                (rect.centerx - 29, rect.top - 29, 62, 60, (101, 181, 94)),
                (rect.right - 61, rect.top - 14, 59, 56, (79, 158, 81)),
                (rect.right - 43, rect.top + 12, 50, 49, (62, 137, 70)),
            ]

            for fx, fy, fw, fh, color in foliage_layers:
                pygame.draw.ellipse(
                    screen,
                    color,
                    pygame.Rect(fx, fy, fw, fh)
                )

            # Soft top highlight: a large curved patch rather than a flat
            # circle, making the canopy appear rounded toward the light.
            highlight = pygame.Rect(
                rect.left + 18,
                rect.top - 5,
                64,
                25
            )
            pygame.draw.ellipse(
                screen,
                (139, 207, 120),
                highlight
            )
            pygame.draw.ellipse(
                screen,
                (169, 222, 137),
                highlight.inflate(-15, -10)
            )

            # A few small darker leaf clusters add depth at the front.
            for fx, fy, r in [
                (rect.left + 16, rect.top + 43, 10),
                (rect.centerx + 2, rect.top + 51, 12),
                (rect.right - 14, rect.top + 42, 9),
            ]:
                pygame.draw.circle(screen, (48, 111, 58), (fx, fy), r)

            # Tiny leaf highlights.
            for fx, fy in [
                (rect.left + 31, rect.top + 19),
                (rect.centerx - 5, rect.top + 7),
                (rect.right - 30, rect.top + 16),
            ]:
                pygame.draw.ellipse(
                    screen,
                    (186, 225, 143),
                    pygame.Rect(fx, fy, 9, 5)
                )

        elif self.kind == "rock":

            pygame.draw.ellipse(screen, (105, 110, 125), rect)
            top = rect.inflate(-10, -8)
            top.move_ip(-2, -5)
            pygame.draw.ellipse(screen, (158, 164, 178), top)
            pygame.draw.ellipse(screen, (190, 195, 207), top.inflate(-14, -10))
            pygame.draw.line(screen, (220, 224, 232),
                             (top.left + 8, top.centery - 4),
                             (top.centerx, top.top + 4), 3)

        elif self.kind == "house":

            # Every house has its own silhouette, construction and entrance.
            style = self.style
            pygame.draw.ellipse(
                screen, (82, 100, 88),
                (rect.left - 20, rect.bottom - 3, rect.width + 65, 28)
            )

            if style == "mushroom":
                # Round mushroom cottage.
                wall = pygame.Rect(rect.left + 35, rect.top + 38, rect.width - 70, rect.height - 48)
                pygame.draw.rect(screen, (204, 139, 105), wall.move(8, 9), border_radius=28)
                pygame.draw.rect(screen, (246, 197, 157), wall, border_radius=28)
                cap = pygame.Rect(rect.left - 18, rect.top - 25, rect.width + 36, 92)
                pygame.draw.ellipse(screen, (158, 54, 91), cap.move(7, 13))
                pygame.draw.ellipse(screen, (218, 69, 122), cap)
                pygame.draw.arc(screen, (250, 137, 170), cap.inflate(-8, -8), math.pi*.08, math.pi*.92, 5)
                for sx, sy, sr in [(rect.left+28,rect.top+8,12),(rect.centerx-5,rect.top-9,16),(rect.right-28,rect.top+9,11)]:
                    pygame.draw.circle(screen, (255,232,235), (sx,sy), sr)
                    pygame.draw.circle(screen, (239,183,198), (sx,sy), sr, 2)
                porch = pygame.Rect(rect.centerx-43, wall.bottom-17, 86, 18)
                pygame.draw.rect(screen, (133,88,67), porch, border_radius=7)
                door = pygame.Rect(rect.centerx-22, wall.bottom-61, 44, 61)
                pygame.draw.ellipse(screen, (104,67,55), door)
                pygame.draw.circle(screen, (255,214,103), (door.right-9,door.centery), 4)
                for wx in (wall.left+22, wall.right-22):
                    pygame.draw.circle(screen, (117,78,67), (wx,wall.top+47), 17)
                    pygame.draw.circle(screen, (154,226,237), (wx,wall.top+47), 12)

            elif style == "flower":
                # Flower-shaped cottage with six giant petals.
                base = [(rect.left+50,rect.bottom-10),(rect.left+36,rect.top+65),(rect.left+58,rect.top+37),
                        (rect.centerx,rect.top+52),(rect.right-58,rect.top+37),(rect.right-36,rect.top+65),(rect.right-50,rect.bottom-10)]
                pygame.draw.polygon(screen, (177,111,91), [(x+8,y+9) for x,y in base])
                pygame.draw.polygon(screen, (249,205,151), base)
                cx,cy = rect.centerx,rect.top+27
                petals=[(245,117,169),(255,145,188),(239,112,180)]
                for i,angle in enumerate(range(0,360,60)):
                    rad=math.radians(angle); px=cx+int(math.cos(rad)*49); py=cy+int(math.sin(rad)*28)
                    petal=pygame.Rect(px-38,py-20,76,40)
                    pygame.draw.ellipse(screen,(185,78,130),petal.move(5,7))
                    pygame.draw.ellipse(screen,petals[i%3],petal)
                pygame.draw.circle(screen,(255,214,77),(cx,cy),25)
                pygame.draw.circle(screen,(255,238,126),(cx-5,cy-5),12)
                door=pygame.Rect(cx-22,rect.bottom-69,44,69)
                pygame.draw.ellipse(screen,(137,79,105),door)
                pygame.draw.ellipse(screen,(190,111,139),door.inflate(-7,-6))
                pygame.draw.ellipse(screen,(87,158,91),(rect.left+5,rect.bottom-48,55,25))
                pygame.draw.ellipse(screen,(105,177,95),(rect.right-60,rect.bottom-48,55,25))

            elif style == "crystal":
                # Tall crystal palace with three independent towers.
                body=[(rect.left+45,rect.bottom-15),(rect.left+45,rect.top+54),(rect.centerx,rect.top+15),
                      (rect.right-45,rect.top+54),(rect.right-45,rect.bottom-15)]
                pygame.draw.polygon(screen,(105,101,164),[(x+8,y+10) for x,y in body])
                pygame.draw.polygon(screen,(187,177,231),body)
                for cx,base_y,w,h in [(rect.left+32,rect.top+55,34,100),(rect.centerx,rect.top+8,46,145),(rect.right-32,rect.top+55,34,100)]:
                    pts=[(cx,base_y-h),(cx+w//2,base_y-24),(cx+w//3,base_y),(cx-w//3,base_y),(cx-w//2,base_y-24)]
                    pygame.draw.polygon(screen,(78,106,180),[(x+6,y+8) for x,y in pts])
                    pygame.draw.polygon(screen,(112,163,231),pts)
                    pygame.draw.line(screen,(225,247,255),pts[0],pts[2],3)
                crystal=[(rect.centerx,rect.top-33),(rect.centerx+13,rect.top-9),(rect.centerx,rect.top+14),(rect.centerx-13,rect.top-9)]
                pygame.draw.polygon(screen,(104,204,247),crystal)
                pygame.draw.polygon(screen,(235,255,255),crystal,2)
                door=pygame.Rect(rect.centerx-25,rect.bottom-79,50,79)
                pygame.draw.ellipse(screen,(63,65,117),door)
                pygame.draw.ellipse(screen,(121,142,214),door.inflate(-8,-7))
                for wx in (rect.left+70,rect.right-70):
                    pts=[(wx,rect.top+63),(wx+15,rect.top+82),(wx,rect.top+101),(wx-15,rect.top+82)]
                    pygame.draw.polygon(screen,(118,218,245),pts)
                    pygame.draw.polygon(screen,(238,255,255),pts,2)

            elif style == "treehouse":
                # Elevated wooden cabin built into a giant tree.
                tx=rect.centerx
                pygame.draw.polygon(screen,(87,57,36),[(tx-27,rect.bottom+15),(tx-17,rect.top+35),(tx+17,rect.top+35),(tx+32,rect.bottom+15)])
                pygame.draw.polygon(screen,(132,86,48),[(tx-13,rect.bottom+10),(tx-8,rect.top+43),(tx+11,rect.top+43),(tx+18,rect.bottom+10)])
                pygame.draw.line(screen,(95,61,37),(tx,rect.top+65),(rect.left-15,rect.top+20),14)
                pygame.draw.line(screen,(95,61,37),(tx+2,rect.top+62),(rect.right+15,rect.top+14),12)
                cabin=pygame.Rect(rect.left+25,rect.top+45,rect.width-50,76)
                pygame.draw.rect(screen,(91,57,38),cabin.move(8,10),border_radius=8)
                pygame.draw.rect(screen,(181,128,76),cabin,border_radius=8)
                for yy in range(cabin.top+10,cabin.bottom,16):
                    pygame.draw.line(screen,(130,85,51),(cabin.left+5,yy),(cabin.right-5,yy),3)
                leaves=[(rect.left+30,rect.top+28,38,(71,133,71)),(rect.centerx-35,rect.top+8,47,(94,161,76)),
                        (rect.centerx+30,rect.top+18,43,(79,145,69)),(rect.right-25,rect.top+38,34,(62,122,65))]
                for cx,cy,r,col in leaves: pygame.draw.circle(screen,col,(cx,cy),r)
                pygame.draw.line(screen,(151,103,61),(rect.centerx-27,cabin.bottom),(rect.centerx-27,rect.bottom+4),5)
                pygame.draw.line(screen,(151,103,61),(rect.centerx+27,cabin.bottom),(rect.centerx+27,rect.bottom+4),5)
                for yy in range(cabin.bottom+5,rect.bottom,14):
                    pygame.draw.line(screen,(181,130,76),(rect.centerx-27,yy),(rect.centerx+27,yy),4)
                for wx in (cabin.left+25,cabin.right-25):
                    pygame.draw.circle(screen,(92,61,43),(wx,cabin.centery),15)
                    pygame.draw.circle(screen,(154,220,229),(wx,cabin.centery),10)

            elif style == "pond":
                # Water dwelling sitting on a little magical pond.
                pond=pygame.Rect(rect.left-18,rect.bottom-15,rect.width+36,46)
                pygame.draw.ellipse(screen,(45,126,160),pond)
                pygame.draw.ellipse(screen,(83,187,205),pond.inflate(-8,-8))
                pygame.draw.arc(screen,(208,250,250),pond.inflate(-12,-12),math.pi,math.pi*2,4)
                body=pygame.Rect(rect.left+25,rect.top+48,rect.width-50,80)
                pygame.draw.ellipse(screen,(53,125,145),body.move(7,10))
                pygame.draw.ellipse(screen,(148,209,201),body)
                dome=pygame.Rect(rect.left+7,rect.top-16,rect.width-14,105)
                pygame.draw.ellipse(screen,(40,128,165),dome.move(6,9))
                pygame.draw.ellipse(screen,(78,181,201),dome)
                pygame.draw.arc(screen,(221,255,255),dome.inflate(-16,-16),math.pi*.08,math.pi*.92,5)
                door=pygame.Rect(rect.centerx-23,rect.bottom-62,46,62)
                pygame.draw.ellipse(screen,(36,103,132),door)
                pygame.draw.ellipse(screen,(91,194,211),door.inflate(-7,-5))
                for wx in (rect.left+40,rect.right-40):
                    pygame.draw.circle(screen,(43,120,150),(wx,rect.top+70),17)
                    pygame.draw.circle(screen,(167,239,241),(wx,rect.top+70),11)
                for px,py in [(rect.left+2,rect.bottom+12),(rect.right-4,rect.bottom+18)]:
                    pygame.draw.ellipse(screen,(76,158,96),(px-18,py-8,36,16))

            else:
                wall=pygame.Rect(rect.left+20,rect.top+35,rect.width-40,rect.height-45)
                pygame.draw.rect(screen,(225,180,140),wall,border_radius=12)
                pygame.draw.polygon(screen,(180,90,125),[(rect.left,rect.top+45),(rect.centerx,rect.top-35),(rect.right,rect.top+45)])
                pygame.draw.rect(screen,(105,70,58),(rect.centerx-20,wall.bottom-60,40,60),border_radius=8)

            for dx in (-62,62):
                gx=rect.centerx+dx
                pygame.draw.ellipse(screen,(126,137,128),(gx-8,rect.bottom-5,16,8))

            # --------------------------------------------------------
            # FAIRY HOUSE OWNER LABEL
            # --------------------------------------------------------
            # Keep this label attached to the actual house object. This
            # makes it impossible for the displayed owner to get separated
            # from a house if its world position changes.
            if self.owner:
                label = f"{self.owner}'s House"
                font = pygame.font.SysFont("arial", 16, bold=True)
                label_surface = font.render(label, True, (255, 255, 255))
                label_rect = label_surface.get_rect(
                    center=(rect.centerx, rect.top - 42)
                )
                bg = label_rect.inflate(18, 8)
                pygame.draw.rect(
                    screen, (67, 49, 84), bg, border_radius=9
                )
                pygame.draw.rect(
                    screen, (255, 224, 137), bg, 2, border_radius=9
                )
                screen.blit(label_surface, label_rect)

        elif self.kind == "fence":

            # Chunky isometric-style fence: rear shadow, thick rails,
            # highlighted front faces and dark side faces give each post
            # actual depth instead of a flat rectangle.
            shadow = pygame.Rect(rect.left - 2, rect.bottom - 2, rect.width + 8, 12)
            pygame.draw.ellipse(screen, (58, 78, 58), shadow)

            rail_back = pygame.Rect(rect.left, rect.top + 5, rect.width, max(8, rect.height - 4))
            pygame.draw.rect(screen, (108, 70, 42), rail_back, border_radius=5)
            pygame.draw.rect(screen, (184, 127, 70), rect.inflate(0, -4), border_radius=4)
            pygame.draw.line(screen, (232, 178, 103), (rect.left + 3, rect.top + 2), (rect.right - 3, rect.top + 2), 3)

            for x in range(rect.left + 10, rect.right, 35):
                post = pygame.Rect(x, rect.top - 14, 14, rect.height + 28)
                pygame.draw.rect(screen, (91, 57, 37), post.move(5, 4), border_radius=4)
                pygame.draw.rect(screen, (180, 119, 66), post, border_radius=4)
                pygame.draw.polygon(screen, (119, 75, 43), [(post.right-5, post.top+2), (post.right+5, post.top+7), (post.right+5, post.bottom-4), (post.right-5, post.bottom)])
                pygame.draw.line(screen, (235, 181, 104), (post.left+3, post.top+4), (post.left+3, post.bottom-5), 3)
                pygame.draw.polygon(screen, (201, 144, 81), [(post.left-2, post.top), (post.centerx, post.top-6), (post.right+2, post.top), (post.centerx, post.top+6)])


class Flower:

    def __init__(
        self,
        x,
        y,
        flower_id
    ):

        self.x = x
        self.y = y
        self.flower_id = flower_id

        self.collected = False

        self.phase = random.uniform(
            0,
            math.pi * 2
        )

    def update(self, dt):

        self.phase += dt * 0.003

    def draw(self, screen, camera):

        if self.collected:
            return

        sx, sy = camera.world_to_screen(
            self.x,
            self.y
        )

        if (
            sx < -20
            or sx > SCREEN_WIDTH + 20
            or sy < -20
            or sy > SCREEN_HEIGHT + 20
        ):
            return

        bob = math.sin(
            self.phase
        ) * 2

        pygame.draw.line(
            screen,
            (70, 155, 75),
            (
                sx,
                sy + 8 + bob
            ),
            (
                sx,
                sy + 22 + bob
            ),
            3
        )

        colors = [
            (255, 145, 190),
            (245, 170, 220),
            (185, 145, 255),
            (255, 190, 120)
        ]

        color = colors[
            self.flower_id
            % len(colors)
        ]

        for angle in range(
            0,
            360,
            90
        ):

            rad = math.radians(
                angle
            )

            px = sx + int(
                math.cos(rad) * 7
            )

            py = sy + int(
                math.sin(rad) * 7
                + bob
            )

            pygame.draw.circle(
                screen,
                color,
                (px, py),
                6
            )

        pygame.draw.circle(
            screen,
            (255, 220, 80),
            (
                sx,
                sy + bob
            ),
            5
        )


class QuestItem:

    def __init__(
        self,
        x,
        y,
        item_type,
        name
    ):

        self.x = x
        self.y = y

        self.item_type = item_type
        self.name = name

        self.collected = False

        self.phase = random.uniform(
            0,
            math.pi * 2
        )

    def update(self, dt):

        self.phase += dt * 0.004

    def draw(self, screen, camera):

        if self.collected:
            return

        sx, sy = camera.world_to_screen(
            self.x,
            self.y
        )

        if (
            sx < -40
            or sx > SCREEN_WIDTH + 40
            or sy < -40
            or sy > SCREEN_HEIGHT + 40
        ):
            return

        bob = math.sin(
            self.phase
        ) * 3

        if self.item_type == "ribbon":

            color = (255, 120, 170)

            pygame.draw.line(
                screen,
                color,
                (
                    sx - 8,
                    sy - 5 + bob
                ),
                (
                    sx + 8,
                    sy + 5 + bob
                ),
                5
            )

            pygame.draw.circle(
                screen,
                color,
                (
                    sx,
                    sy + bob
                ),
                5
            )

        elif self.item_type == "seed":

            color = (125, 190, 100)

            pygame.draw.ellipse(
                screen,
                color,
                (
                    sx - 8,
                    sy - 12 + bob,
                    16,
                    24
                )
            )

        elif self.item_type == "crystal":

            color = (150, 190, 255)

            points = [
                (
                    sx,
                    sy - 15 + bob
                ),
                (
                    sx + 11,
                    sy + bob
                ),
                (
                    sx,
                    sy + 15 + bob
                ),
                (
                    sx - 11,
                    sy + bob
                )
            ]

            pygame.draw.polygon(
                screen,
                color,
                points
            )

            pygame.draw.polygon(
                screen,
                (225, 240, 255),
                points,
                2
            )

        elif self.item_type == "lost_star":

            color = (255, 220, 80)

            points = []

            for i in range(10):

                angle = (
                    -math.pi / 2
                    + i * math.pi / 5
                )

                radius = (
                    16
                    if i % 2 == 0
                    else 7
                )

                points.append(
                    (
                        sx
                        + math.cos(angle)
                        * radius,

                        sy
                        + bob
                        + math.sin(angle)
                        * radius
                    )
                )

            pygame.draw.polygon(
                screen,
                color,
                points
            )


class QuestLocation:

    def __init__(
        self,
        location_id,
        name,
        x,
        y,
        radius=90
    ):

        self.location_id = location_id
        self.name = name

        self.x = x
        self.y = y

        self.radius = radius

    def draw(self, screen, camera):

        sx, sy = camera.world_to_screen(
            self.x,
            self.y
        )

        if (
            sx < -150
            or sx > SCREEN_WIDTH + 150
            or sy < -150
            or sy > SCREEN_HEIGHT + 150
        ):
            return

        pygame.draw.circle(
            screen,
            (255, 230, 150),
            (
                sx,
                sy
            ),
            self.radius,
            2
        )

        pygame.draw.circle(
            screen,
            (255, 240, 180),
            (
                sx,
                sy
            ),
            8
        )


class Fairy:

    def __init__(
        self,
        name,
        image_filename,
        x,
        y
    ):

        self.name = name

        self.x = float(x)
        self.y = float(y)

        self.image = load_image(
            image_filename,
            (64, 78)
        )

        self.rect = pygame.Rect(
            int(x),
            int(y),
            44,
            60
        )

    def sync_rect(self):

        self.rect.topleft = (
            int(self.x),
            int(self.y)
        )

    def draw(
        self,
        screen,
        camera
    ):

        sx, sy = camera.world_to_screen(
            self.x,
            self.y
        )

        if self.image:

            image_rect = self.image.get_rect(
                center=(
                    sx
                    + self.rect.width // 2,

                    sy
                    + self.rect.height // 2
                )
            )

            screen.blit(
                self.image,
                image_rect
            )

        else:

            pygame.draw.circle(
                screen,
                (255, 220, 200),
                (
                    sx + 22,
                    sy + 17
                ),
                12
            )

            pygame.draw.circle(
                screen,
                (90, 180, 240),
                (
                    sx + 11,
                    sy + 27
                ),
                11
            )

            pygame.draw.circle(
                screen,
                (90, 180, 240),
                (
                    sx + 33,
                    sy + 27
                ),
                11
            )

            pygame.draw.ellipse(
                screen,
                (255, 180, 210),
                (
                    sx + 10,
                    sy + 28,
                    25,
                    30
                )
            )


class PartyFairy(Fairy):

    def __init__(
        self,
        name,
        image_filename,
        x,
        y
    ):

        super().__init__(
            name,
            image_filename,
            x,
            y
        )

        self.speed = COMPANION_SPEED


