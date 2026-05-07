# Documentación Técnica

## Objetivos técnicos

- Mantener una arquitectura modular y escalable.
- Preparar el proyecto para una aplicación de escritorio en Python.
- Facilitar distribución portable y, posteriormente, instalador.
- Separar interfaz, persistencia, reglas de negocio, documentos, reportes y respaldos.
- Documentar decisiones, supuestos y riesgos desde el inicio.

## Principios de diseño

- Implementar por fases pequeñas y revisables.
- Evitar dependencias hasta que exista una necesidad concreta.
- No introducir lógica de negocio definitiva sin datos reales o validación previa.
- No borrar información automáticamente.
- Requerir confirmación explícita para cualquier eliminación futura.
- Mantener trazabilidad sobre cambios relevantes.
- Priorizar código claro sobre abstracciones prematuras.

## Estrategia incremental

El proyecto avanzará por versiones. Cada versión deberá definir alcance, entregables, pruebas y documentación actualizada.

Fases tentativas:

1. Base documental y estructura del repositorio.
2. Esqueleto técnico de la aplicación.
3. Modelo de datos preliminar con muestras controladas.
4. Prototipo de interfaz.
5. Importacion validada desde Excel real.
6. Persistencia local.
7. Documentos de vencimiento por cliente.
8. Reportes, respaldos y empaquetado.

## Versionado

El proyecto usa versionado `X.Y.Z`.

- `X` versión mayor: cambios estructurales, incompatibles o que redefinen el producto.
- `Y` versión menor: nuevas fases, módulos, capacidades o avances funcionales revisables.
- `Z` parche: correcciones acotadas, ajustes documentales menores, mantenimiento o mejoras sin cambio de alcance.

Antes de publicar una versión se debe confirmar que el alcance este documentado, que los archivos relevantes hayan sido actualizados y que las pruebas o revisiones aplicables esten registradas.

## Estandar de commits

Los commits deben ser pequeños, revisables y describir una intención clara. Se recomienda usar un prefijo de tipo:

- `docs`: cambios de documentación.
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

La estrategia inicial será simple:

- `main`: rama estable y revisable.
- `codex/<descripcion>`: ramas de trabajo asistido.
- `feature/<descripcion>`: nuevas capacidades funcionales.
- `docs/<descripcion>`: cambios documentales amplios.
- `fix/<descripcion>`: correcciones acotadas.

Las ramas deben tener nombres cortos, descriptivos y en minusculas, usando guiones cuando sea necesario.

## Criterios de release

Una release debe cumplir, segun aplique:

- versión definida en formato `X.Y.Z`;
- entrada actualizada en `CHANGELOG.md`;
- notas de release en `docs/releases/` cuando exista entregable;
- documentación de usuario actualizada si cambia el uso del sistema;
- documentación técnica actualizada si cambia arquitectura, dependencias o reglas;
- pruebas o revisiones registradas;
- confirmación de que no se incluyen datos reales confidenciales.

Las notas de release deben indicar alcance, cambios principales, limitaciones conocidas, instrucciones de revisión y riesgos pendientes.

## Lineamientos de mantenimiento

- Mantener `README.md`, `CHANGELOG.md` y documentos en `docs/proyecto/` sincronizados con cada versión.
- Registrar cambios relevantes en `CHANGELOG.md`.
- Documentar supuestos cuando falte información.
- Agregar pruebas cuando exista código ejecutable.
- Evitar mezclar cambios funcionales con refactorizaciones no relacionadas.

## Lineamientos de modularidad

La futura aplicación deberá separar responsabilidades:

- interfaz de usuario;
- acceso a datos;
- modelos y validaciones;
- lógica de aplicación;
- dataset canónico y normalización;
- generación de reportes;
- generación de documentos;
- respaldo y recuperacion;
- utilidades compartidas.

La estructura exacta de paquetes se definirá cuando inicie la implementación técnica.

## Documentación del código principal

Cuando exista código principal, debe quedar documentado de forma suficiente para facilitar mantenimiento:

- módulos con propósito claro;
- funciones publicas con nombres descriptivos;
- comentarios breves en bloques complejos o decisiones no evidentes;
- docstrings cuando una función, clase o módulo tenga contrato relevante;
- referencias a reglas de negocio solo cuando hayan sido aprobadas y documentadas.

