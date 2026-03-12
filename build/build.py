#!/usr/bin/env python3
"""
Script de build para criar executável do PyBlaze.

Uso:
    python scripts/build.py

Gera executável standalone em dist/
"""

import subprocess
import sys
from pathlib import Path


def main() -> None:
    """Cria executável do PyBlaze usando PyInstaller."""

    print("=" * 60)
    print("PyBlaze - Build de Executável")
    print("=" * 60)

    # Verificar se PyInstaller está instalado
    try:
        import PyInstaller
        print(f"✓ PyInstaller {PyInstaller.__version__} encontrado")
    except ImportError:
        print("✗ PyInstaller não encontrado. Instalando...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
        print("✓ PyInstaller instalado com sucesso")

    # Caminhos
    project_root = Path(__file__).parent.parent
    main_script = project_root / "src" / "pyblaze" / "main.py"

    if not main_script.exists():
        print(f"✗ Erro: {main_script} não encontrado!")
        sys.exit(1)

    print(f"✓ Script principal: {main_script}")

    # Argumentos do PyInstaller
    args = [
        "pyinstaller",
        str(main_script),
        "--name=PyBlaze",
        "--onefile",                    # Único arquivo executável
        "--windowed",                   # Sem console (somente janela do jogo)
        "--clean",                      # Limpa cache antes de build
        "--noconfirm",                  # Não pede confirmação

        # Coletar dados necessários
        "--collect-all=pygame",
        "--collect-all=pygame_ce",

        # Opções adicionais
        "--log-level=INFO",

        # Hidden imports (se necessário)
        "--hidden-import=pygame",
        "--hidden-import=pygame.base",
        "--hidden-import=pygame.constants",
        "--hidden-import=pygame.rect",
        "--hidden-import=pygame.surface",

        # Diretórios
        f"--distpath={project_root / 'dist'}",
        f"--workpath={project_root / 'build'}",
        f"--specpath={project_root}",
    ]

    # Adicionar ícone se existir
    icon_path = project_root / "assets" / "icon.ico"
    if icon_path.exists():
        args.append(f"--icon={icon_path}")
        print(f"✓ Ícone: {icon_path}")
    else:
        print("⚠ Ícone não encontrado - executável sem ícone customizado")

    # Executar build
    print("\n" + "=" * 60)
    print("Iniciando build...")
    print("=" * 60 + "\n")

    try:
        subprocess.run(args, check=True, cwd=project_root)

        print("\n" + "=" * 60)
        print("✓ Build concluído com sucesso!")
        print("=" * 60)

        exe_path = project_root / "dist" / "PyBlaze.exe"
        if exe_path.exists():
            size_mb = exe_path.stat().st_size / (1024 * 1024)
            print(f"\n✓ Executável: {exe_path}")
            print(f"✓ Tamanho: {size_mb:.2f} MB")
            print(f"\nPara executar: dist/PyBlaze.exe")
        else:
            exe_path = project_root / "dist" / "PyBlaze"
            if exe_path.exists():
                size_mb = exe_path.stat().st_size / (1024 * 1024)
                print(f"\n✓ Executável: {exe_path}")
                print(f"✓ Tamanho: {size_mb:.2f} MB")
                print(f"\nPara executar: dist/PyBlaze")

    except subprocess.CalledProcessError as e:
        print(f"\n✗ Erro durante o build: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
