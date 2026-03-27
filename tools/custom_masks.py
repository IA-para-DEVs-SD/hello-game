"""Máscaras customizadas para geração procedural de sprites.

Adicione suas próprias máscaras aqui para criar novos tipos de sprites.
"""

# Plataforma/Bloco
PLATFORM_MASK = [
    [1, 2, 2, 2, 1],
    [2, 3, 3, 3, 2],
    [2, 3, 4, 3, 2],
    [2, 2, 2, 2, 2],
]

# Moeda/Anel giratório
COIN_MASK = [
    [0, 1, 2, 1, 0],
    [1, 2, 3, 2, 1],
    [2, 3, 0, 3, 2],
    [1, 2, 3, 2, 1],
    [0, 1, 2, 1, 0],
]

# Estrela/Power-up
STAR_MASK = [
    [0, 0, 1, 0, 0],
    [0, 1, 2, 1, 0],
    [1, 2, 3, 2, 1],
    [0, 2, 3, 2, 0],
    [0, 1, 2, 1, 0],
    [1, 0, 2, 0, 1],
    [0, 0, 1, 0, 0],
]

# Cogumelo/Fungo
MUSHROOM_MASK = [
    [0, 1, 2, 2, 1, 0],
    [1, 2, 3, 3, 2, 1],
    [2, 3, 4, 4, 3, 2],
    [0, 0, 2, 2, 0, 0],
    [0, 0, 2, 2, 0, 0],
    [0, 0, 1, 1, 0, 0],
]

# Árvore
TREE_MASK = [
    [0, 0, 1, 1, 0, 0],
    [0, 1, 2, 2, 1, 0],
    [1, 2, 3, 3, 2, 1],
    [0, 2, 3, 3, 2, 0],
    [0, 1, 2, 2, 1, 0],
    [0, 0, 1, 1, 0, 0],
    [0, 0, 2, 2, 0, 0],
    [0, 0, 2, 2, 0, 0],
    [0, 0, 1, 1, 0, 0],
]

# Nuvem
CLOUD_MASK = [
    [0, 1, 2, 2, 1, 0],
    [1, 2, 3, 3, 2, 1],
    [2, 3, 3, 3, 3, 2],
    [1, 2, 2, 2, 2, 1],
]

# Espinho/Perigo
SPIKE_MASK = [
    [0, 0, 1, 0, 0],
    [0, 1, 2, 1, 0],
    [1, 2, 3, 2, 1],
    [2, 2, 2, 2, 2],
]

# Porta/Portal
PORTAL_MASK = [
    [1, 1, 1, 1, 1],
    [1, 2, 3, 2, 1],
    [1, 2, 4, 2, 1],
    [1, 2, 4, 2, 1],
    [1, 2, 4, 2, 1],
    [1, 2, 3, 2, 1],
    [1, 1, 1, 1, 1],
]

# Chave
KEY_MASK = [
    [0, 1, 2, 2, 1],
    [1, 2, 3, 3, 2],
    [0, 1, 2, 2, 1],
    [0, 0, 1, 1, 0],
    [0, 0, 1, 1, 0],
    [0, 1, 2, 0, 0],
    [0, 1, 2, 0, 0],
]

# Baú/Caixa
CHEST_MASK = [
    [1, 1, 1, 1, 1, 1],
    [1, 2, 2, 2, 2, 1],
    [1, 2, 3, 3, 2, 1],
    [2, 2, 2, 2, 2, 2],
    [2, 3, 3, 3, 3, 2],
    [2, 2, 2, 2, 2, 2],
]

# Escudo
SHIELD_MASK = [
    [0, 0, 1, 1, 0, 0],
    [0, 1, 2, 2, 1, 0],
    [1, 2, 3, 3, 2, 1],
    [1, 2, 3, 3, 2, 1],
    [0, 2, 3, 3, 2, 0],
    [0, 1, 2, 2, 1, 0],
    [0, 0, 1, 1, 0, 0],
]

