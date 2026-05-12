"""
Script para descargar imágenes de medicamentos oftálmicos
y generar los UPDATE SQL correspondientes.

Requisitos:
    pip install requests icrawler Pillow

Uso:
    python descargar_imagenes.py
"""

import os
import time
import re
from pathlib import Path

# ─── CONFIGURACIÓN ────────────────────────────────────────────────────────────
OUTPUT_DIR = "./static/uploads"          # Carpeta donde se guardan las imágenes
SQL_OUTPUT  = "./update_image_urls.sql"  # Archivo SQL generado
BASE_URL    = "http://localhost:5000/static/uploads"
DELAY       = 1.5                        # Segundos entre búsquedas (evita bloqueos)
# ──────────────────────────────────────────────────────────────────────────────

# Lista completa de productos por nombre comercial
PRODUCTOS = [
    # Antibióticos
    "Altracine-A",
    "Wassetrol",
    "Oxyoftal",
    "Mixoftal",
    "Oftabiotico",
    "Iloticina Plus",
    "Eritrofarm",
    "Azydrop",
    "Meibos",
    "Cloranfenicol",
    "Oftagen",
    "Provisual compuesto",
    "Decadron",
    "Oftaflox",
    "Conjuntin-S",
    "Maxitrol",
    "Gotabiotic",
    "Gotabiotic-D",
    "Gotabiotic-F",
    "Ophthabracin",
    "Ophthabracin-D",
    "Xolof",
    "Tobraoftal",
    "Tobraoftal-D",
    "Lotemicin",
    "Tobrex",
    "Tobradex",
    "Trazidex",
    "Tobragan D",
    "Tobracort",
    "Terramicina",
    "Terravital",
    "Fucithalmic",
    "Blef-10 con lagrifilm",
    "Deltamid Ofteno",
    "OQ-PLUS",
    # Quinolonas
    "Oflox",
    "Ocuflox",
    "Ciprodex",
    "Ciproval",
    "Cifloblas",
    "Wassercipro",
    "Poenbiotic",
    "Sophixin",
    "Flobact",
    "Flobact-D",
    "Cilox",
    "Cilodex",
    "Moxof",
    "Oftamox",
    "Vigadexa",
    "Quimox",
    "ZYPRED",
    "gasyn",
    "Poengatif",
    "ZYMAXID",
    "Gatidex",
    "Carteof",
    # Antialérgicos
    "Syvicrom",
    "Cromovital",
    "Oftacromax",
    "Oftalirio",
    "Optialerg",
    "Vidizine",
    "Alerxy-c",
    "Atergit",
    "Kenaler",
    "Olopat",
    "Dolcettina",
    "Alecrix",
    # Antiinflamatorios AINES
    "Oftic",
    "3A Ofteno",
    "Dinaclord",
    "Voltaren Ophtha",
    "Acular",
    "Poenkerat",
    "Ophthaker",
    "Kenalgesic",
    "Zebesten",
    "Bronax",
    "Nepaoftal",
    "Nevanac",
    "Opticam",
    "Coxylan",
    # Corticoesteroides
    "Disalot",
    "Talof",
    "Lotemax",
    "Oftaprednol Max",
    "Flusure",
    "Flumex",
    "Flumetol NF",
    "Aflarex",
    "Ophthasona",
    "Maxidex",
    "Pred-f",
    "Cortioftal",
    "Durezol",
    "Tolf",
    # Inmunomoduladores
    "Modusik A",
    "Restasis",
    # Lubricantes
    "Hiprolub",
    "Freegen",
    "Genteal",
    "Oftalub",
    "TotalConfort",
    "Systane",
    "Acrylarm",
    "Kliner",
    "Toptear",
    "Humylub",
    # Anestésicos
    "Ponti ofteno",
    "Alcaine",
    "OQ-seina",
    # Autónomos ciclopléjicos
    "Cyclogil",
    "Isopto atropina",
    "Mydriacyl",
    "Fotorretin",
    # Vasoconstrictores
    "Cortioftal F",
    "NafOftalm",
    "Clarivis",
    "Visine",
    # Antiglaucomatosos
    "Timolol TQ",
    "Xalatan",
    "Travatan Z",
    "Lumigan",
    "Trusopt",
    "Azopt",
    "Alphagan",
    "Xalacom",
    "Combigan",
    "Simbrinza",
]


def nombre_a_archivo(nombre: str) -> str:
    """Convierte el nombre comercial en un nombre de archivo seguro."""
    safe = re.sub(r'[^\w\s\-]', '', nombre)
    safe = safe.strip().replace(' ', '_')
    return safe


def descargar_imagen(nombre: str, output_dir: str) -> str | None:
    """
    Descarga la primera imagen encontrada para el nombre comercial dado.
    Retorna el nombre del archivo guardado o None si falla.
    """
    try:
        from icrawler.builtin import GoogleImageCrawler

        safe_name = nombre_a_archivo(nombre)
        tmp_dir = os.path.join(output_dir, f"_tmp_{safe_name}")
        os.makedirs(tmp_dir, exist_ok=True)

        crawler = GoogleImageCrawler(
            storage={"root_dir": tmp_dir},
            log_level=50,           # silencioso
        )
        crawler.crawl(
            keyword=f"{nombre} colirio oftálmico medicamento",
            max_num=1,
            min_size=(100, 100),
            file_idx_offset=0,
        )

        # Buscar el archivo descargado
        archivos = list(Path(tmp_dir).glob("*"))
        if not archivos:
            print(f"  ✗ Sin imagen: {nombre}")
            return None

        src = archivos[0]
        ext = src.suffix.lower() or ".jpg"
        dst_name = f"{safe_name}{ext}"
        dst_path = os.path.join(output_dir, dst_name)

        src.rename(dst_path)
        Path(tmp_dir).rmdir()

        print(f"  ✓ Descargada: {nombre}  →  {dst_name}")
        return dst_name

    except Exception as e:
        print(f"  ✗ Error en '{nombre}': {e}")
        return None


def generar_sql(resultados: dict[str, str], base_url: str, sql_path: str):
    """Genera el archivo .sql con los UPDATE para cada producto."""
    lines = ["-- UPDATE image_url generado automáticamente\n"]
    for nombre, archivo in resultados.items():
        url = f"{base_url}/{archivo}"
        # Escapar comillas simples en el nombre
        nombre_escaped = nombre.replace("'", "''")
        lines.append(
            f"UPDATE products SET image_url = '{url}' "
            f"WHERE commercial_name = '{nombre_escaped}';"
        )

    with open(sql_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"\n✅ SQL guardado en: {sql_path}")


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    resultados: dict[str, str] = {}

    print(f"🔍 Descargando imágenes para {len(PRODUCTOS)} productos...\n")

    for i, nombre in enumerate(PRODUCTOS, 1):
        print(f"[{i}/{len(PRODUCTOS)}] {nombre}")
        archivo = descargar_imagen(nombre, OUTPUT_DIR)
        if archivo:
            resultados[nombre] = archivo
        time.sleep(DELAY)

    print(f"\n📊 Resultado: {len(resultados)}/{len(PRODUCTOS)} imágenes descargadas")

    if resultados:
        generar_sql(resultados, BASE_URL, SQL_OUTPUT)
    else:
        print("⚠️  No se descargó ninguna imagen.")


if __name__ == "__main__":
    main()
