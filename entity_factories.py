from components.ai import HostileEnemy
from components.fighter import TFighter
from entity import TActor

player = TActor(
    char="@",
    color=(255, 255, 255),
    name="Player",
    ai_cls=HostileEnemy,
    fighter=TFighter(hp=30, defense=2, power=5),
)

orc = TActor(
    char="o",
    color=(63, 127, 63),
    name="Orc",
    ai_cls=HostileEnemy,
    fighter=TFighter(hp=10, defense=0, power=3),
)
troll = TActor(
    char="T",
    color=(0, 127, 0),
    name="Troll",
    ai_cls=HostileEnemy,
    fighter=TFighter(hp=16, defense=1, power=4),
)
