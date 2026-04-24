# Documentacion Tecnica

## Objetivos tecnicos

- Mantener una arquitectura modular y escalable.
- Preparar el proyecto para una aplicacion de escritorio en Python.
- Facilitar distribucion portable y, posteriormente, instalador.
- Separar interfaz, persistencia, reglas de negocio, documentos, reportes y respaldos.
- Documentar decisiones, supuestos y riesgos desde el inicio.

## Principios de diseno

- Implementar por fases pequenas y revisables.
- Evitar dependencias hasta que exista una necesidad concreta.
- No introducir logica de negocio definitiva sin datos reales o validacion previa.
- No borrar informacion automaticamente.
- Requerir confirmacion explicita para cualquier eliminacion futura.
- Mantener trazabilidad sobre cambios relevantes.
- Priorizar codigo claro sobre abstracciones prematuras.

## Estrategia incremental

El proyecto avanzara por versiones. Cada version debera definir alcance, entregables, pruebas y documentacion actualizada.

Fases tentativas:

1. Base documental y estructura del repositorio.
2. Esqueleto tecnico de la aplicacion.
3. Modelo de datos preliminar con muestras controladas.
4. Prototipo de interfaz.
5. Importacion validada desde Excel real.
6. Persistencia local.
7. Documentos de vencimiento por cliente.
8. Reportes, respaldos y empaquetado.

## Versionado

El proyecto usa versionado `X.Y.Z`.

- `X` version mayor: cambios estructurales, incompatibles o que redefinen el producto.
- `Y` version menor: nuevas fases, modulos, capacidades o avances funcionales revisables.
- `Z` parche: correcciones acotadas, ajustes documentales menores, mantenimiento o mejoras sin cambio de alcance.

Antes de publicar una version se debe confirmar que el alcance este documentado, que los archivos relevantes hayan sido actualizados y que las pruebas o revisiones aplicables esten registradas.

## Estandar de commits

Los commits deben ser pequenos, revisables y describir una intencion clara. Se recomienda usar un prefijo de tipo:

- `docs`: cambios de documentacion.
- `chore`: mantenimiento sin cambio funcional.
- `feat`: nueva capacidad funcional futura.
- `fix`: correccion de comportamiento futuro.
- `test`: pruebas.
- `refactor`: cambio interno sin cambio esperado de comportamiento.

Ejemplos:

```text
docs: actualizar politica de datos confidenciales
docs: documentar reglas preliminares de polizas
chore: ajustar gitignore para archivos locales
feat: agregar esqueleto de modulo de clientes
test: cubrir validacion de monedas de poliza
```

Cada commit debe evitar mezclar temas no relacionados.

## Estrategia de ramas

La estrategia inicial sera simple:

- `main`: rama estable y revisable.
- `codex/<descripcion>`: ramas de trabajo asistido.
- `feature/<descripcion>`: nuevas capacidades funcionales.
- `docs/<descripcion>`: cambios documentales amplios.
- `fix/<descripcion>`: correcciones acotadas.

Las ramas deben tener nombres cortos, descriptivos y en minusculas, usando guiones cuando sea necesario.

## Criterios de release

Una release debe cumplir, segun aplique:

- version definida en formato `X.Y.Z`;
- entrada actualizada en `CHANGELOG.md`;
- notas de release en `docs/releases/` cuando exista entregable;
- documentacion de usuario actualizada si cambia el uso del sistema;
- documentacion tecnica actualizada si cambia arquitectura, dependencias o reglas;
- pruebas o revisiones registradas;
- confirmacion de que no se incluyen datos reales confidenciales.

Las notas de release deben indicar alcance, cambios principales, limitaciones conocidas, instrucciones de revision y riesgos pendientes.

## Lineamientos de mantenimiento

