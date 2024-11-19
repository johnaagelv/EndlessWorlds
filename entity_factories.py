from components.ai import HostileEnemy
from components import consumable
from components.fighter import TFighter
from components.inventory import TInventory
from entity import TActor, TItem

player = TActor(
    char="@",
    colour=(255, 255, 255),
    name="Player",
    ai_cls=HostileEnemy,
    fighter=TFighter(hp=30, defense=2, power=5),
	inventory=TInventory(capacity=12),
)

orc = TActor(
    char="o",
    colour=(63, 127, 63),
    name="Orc",
    ai_cls=HostileEnemy,
    fighter=TFighter(hp=10, defense=0, power=3),
	inventory=TInventory(capacity=12),
)

troll = TActor(
    char="T",
    colour=(0, 127, 0),
    name="Troll",
    ai_cls=HostileEnemy,
    fighter=TFighter(hp=16, defense=1, power=4),
	inventory=TInventory(capacity=8),
)

health_potion = TItem(
	char="!",
	colour=(127, 0, 255),
	name="Health potion",
	consumable=consumable.THealingConsumable(amount=4)
)

lightning_scroll = TItem(
	char="~",
	colour=(255, 255, 0),
	name="Lightning scroll",
	consumable=consumable.TLightningDamageConsumable(damage=20, maximum_range=5),
)