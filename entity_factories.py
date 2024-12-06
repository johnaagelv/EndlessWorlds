from components.ai import HostileEnemy
from components import consumable
from components.fighter import Fighter
from components.inventory import Inventory
from components.level import Level
from entity import Actor, Item
import color as colour

player = Actor(
    char="@",
    color=colour.white,
    name="Player",
    ai_cls=HostileEnemy,
    fighter=Fighter(hp=30, defense=2, power=5),
    inventory=Inventory(capacity=26),
    level=Level(level_up_base=200),
)

orc = Actor(
    char="o",
    color=colour.white,
    name="Orc",
    ai_cls=HostileEnemy,
    fighter=Fighter(hp=10, defense=0, power=3),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=35),
)
troll = Actor(
    char="T",
    color=colour.white,
    name="Troll",
    ai_cls=HostileEnemy,
    fighter=Fighter(hp=16, defense=1, power=4),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=100),
)

confusion_scroll = Item(
    char="~",
    color=colour.grey,
    name="Confusion Scroll",
    consumable=consumable.ConfusionConsumable(number_of_turns=10),
)
fireball_scroll = Item(
    char="~",
    color=colour.green,
    name="Fireball Scroll",
    consumable=consumable.FireballDamageConsumable(damage=12, radius=3),
)
health_potion = Item(
    char="!",
    color=colour.blue,
    name="Health Potion",
    consumable=consumable.HealingConsumable(amount=4),
)
lightning_scroll = Item(
    char="~",
    color=colour.green,
    name="Lightning Scroll",
    consumable=consumable.LightningDamageConsumable(damage=20, maximum_range=5),
)