No se deben agregar comentarios decorativos ni duplicar lo que el código ya expresa claramente.

## Calidad textual de futura GUI

Cuando exista interfaz grafica, todo texto visible debe revisarse antes de cada entrega:

- ortografia en espanol;
- consistencia de terminos;
- mensajes claros y acciónables;
- uso consistente de moneda, fechas e identificadores;
- confirmaciones explícitas antes de operaciones destructivas;
- respeto por los nombres originales de registros cuando se muestren datos importados.

## Política de datos confidenciales

La base real es confidencial y no debe subirse a GitHub. Los archivos reales deben mantenerse en rutas locales excluidas por `.gitignore`, como `data/input/`, `data/output/` y `data/backups/`.

No se deben publicar nombres reales, identificaciones, teléfonos, correos, placas, fincas, números de póliza, archivos originales ni capturas con datos sensibles.

## Política de anonimización para pruebas

Las pruebas podrán usar datos ficticios o anonimizados. Una copia anonimizada debe:

- reemplazar nombres reales por nombres ficticios;
- reemplazar identificaciones, teléfonos y correos;
- reemplazar placas, fincas y números de póliza;
- conservar estructuras de columnas y formatos útiles para pruebas;
- marcarse claramente como muestra o dato ficticio;
- evitar cualquier dato que permita reconstruir información real.

La anonimización debe preservar patrónes técnicos necesarios para probar el sistema, sin conservar datos sensibles reales.

## Auditoría local segura de Excel

La auditoría local de la base confidencial se ejecuta mediante `scripts/auditar_base_local.py`.

El script:

- recibe una ruta de entrada y una ruta de salida;
- abre el workbook en modo de lectura;
- no modifica el Excel original;
- detecta hojas, dimensiones y encabezados solo cuando alcanzan confianza suficiente;
- estima la hoja principal por volumen de datos y encabezados seguros;
- calcula completitud por columna;
- resume categorías de vigencia o frecuencia como conteos;
- clasifica patrónes de número de póliza sin mostrar valores completos;
- detecta campos separados de día, mes y año de vencimiento;
- revisa presencia de columnas candidatas de `detalle` y placa o finca;
- usa identificadores `COL_A`, `COL_B`, etc. cuando el encabezado es dudoso o no confirmado;
- genera reportes locales en `data/output/auditoria/`.

Los reportes de auditoría pueden incluir nombres de columnas solo si la fila de encabezado fue confirmada y el nombre supera el saneamiento. No deben incluir muestras de filas, nombres reales, identificaciones, pólizas completas, placas, fincas ni anotaciones reales.

Las reglas detectadas por esta auditoría siguen siendo preliminares hasta que sean revisadas y aprobadas.

Si una decision de encabezado no es totalmente segura, la salida debe preferir una etiqueta técnica conservadora antes que exponer texto de una celda real.

## Dataset canónico interno

La fase `1.4.0` introduce, a nivel de diseño documental, el concepto de dataset canónico interno. Su objetivo es dar una representación estable y trazable para la app sin reemplazar de golpe el workbook operativo.

Principios de esta capa:

- el workbook sigue siendo la fuente operativa principal en el corto plazo;
- el dataset canónico organiza el modelo interno futuro de la aplicación;
- los campos deben distinguirse entre originales, normalizados, derivados y operativos;
- la sensibilidad y la editabilidad futura deben documentarse de forma explícita;
- toda transformacion debe mantener trazabilidad con el origen.

Documentos de referencia de esta fase:

- `docs/proyecto/ESPECIFICACION_DATASET_CANONICO.md`
- `docs/proyecto/MAPA_ORIGEN_A_CANONICO.md`
- `docs/proyecto/ESTRATEGIA_MODERNIZACION_WORKBOOK.md`
- `docs/proyecto/DECISIONES_IMPLEMENTACION_1_5_1_6.md`

## Relacion workbook -> app

La estrategia aprobada para esta fase es `workbook primero`.

Esto implica que:

- el workbook no se elimina ni se considera legado descartable todavía;
- la app futura debe poder leer su estructura real sin forzar cambios manuales inmedíatos;
- el mapeo origen -> canónico se documenta antes de implementar lectura funcional;
- la normalización debe ocurrir como capa controlada, sin perder el valor original;
- cualquier automatización futura debe ser reversible y compatible con la operación manual.

## Esqueleto técnico Python

La fase `1.5.0` crea la base técnica minima de la aplicación en `app/`.

El entry point técnico original de `1.5.0` fue:

```powershell
python -m app
```

Desde `1.8.0`, ese comando abre la interfaz grafica. El chequeo técnico equivalente queda disponible como:

```powershell
python -m app --check
```

El arranque técnico:

- carga configuración por defecto desde `app/config/`;
- resuelve rutas locales desde `app/core/paths.py`;
- configura logging de consola desde `app/core/logging.py`;
- expone excepciones técnicas centralizadas en `app/core/exceptions.py`;
- mantiene contratos preliminares del dataset canónico en `app/domain/contracts.py`;
- devuelve un estado técnico seguro sin leer el workbook real.

La fase `1.5.0` no implemento GUI, lectura funcional del workbook, persistencia, búsqueda, edición, bitácoras, exportaciones ni documentos.

## Configuración, rutas y logging

La configuración se representa mediante `AppConfig` y contiene:

- nombre de la aplicación;
- versión actual;
- raiz del proyecto;
- rutas locales para `data/input/`, `data/output/`, `data/backups/` y `data/samples/`;
- nivel de logging.

La resolucion de rutas no crea carpetas ni toca archivos de datos. El logging usa solo la libreria esténdar, escribe en consola y no genera archivos persistentes.

## Contratos preliminares

Los contratos de `app/domain/contracts.py` describen campos canónicos sin transformar datos reales. Cada campo registra:

- nombre canónico;
- procedencia: original, normalizado, derivado u operativo;
- sensibilidad;
- editabilidad futura;
- descripcion técnica breve.

Estos contratos son descriptivos y testeables, pero no ejecutan reglas funcionales.

## Modernizacion controlada del workbook

El flujo de modernización local creado en fases previas queda retirado como dependencia activa desde `1.8.2`. La app ya no requiere copias en `data/output/workbook_modernizado/` para visualizar datos.

La fuente activa de lectura es:

```text
data/input/CONTROLCARTERA_V2.xlsx
```

Las validaciones futuras deberán manejarse internamente en la aplicación, sin agregar columnas técnicas al Excel operativo. `data/output/` queda reservado para copias, exportaciones o cambios futuros aprobados.

## Mantenimiento controlado del workbook operativo

La fase `1.6.1` agrega un script local para eliminar una hoja obsoleta especifica del workbook operativo real, con respaldo previo obligatorio.

Comando:

```powershell
python scripts/limpiar_workbook_operativo.py data/input/CONTROLCARTERA_V2.xlsx data/backups/workbook_mantenimiento data/output/workbook_mantenimiento
```

Comportamiento técnico:

- valida que el workbook exista;
- crea un respaldo timestamped antes de abrir y guardar cambios;
- busca exactamente la hoja `Reporte de vencimientos del mes`;
- elimina solo esa hoja si existe;
- no modifica hojas de cartera ni datos de filas;
- si la hoja no existe, no guarda cambios sobre el workbook;
- genera reportes locales Markdown y JSON sin datos de filas.

Salidas locales:

- `data/backups/workbook_mantenimiento/`;
- `data/output/workbook_mantenimiento/reporte_limpieza_workbook.md`;
- `data/output/workbook_mantenimiento/reporte_limpieza_workbook.json`.

Esta fase no implementa generación de vencimientos. La eliminación de la hoja obsoleta responde a que ese flujo será diseñado e implementado posteriormente dentro del sistema.

## Carga controlada del Control Cartera

Comando:

```powershell
python scripts/cargar_control_cartera.py data/input/CONTROLCARTERA_V2.xlsx
```

Componentes:

- `app/domain/workbook_records.py`: contratos internos de columnas, registros y resumen de carga.
- `app/services/workbook_loader.py`: servicio que valida ruta, extensión, hoja principal y carga registros útiles en memoria.
- `scripts/cargar_control_cartera.py`: comando local que imprime resumen técnico sin valores de filas.