- Mantener `README.md`, `CHANGELOG.md` y documentos en `docs/proyecto/` sincronizados con cada version.
- Registrar cambios relevantes en `CHANGELOG.md`.
- Documentar supuestos cuando falte informacion.
- Agregar pruebas cuando exista codigo ejecutable.
- Evitar mezclar cambios funcionales con refactorizaciones no relacionadas.

## Lineamientos de modularidad

La futura aplicacion debera separar responsabilidades:

- interfaz de usuario;
- acceso a datos;
- modelos y validaciones;
- logica de aplicacion;
- dataset canonico y normalizacion;
- generacion de reportes;
- generacion de documentos;
- respaldo y recuperacion;
- utilidades compartidas.

La estructura exacta de paquetes se definira cuando inicie la implementacion tecnica.

## Documentacion del codigo principal

Cuando exista codigo principal, debe quedar documentado de forma suficiente para facilitar mantenimiento:

- modulos con proposito claro;
- funciones publicas con nombres descriptivos;
- comentarios breves en bloques complejos o decisiones no evidentes;
- docstrings cuando una funcion, clase o modulo tenga contrato relevante;
- referencias a reglas de negocio solo cuando hayan sido aprobadas y documentadas.

No se deben agregar comentarios decorativos ni duplicar lo que el codigo ya expresa claramente.

## Calidad textual de futura GUI

Cuando exista interfaz grafica, todo texto visible debe revisarse antes de cada entrega:

- ortografia en espanol;
- consistencia de terminos;
- mensajes claros y accionables;
- uso consistente de moneda, fechas e identificadores;
- confirmaciones explicitas antes de operaciones destructivas;
- respeto por los nombres originales de registros cuando se muestren datos importados.

## Politica de datos confidenciales

La base real es confidencial y no debe subirse a GitHub. Los archivos reales deben mantenerse en rutas locales excluidas por `.gitignore`, como `data/input/`, `data/output/` y `data/backups/`.

No se deben publicar nombres reales, identificaciones, telefonos, correos, placas, fincas, numeros de poliza, archivos originales ni capturas con datos sensibles.

## Politica de anonimizacion para pruebas

Las pruebas podran usar datos ficticios o anonimizados. Una copia anonimizada debe:

- reemplazar nombres reales por nombres ficticios;
- reemplazar identificaciones, telefonos y correos;
- reemplazar placas, fincas y numeros de poliza;
- conservar estructuras de columnas y formatos utiles para pruebas;
- marcarse claramente como muestra o dato ficticio;
- evitar cualquier dato que permita reconstruir informacion real.

La anonimizacion debe preservar patrones tecnicos necesarios para probar el sistema, sin conservar datos sensibles reales.

## Auditoria local segura de Excel

La auditoria local de la base confidencial se ejecuta mediante `scripts/auditar_base_local.py`.

El script:

- recibe una ruta de entrada y una ruta de salida;
- abre el workbook en modo de lectura;
- no modifica el Excel original;
- detecta hojas, dimensiones y encabezados solo cuando alcanzan confianza suficiente;
- estima la hoja principal por volumen de datos y encabezados seguros;
- calcula completitud por columna;
- resume categorias de vigencia o frecuencia como conteos;
- clasifica patrones de numero de poliza sin mostrar valores completos;
- detecta campos separados de dia, mes y ano de vencimiento;
- revisa presencia de columnas candidatas de `detalle` y placa o finca;
- usa identificadores `COL_A`, `COL_B`, etc. cuando el encabezado es dudoso o no confirmado;
- genera reportes locales en `data/output/auditoria/`.

Los reportes de auditoria pueden incluir nombres de columnas solo si la fila de encabezado fue confirmada y el nombre supera el saneamiento. No deben incluir muestras de filas, nombres reales, identificaciones, polizas completas, placas, fincas ni anotaciones reales.

Las reglas detectadas por esta auditoria siguen siendo preliminares hasta que sean revisadas y aprobadas.

Si una decision de encabezado no es totalmente segura, la salida debe preferir una etiqueta tecnica conservadora antes que exponer texto de una celda real.

