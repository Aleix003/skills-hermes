---
name: "arquitecto-de-prompts"
description: "Redactar el prompt óptimo para pedirle algo a una IA (Claude, Codex, ChatGPT). Usar siempre que Aleix diga «redáctame el prompt», «prepárame el prompt», «arquitecto de prompts», «quiero pedirle a la IA…», «cómo le pido esto a la IA», o pase un prompt en borrador para mejorarlo. Entrega: prompt listo para pegar + modelo y esfuerzo recomendados + avisos de su biblioteca, su conocimiento y sus skills instaladas."
---

# Arquitecto de prompts

Convierte una petición dictada en bruto en un prompt excelente, listo para pegar en la IA de destino, con recomendación de modelo y esfuerzo. Regla de oro: **nunca dos verdades** — esta skill contiene solo el proceso; el contenido de Aleix (sus prompts guardados, su conocimiento, sus skills) se lee EN VIVO en cada uso, jamás se copia aquí.

## Requisito

Necesita conectadas la carpeta del vault de Obsidian, «Mi Cerebro Digital v3», y la de Productividad (`02_Areas_de_responsabilidad/07_Entorno_y_sistema_de_vida/Productividad`), donde vive la Biblioteca. Si no lo están, dilo en una línea y redacta el prompt sin las consultas 2a y 2b — nunca falles en silencio.

## Proceso

### 1 · Extraer

Del dictado en bruto, identifica: objetivo real · entregable esperado · contexto disponible · restricciones. Aplica sus instrucciones generales (reglas 5 y 6): asume lo ambiguo y dilo en 2-3 líneas; haz UNA pregunta como máximo, y solo si falta un dato que haga el prompt inutilizable.

### 2 · Consultar en vivo (buscar, no leer)

a. **Biblioteca**: la nota `APOYO_INFO - Biblioteca de promps`, en Productividad (no está en el vault). **Búscala por su nombre, no por su ruta** — las carpetas se mueven, los nombres no. ¿Hay un prompt guardado que sirva de base? Úsalo y di cuál. Respeta su sección «Descartados y por qué»: lo descartado no se resucita.

b. **Conocimiento**: búsqueda por palabras clave del tema en la carpeta `Wiki` del vault: `Mi pensamiento`, `Procedimientos`, `Conceptos`, `Resúmenes` y `Respuestas`. Solo abre una nota si la búsqueda la señala. Si no hay nada, dilo en media línea y sigue.

c. **Skills instaladas**: solo si el destino es Claude Code, Codex o la app de Claude — revisa la lista de skills disponibles de la sesión y localiza las aplicables al encargo.

### 3 · Redactar el prompt

Estructura completa, en este orden:

- **Rol(es)**: 1-2 roles con detalle concreto — números y prohibiciones explícitas (estilo «propietario de 1 a 3 alojamientos… no eres experto en tecnicismos»), nunca roles genéricos. El patrón de referencia es el prompt de simulación de buyer persona de su Biblioteca.
- **Contexto**: lo extraído en el paso 1 más lo hallado en el paso 2. Si hay nota de conocimiento relevante, el prompt debe decir: «parte de [nombre exacto de la nota], pero no te limites a ella: úsala y expándela».
- **Encargo**: qué hacer, en imperativo, sin ambigüedad.
- **Formato de salida**: qué devuelve y cómo (estructura, longitud, idioma).
- **Criterios y restricciones**: qué hace válida la respuesta, qué evitar.

No dupliques reglas que ya traen sus instrucciones generales: las cargan Claude Code y Codex, y su versión corta va en las cajas de la app de Claude y de ChatGPT.

### 4 · Recomendar destino

En 3 líneas:

- **Modelo y esfuerzo**: pequeño/rápido para tareas mecánicas y formateo · medio para redacción y análisis estándar · grande para razonamiento profundo, estrategia o mucho contexto — y si conviene el pensamiento extendido.
- **Superficie**: chat de la app de Claude · Claude Code o Codex, abiertos en su carpeta, si toca archivos · ChatGPT para exploración rápida.
- **Skill aplicable**, si el destino es Claude Code, Codex o la app de Claude y la hay.

### 5 · Entregar

- El prompt final en un bloque de código, listo para copiar.
- La recomendación del paso 4.
- Avisos: prompt de Biblioteca usado · notas de conocimiento detectadas (nombre exacto) · skill aplicable.
- Si el prompt resultante es bueno y previsiblemente repetible, propón en una línea guardarlo en la Biblioteca (en su sección temática, como callout de cita igual que los existentes). **Solo escribes en la nota tras el sí explícito de Aleix.**

## Qué NO hace

- No escribe en el vault. Fuera de él, solo tras el sí explícito: añadir el prompt aprobado a la Biblioteca.
- No inventa conocimiento de Aleix: si la búsqueda no da resultados, se dice.
- No re-lista las reglas de sus instrucciones generales en prompts para una IA que ya las carga.

