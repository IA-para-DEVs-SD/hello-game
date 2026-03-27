"""Script para alternar entre sprites normais e procedurais.

Uso:
    python tools/switch_sprites.py procedural  # Usa sprites procedurais
    python tools/switch_sprites.py normal      # Usa sprites normais
    python tools/switch_sprites.py random      # Escolhe sprites aleatórios
"""

import sys
import shutil
import random
from pathlib import Path

ASSETS_DIR = Path(__file__).parent.parent / "assets" / "sprites"
PROCEDURAL_DIR = ASSETS_DIR / "procedural"

def switch_to_procedural():
    """Troca para sprites procedurais."""
    print("🔄 Alternando para sprites procedurais...")
    
    # Lista de sprites procedurais disponíveis
    procedural_sprites = {
        "player": list(PROCEDURAL_DIR.glob("player_procedural_*.png")),
        "enemy": list(PROCEDURAL_DIR.glob("enemy_*_var*.png")),
        "ring": list(PROCEDURAL_DIR.glob("coin_var*.png")),
    }
    
    # Escolhe aleatoriamente
    if procedural_sprites["player"]:
        chosen = random.choice(procedural_sprites["player"])
        shutil.copy(chosen, ASSETS_DIR / "player_procedural.png")
        print(f"  ✓ Player: {chosen.name}")
    
    if procedural_sprites["enemy"]:
        chosen = random.choice(procedural_sprites["enemy"])
        shutil.copy(chosen, ASSETS_DIR / "enemy_procedural.png")
        print(f"  ✓ Enemy: {chosen.name}")
    
    if procedural_sprites["ring"]:
        chosen = random.choice(procedural_sprites["ring"])
        shutil.copy(chosen, ASSETS_DIR / "ring_procedural.png")
        print(f"  ✓ Ring: {chosen.name}")
    
    print("\n✅ Sprites procedurais ativados!")
    print("   Reinicie o jogo para ver as mudanças.")

def switch_to_normal():
    """Remove sprites procedurais para usar os normais."""
    print("🔄 Alternando para sprites normais...")
    
    procedural_files = [
        ASSETS_DIR / "player_procedural.png",
        ASSETS_DIR / "enemy_procedural.png",
        ASSETS_DIR / "ring_procedural.png",
    ]
    
    for file in procedural_files:
        if file.exists():
            file.unlink()
            print(f"  ✓ Removido: {file.name}")
    
    print("\n✅ Sprites normais ativados!")
    print("   Reinicie o jogo para ver as mudanças.")

def show_available():
    """Mostra sprites disponíveis."""
    print("📊 Sprites disponíveis:\n")
    
    print("🧍 Players procedurais:")
    for sprite in sorted(PROCEDURAL_DIR.glob("player_procedural_*.png")):
        print(f"  • {sprite.name}")
    
    print("\n👾 Enemies procedurais:")
    for sprite in sorted(PROCEDURAL_DIR.glob("enemy_*_var*.png"))[:10]:
        print(f"  • {sprite.name}")
    if len(list(PROCEDURAL_DIR.glob("enemy_*_var*.png"))) > 10:
        print(f"  ... e mais {len(list(PROCEDURAL_DIR.glob('enemy_*_var*.png'))) - 10}")
    
    print("\n💰 Coins/Rings procedurais:")
    for sprite in sorted(PROCEDURAL_DIR.glob("coin_var*.png")):
        print(f"  • {sprite.name}")
    
    print(f"\n📁 Total: {len(list(PROCEDURAL_DIR.glob('*.png')))} sprites procedurais")

def main():
    if len(sys.argv) < 2:
        print("Uso: python tools/switch_sprites.py [procedural|normal|random|list]")
        print("\nOpções:")
        print("  procedural - Usa sprites procedurais aleatórios")
        print("  normal     - Usa sprites normais (desenhados)")
        print("  random     - Escolhe aleatoriamente entre normal e procedural")
        print("  list       - Lista sprites disponíveis")
        sys.exit(1)
    
    mode = sys.argv[1].lower()
    
    if mode == "procedural":
        switch_to_procedural()
    elif mode == "normal":
        switch_to_normal()
    elif mode == "random":
        if random.choice([True, False]):
            switch_to_procedural()
        else:
            switch_to_normal()
    elif mode == "list":
        show_available()
    else:
        print(f"❌ Modo desconhecido: {mode}")
        print("Use: procedural, normal, random ou list")
        sys.exit(1)

if __name__ == "__main__":
    main()