## Dataset canonico interno

La fase `1.4.0` introduce, a nivel de diseno documental, el concepto de dataset canonico interno. Su objetivo es dar una representacion estable y trazable para la app sin reemplazar de golpe el workbook operativo.

Principios de esta capa:

- el workbook sigue siendo la fuente operativa principal en el corto plazo;
- el dataset canonico organiza el modelo interno futuro de la aplicacion;
- los campos deben distinguirse entre originales, normalizados, derivados y operativos;
- la sensibilidad y la editabilidad futura deben documentarse de forma explicita;
- toda transformacion debe mantener trazabilidad con el origen.

Documentos de referencia de esta fase:

- `docs/proyecto/ESPECIFICACION_DATASET_CANONICO.md`
- `docs/proyecto/MAPA_ORIGEN_A_CANONICO.md`
- `docs/proyecto/ESTRATEGIA_MODERNIZACION_WORKBOOK.md`
- `docs/proyecto/DECISIONES_IMPLEMENTACION_1_5_1_6.md`

## Relacion workbook -> app

La estrategia aprobada para esta fase es `workbook primero`.

Esto implica que:

- el workbook no se elimina ni se considera legado descartable todavia;
- la app futura debe poder leer su estructura real sin forzar cambios manuales inmediatos;
- el mapeo origen -> canonico se documenta antes de implementar lectura funcional;
- la normalizacion debe ocurrir como capa controlada, sin perder el valor original;
- cualquier automatizacion futura debe ser reversible y compatible con la operacion manual.

## Esqueleto tecnico Python

La fase `1.5.0` crea la base tecnica minima de la aplicacion en `app/`.

El entry point oficial es:

```powershell
python -m app
```

El arranque tecnico:

- carga configuracion por defecto desde `app/config/`;
- resuelve rutas locales desde `app/core/paths.py`;
- configura logging de consola desde `app/core/logging.py`;
- expone excepciones tecnicas centralizadas en `app/core/exceptions.py`;
- mantiene contratos preliminares del dataset canonico en `app/domain/contracts.py`;
- devuelve un estado tecnico seguro sin leer el workbook real.

Esta fase no implementa GUI, lectura funcional del workbook, persistencia, busqueda, edicion, bitacoras, exportaciones ni documentos.

## Configuracion, rutas y logging

La configuracion se representa mediante `AppConfig` y contiene:

- nombre de la aplicacion;
- version actual;
- raiz del proyecto;
- rutas locales para `data/input/`, `data/output/`, `data/backups/` y `data/samples/`;
- nivel de logging.

La resolucion de rutas no crea carpetas ni toca archivos de datos. El logging usa solo la libreria estandar, escribe en consola y no genera archivos persistentes.

## Contratos preliminares

Los contratos de `app/domain/contracts.py` describen campos canonicos sin transformar datos reales. Cada campo registra:

- nombre canonico;
- procedencia: original, normalizado, derivado u operativo;
- sensibilidad;
- editabilidad futura;
- descripcion tecnica breve.

Estos contratos son descriptivos y testeables, pero no ejecutan reglas funcionales.

## Modernizacion controlada del workbook

La fase `1.6.0` agrega un flujo local para crear una copia modernizada del workbook operativo sin sobrescribir el archivo original.

Comando:

```powershell
python scripts/modernizar_workbook_local.py data/input/CONTROLCARTERA_V2.xlsx data/output/workbook_modernizado
```

Componentes:

- `app/domain/workbook_rules.py`: reglas preliminares puras para clasificar frecuencia, poliza, moneda, identificacion y fecha.
- `app/services/workbook_modernizer.py`: servicio que genera copia modernizada, columnas auxiliares, formato y reportes.
- `scripts/modernizar_workbook_local.py`: comando local explicito para ejecutar el flujo.

Salidas locales:

- `data/output/workbook_modernizado/CONTROLCARTERA_V2_modernizado_YYYYMMDD_HHMMSS.xlsx`
- `data/output/workbook_modernizado/resumen_modernizacion.md`
- `data/output/workbook_modernizado/resumen_modernizacion.json`
- `data/output/workbook_modernizado/control_revision.csv`

El flujo conserva datos originales, no borra registros, no corrige valores automaticamente y agrega columnas auxiliares al final de la hoja principal. Los reportes locales no deben copiarse a documentacion versionada.

## Estructura minima vigente

La estructura del repositorio debe mantenerse sobria en esta etapa:

- raiz con archivos de gobierno del proyecto;
- `app/`, `scripts/` y `tests/` como base tecnica;
- `data/input/`, `data/output/`, `data/backups/` y `data/samples/` para trabajo local;
- `docs/proyecto/` como contenedor unico de documentacion interna;
- `docs/capturas/`, `docs/diagramas/` y `docs/releases/` para evidencia futura.

No se deben conservar carpetas placeholder que no aporten valor inmediato. La estructura de plantillas DOCX puede crearse cuando comience la fase correspondiente.

## Reglas conocidas no implementadas

Las siguientes reglas se documentan para analisis futuro, pero no deben implementarse todavia como validaciones rigidas:

- Las vigencias `D.M.` significan deduccion mensual.
- Las polizas con vigencia `D.M.` no generan avisos, pero si deben almacenarse.
- Ademas de `D.M.` o deduccion mensual, pueden observarse frecuencias mensuales, trimestrales, semestrales y anuales.
- Las frecuencias observadas deben contarse y documentarse antes de convertirse en reglas funcionales.
- Las polizas que inician en `01` corresponden preliminarmente a colones.
- Las polizas que inician en `02` corresponden preliminarmente a dolares.
- La regla de prefijo `01` y `02` no aplica a riesgos del trabajo, identificados preliminarmente como polizas cuyo numero es completamente numerico.
- La columna `Numero de Placa / Finca` usualmente contiene numeros de placa de vehiculos.
- La fecha de vencimiento puede venir separada en dia, mes y ano.
- La columna `detalle` se usa para anotaciones o para relacionar polizas de un mismo dueno.

## Decisiones tecnicas iniciales

- Lenguaje base: Python.
- GUI probable: PySide6.
- Persistencia local probable: SQLite.
- Excel probable: openpyxl y/o pandas.
- DOCX probable: python-docx.
- Pruebas probables: pytest.
- Empaquetado probable: PyInstaller.

Estas decisiones son preliminares y podran ajustarse con evidencia tecnica.

## Riesgos iniciales

- La base real en Excel puede contener ambiguedades adicionales a las ya auditadas.
- Las reglas de negocio no estan completamente definidas.
- La estructura final de datos podria cambiar al revisar relaciones y duplicados.
- La generacion documental dependera de plantillas y criterios aun pendientes.
- Un modelo canonico demasiado rigido podria romper compatibilidad con la operacion manual.

## Limite de 1.4.0

La version `1.4.0` solo deja decisiones y diseno documental listos para revision.

No debe implementar todavia:

- logica funcional de negocio;
- importacion operativa del workbook;
- persistencia definitiva;
- edicion de registros;
- automatizacion del archivo real;
- interfaz grafica.

## Limite de 1.5.0

La version `1.5.0` crea base tecnica, no producto funcional.

No debe implementar todavia:

- lectura funcional del workbook;
- escritura sobre Excel;
- persistencia operativa;
- busqueda o edicion;
- bitacoras funcionales;
- exportaciones;
- generacion DOCX;
- GUI.

## Limite de 1.6.0

La version `1.6.0` genera una copia local modernizada, no una app operativa completa.

No implementa:

- escritura sobre el workbook original;
- busqueda funcional;
- edicion desde la app;
- bitacoras funcionales;
- persistencia SQLite;
- DOCX;
- avisos;
- GUI.
