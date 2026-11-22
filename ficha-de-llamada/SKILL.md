---
name: "ficha-de-llamada"
description: "Convertir la transcripción de una llamada de venta de Aleix en su ficha de llamada: siete campos, formato idéntico siempre, para poder comparar la llamada 3 con la 17. Usar cuando pegue o señale una transcripción de una llamada con un cliente o candidato, o diga «hazme la ficha de la llamada», «analiza cómo fue la llamada con X», «revisa esta llamada», «qué hice mal en esta llamada», «saca las objeciones de esto». También al cerrar una sesión de cliente en la que hubo llamada grabada. NO usar para preparar la llamada antes (eso es el Estratega de negocio), ni para redactar el mensaje de seguimiento (skill comunicador), ni para convertir la ficha en conocimiento del vault (skill pasos-del-vault)."
---

# Ficha de llamada

Convierte la transcripción de una llamada de venta en una ficha de **siete campos, siempre los mismos, siempre en el mismo orden**.

## La regla dura, y es la única que no se negocia

**El valor no está en la profundidad: está en que sea idéntica.** Solo así se puede comparar la llamada 3 con la 17. Una ficha más completa que las anteriores rompe la serie y vale menos que una mediocre pero igual.

Por eso: **no se añaden campos, no se quitan, no se reordenan.** Si un campo no aplica, se escribe «no aplica» y se dice por qué. Si algo importante no cabe en ninguno de los siete, va al campo 7 como nota — no se inventa un campo octavo.

## Antes de empezar

1. **La transcripción manda sobre el recuerdo.** Si Aleix dice «yo creo que dije X» y la transcripción dice Y, gana la transcripción, y se señala la diferencia: esa brecha es de las cosas más útiles que da esta ficha.
2. **Se hace en caliente**, dentro de los 30 minutos siguientes si se puede. Una ficha de tres días después ya está contada, no observada.
3. **Cita literal siempre que se pueda.** Un campo con una cita vale diez veces uno con una paráfrasis.

## Los siete campos

**1 · Qué vendías y a quién.** Una línea. El servicio concreto y quién era el interlocutor —nombre, rol, y si venía frío, referido o de agenda.

**2 · El minuto exacto donde se torció, con la cita literal.** No «se enfrió a la mitad». El momento, y lo que se dijo. Si la llamada fue bien, el campo dice dónde estuvo el punto de riesgo que no llegó a romper.

**3 · La objeción declarada frente a la objeción real.** Casi nunca coinciden: «es caro» suele ser «no veo que esto me lo resuelva». Las dos, en su columna, y la razón por la que crees que la real es la real — con lo que dijo, no con lo que intuyes.

**4 · Cuánto hablaste tú frente a cuánto preguntaste.** Sale de la transcripción: porcentaje aproximado de palabras suyas, y número de preguntas abiertas que hizo él. Dos números, sin adornos.

**5 · La frase que deberías haber dicho ahí.** Una, en el punto del campo 2. Escrita como se diría en voz alta, no como se escribiría en un correo.

**6 · La calidad de tus preguntas.** Cuántas fueron abiertas, cuántas cerradas, cuántas sugerían la respuesta. Y la mejor pregunta de la llamada, literal — para poder repetirla.

**7 · Un solo cambio para la siguiente llamada. UNO.** Si salen tres, se eligen por cuál habría cambiado más el resultado de ESTA llamada. Los otros dos no se apuntan: volverán solos si importan.

## Y un octavo campo que se rellena después

**· Qué pasó.** Se deja vacío al cerrar la ficha y se rellena cuando se sepa: ¿hubo segunda llamada? ¿compromiso con fecha? ¿silencio?

**No es opcional y es el campo que hace que todo lo demás sirva.** Sin él, el manual de objeciones sabrá qué objeciones aparecen pero nunca **qué respuesta funcionó**. Es el bucle de siempre —qué se esperaba · cuándo se mira · qué pasó—: sin la última columna no se sabe qué funcionó, solo qué se dijo.

Se rellena **en la propia ficha**, con su fecha delante. Es la única edición permitida sobre una ficha cerrada.

## El número

Uno solo, y es binario: **¿salí de la llamada con un compromiso con fecha?** Sí o no. Se ve en una sola llamada y no necesita muestra.

El **ratio de habla** del campo 4 se apunta igualmente porque sale gratis de la transcripción, pero es el segundo número: es un porcentaje y necesita muchas llamadas para significar algo. Cuando haya quince fichas, se mira.

## Dónde se guarda

Junto a su materia prima, nunca en carpeta nueva: en la carpeta del cliente, que vive en la carpeta de clientes del proyecto con el que se trabaja con él (en `01_Proyectos/`), dentro de su subcarpeta de grabaciones o reuniones y transcripciones.

```
<Proyecto>/<carpeta de clientes>/<Nombre>/Grabaciones y transcripciones/
    AAAA-MM-DD_Ficha-llamada_<Nombre>.md
```

Si el cliente no tiene esa subcarpeta, se crea con ese nombre. Si la llamada no es de un cliente con carpeta —un candidato, un contacto de agenda—, se le crea la suya, con su nombre real, en la carpeta de clientes del proyecto por el que llamaste.

## Qué alimenta después, y no lo hace esta skill

- **El manual de objeciones.** Cuando **la misma objeción aparece tres veces** en fichas distintas, es método y toca destilarla. Tres, no quince: es el umbral que ya usa el resto del sistema. La nota la produce la skill `pasos-del-vault` — aquí solo se avisa de que el umbral se ha cumplido.
- **El sparring antes de la siguiente llamada.** Lo hace el Estratega de negocio, con las fichas delante. El valor está en que las objeciones sean las que le tumbaron a él, no las de un manual.
- **El `REGISTRO DE HABILIDADES`.** Si la ficha deja un hecho observable y citable sobre «conversación de venta en vivo», se apunta una línea allí por la regla 17 de sus instrucciones generales. Sin narrarlo y sin comentárselo.

## El aviso honesto, y va dentro de cada ficha

**Una transcripción lee palabras, no la sala.** No sabe si sonó inseguro, si interrumpió, ni si aquel silencio de doce segundos era el bueno. La ficha es un primer diagnóstico muy superior a no tener ninguno — no un veredicto.

Por eso cada ficha cierra con una línea: *«Esto sale de la transcripción. Si el resultado te sorprende, escucha el audio de los minutos X-Y.»* Y en las tres o cuatro llamadas en las que la ficha y su recuerdo no coincidan, que escuche.

## Al terminar

Entregar la ficha completa, decir dónde se ha guardado, y **una sola frase** con el cambio del campo 7. Nada de resumen de la llamada: para eso está la transcripción.

Si es la tercera ficha o más, decir además si alguna objeción ya va por su tercera aparición.

