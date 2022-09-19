import pandas as pd

from world_generator import generate_world

map = generate_world(10, 2)


df = pd.DataFrame(map)

print(df[0])
