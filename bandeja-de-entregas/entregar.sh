#!/bin/sh
# Bandeja de entregas (D-31 de Hermes): deja un archivo para Aleix.
# Lo guarda en /opt/data/bandeja y lo sube al almacén privado Aleix003/hermes-bandeja;
# el reloj del Mac lo copia a su Inbox de iCloud en menos de una hora.
# Uso: sh entregar.sh /ruta/al/archivo ["nombre final.md"]
# Original en el Mac (proyecto Hermes, puente/skills-solo-hermes/): no lo edites aquí, se pisa cada hora.
BANDEJA=/opt/data/bandeja
MAX=10485760   # 10 MB

origen="$1"
[ -n "$origen" ] && [ -f "$origen" ] || { echo "ERROR: no existe el archivo «$origen»."; exit 1; }
case "$origen" in /*) ;; *) origen="$PWD/$origen" ;; esac
[ "$(wc -c < "$origen")" -le "$MAX" ] || { echo "ERROR: pesa más de 10 MB; no se entrega."; exit 1; }

nombre="${2:-$(basename "$origen")}"
nombre=$(printf '%s' "$nombre" | tr '/\\:' '---' | sed 's/^[.]*//')
[ -n "$nombre" ] || { echo "ERROR: el nombre quedó vacío."; exit 1; }

cd "$BANDEJA" 2>/dev/null || { echo "ERROR: no encuentro $BANDEJA."; exit 1; }
mkdir -p entregas
destino="entregas/$(date +%Y-%m-%d_%H%M) $nombre"
[ -e "$destino" ] && destino="entregas/$(date +%Y-%m-%d_%H%M%S) $nombre"
cp "$origen" "$destino" || { echo "ERROR: no pude copiar el archivo."; exit 1; }

git add -- "$destino" &&
  git -c user.name=Hermes -c user.email=hermes@localhost commit -q -m "Entrega: $nombre" ||
  { echo "ERROR: no pude guardarlo en la bandeja."; exit 1; }

# Sube todo lo pendiente (también una entrega anterior que no llegó a subir).
if salida=$(git push -q origin HEAD:main 2>&1); then
  echo "OK: entregado «$(basename "$destino")». Llega al Inbox del Mac en menos de una hora, si el Mac está encendido."
else
  echo "AVISO: guardado en el servidor pero no subido ($salida). Se subirá con la próxima entrega."
  exit 2
fi