# Espada
SWORD_MASK = [
    [0, 0, 0, 1, 0],
    [0, 0, 1, 2, 0],
    [0, 1, 2, 3, 0],
    [1, 2, 3, 0, 0],
    [0, 2, 0, 0, 0],
    [0, 1, 2, 0, 0],
    [0, 0, 1, 0, 0],
]

# Bomba
BOMB_MASK = [
    [0, 0, 1, 0, 0],
    [0, 0, 1, 0, 0],
    [0, 1, 2, 1, 0],
    [1, 2, 3, 2, 1],
    [1, 2, 3, 2, 1],
    [0, 1, 2, 1, 0],
]

# Foguete
ROCKET_MASK = [
    [0, 0, 1, 0, 0],
    [0, 1, 2, 1, 0],
    [0, 1, 3, 1, 0],
    [1, 2, 3, 2, 1],
    [0, 2, 3, 2, 0],
    [0, 1, 2, 1, 0],
    [0, 0, 2, 0, 0],
    [0, 0, 3, 0, 0],
]

# Fantasma
GHOST_MASK = [
    [0, 1, 2, 2, 1, 0],
    [1, 2, 3, 3, 2, 1],
    [2, 3, 4, 4, 3, 2],
    [2, 4, 3, 3, 4, 2],
    [2, 3, 3, 3, 3, 2],
    [2, 3, 3, 3, 3, 2],
    [2, 3, 3, 3, 3, 2],
    [2, 3, 2, 3, 2, 3],
]

# Slime/Gosma
SLIME_MASK = [
    [0, 1, 2, 2, 1, 0],
    [1, 2, 3, 3, 2, 1],
    [2, 3, 4, 4, 3, 2],
    [2, 4, 3, 3, 4, 2],
    [2, 3, 3, 3, 3, 2],
    [1, 2, 2, 2, 2, 1],
]

# Morcego
BAT_MASK = [
    [1, 0, 0, 0, 1],
    [2, 1, 0, 1, 2],
    [2, 2, 1, 2, 2],
    [0, 2, 3, 2, 0],
    [0, 1, 2, 1, 0],
]

# Pássaro
BIRD_MASK = [
    [0, 0, 1, 1, 0],
    [0, 1, 2, 2, 0],
    [1, 2, 3, 2, 1],
    [0, 2, 2, 1, 0],
    [0, 1, 0, 0, 0],
]

# Peixe
FISH_MASK = [
    [0, 0, 1, 2, 2],
    [0, 1, 2, 3, 3],
    [1, 2, 3, 4, 3],
    [0, 1, 2, 3, 3],
    [0, 0, 1, 2, 2],
]

# Borboleta
BUTTERFLY_MASK = [
    [1, 2, 0, 0, 2, 1],
    [2, 3, 1, 1, 3, 2],
    [0, 1, 2, 2, 1, 0],
    [0, 0, 1, 1, 0, 0],
]

# Flor
FLOWER_MASK = [
    [0, 1, 2, 1, 0],
    [1, 2, 3, 2, 1],
    [0, 1, 2, 1, 0],
    [0, 0, 1, 0, 0],
    [0, 0, 1, 0, 0],
    [0, 1, 2, 1, 0],
]

# Todas as máscaras disponíveis
ALL_MASKS = {
    "platform": PLATFORM_MASK,
    "coin": COIN_MASK,
    "star": STAR_MASK,
    "mushroom": MUSHROOM_MASK,
    "tree": TREE_MASK,
    "cloud": CLOUD_MASK,
    "spike": SPIKE_MASK,
    "portal": PORTAL_MASK,
    "key": KEY_MASK,
    "chest": CHEST_MASK,
    "shield": SHIELD_MASK,
    "sword": SWORD_MASK,
    "bomb": BOMB_MASK,
    "rocket": ROCKET_MASK,
    "ghost": GHOST_MASK,
    "slime": SLIME_MASK,
    "bat": BAT_MASK,
    "bird": BIRD_MASK,
    "fish": FISH_MASK,
    "butterfly": BUTTERFLY_MASK,
    "flower": FLOWER_MASK,
}
