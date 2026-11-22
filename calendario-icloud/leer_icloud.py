#!/usr/bin/env python3
"""Lee los calendarios de iCloud de Aleix (solo lectura) y dice qué eventos hay en unos días.

Los enlaces públicos están en /opt/data/icloud_calendars.txt, una línea por calendario:
    Nombre | webcal://...
El enlace no se escribe nunca en la salida: es como una llave.

Uso: leer_icloud.py [--desde AAAA-MM-DD | hoy | mañana] [--dias N]
     Por defecto, desde hoy, 2 días (hoy y mañana). Horas en Europe/Madrid.
Solo usa la biblioteca de serie de Python. Escrito en el Mac (proyecto Hermes, D-27); no se edita en el servidor.
"""
import os
import sys
import urllib.request
from datetime import date, datetime, time, timedelta, timezone

try:
    from zoneinfo import ZoneInfo
    MADRID = ZoneInfo("Europe/Madrid")
except Exception:  # sin tzdata: hora fija de invierno, y se avisa
    MADRID = timezone(timedelta(hours=1))
    print("Aviso: sin zona horaria completa; las horas pueden ir una hora mal en verano.")

ENLACES = os.environ.get("ICLOUD_ENLACES", "/opt/data/icloud_calendars.txt")  # otra ruta, solo para probar
DIAS = ["lun", "mar", "mié", "jue", "vie", "sáb", "dom"]
MESES = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]
SEMANA = {"MO": 0, "TU": 1, "WE": 2, "TH": 3, "FR": 4, "SA": 5, "SU": 6}
TOPE = 5000  # repeticiones como mucho por evento


def zona(nombre):
    try:
        return ZoneInfo(nombre)
    except Exception:
        return MADRID


def leer_enlaces():
    calendarios = []
    with open(ENLACES, encoding="utf-8") as f:
        for linea in f:
            if "|" in linea and not linea.strip().startswith("#"):
                nombre, enlace = (t.strip() for t in linea.split("|", 1))
                if enlace.startswith("webcal://"):
                    enlace = "https://" + enlace[len("webcal://"):]
                calendarios.append((nombre, enlace))
    return calendarios


def descargar(enlace):
    pedido = urllib.request.Request(enlace, headers={"User-Agent": "calendario-icloud/1"})
    with urllib.request.urlopen(pedido, timeout=30) as r:
        return r.read().decode("utf-8", "replace")


def lineas(texto):
    """Junta las líneas partidas del formato iCalendar."""
    salida = []
    for l in texto.replace("\r\n", "\n").split("\n"):
        if l[:1] in (" ", "\t") and salida:
            salida[-1] += l[1:]
        elif l:
            salida.append(l)
    return salida


def partir(linea):
    """'DTSTART;TZID=Europe/Madrid:2026...' -> ('DTSTART', {'TZID': ...}, '2026...')"""
    cabeza, _, valor = linea.partition(":")
    trozos = cabeza.split(";")
    params = dict(t.split("=", 1) for t in trozos[1:] if "=" in t)
    return trozos[0].upper(), params, valor


def fecha(valor, params):
    """Devuelve (momento, todo_el_dia). momento: date o datetime con zona."""
    valor = valor.strip()
    if params.get("VALUE") == "DATE" or len(valor) == 8:
        return date(int(valor[:4]), int(valor[4:6]), int(valor[6:8])), True
    d = datetime.strptime(valor[:15], "%Y%m%dT%H%M%S")
    if valor.endswith("Z"):
        return d.replace(tzinfo=timezone.utc), False
    return d.replace(tzinfo=zona(params.get("TZID", "Europe/Madrid"))), False


def texto(v):
    return v.replace("\\n", " ").replace("\\,", ",").replace("\\;", ";").replace("\\\\", "\\").strip()


