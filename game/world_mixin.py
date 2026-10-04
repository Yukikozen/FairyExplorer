from .core import *
from .entities import Obstacle, Flower, QuestItem, QuestLocation
from .npc import FairyNPC

class WorldMixin:
    def generate_world(self):

        random.seed(42)

        # Fixed fence areas are reserved before generating trees so trees
        # never grow through the fences.
        fence_layout = [
            (350, 850, 300, 20),
            (2100, 1200, 350, 20),
            (1200, 1900, 300, 20),
            (2800, 1700, 300, 20),
        ]
        fence_rects = [pygame.Rect(x, y, w, h) for x, y, w, h in fence_layout]

        # Generate trees with generous 3D clearance.  The rendered canopy
        # extends well beyond the 70x90 collision footprint, so spacing is
        # based on an enlarged reservation rectangle rather than just the
        # trunk collision box.
        placed_tree_reservations = []
        for _ in range(75):
            placed = False

            for _attempt in range(180):
                x = random.randint(130, WORLD_WIDTH - 190)
                y = random.randint(150, WORLD_HEIGHT - 200)

                # The collision box is the trunk/base. The reservation is
                # intentionally much larger because the 3D canopy, branches
                # and ground shadow extend beyond the trunk.
                tree_rect = pygame.Rect(x, y, 78, 104)
                reserved = tree_rect.inflate(175, 165)

                # Keep the visible 3D canopy away from fences.
                if any(reserved.colliderect(fr.inflate(55, 55)) for fr in fence_rects):
                    continue

                # Keep neighboring trees separated so their canopies and
                # ground shadows do not visually merge.
                if any(reserved.colliderect(other) for other in placed_tree_reservations):
                    continue

                # Keep trees away from the player starting area.
                if reserved.colliderect(pygame.Rect(150, 150, 260, 220)):
                    continue

                self.obstacles.append(Obstacle(x, y, 78, 104, "tree"))
                placed_tree_reservations.append(reserved)
                placed = True
                break

            if not placed:
                continue

        # Five distinct fairy homes placed around the world.
        # Each house uses the same collision footprint but a different
        # visual style so the world feels like a real fairy village.
        houses = [
            (500, 500, "mushroom"),
            (1800, 700, "flower"),
            (2900, 500, "crystal"),
            (900, 2200, "treehouse"),
            (3000, 2200, "pond"),
        ]

        # Place houses only in clear areas.  The visible house artwork is
        # larger than its collision rectangle, so we reserve extra space
        # around every house to keep nearby trees from visually overlapping it.
        placed_houses = []

        house_owners = {
            "mushroom": "Lumi",
            "flower": "Pipi",
            "crystal": "Coco",
            "treehouse": "Ruru",
            "pond": "Nana",
        }

        for original_x, original_y, style in houses:
            house_w = 170
            house_h = 130
            chosen = None

            # Try the requested position first, then search outward in a
            # deterministic spiral/grid pattern for a clear location.
            candidates = [(original_x, original_y)]
            for radius in range(100, 701, 100):
                for ox, oy in (
                    (radius, 0), (-radius, 0),
                    (0, radius), (0, -radius),
                    (radius, radius), (-radius, radius),
                    (radius, -radius), (-radius, -radius),
                ):
                    candidates.append((original_x + ox, original_y + oy))

            for cx, cy in candidates:
                if cx < 100 or cy < 100:
                    continue
                if cx + house_w > WORLD_WIDTH - 100:
                    continue
                if cy + house_h > WORLD_HEIGHT - 100:
                    continue

                test_rect = pygame.Rect(cx, cy, house_w, house_h)

                # Extra clearance is intentional because some roofs,
                # branches and decorations extend beyond self.rect.
                reserved = test_rect.inflate(95, 85)

                blocked = False
                for obstacle in self.obstacles:
                    if reserved.colliderect(obstacle.rect):
                        blocked = True
                        break

                if not blocked:
                    for other in placed_houses:
                        if reserved.colliderect(other.inflate(95, 85)):
                            blocked = True
                            break

                if not blocked:
                    chosen = (cx, cy)
                    break

            if chosen is None:
                # Extremely unlikely fallback: use the requested position.
                chosen = (original_x, original_y)

            hx, hy = chosen
            house = Obstacle(
                hx,
                hy,
                house_w,
                house_h,
                "house",
                style
            )
            house.owner = house_owners.get(style, "Fairy")
            self.obstacles.append(house)
            placed_houses.append(house.rect.copy())

        # Pebbles/rocks are placed only where they do not overlap trees,
        # houses, fences, or other rocks. This prevents rocks from appearing
        # inside tree trunks or under buildings.
        for _ in range(35):
            for _attempt in range(60):
                x = random.randint(100, WORLD_WIDTH - 150)
                y = random.randint(100, WORLD_HEIGHT - 120)
                rock_rect = pygame.Rect(x, y, 70, 45)

                # Check all existing obstacles AND the reserved fence
                # rectangles. Fences are added to self.obstacles later, so
                # they must be checked explicitly here as well. The extra
                # clearance keeps the pebble artwork from touching fence posts.
                blocked = any(
                    rock_rect.inflate(24, 24).colliderect(obstacle.rect)
                    for obstacle in self.obstacles
                )

                if not blocked:
                    blocked = any(
                        rock_rect.inflate(24, 24).colliderect(fence_rect.inflate(18, 18))
                        for fence_rect in fence_rects
                    )

                if not blocked:
                    self.obstacles.append(
                        Obstacle(x, y, 70, 45, "rock")
                    )
                    break

        # Add the reserved fences after tree/house/rock placement.  Their
        # positions were already reserved during tree generation, and houses
        # also check against the actual obstacle list when placed.
        for x, y, w, h in fence_layout:
            self.obstacles.append(
                Obstacle(x, y, w, h, "fence")
            )

        for i in range(180):

            for _attempt in range(50):

                x = random.randint(
                    80,
                    WORLD_WIDTH - 80
                )

                y = random.randint(
                    80,
                    WORLD_HEIGHT - 80
                )

                rect = pygame.Rect(
                    x - 8,
                    y - 8,
                    16,
                    16
                )

                blocked = any(
                    rect.colliderect(
                        obstacle.rect.inflate(
                            30,
                            30
                        )
                    )
                    for obstacle in self.obstacles
                )

                if not blocked:

                    self.flowers.append(
                        Flower(
                            x,
                            y,
                            i
                        )
                    )

                    break

        self.quest_locations = [

            QuestLocation(
                "flower_meadow",
                "Flower Meadow",
                1250,
                650,
                100
            ),

            QuestLocation(
                "ancient_grove",
                "Ancient Grove",
                1900,
                500,
                100
            ),

            QuestLocation(
                "fairy_lake",
                "Fairy Lake",
                3200,
                900,
                110
            ),

            QuestLocation(
                "crystal_cave",
                "Crystal Cave",
                3350,
                1900,
                110
            ),

            QuestLocation(
                "star_shrine",
                "Star Shrine",
                2200,
                2500,
                100
            ),

            QuestLocation(
                "garden",
                "Fairy Garden",
                900,
                2500,
                100
            ),

            QuestLocation(
                "forest_pond",
                "Forest Pond",
                2600,
                2700,
                100
            )
        ]

        self.quest_items = [

            QuestItem(
                700,
                1300,
                "ribbon",
                "Pink Ribbon"
            ),

            QuestItem(
                950,
                1450,
                "ribbon",
                "Pink Ribbon"
            ),

            QuestItem(
                1200,
                1250,
                "ribbon",
                "Pink Ribbon"
            ),

            QuestItem(
                1500,
                2100,
                "seed",
                "Magical Seed"
            ),

            QuestItem(
                1700,
                2250,
                "seed",
                "Magical Seed"
            ),

            QuestItem(
                1900,
                2050,
                "seed",
                "Magical Seed"
            ),

            QuestItem(
                2050,
                2350,
                "seed",
                "Magical Seed"
            ),

            QuestItem(
                3300,
                1850,
                "crystal",
                "Fairy Crystal"
            ),

            QuestItem(
                3500,
                2050,
                "crystal",
                "Fairy Crystal"
            ),

            QuestItem(
                3200,
                2150,
                "crystal",
                "Fairy Crystal"
            ),

            QuestItem(
                3000,
                1950,
                "crystal",
                "Fairy Crystal"
            ),

            QuestItem(
                2200,
                2500,
                "lost_star",
                "Lost Star"
            )
        ]

        self.npcs = [

            FairyNPC(
                "Lumi",
                "lumi.png",
                2300,
                1300,
                [
                    "Hi there! I'm Lumi!",
                    "I've been exploring this magical forest all morning.",
                    "There are so many mysterious places around here.",
                    "I could really use your help!"
                ],
                300
            ),

            FairyNPC(
                "Pipi",
                "mepple.png",
                800,
                800,
                [
                    "Hello!",
                    "I was carrying something very important earlier.",
                    "But now I can't remember where I dropped it.",
                    "Could you help me look around?"
                ],
                220
            ),

            FairyNPC(
                "Coco",
                "mipple.png",
                1500,
                1700,
                [
                    "Welcome to the magical forest!",
                    "I love growing magical plants.",
                    "But my supply of magical seeds is running low."
                ],
                250
            ),

            FairyNPC(
                "Ruru",
                "lumi.png",
                3100,
                1100,
                [
                    "Hi!",
                    "There are mysterious crystals hidden in the forest.",
                    "I wonder what secrets they contain..."
                ],
                260
            ),

            FairyNPC(
                "Nana",
                "lumi.png",
                1000,
                2500,
                [
                    "Good morning!",
                    "Have you explored the eastern forest yet?",
                    "There is a peaceful pond hidden among the trees."
                ],
                240
            )
        ]

        # Ensure every fairy starts completely outside the visual footprint
        # of trees, fences and houses. If a fixed NPC spawn is too close,
        # move it to the nearest safe point around its original location.
        for npc in self.npcs:
            if not npc.can_move_to(npc.x, npc.y, self.obstacles):
                found = False
                for radius in (50, 80, 110, 140, 180, 220):
                    for angle_deg in range(0, 360, 15):
                        angle = math.radians(angle_deg)
                        nx = clamp(npc.spawn_x + math.cos(angle) * radius, 100, WORLD_WIDTH - 130)
                        ny = clamp(npc.spawn_y + math.sin(angle) * radius, 100, WORLD_HEIGHT - 130)
                        if npc.can_move_to(nx, ny, self.obstacles):
                            npc.x = nx
                            npc.y = ny
                            npc.sync_rect()
                            npc.spawn_x = nx
                            npc.spawn_y = ny
                            npc.choose_new_destination(self.obstacles)
                            found = True
                            break
                    if found:
                        break


    def find_safe_spawn(self):

        candidates = [
            (700, 1000),
            (750, 1100),
            (650, 1050),
            (800, 1050),
            (600, 1000)
        ]

        for x, y in candidates:

            rect = pygame.Rect(
                x,
                y,
                44,
                60
            )

            blocked = any(
                rect.colliderect(
                    obstacle.rect.inflate(
                        20,
                        20
                    )
                )
                for obstacle in self.obstacles
            )

            if not blocked:
                return x, y

        return 700, 1000


