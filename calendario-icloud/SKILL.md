---
name: calendario-icloud
description: Leer los calendarios de iCloud de Aleix (solo lectura) para saber qué tiene un día o unos días. Usar siempre que pregunte qué tiene hoy, mañana, esta semana o un día concreto, si tiene hueco, o antes de proponerle una hora; junto con los calendarios de Google (skill google-workspace), que son los otros. NO sirve para apuntar nada: iCloud solo se lee.
---

# Calendario de iCloud (solo lectura)

Sus calendarios propios (eventos, citas) viven en iCloud; los de Google son los que llegan solos (Meet, Núcleo, festivos) y «Hermes». Para saber qué tiene Aleix, **mira los dos**: este y Google.

## Cómo se lee

```
python3 /opt/data/skills-aleix/calendario-icloud/leer_icloud.py --desde mañana --dias 1
```

- `--desde`: `hoy`, `mañana` o una fecha `AAAA-MM-DD`. Por defecto, hoy.
- `--dias`: cuántos días, contando el primero. Por defecto, 2 (hoy y mañana).
- Las horas salen en hora de Madrid; cada evento lleva entre corchetes de qué calendario viene.

## Lo que hay que saber

- Los enlaces de cada calendario están en `/opt/data/icloud_calendars.txt`. **Son como una llave:** no los enseñes, no los copies en la respuesta ni en tu memoria.
- Hoy solo está «Eventos, citas y recordatorios». Sus bloques de tiempo no están: si te pregunta por ellos, díselo.
- iCloud publica estos enlaces con retraso (puede ser de horas): si algo lo acaba de crear, puede no salir todavía. Dilo cuando importe.
- Si sale un «Aviso», cuéntaselo: un calendario que no se pudo descargar o un evento que se repite de una forma que el programa no entiende (entonces sale solo su primera vez).
- iCloud no se escribe nunca. Para apuntar algo, el calendario «Hermes» de Google, con su OK (reglas en tu SOUL.md).

Original en el Mac de Aleix (proyecto Hermes, `02_Material-interno/puente/skills-solo-hermes/`): no la edites aquí, se pisa cada hora.