def eventos(ics):
    actual, todos = None, []
    for l in lineas(ics):
        clave, params, valor = partir(l)
        if l == "BEGIN:VEVENT":
            actual = {"exdate": []}
        elif l == "END:VEVENT" and actual is not None:
            if "inicio" in actual:
                todos.append(actual)
            actual = None
        elif actual is None:
            continue
        elif clave == "DTSTART":
            actual["inicio"], actual["dia_entero"] = fecha(valor, params)
        elif clave == "DTEND":
            actual["fin"] = fecha(valor, params)[0]
        elif clave == "DURATION":
            actual["duracion"] = duracion(valor)
        elif clave == "SUMMARY":
            actual["titulo"] = texto(valor)
        elif clave == "LOCATION":
            actual["lugar"] = texto(valor)
        elif clave == "UID":
            actual["uid"] = valor
        elif clave == "STATUS":
            actual["estado"] = valor.upper()
        elif clave == "RRULE":
            actual["regla"] = dict(t.split("=", 1) for t in valor.split(";") if "=" in t)
        elif clave == "EXDATE":
            actual["exdate"] += [fecha(v, params)[0] for v in valor.split(",") if v]
        elif clave == "RECURRENCE-ID":
            actual["recurrence_id"] = fecha(valor, params)[0]
    return todos


def duracion(v):
    signo, v = (-1, v[1:]) if v.startswith("-") else (1, v.lstrip("+"))
    v = v[1:]  # quita la P
    total, numero, en_hora = timedelta(), "", False
    for c in v:
        if c.isdigit():
            numero += c
        elif c == "T":
            en_hora = True
        else:
            n = int(numero or 0)
            numero = ""
            total += {"W": timedelta(weeks=n), "D": timedelta(days=n), "H": timedelta(hours=n),
                      "M": timedelta(minutes=n) if en_hora else timedelta(days=30 * n),
                      "S": timedelta(seconds=n)}.get(c, timedelta())
    return signo * total


def clave_tiempo(m):
    """Para comparar fechas sueltas, con o sin hora."""
    if isinstance(m, datetime):
        return m.astimezone(timezone.utc).replace(tzinfo=None)
    return datetime.combine(m, time())


def en_local(m, zona_original):
    """Una repetición calculada en hora de pared, con su zona (respeta el cambio de hora)."""
    if isinstance(m, datetime) and zona_original is not None:
        return m.replace(tzinfo=zona_original)
    return m


def repeticiones(ev, hasta):
    """Los inicios de cada repetición, hasta 'hasta' (datetime en UTC sin zona). None si la regla no se entiende."""
    inicio, regla = ev["inicio"], ev.get("regla")
    if not regla:
        return [inicio]
    zona_original = inicio.tzinfo if isinstance(inicio, datetime) else None
    base = inicio.replace(tzinfo=None) if isinstance(inicio, datetime) else inicio
    frec = regla.get("FREQ")
    paso = int(regla.get("INTERVAL", "1"))
    cuantas = int(regla["COUNT"]) if "COUNT" in regla else None
    limite = hasta
    if "UNTIL" in regla:
        u = fecha(regla["UNTIL"], {})[0]
        limite = min(limite, clave_tiempo(u) + (timedelta(days=1) if not isinstance(u, datetime) else timedelta()))
    byday = regla.get("BYDAY", "")
    salida, vueltas = [], 0

    def candidatos(i):
        if frec == "DAILY":
            return [base + timedelta(days=i * paso)]
        if frec == "WEEKLY":
            lunes = base - timedelta(days=base.weekday()) + timedelta(weeks=i * paso)
            dias = sorted(SEMANA[d[-2:]] for d in byday.split(",") if d) if byday else [base.weekday()]
            return [lunes + timedelta(days=d) for d in dias]
        if frec in ("MONTHLY", "YEARLY"):
            meses = i * paso * (12 if frec == "YEARLY" else 1)
            a, m = divmod(base.month - 1 + meses, 12)
            a, m = base.year + a, m + 1
            if frec == "MONTHLY" and byday:
                return [d for d in (dia_ordinal(a, m, t, base) for t in byday.split(",")) if d]
            try:
                return [base.replace(year=a, month=m)]
            except ValueError:  # 31 en un mes de 30, o 29 de febrero
                return []
        return None

    i = 0
    while vueltas < TOPE:
        grupo = candidatos(i)
        if grupo is None:
            return None
        for c in grupo:
            if c < base:
                continue
            m = en_local(c, zona_original)
            if clave_tiempo(m) >= limite:
                return salida
            salida.append(m)
            if cuantas is not None and len(salida) >= cuantas:
                return salida
        i += 1
        vueltas += 1
    return salida


