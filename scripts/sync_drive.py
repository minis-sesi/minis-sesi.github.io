#!/usr/bin/env python3
"""
Sincronizador Automático: Google Drive + Planilha Google -> Site Mini S
-----------------------------------------------------------------------
1. Varre a pasta pública do Google Drive do projeto Mini S:
   - Detecta automaticamente qualquer Planilha Google (Google Sheets) na pasta
     raiz ou em "Gestão e Cronograma" / "Atividades e Planos de Aula" para ler
     os textos (título, resumo, idade, tempo, objetivos, roteiro, materiais, vídeo).
   - Varre as subpastas "Aula 01..." até "Aula 15..." em "Atividades e Planos de Aula".
   - Quando encontra um PDF novo em uma pasta de aula, baixa o PDF para `public/pdf/`,
     renderiza todas as páginas em `public/img/paginas/` e cria/atualiza `content/aulas/aula-XX.json`.
2. Também verifica todas as aulas já existentes em `content/aulas/*.json`:
   - Se alguma aula tiver PDF mas estiver sem `capa` ou `paginas` (ex.: enviada pelo /admin),
     gera automaticamente a capa e as páginas em JPG a partir do PDF.
"""

import csv
import glob
import io
import json
import os
import re
import sys
import unicodedata
import urllib.request
from pathlib import Path

import pypdf
import pypdfium2 as pdfium

ROOT_DRIVE_FOLDER_ID = "1TeA6AENeQ5RrVho9R6CdlckK_InAXTpp"
ATIVIDADES_FOLDER_ID = "1xSdiGdEv9prR9mz8UOOJUbd8dODX_jWy"
CRONOGRAMA_FOLDER_ID = "1L30u-2YkWJxaBaMPw8ieN6_WD-9_OoZU"

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"


def slugify(value: str) -> str:
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    value = re.sub(r"[^a-zA-Z0-9]+", "-", value.lower()).strip("-")
    return value or "material"


def infer_equipe(folder_name: str) -> str:
    upper = folder_name.upper()
    if "FRC" in upper:
        return "S ROBOTS FRC"
    if "STEM" in upper or "ATLAS" in upper:
        return "Scuderia S ATLAS"
    if "FTC" in upper or "ROBOTS" in upper:
        return "S ROBOTS FTC"
    return ""


def infer_serie(equipe: str) -> str:
    if equipe == "Scuderia S ATLAS":
        return "STEM Racing"
    if equipe == "S ROBOTS FRC":
        return "FIRST Robotics Competition"
    return "S Robots Explorer"


def fetch_drive_folder_items(folder_id: str) -> list[dict] | None:
    """Lê os arquivos/pastas de uma pasta pública do Google Drive. Retorna None em erro de rede."""
    url = f"https://drive.google.com/drive/folders/{folder_id}?usp=sharing"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            html = resp.read().decode("utf-8", errors="ignore")
    except Exception as e:
        print(f"[AVISO] Não foi possível acessar a pasta {folder_id}: {e}")
        return None

    callbacks = re.findall(r"AF_initDataCallback\(({.*?})\);</script>", html, re.DOTALL)
    if not callbacks:
        return []

    cb = callbacks[3] if len(callbacks) > 3 else callbacks[-1]
    excluded = {
        "Name", "A to Z", "Z to A", "Date modified", "New to old",
        "Modified", "File size", "Size not available", "Drop files here",
        "or use the “New” button.", ""
    }

    items_by_id = {}
    for m in re.finditer(r'\[(?:null,)?"([a-zA-Z0-9_-]{25,50})"', cb):
        item_id = m.group(1)
        if item_id == folder_id:
            continue
        sub = cb[m.end(): m.end() + 650]
        fn_match = re.search(r'\[\[\["([^"\\]+)"', sub)
        mime_match = re.search(r'"(application/[^"]+|video/[^"]+|image/[^"]+)"', sub)
        if fn_match:
            fname = fn_match.group(1).strip()
            if (
                fname not in excluded
                and not re.match(r"^\d+ de [a-z]+\.?$", fname, re.I)
                and not re.match(r"^\d+(?:,\d+)?\s*(?:KB|MB|B|GB)$", fname, re.I)
            ):
                mime = mime_match.group(1) if mime_match else ""
                if item_id not in items_by_id or (not items_by_id[item_id]["mime"] and mime):
                    items_by_id[item_id] = {
                        "id": item_id,
                        "name": fname,
                        "mime": mime,
                    }
    return list(items_by_id.values())


