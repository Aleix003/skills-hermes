"""Aviso antes de cada reunión (D-30): el filtro que va delante de la tarea «aviso-reunion».

Mira, sin IA, si en la hora siguiente empieza un evento con hora en Google (principal y «Hermes»)
o en iCloud. Si no hay ninguno nuevo, imprime {"wakeAgent": false} y Hermes no despierta a ChatGPT.
Si lo hay, lo apunta (para no avisar dos veces) y despierta al agente pasándole los eventos.
Si un calendario falla, lo dice una vez al día como fallo (Hermes lo manda por Telegram).

Original en el Mac de Aleix (proyecto Hermes, 02_Material-interno/puente/skills-solo-hermes/calendario-icloud/):
no lo edites en el servidor, se pisa cada hora. En el servidor lo lanza /opt/data/scripts/aviso_reunion.py.
Para probar: AHORA=2026-11-24T13:00 (hora de Madrid) y AVISO_ESTADO=/otra/ruta.json.
"""
import json
import os
import re
import subprocess
import sys
from datetime import date, datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

MADRID = ZoneInfo("Europe/Madrid")
VENTANA = timedelta(minutes=60)
AQUI = Path(__file__).resolve().parent
GAPI = os.environ.get("AVISO_GAPI", "/opt/hermes/skills/productivity/google-workspace/scripts/google_api.py")
ICLOUD = AQUI / "leer_icloud.py"
ESTADO = Path(os.environ.get("AVISO_ESTADO", "/opt/data/aviso_reunion_estado.json"))
CALENDARIOS_GOOGLE = {
    "primary": "Google",
    "e06de4abe27d00f8304e113b1b0680a2333d6838eeb3f33695366e92cc3e7a3d@group.calendar.google.com": "Hermes",
}
MESES = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]


def ahora():
    if os.environ.get("AHORA"):
        return datetime.fromisoformat(os.environ["AHORA"]).replace(tzinfo=MADRID)
    return datetime.now(MADRID)


def entorno():
    e = dict(os.environ)
    e["HERMES_HOME"] = "/opt/data"  # la llave de Google vive ahí; el programa llega con el entorno limpio
    return e


def google(desde, hasta):
    # margen a los dos lados: Google deja fuera lo que empieza justo en el final pedido; se filtra en main()
    eventos = []
    for cal, nombre in CALENDARIOS_GOOGLE.items():
        r = subprocess.run(
            [sys.executable, GAPI, "calendar", "list", "--calendar", cal,
             "--start", desde.isoformat(), "--end", hasta.isoformat()],
            capture_output=True, text=True, timeout=120, env=entorno())
        if r.returncode != 0:
            raise RuntimeError(f"Google ({nombre}): {(r.stderr or r.stdout).strip()[-300:]}")
        for ev in json.loads(r.stdout or "[]"):
            inicio = ev.get("start", "")
            if "T" not in inicio:  # de todo el día: no es una reunión con hora
                continue
            eventos.append({
                "calendario": nombre,
                "id": ev.get("id", ""),
                "titulo": ev.get("summary", "(sin título)"),
                "inicio": datetime.fromisoformat(inicio.replace("Z", "+00:00")).astimezone(MADRID),
                "fin": ev.get("end", ""),
                "lugar": ev.get("location", ""),
                "descripcion": (ev.get("description") or "")[:400],
            })
    return eventos


def icloud(momento):
    r = subprocess.run([sys.executable, str(ICLOUD), "--desde", momento.date().isoformat(), "--dias", "2"],
                       capture_output=True, text=True, timeout=120)
    if r.returncode != 0:
        raise RuntimeError(f"iCloud: {r.stdout.strip()[-300:]}")
    avisos = [l for l in r.stdout.splitlines() if l.startswith("Aviso:") and "no se pudo descargar" in l]
    if avisos:
        raise RuntimeError("iCloud: " + avisos[0][7:])
    eventos, dia = [], None
    for linea in r.stdout.splitlines():
        m = re.match(r"^\S+ (\d+) (\w+)$", linea)
        if m and m.group(2) in MESES:
            mes = MESES.index(m.group(2)) + 1
            anio = momento.year + (1 if mes < momento.month else 0)
            dia = date(anio, mes, int(m.group(1)))
            continue
        m = re.match(r"^  (\d\d):(\d\d)(?:–(\d\d:\d\d))? · (.*) \[(.*)\]$", linea)
        if m and dia:
            inicio = datetime(dia.year, dia.month, dia.day, int(m.group(1)), int(m.group(2)), tzinfo=MADRID)
            eventos.append({"calendario": f"iCloud · {m.group(5)}", "id": "", "titulo": m.group(4),
                            "inicio": inicio, "fin": m.group(3) or "", "lugar": "", "descripcion": ""})
    return eventos


def leer_estado():
    try:
        return json.loads(ESTADO.read_text())
    except (OSError, ValueError):
        return {"avisados": {}, "error_dia": ""}


def main():
    t = ahora()
    estado = leer_estado()
    eventos, errores = [], []
    for fuente in (lambda: google(t - timedelta(minutes=5), t + VENTANA + timedelta(minutes=30)), lambda: icloud(t)):
        try:
            eventos += fuente()
        except Exception as e:  # sin enseñar llaves ni enlaces: solo el final del mensaje
            errores.append(str(e) or type(e).__name__)

    nuevos = []
    for ev in eventos:
        if not (t < ev["inicio"] <= t + VENTANA):
            continue
        clave = f'{ev["calendario"]}|{ev["id"] or ev["titulo"]}|{ev["inicio"].isoformat()}'
        if clave in estado["avisados"]:
            continue
        estado["avisados"][clave] = ev["inicio"].isoformat()
        nuevos.append(ev)

    # olvida lo de hace más de dos días
    limite = (t - timedelta(days=2)).isoformat()
    estado["avisados"] = {k: v for k, v in estado["avisados"].items() if v >= limite}

    fallo_hoy = errores and estado.get("error_dia") != t.date().isoformat()
    if fallo_hoy:
        estado["error_dia"] = t.date().isoformat()
    ESTADO.write_text(json.dumps(estado, ensure_ascii=False, indent=1))

    if fallo_hoy and not nuevos:
        print("⚠️ Aviso de reuniones: no pude leer un calendario. " + " | ".join(errores))
        sys.exit(1)
    if not nuevos:
        print(json.dumps({"wakeAgent": False}))
        return
    lista = [{**ev, "inicio": ev["inicio"].strftime("%d/%m %H:%M")} for ev in nuevos]
    print("Eventos que empiezan en la próxima hora:")
    for ev in lista:
        print(f'- {ev["inicio"]} · {ev["titulo"]} [{ev["calendario"]}]')
    if errores:
        print("Aviso: no pude leer un calendario: " + " | ".join(errores))
    print(json.dumps({"wakeAgent": True, "context": {"eventos": lista, "errores": errores}}, ensure_ascii=False))


if __name__ == "__main__":
    main()