Comportamiento técnico:

- acepta una ruta exacta de workbook `.xlsx`;
- valida la hoja `CONTROLCARTERA`;
- detecta fila de encabezados a partir de columnas originales;
- excluye columnas técnicas auxiliares del flujo visible si aparecieran en archivos heredados;
- calcula filas útiles por contenido real, no por formato residual de Excel;
- reporta filas útiles detectadas, filas omitidas y columnas visibles;
- carga filas en memoria sin modificar ni guardar el workbook.

Esta fase no crea reportes obligatorios, no escribe archivos de salida y no imprime clientes, identificaciones, pólizas, placas, teléfonos ni detalle.

## Interfaz grafica inicial

La fase `1.8.0` introduce la primera GUI real con PySide6. La fase `1.8.1` agrega visualización tabular de registros en modo solo lectura. La fase `1.8.2` cambia la fuente activa a `data/input/CONTROLCARTERA_V2.xlsx`. La fase `1.8.3` agrega pulido visual inicial y cambio entre tema claro y oscuro. La fase `1.8.4` agrega ícono profesional propio e identidad visual básica. La fase `1.9.0` agrega búsqueda y filtros básicos en memoria sobre la tabla de registros. La fase `1.9.1` agrega una ventana de detalle del registro seleccionado en modo solo lectura.

Comando principal:

```powershell
python -m app
```

Componentes:

- `app/ui/main_window.py`: ventana principal, selección de Control Cartera, carga y resumen visual.
- `app/ui/table_model.py`: modelo `QAbstractTableModel` de solo lectura para registros cargados.
- `app/ui/filter_proxy_model.py`: proxy `QSortFilterProxyModel` para búsqueda en todas las columnas o en una columna específica.
- `app/ui/detail_model.py`: modelo de solo lectura para campos y valores del registro seleccionado.
- `app/ui/detail_dialog.py`: ventana modal de detalle abierta por doble clic sobre una fila.
- `app/ui/theme.py`: estilos visuales para tema claro y oscuro.
- `app/ui/assets.py`: resolucion de assets visuales para desarrollo y futuro empaquetado.
- `app/ui/__init__.py`: exportacion minima de la interfaz.
- `app/main.py`: entry point que abre GUI por defecto y conserva `--check`.
- `assets/app_icon.svg`: ícono propio del proyecto, sin marcas oficiales ni logos externos.

La ventana:

- muestra `Gestor de Seguros- Dagoberto Quirós Madriz` y la versión actual;
- muestra la ruta predeterminada `data/input/CONTROLCARTERA_V2.xlsx`;
- permite cargar la ruta predeterminada mediante una acción explícita;
- permite seleccionar otro archivo `.xlsx` y lo carga automáticamente;
- valida que la ruta exista y que la extensión sea `.xlsx` antes de llamar al lector;
- carga el archivo mediante `app/services/workbook_loader.py`;
- muestra archivo, hoja, filas útiles, filas cargadas, filas omitidas, columnas visibles, modo de solo lectura y estado de carga;
- usa scroll y areas de texto de solo lectura para evitar cortes en listas largas;
- muestra registros cargados en una pestaña `Registros` mediante `QTableView`;
- permite buscar coincidencias parciales, sin distinguir mayúsculas/minúsculas y con tolerancia básica a tildes;
- permite buscar en `Todas las columnas` o en una columna visible detectada;
- permite limpiar la búsqueda y restaurar todos los registros cargados;
- muestra el contador `Mostrando X de Y registros`;
- reporta filas cargadas y columnas visibles;
- abre `Detalle del registro` con doble clic sobre una fila de la tabla;
- muestra solo campos con información en la ventana de detalle;
- respeta filtros activos al mostrar el detalle del registro seleccionado;
- permite alternar entre tema claro y oscuro mediante un botón compacto;
- recuerda localmente el tema seleccionado mediante `QSettings`;
- aplica el ícono propio del proyecto a `QApplication` y a la ventana principal;
- no trata la cancelacion del selector como error y conserva el estado anterior;
- presenta errores reales de forma amigable con barra de estado y `QMessageBox`;
- mantiene la tabla en modo solo lectura.