def download_drive_file(file_id: str, dest_path: Path) -> bool:
    """Baixa um arquivo público do Google Drive pelo ID."""
    url = f"https://drive.google.com/uc?id={file_id}&export=download"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            content = resp.read()
        if content[:15].startswith((b"<!DOCTYPE", b"<html")):
            print(f"[AVISO] Arquivo {file_id} retornou página HTML em vez de binário.")
            return False
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        dest_path.write_bytes(content)
        return True
    except Exception as e:
        print(f"[ERRO] Falha ao baixar {file_id}: {e}")
        return False


def render_pdf_pages(pdf_path: Path, aula_num: int, scale: int = 2) -> list[str]:
    """Renderiza as páginas de um PDF como imagens JPG em public/img/paginas/."""
    out_dir = Path("public/img/paginas")
    out_dir.mkdir(parents=True, exist_ok=True)
    prefix = f"a{aula_num:02d}"
    pages = []
    try:
        pdf = pdfium.PdfDocument(str(pdf_path))
        for i, page in enumerate(pdf):
            page_num = i + 1
            img = page.render(scale=scale).to_pil()
            fn = f"{prefix}_p{page_num:02d}.jpg"
            out_path = out_dir / fn
            img.save(str(out_path), format="JPEG", quality=85)
            pages.append(f"img/paginas/{fn}")
        pdf.close()
    except Exception as e:
        print(f"[ERRO] Falha ao renderizar páginas de {pdf_path}: {e}")
    return pages


def extract_pdf_metadata(pdf_path: Path, fallback_title: str) -> dict:
    """Extrai um título e resumo inicial do texto do PDF, quando disponível."""
    title = re.sub(r"\.pdf$", "", fallback_title, flags=re.I)
    title = re.sub(r"^c[oó]pia de\s+", "", title, flags=re.I)
    title = re.sub(r"^mini s[_\s:-]*", "", title, flags=re.I)
    title = re.sub(r"^plano de aula\s*[—–-]\s*", "", title, flags=re.I)
    title = re.sub(r"^roteiro de oficina[_\s:-]*", "", title, flags=re.I)
    title = title.strip(" _-") or fallback_title

    resumo = "Atividade prática desenvolvida pelas equipes de robótica para aplicação em sala."
    try:
        reader = pypdf.PdfReader(str(pdf_path))
        full_text = "\n".join((p.extract_text() or "") for p in reader.pages[:2])
        lines = [re.sub(r"\s+", " ", l).strip() for l in full_text.splitlines() if l.strip()]
        if lines:
            # Procura linha descritiva para resumo
            for l in lines:
                if len(l) > 50 and not l.lower().startswith(("módulo", "tema:", "data:")):
                    resumo = l[:240]
                    break
    except Exception:
        pass

    return {"titulo": title, "resumo": resumo}


