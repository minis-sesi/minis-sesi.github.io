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
   - Quando encontra um vídeo `.mp4` na pasta da aula, baixa para `public/videos/aula-XX.mp4`,
     otimiza com faststart (para reprodução instantânea em qualquer dispositivo) e vincula na aula.
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
import struct
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
CONTAINER_ATOMS = {b"moov", b"trak", b"mdia", b"minf", b"dinf", b"stbl", b"edts", b"udta"}


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


def _parse_atoms(buf: bytes, start: int = 0, end: int | None = None):
    if end is None:
        end = len(buf)
    pos = start
    atoms = []
    while pos + 8 <= end:
        size, atype = struct.unpack(">I4s", buf[pos : pos + 8])
        hdr = 8
        if size == 1:
            if pos + 16 > end:
                break
            size = struct.unpack(">Q", buf[pos + 8 : pos + 16])[0]
            hdr = 16
        elif size == 0:
            size = end - pos
        if size < hdr or pos + size > end:
            break
        atoms.append((atype, pos, size, hdr))
        pos += size
    return atoms


def _patch_chunk_offsets(moov_buf: bytearray, start: int, end: int, delta: int):
    for atype, pos, size, hdr in _parse_atoms(moov_buf, start, end):
        if atype in CONTAINER_ATOMS:
            _patch_chunk_offsets(moov_buf, pos + hdr, pos + size, delta)
        elif atype == b"stco":
            count = struct.unpack(">I", moov_buf[pos + hdr + 4 : pos + hdr + 8])[0]
            base = pos + hdr + 8
            for i in range(count):
                off = base + i * 4
                val = struct.unpack(">I", moov_buf[off : off + 4])[0]
                struct.pack_into(">I", moov_buf, off, val + delta)
        elif atype == b"co64":
            count = struct.unpack(">I", moov_buf[pos + hdr + 4 : pos + hdr + 8])[0]
            base = pos + hdr + 8
            for i in range(count):
                off = base + i * 8
                val = struct.unpack(">Q", moov_buf[off : off + 8])[0]
                struct.pack_into(">Q", moov_buf, off, val + delta)


def make_faststart(path: Path) -> bool:
    """Move o átomo moov para o início do MP4 para reprodução imediata em qualquer dispositivo."""
    try:
        data = path.read_bytes()
        top = _parse_atoms(data)
        moov = next((a for a in top if a[0] == b"moov"), None)
        mdat = next((a for a in top if a[0] == b"mdat"), None)
        if not moov or not mdat or moov[1] < mdat[1]:
            return False
        moov_bytes = bytearray(data[moov[1] : moov[1] + moov[2]])
        _patch_chunk_offsets(moov_bytes, moov[3], len(moov_bytes), len(moov_bytes))
        out = bytearray()
        for atype, pos, size, _ in top:
            if atype == b"moov":
                continue
            if atype == b"mdat":
                out.extend(moov_bytes)
            out.extend(data[pos : pos + size])
        path.write_bytes(bytes(out))
        return True
    except Exception as e:
        print(f"[AVISO] Não foi possível aplicar faststart em {path.name}: {e}")
        return False


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
    pattern = re.compile(
        r'\[\[null,"([a-zA-Z0-9_-]{25,50})"\],null,null,null,"([^"]+)".*?\[\[\["([^"\\]+)"',
        re.DOTALL,
    )
    items = []
    seen = set()
    for m in pattern.finditer(cb):
        item_id, mime, fname = m.group(1), m.group(2), m.group(3).strip()
        if item_id != folder_id and item_id not in seen:
            seen.add(item_id)
            items.append({"id": item_id, "name": fname, "mime": mime})
    return items


def download_drive_file(file_id: str, dest_path: Path) -> bool:
    """Baixa um arquivo público do Google Drive pelo ID."""
    url = f"https://drive.google.com/uc?id={file_id}&export=download"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
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
        vids = [
            f for f in files
            if f["name"].lower().endswith((".mp4", ".mov", ".webm")) or "video" in f.get("mime", "").lower()
        ]

        if not pdfs:
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

        # Se a aula já existe mas tem um vídeo novo na pasta do Drive e ainda não tem vídeo vinculado
        if aula_num in existing and not force:
            json_path, aula_data = existing[aula_num]
            if vids and not aula_data.get("video"):
                vid_rel = f"videos/aula-{aula_num:02d}.mp4"
                vid_dest = Path("public") / vid_rel
                if not vid_dest.exists():
                    print(f" -> Baixando vídeo da Aula {aula_num:02d}: {vids[0]['name']}...")
                    if download_drive_file(vids[0]["id"], vid_dest):
                        make_faststart(vid_dest)
                if vid_dest.exists():
                    aula_data["video"] = vid_rel
                    json_path.write_text(json.dumps(aula_data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
                    changes += 1
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

        video_rel = ""
        if vids:
            vid_candidate = f"videos/aula-{aula_num:02d}.mp4"
            vid_dest = Path("public") / vid_candidate
            print(f" -> Baixando vídeo da Aula {aula_num:02d}: {vids[0]['name']}...")
            if download_drive_file(vids[0]["id"], vid_dest):
                make_faststart(vid_dest)
                video_rel = vid_candidate

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
            "video": video_rel,
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
