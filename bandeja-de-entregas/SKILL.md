---
name: bandeja-de-entregas
description: Dejarle a Aleix un archivo en su Mac: lo que dejes en la bandeja aparece solo, en menos de una hora, en su Inbox de iCloud. Usar cuando diga «déjamelo en la bandeja», «pásamelo al Mac», «mándamelo al Inbox», «prepárame el documento y déjalo en el ordenador» o algo equivalente, o cuando te encargue un texto largo (un borrador, una lista, un resumen) que vaya a trabajar en el Mac. NO sirve para guardar en el vault, en sus apps ni en sus carpetas: llega a su Inbox y él lo coloca.
---

# Bandeja de entregas

Es tu única forma de dejarle un archivo a Aleix. Llega a la carpeta «Icoud Inbox» de su escritorio, y él lo procesa en su Cierre del día.

## Cómo se entrega

1. Escribe el archivo en `/tmp/` (por ejemplo `/tmp/borrador-propuesta.md`). Mejor en Markdown (`.md`); otro formato, solo si te lo pide.
2. Entrégalo:
   ```
   sh /opt/data/skills-aleix/bandeja-de-entregas/entregar.sh /tmp/borrador-propuesta.md "Borrador propuesta Rais.md"
   ```
   El segundo dato es el nombre con el que le llega; si no lo pones, se queda el del archivo. Delante se le añade la fecha y la hora.
3. Lee lo que contesta y díselo:
   - `OK`: entregado; llega en menos de una hora si su Mac está encendido.
   - `AVISO`: se guardó pero no subió; dile que llegará con la próxima entrega.
   - `ERROR`: no se entregó; dile por qué.

## Lo que no se hace

- Entregas solo lo que él te pide o lo que es claramente el resultado de su encargo; nada por tu cuenta.
- Nunca entregues llaves, contraseñas, los enlaces de sus calendarios ni el contenido de `/opt/data/ssh` o de los archivos de configuración.
- No uses órdenes de git a mano en `/opt/data/bandeja`: solo este programa.
- Lo que entregas no se puede deshacer desde aquí: si te equivocas, díselo y él lo descarta en su Inbox.

Original en el Mac de Aleix (proyecto Hermes, `02_Material-interno/puente/skills-solo-hermes/`): no la edites aquí, se pisa cada hora.
