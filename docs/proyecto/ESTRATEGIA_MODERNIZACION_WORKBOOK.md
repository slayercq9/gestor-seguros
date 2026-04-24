# Estrategia Modernizacion Workbook

## Objetivo

Definir una estrategia de modernizacion gradual del workbook operativo sin eliminarlo, sin volverlo incompatible con el trabajo manual y sin asumir todavia que la app reemplazara su uso diario.

## Principio de trabajo

El workbook:

- se conserva como herramienta operativa vigente;
- no se elimina ni se reemplaza de golpe;
- puede modernizarse por pasos pequenos, reversibles y verificables;
- debe seguir siendo usable por operacion aun cuando la app empiece a leer su estructura.

## Lo que se conserva desde ya

- columnas originales y su semantica operativa;
- utilidad manual del archivo;
- flujo de trabajo actual mientras no exista reemplazo aprobado;
- capacidad de revision humana sobre los registros.

## Lo que puede mejorarse mas adelante

- orden y consistencia visual de hojas de trabajo;
- separacion mas clara entre columnas originales, auxiliares y de control;
- validaciones de captura externas o no intrusivas;
- exportaciones mejor alineadas con el formato mejorado;
- sincronizacion controlada con la app cuando exista trazabilidad aprobada.

## Lo que no debe hacerse aun

- renombrar columnas originales por criterio tecnico;
- imponer un formato nuevo obligatorio al workbook actual;
- mover la operacion al dataset canonico antes de validar el diseno;
- introducir formulas, hojas auxiliares o automatizaciones dentro del archivo real sin fase especifica;
- asumir que el workbook desaparecera pronto.

## Etapas recomendadas

### 1. Convivencia documental

- El workbook sigue igual.
- La app futura solo entiende su estructura y mapeo.

### 2. Capa de lectura controlada

- La app futura podra leer y normalizar sin alterar el workbook.
- Los hallazgos se documentaran por fuera del archivo original.

### 3. Mejoras auxiliares no intrusivas

- auditorias locales;
- reportes de integridad fuera del archivo;
- validaciones previas a importacion;
- catalogos o controles documentados fuera del workbook.

### 4. Automatizacion parcial opcional

Solo cuando existan reglas cerradas y aprobadas:

- hojas auxiliares o plantillas nuevas fuera del archivo operativo principal;
- controles de integridad reproducibles;
- consolidaciones verificables;
- salidas complementarias sin romper operacion manual.

### 5. Revision de autoridad operativa

Mas adelante se evaluara si alguna parte del dataset canonico pasa a ser fuente principal de trabajo. Esa decision no pertenece a `1.4.0`.

## Criterios de compatibilidad manual

Cualquier modernizacion futura debera cumplir:

- no bloquear el flujo manual actual;
- ser reversible;
- ser comprensible por operacion;
- no ocultar informacion original;
- no degradar trazabilidad;
- no depender de supuestos no validados sobre columnas ambiguas.

## Convivencia con la app

- la app trabajara con un modelo interno mas consistente que el layout visual del workbook;
- el workbook podra seguir usandose para trabajo manual y como respaldo;
- la lectura desde la app no debe requerir rediseñar primero el archivo real;
- las futuras exportaciones deberan ser comprensibles para operacion y alinearse al formato mejorado.

## Estrategia de respaldo y transicion

- mantener el workbook operativo como respaldo vigente durante las primeras fases tecnicas;
- evitar cualquier cambio que impida volver al flujo manual existente;
- introducir mejoras por etapas pequenas y verificables;
- documentar antes de implementar cualquier sincronizacion o exportacion bidireccional.

## Recomendaciones para futuras exportaciones y sincronizacion

- exportar con estructura coherente con el dataset canonico, pero sin perder referencias al origen;
- preservar columnas originales cuando sean necesarias para trazabilidad o validacion humana;
- separar claramente datos originales, normalizados y operativos en cualquier formato mejorado;
- no automatizar escritura sobre el workbook real hasta que exista una politica aprobada de autoridad y respaldo.

## Riesgos de modernizacion prematura

- romper la forma de trabajo operativa antes de tener reemplazo;
- mezclar datos normalizados con datos originales dentro del mismo archivo;
- introducir reglas rigidas sobre campos aun ambiguos;
- reducir confianza del usuario sobre el control manual del proceso.

## Resultado esperado de esta fase

Dejar definida la ruta de convivencia y modernizacion, sin cambios funcionales sobre el workbook ni automatizacion intrusiva.