Esta fase usa `PySide6` y no agrega dependencias nuevas. Las pruebas GUI usan `QT_QPA_PLATFORM=offscreen` y no requieren abrir ventanas reales durante la automatización. El ícono SVG queda preparado como fuente para una fase futura de empaquetado con PyInstaller; no se crea instalador todavía.

La búsqueda de `1.9.0` se implementa como una capa de filtrado visual sobre el modelo de tabla. La vista de detalle de `1.9.1` consulta el registro seleccionado desde el modelo fuente y lo presenta en una ventana modal de solo lectura, omitiendo campos vacíos. Ninguna de estas capas modifica registros originales, escribe en Excel, crea persistencia o implementa edición.

## Release técnico inicial

El release `v1.8.4-alpha` documenta el primer corte técnico revisable del proyecto. Mantiene la versión interna `1.8.4`, no agrega ejecutable, no configura PyInstaller y no modifica lógica funcional.

El documento de release vive en `docs/releases/v1.8.4-alpha.md` e incluye instrucciones de instalación, ejecución, pruebas, checklist de validación y release notes para GitHub.

## Bitácoras o pistas de auditoría futuras

Cuando se apruebe la edición o guardado de cambios sobre el Control Cartera, deberá incorporarse un módulo de bitácoras o pistas de auditoría. Ese módulo no existe todavía en `1.8.4`, pero deberá registrar como mínimo fecha y hora del cambio, campo modificado, valor anterior, valor nuevo, origen del cambio, usuario local si aplica, archivo afectado y resultado de la operación.

## Estructura minima vigente

La estructura del repositorio debe mantenerse sobria en esta etapa:

- raiz con archivos de gobierno del proyecto;
- `app/`, `scripts/` y `tests/` como base técnica;
- `data/input/`, `data/output/`, `data/backups/` y `data/samples/` para trabajo local;
- `docs/proyecto/` como contenedor único de documentación interna;
- `docs/capturas/`, `docs/diagramas/` y `docs/releases/` para evidencia futura.

No se deben conservar carpetas placeholder que no aporten valor inmedíato. La estructura de plantillas DOCX puede crearse cuando comience la fase correspondiente.

## Reglas conocidas no implementadas

Las siguientes reglas se documentan para analisis futuro, pero no deben implementarse todavía como validaciones rigidas:

- Las vigencias `D.M.` significan deduccion mensual.
- Las pólizas con vigencia `D.M.` no generan avisos, pero si deben almacenarse.
- Ademas de `D.M.` o deduccion mensual, pueden observarse frecuencias mensuales, trimestrales, semestrales y anuales.
- Las frecuencias observadas deben contarse y documentarse antes de convertirse en reglas funcionales.
- Las pólizas que inician en `01` corresponden preliminarmente a colones.
- Las pólizas que inician en `02` corresponden preliminarmente a dólares.
- La regla de prefijo `01` y `02` no aplica a riesgos del trabajo, identificados preliminarmente como pólizas cuyo número es completamente numerico.
- La columna `Numero de Placa / Finca` usualmente contiene números de placa de vehiculos.
- La fecha de vencimiento puede venir separada en día, mes y año.
- La columna `detalle` se usa para anotaciones o para relacionar pólizas de un mismo dueño.

## Decisiones técnicas iniciales

- Lenguaje base: Python.
- GUI probable: PySide6.
- Persistencia local probable: SQLite.
- Excel probable: openpyxl y/o pandas.
- DOCX probable: python-docx.
- Pruebas probables: pytest.
- Empaquetado probable: PyInstaller.

Estas decisiones son preliminares y podrán ajustarse con evidencia técnica.

## Riesgos iniciales

- La base real en Excel puede contener ambigüedades adicionales a las ya auditadas.
- Las reglas de negocio no estén completamente definidas.
- La estructura final de datos podria cambiar al revisar relaciones y duplicados.
- La generación documental dependera de plantillas y criterios aún pendientes.
- Un modelo canónico demasiado rigido podria romper compatibilidad con la operación manual.

## Limite de 1.4.0

La versión `1.4.0` solo deja decisiones y diseño documental listos para revisión.

No debe implementar todavía:

- lógica funcional de negocio;
- importación operativa del workbook;
- persistencia definitiva;
- edición de registros;
- automatización del archivo real;
- interfaz grafica.

## Limite de 1.5.0

La versión `1.5.0` crea base técnica, no producto funcional.

No debe implementar todavía:

- lectura funcional del workbook;
- escritura sobre Excel;
- persistencia operativa;
- búsqueda o edición;
- bitácoras funcionales;
- exportaciones;
- generación DOCX;
- GUI.

## Limite de 1.6.0

La versión `1.6.0` genera una copia local modernizada, no una app operativa completa.

No implementa:

- escritura sobre el workbook original;
- búsqueda funcional;
- edición desde la app;
- bitácoras funcionales;
- persistencia SQLite;
- DOCX;
- avisos;
- GUI.

## Limite de 1.6.1

La versión `1.6.1` permite una única modificacion controlada sobre el workbook operativo real: eliminar la hoja obsoleta `Reporte de vencimientos del mes` después de crear respaldo local.

No implementa:

- generación de vencimientos;
- limpieza de datos de clientes;
- cambios en la hoja principal de cartera;
- búsqueda o edición desde la app;
- bitácoras funcionales;
- persistencia SQLite;
- DOCX;
- dashboards;
- GUI.

## Limite de 1.7.0

La versión `1.7.0` implementa lectura controlada en memoria, no funcionalidad operativa completa.

No implementa:

- escritura sobre workbooks;
- búsqueda funcional;
- edición de registros;
- persistencia SQLite;
- bitácoras funcionales;
- reportes finales;
- DOCX;
- generación de vencimientos;
- GUI.

## Limite de 1.8.0

La versión `1.8.0` crea la primera GUI, pero no una aplicación operativa completa.

No implementa:

- tabla completa de registros;
- búsqueda o filtros;
- edición;
- guardado;
- bitácoras funcionales;
- persistencia SQLite;
- reportes finales;
- DOCX;
- dashboards;
- generación de vencimientos;
- tema claro u oscuro.

## Limite de 1.8.1

La versión `1.8.1` agrega tabla de registros de solo lectura.

No implementa:

- búsqueda;
- filtros;
- edición;
- guardado;
- bitácoras funcionales;
- vista de detalle;
- persistencia SQLite;
- reportes finales;
- DOCX;
- dashboards;
- generación de vencimientos;
- tema claro u oscuro;
- ícono profesional.

## Limite de 1.8.2

La versión `1.8.2` lee directamente el Control Cartera operativo desde `data/input/` y mantiene visualización de solo lectura.

No implementa:

- búsqueda;
- filtros;
- edición;
- guardado;
- bitácoras funcionales;
- persistencia SQLite;
- reportes finales;
- DOCX;
- dashboards;
- generación de vencimientos;
- tema claro u oscuro;
- ícono profesional.

## Limite de 1.8.3

La versión `1.8.3` agrega pulido visual inicial y control compacto de tema claro/oscuro.

No implementa:

- búsqueda;
- filtros;
- edición;
- guardado;
- bitácoras funcionales;
- persistencia SQLite;
- reportes finales;
- DOCX;
- dashboards;
- generación de vencimientos;
- ícono profesional.

## Limite de 1.8.4

La versión `1.8.4` agrega ícono profesional propio e identidad visual básica.

No implementa:

- búsqueda;
- filtros;
- edición;
- guardado;
- bitácoras funcionales;
- persistencia SQLite;
- reportes finales;
- DOCX;
- dashboards;
- generación de vencimientos;
- instalador;
- release.

## Limite de 1.9.0

La versión `1.9.0` agrega búsqueda y filtros básicos en la pestaña `Registros`.

No implementa:

- edición;
- guardado;
- bitácoras funcionales;
- persistencia SQLite;
- reportes finales;
- DOCX;
- dashboards;
- generación de vencimientos;
- release.

## Limite de 1.9.1

La versión `1.9.1` agrega vista de detalle del registro seleccionado en la pestaña `Registros`.

No implementa:

- edición;
- guardado;
- bitácoras funcionales;
- persistencia SQLite;
- reportes finales;
- DOCX;
- dashboards;
- generación de vencimientos;
- release.