def fetch_sheet_overrides() -> dict[int, dict]:
    """
    Procura uma Planilha Google (spreadsheet) na pasta do Drive (ou variável GOOGLE_SHEET_ID)
    e retorna os dados preenchidos pela equipe indexados pelo número da aula.
    """
    sheet_id = os.environ.get("GOOGLE_SHEET_ID", "").strip()
    if not sheet_id:
        for fid in (ROOT_DRIVE_FOLDER_ID, ATIVIDADES_FOLDER_ID, CRONOGRAMA_FOLDER_ID):
            for item in (fetch_drive_folder_items(fid) or []):
                if "spreadsheet" in item.get("mime", ""):
                    sheet_id = item["id"]
                    print(f"[INFO] Planilha Google detectada no Drive: {item['name']} ({sheet_id})")
                    break
            if sheet_id:
                break

    if not sheet_id:
        return {}

    csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
    req = urllib.request.Request(csv_url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            csv_text = resp.read().decode("utf-8-sig", errors="ignore")
    except Exception as e:
        print(f"[AVISO] Não foi possível baixar a planilha {sheet_id}: {e}")
        return {}

    overrides = {}
    reader = csv.DictReader(io.StringIO(csv_text))
    for row in reader:
        # Normaliza nomes das colunas
        norm = {slugify(k): (v or "").strip() for k, v in row.items() if k}
        num_str = norm.get("numero") or norm.get("aula") or norm.get("n") or ""
        m = re.search(r"\d+", num_str)
        if not m:
            continue
        num = int(m.group(0))
        entry = {}
        for key, col_aliases in [
            ("titulo", ["titulo", "nome", "titulo-da-aula"]),
            ("equipe", ["equipe", "equipe-que-criou"]),
            ("serie", ["serie", "serie-missao"]),
            ("modulo", ["modulo"]),
            ("resumo", ["resumo", "descricao"]),
            ("idade", ["idade", "idade-recomendada"]),
            ("tempo", ["tempo", "tempo-estimado", "duracao"]),
            ("video", ["video", "youtube", "link-do-video"]),
        ]:
            for alias in col_aliases:
                if norm.get(alias):
                    entry[key] = norm[alias]
                    break

        for list_key, col_aliases in [
            ("habilidades", ["habilidades", "habilidades-desenvolvidas"]),
            ("objetivos", ["objetivos"]),
            ("roteiro", ["roteiro", "passo-a-passo"]),
            ("materiais", ["materiais", "materiais-necessarios"]),
        ]:
            for alias in col_aliases:
                val = norm.get(alias)
                if val:
                    sep = ";" if ";" in val else "\n" if "\n" in val else ","
                    items = [x.strip(" •-*") for x in val.split(sep) if x.strip(" •-*")]
                    if items:
                        entry[list_key] = items
                    break

        if entry:
            overrides[num] = entry
    return overrides


def load_existing_aulas() -> dict[int, tuple[Path, dict]]:
    aulas = {}
    for p in sorted(glob.glob("content/aulas/*.json")):
        path = Path(p)
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            num = int(data.get("numero", 0))
            if num > 0:
                aulas[num] = (path, data)
        except Exception as e:
            print(f"[AVISO] Erro lendo {p}: {e}")
    return aulas


def sync_from_drive(force: bool = False) -> int:
    changes = 0
    existing = load_existing_aulas()
    sheet_overrides = fetch_sheet_overrides()

    print("[1/3] Consultando pastas de aulas no Google Drive...")
    subfolders = fetch_drive_folder_items(ATIVIDADES_FOLDER_ID) or []

    for folder in sorted(subfolders, key=lambda x: x["name"]):
        m = re.search(r"Aula\s*(\d+)", folder["name"], re.I)
        if not m:
            continue
        aula_num = int(m.group(1))

        files = fetch_drive_folder_items(folder["id"])
        if files is None:
            continue

        pdfs = [
            f for f in files
            if f["name"].lower().endswith(".pdf") or "pdf" in f.get("mime", "").lower()
        ]
        if not pdfs:
            # Se a pasta ficou vazia no Drive (a partir da Aula 4), remove a aula do site
            if aula_num >= 4 and aula_num in existing:
                old_json, old_data = existing.pop(aula_num)
                print(f" -> Pasta Aula {aula_num:02d} vazia no Drive: removendo {old_json.name} (voltando para 'Em breve')...")
                old_pdf = (old_data.get("pdf") or "").lstrip("/").removeprefix("public/")
                if old_pdf and (Path("public") / old_pdf).exists():
                    (Path("public") / old_pdf).unlink()
                for old_pg in old_data.get("paginas", []):
                    pg_path = Path("public") / old_pg.lstrip("/").removeprefix("public/")
                    if pg_path.exists() and pg_path.name.startswith(f"a{aula_num:02d}_"):
                        pg_path.unlink()
                if old_json.exists():
                    old_json.unlink()
                changes += 1
            continue

        if aula_num in existing and not force:
            continue

        chosen_pdf = pdfs[0]
        print(f" -> Nova aula encontrada no Drive! Aula {aula_num:02d}: {chosen_pdf['name']}")
        pdf_slug = slugify(re.sub(r"\.pdf$", "", chosen_pdf["name"], flags=re.I))
        pdf_rel = f"pdf/aula-{aula_num:02d}-{pdf_slug}.pdf"
        pdf_dest = Path("public") / pdf_rel

        if not download_drive_file(chosen_pdf["id"], pdf_dest):
            continue

        pages = render_pdf_pages(pdf_dest, aula_num)
        meta = extract_pdf_metadata(pdf_dest, chosen_pdf["name"])
        equipe = infer_equipe(folder["name"])

        aula_data = {
            "numero": aula_num,
            "titulo": meta["titulo"],
            "equipe": equipe,
            "serie": infer_serie(equipe),
            "modulo": "",
            "resumo": meta["resumo"],
            "idade": "6 a 12 anos",
            "tempo": "30 a 45 min",
            "habilidades": ["Criatividade", "Trabalho em equipe", "Raciocínio lógico"],
            "objetivos": [],
            "roteiro": [],
            "materiais": ["Atividade impressa ou materiais da oficina"],
            "pdf": pdf_rel,
            "capa": pages[0] if pages else "",
            "paginas": pages,
            "video": "",
        }

        if aula_num in sheet_overrides:
            aula_data.update(sheet_overrides[aula_num])

        json_path = Path(f"content/aulas/aula-{aula_num:02d}.json")
        json_path.write_text(json.dumps(aula_data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        existing[aula_num] = (json_path, aula_data)
        changes += 1
        print(f"    [OK] Publicada {json_path} com {len(pages)} página(s).")

    print("[2/3] Aplicando atualizações da Planilha Google (se houver)...")
    for num, override in sheet_overrides.items():
        if num in existing:
            path, data = existing[num]
            updated = False
            for k, v in override.items():
                if v and data.get(k) != v:
                    data[k] = v
                    updated = True
            if updated:
                path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
                changes += 1
                print(f" -> Aula {num:02d} atualizada a partir da Planilha Google.")

    print("[3/3] Verificando capas e páginas das aulas existentes...")
    for num, (path, data) in existing.items():
        pdf_rel = (data.get("pdf") or "").lstrip("/").removeprefix("public/")
        if not pdf_rel:
            continue
        pdf_file = Path("public") / pdf_rel
        paginas = data.get("paginas") or []
        capa = data.get("capa") or ""
        missing_imgs = not paginas or any(
            not (Path("public") / p.lstrip("/").removeprefix("public/")).exists()
            for p in paginas
        )
        if pdf_file.exists() and missing_imgs:
            print(f" -> Gerando capa e páginas automaticamente para Aula {num:02d}...")
            rendered = render_pdf_pages(pdf_file, num)
            if rendered:
                data["paginas"] = rendered
                if not capa:
                    data["capa"] = rendered[0]
                path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
                changes += 1

    print(f"Sincronização concluída! Total de aulas atualizadas/criadas: {changes}")
    return changes


if __name__ == "__main__":
    force_flag = "--force" in sys.argv
    sync_from_drive(force=force_flag)
