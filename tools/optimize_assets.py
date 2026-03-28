"""Script para otimizar assets (compressão de sprites)."""

import argparse
import logging
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("PIL/Pillow não instalado. Instale com: pip install Pillow")
    exit(1)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def optimize_png(image_path: Path, quality: int = 85) -> int:
    """Otimiza um arquivo PNG.

    Args:
        image_path: Caminho para o arquivo PNG.
        quality: Qualidade da compressão (1-100).

    Returns:
        Bytes economizados.
    """
    try:
        original_size = image_path.stat().st_size

        img = Image.open(image_path)

        # Converte para RGB se for RGBA (remove alpha se não necessário)
        if img.mode == "RGBA":
            # Verifica se realmente usa transparência
            if img.getextrema()[3] == (255, 255):
                img = img.convert("RGB")

        # Salva otimizado
        img.save(image_path, "PNG", optimize=True, quality=quality)

        new_size = image_path.stat().st_size
        saved = original_size - new_size

        logger.info(
            "Optimized %s: %d KB -> %d KB (saved %d KB)",
            image_path.name,
            original_size // 1024,
            new_size // 1024,
            saved // 1024,
        )

        return saved

    except Exception as e:
        logger.error("Failed to optimize %s: %s", image_path, e)
        return 0


def optimize_directory(directory: Path, quality: int = 85) -> None:
    """Otimiza todos os PNGs em um diretório.

    Args:
        directory: Diretório com os PNGs.
        quality: Qualidade da compressão.
    """
    png_files = list(directory.rglob("*.png"))
    total_saved = 0

    logger.info("Found %d PNG files to optimize", len(png_files))

    for png_file in png_files:
        saved = optimize_png(png_file, quality)
        total_saved += saved

    logger.info(
        "Optimization complete! Total saved: %d KB (%d MB)",
        total_saved // 1024,
        total_saved // (1024 * 1024),
    )


def main() -> None:
    """Entry point do script."""
    parser = argparse.ArgumentParser(
        description="Optimize PNG sprites for PyBlaze"
    )
    parser.add_argument(
        "--dir",
        type=Path,
        default=Path("assets/sprites"),
        help="Directory containing sprites (default: assets/sprites)",
    )
    parser.add_argument(
        "--quality",
        type=int,
        default=85,
        help="Compression quality 1-100 (default: 85)",
    )

    args = parser.parse_args()

    if not args.dir.exists():
        logger.error("Directory not found: %s", args.dir)
        return

    optimize_directory(args.dir, args.quality)


if __name__ == "__main__":
    main()