def dia_ordinal(a, m, t, base):
    """'1MO' = primer lunes del mes; '-1FR' = último viernes."""
    n, dia = (int(t[:-2]) if t[:-2] not in ("", "+") else 0), SEMANA[t[-2:]]
    primero = date(a, m, 1)
    ultimo = (date(a + m // 12, m % 12 + 1, 1) - timedelta(days=1))
    if n >= 0:
        d = primero + timedelta(days=(dia - primero.weekday()) % 7 + 7 * (max(n, 1) - 1))
    else:
        d = ultimo - timedelta(days=(ultimo.weekday() - dia) % 7 + 7 * (-n - 1))
    if d.month != m:
        return None
    return datetime.combine(d, base.time()) if isinstance(base, datetime) else d


def principio_y_fin(argumentos):
    dias = 2
    hoy = datetime.now(MADRID).date()
    desde = hoy
    if "--desde" in argumentos:
        v = argumentos[argumentos.index("--desde") + 1]
        desde = {"hoy": hoy, "mañana": hoy + timedelta(days=1), "manana": hoy + timedelta(days=1)}.get(v) \
            or date.fromisoformat(v)
    if "--dias" in argumentos:
        dias = int(argumentos[argumentos.index("--dias") + 1])
    return desde, desde + timedelta(days=dias)


def main():
    desde, hasta = principio_y_fin(sys.argv[1:])
    ventana_ini = clave_tiempo(datetime.combine(desde, time(), MADRID))
    ventana_fin = clave_tiempo(datetime.combine(hasta, time(), MADRID))
    encontrados, avisos = [], []

    try:
        calendarios = leer_enlaces()
    except OSError as e:
        print(f"No puedo leer {ENLACES}: {e.strerror}.")
        sys.exit(1)

    for nombre, enlace in calendarios:
        try:
            todos = eventos(descargar(enlace))
        except Exception as e:  # sin decir el enlace
            avisos.append(f"«{nombre}»: no se pudo descargar ({type(e).__name__}).")
            continue
        cambiados = {(e.get("uid"), clave_tiempo(e["recurrence_id"])) for e in todos if "recurrence_id" in e}
        for ev in todos:
            if ev.get("estado") == "CANCELLED":
                continue
            inicio = ev["inicio"]
            fin = ev.get("fin")
            largo = (clave_tiempo(fin) - clave_tiempo(inicio)) if fin else ev.get(
                "duracion", timedelta(days=1) if ev["dia_entero"] else timedelta())
            if "recurrence_id" in ev:
                lista = [inicio]
            else:
                lista = repeticiones(ev, ventana_fin)
                if lista is None:
                    avisos.append(f"«{ev.get('titulo', '(sin título)')}» se repite con una regla que no sé leer.")
                    lista = [inicio]
            quitadas = {clave_tiempo(x) for x in ev["exdate"]}
            for m in lista:
                k = clave_tiempo(m)
                if k in quitadas or ("recurrence_id" not in ev and (ev.get("uid"), k) in cambiados and ev.get("regla")):
                    continue
                if ev["dia_entero"]:
                    dentro = m < hasta and m + max(largo, timedelta(days=1)) > desde
                else:
                    dentro = k < ventana_fin and (k + largo > ventana_ini or (not largo and k >= ventana_ini))
                if dentro:
                    encontrados.append((m, largo, ev, nombre))

    def orden(x):
        m = x[0]
        return (clave_tiempo(m.astimezone(MADRID).replace(tzinfo=None) if isinstance(m, datetime) else
                             datetime.combine(m, time())), not x[2]["dia_entero"])

    print(f"iCloud, del {desde:%d/%m} al {hasta - timedelta(days=1):%d/%m} "
          f"({len(calendarios)} calendario{'s' if len(calendarios) != 1 else ''}):")
    dia_actual = None
    for m, largo, ev, cal in sorted(encontrados, key=orden):
        if ev["dia_entero"]:
            dia = max(m, desde)
            hora = "todo el día"
        else:
            local = m.astimezone(MADRID)
            dia = local.date()
            fin = (m + largo).astimezone(MADRID)
            hora = f"{local:%H:%M}–{fin:%H:%M}" if largo else f"{local:%H:%M}"
        if dia != dia_actual:
            print(f"\n{DIAS[dia.weekday()]} {dia.day} {MESES[dia.month - 1]}")
            dia_actual = dia
        lugar = f" · {ev['lugar']}" if ev.get("lugar") else ""
        print(f"  {hora} · {ev.get('titulo', '(sin título)')}{lugar} [{cal}]")
    if not encontrados:
        print("  Nada en esos días.")
    for a in avisos:
        print("Aviso:", a)


if __name__ == "__main__":
    main()
