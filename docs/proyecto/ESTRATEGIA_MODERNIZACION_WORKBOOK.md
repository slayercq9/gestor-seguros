# Estrategia Modernizacion Workbook

## Objetivo

Definir una estrategia de modernización gradual del workbook operativo sin eliminarlo, sin volverlo incompatible con el trabajo manual y sin asumir todavía que la app reemplazara su uso diario.

## Principio de trabajo

El workbook:

- se conserva como herramienta operativa vigente;
- no se elimina ni se reemplaza de golpe;
- puede modernizarse por pasos pequeños, reversibles y verificables;
- debe seguir siendo usable por operación aún cuando la app empiece a leer su estructura.

## Lo que se conserva desde ya

- columnas originales y su semantica operativa;
- utilidad manual del archivo;
- flujo de trabajo actual mientras no exista reemplazo aprobado;
- capacidad de revisión humana sobre los registros.

## Lo que puede mejorarse más adelante

- orden y consistencia visual de hojas de trabajo;
- separacion más clara entre columnas originales, auxiliares y de control;
- validaciones de captura externas o no intrusivas;
- exportaciones mejor alineadas con el formato mejorado;
- sincronizacion controlada con la app cuando exista trazabilidad aprobada.

## Lo que no debe hacerse aún

- renombrar columnas originales por criterio técnico;
- imponer un formato nuevo obligatorio al workbook actual;
- mover la operación al dataset canónico antes de validar el diseño;
- introducir formulas, hojas auxiliares o automatizaciones dentro del archivo real sin fase especifica;
- asumir que el workbook desaparecera pronto.

## Etapas recomendadas

### 1. Convivencia documental

- El workbook sigue igual.
- La app futura solo entiende su estructura y mapeo.

### 2. Capa de lectura controlada

- La app futura podrá leer y normalizar sin alterar el workbook.
- Los hallazgos se documentaran por fuera del archivo original.

### 3. Mejoras auxiliares no intrusivas

- auditorias locales;
- reportes de integridad fuera del archivo;
- validaciones previas a importación;
- catalogos o controles documentados fuera del workbook.

### 4. Automatizacion parcial opcional

Solo cuando existan reglas cerradas y aprobadas:

- hojas auxiliares o plantillas nuevas fuera del archivo operativo principal;
- controles de integridad reproducibles;
- consolidaciónes verificables;
- salidas complementarias sin romper operación manual.

### 5. Revisión de autoridad operativa

Más adelante se evaluará si alguna parte del dataset canónico pasa a ser fuente principal de trabajo. Esa decision no pertenece a `1.4.0`.

## Criterios de compatibilidad manual

Cualquier modernización futura deberá cumplir:

- no bloquear el flujo manual actual;
- ser reversible;
- ser comprensible por operación;
- no ocultar información original;
- no degradar trazabilidad;
- no depender de supuestos no validados sobre columnas ambiguas.

## Convivencia con la app

- la app trabajará con un modelo interno más consistente que el layout visual del workbook;
- el workbook podrá seguir usandose para trabajo manual y como respaldo;
- la lectura desde la app no debe requerir rediseñar primero el archivo real;
- las futuras exportaciones deberán ser comprensibles para operación y alinearse al formato mejorado.

## Estrategia de respaldo y transicion

- mantener el workbook operativo como respaldo vigente durante las primeras fases técnicas;
- evitar cualquier cambio que impida volver al flujo manual existente;
- introducir mejoras por etapas pequeñas y verificables;
- documentar antes de implementar cualquier sincronizacion o exportacion bidireccional.

## Recomendaciones para futuras exportaciones y sincronizacion

- exportar con estructura coherente con el dataset canónico, pero sin perder referencias al origen;
- preservar columnas originales cuando sean necesarias para trazabilidad o validación humana;
- separar claramente datos originales, normalizados y operativos en cualquier formato mejorado;
- no automatizar escritura sobre el workbook real hasta que exista una política aprobada de autoridad y respaldo.

## Riesgos de modernización prematura

- romper la forma de trabajo operativa antes de tener reemplazo;
- mezclar datos normalizados con datos originales dentro del mismo archivo;
- introducir reglas rigidas sobre campos aún ambiguos;
- reducir confianza del usuario sobre el control manual del proceso.

## Resultado esperado de esta fase

Dejar definida la ruta de convivencia y modernización, sin cambios funcionales sobre el workbook ni automatización intrusiva.

## Modernizacion local controlada

El flujo de modernización local queda retirado como dependencia activa desde `1.8.2`. La app lee directamente el Control Cartera operativo en `data/input/CONTROLCARTERA_V2.xlsx` y no necesita una copia en `data/output/workbook_modernizado/` para visualizar registros.

Las validaciones futuras deberán ejecutarse como reglas internas de la aplicación. No deben agregarse columnas técnicas al Excel operativo para sostener la visualización.

## Limpieza controlada del workbook operativo

La fase `1.6.1` permite una limpieza puntual del workbook operativo real: eliminar la hoja obsoleta `Reporte de vencimientos del mes`.

La decision se documenta como mantenimiento controlado porque:

- la hoja no funciona correctamente;
- la generación de vencimientos mensuales será implementada luego dentro del sistema;
- el workbook seguirá siendo herramienta manual y respaldo operativo;
- antes de modificar el archivo real se genera un respaldo local automático.

La limpieza no autoriza cambios adicionales sobre clientes, pólizas, identificaciones, placas, teléfonos, datos operativos ni estructura principal de cartera. Si la hoja no existe, el proceso debe reportarlo y no guardar cambios destructivos.

## Lectura controlada del Control Cartera operativo

La lectura vigente:

- usa como ruta normal `data/input/CONTROLCARTERA_V2.xlsx`;
- se abre en modo de solo lectura;
- no se modifica ni se guarda;
- se valida contra la hoja `CONTROLCARTERA`;
- carga solo filas útiles con contenido real;
- deja los registros en memoria para visualización local.

Esta lectura no convierte el Excel en base de datos definitiva. La decision sobre persistencia, IDs internos, búsqueda y edición queda para fases posteriores.
