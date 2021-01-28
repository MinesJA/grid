from grid.models.house import House
from grid.models.battery import Battery
from grid.models.line import Line

battery1 = Battery(50, 20, 5)
house1 = House(-3, 5)
house2 = House(-3, 0)
house3 = House(-5, 2)
house4 = House(-2, 10)
house5 = House(-4, 0)

lines = [
    Line(battery1, house1),
    Line(house1, house2),
    Line(house1, house3),
    Line(house1, house5),
    Line(house2, house3),
    Line(house2, house4)
]

