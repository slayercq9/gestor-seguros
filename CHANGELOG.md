# Changelog

Todos los cambios relevantes del proyecto se documentaran en este archivo.

El formato seguirá una estructura por versiones, con secciones para cambios agregados, modificados, corregidos y decisiones importantes cuando aplique.

## [1.9.1] - 2026-05-06

### Agregado

- Ventana modal `Detalle del registro` abierta con doble clic sobre una fila de la tabla.
- Modelo `RecordDetailModel` para mostrar campos y valores del registro seleccionado en modo solo lectura.
- Omisión de campos vacíos en la ventana de detalle.
- Pruebas automatizadas para detalle, doble clic, compatibilidad con filtros y campos vacíos.

### Modificado

- Versión interna del paquete actualizada a `1.9.1`.
- La documentación de usuario, arquitectura, técnica y pruebas queda alineada con la fase `1.9.1`.

### Notas

- Esta versión no modifica ni guarda archivos Excel.
- Esta versión no implementa edición, guardado, bitácoras, vencimientos ni DOCX.
- El detalle es una vista de consulta local y de solo lectura sobre el registro seleccionado.

## [1.9.0] - 2026-05-06

### Agregado

- Búsqueda básica en la pestaña `Registros`.
- Selector `Buscar en` con opción `Todas las columnas` y columnas reales cargadas desde el Control Cartera.
- Filtro de registros mediante `QSortFilterProxyModel`, sin modificar datos originales.
- Acción `Limpiar` para restaurar la visualización completa.
- Contador `Mostrando X de Y registros`.
- Pruebas automatizadas para búsqueda general, búsqueda por columna, limpieza de filtros y conservación de datos.

### Modificado

- Versión interna del paquete actualizada a `1.9.0`.
- La tabla conserva modo de solo lectura y ahora puede filtrarse en memoria.
- Al cargar un nuevo Control Cartera se limpia la búsqueda y se actualiza el selector de columnas.
- La documentación de usuario, arquitectura, técnica y pruebas queda alineada con la fase `1.9.0`.

### Notas

- Esta versión no modifica ni guarda archivos Excel.
- Esta versión no implementa edición, guardado, vista de detalle, bitácoras, vencimientos ni DOCX.
- Los filtros se aplican solo sobre los registros cargados en memoria.

## [v1.8.4-alpha] - 2026-05-06

### Agregado

- Primer documento de release técnico inicial en `docs/releases/v1.8.4-alpha.md`.
- Checklist de validación para publicar el release en GitHub.
- Release notes breves listas para copiar en GitHub.

### Notas

- La versión interna de la app se mantiene en `1.8.4`.
- Este release no incluye ejecutable, instalador ni artefactos binarios.
- Este release no incluye datos reales ni archivos confidenciales.
- Esta preparacion no modifica lógica funcional de la aplicación.

## [1.8.4] - 2026-05-05

### Agregado

- ícono profesional propio en `assets/app_icon.svg`.
- Utilidad `app/ui/assets.py` para resolver assets en desarrollo y en futuros empaquetados con PyInstaller.
- Aplicación del ícono a `QApplication` y a la ventana principal.
- Pruebas para validar existencia, resolucion y carga del ícono.

### Modificado

- Versión interna del paquete actualizada a `1.8.4`.
- Documentación actualizada para indicar que el ícono no usa logos oficiales ni marcas externas.

### Notas

- Esta versión no modifica ni guarda archivos Excel.
- Esta versión no implementa búsqueda, filtros, edición, guardado, bitácoras, vencimientos, DOCX, instalador ni release.

## [1.8.3] - 2026-05-05

### Agregado

- Botón compacto para alternar tema claro/oscuro en la ventana principal.
- Persistencia local de la preferencia de tema mediante `QSettings`.
- Módulo `app/ui/theme.py` para centralizar estilos visuales de la GUI.

### Modificado

- Versión interna del paquete actualizada a `1.8.3`.
- Estilos de ventana, botónes, pestañas, tabla, encabezados y barra de estado ajustados para tema claro y oscuro.
- Pruebas GUI ampliadas para validar cambio de tema, persistencia local y conservacion de registros cargados.
- Documentación actualizada con el uso del control de tema.

### Notas

- Esta versión no modifica ni guarda archivos Excel.
- Esta versión no implementa búsqueda, filtros, edición, guardado, bitácoras, ícono profesional, vencimientos ni DOCX.

## [1.8.2] - 2026-05-05

### Agregado

- Accion `Cargar predeterminado` en la GUI para leer `data/input/CONTROLCARTERA_V2.xlsx`.
- Script `scripts/cargar_control_cartera.py` para carga técnica directa del Control Cartera operativo.
- Ventanas emergentes amigables para errores de archivo, formato y carga.

### Modificado

- Versión interna del paquete actualizada a `1.8.2`.
- La app deja de depender de `data/output/workbook_modernizado/` para visualizar datos.
- El lector se orienta al Control Cartera operativo de `data/input/`.
- La documentación vigente define `data/input/CONTROLCARTERA_V2.xlsx` como fuente activa.
- Las pruebas cubren lectura directa, ruta predeterminada, filas útiles y diálogos de error.
- Cancelar la selección de archivo en la GUI conserva el estado anterior sin mostrar error ni limpiar registros.
- La pestaña `Resumen` deja de mostrar una seccion visual de advertencias y conserva solo conteos, modo y estado de carga.
- La documentación registra la necesidad futura de un módulo de bitácoras o pistas de auditoría para cambios sobre el Control Cartera.

### Retirado

- Flujo activo de modernización local del workbook.
- Servicio `app/services/workbook_modernizer.py`.
- Script `scripts/modernizar_workbook_local.py`.
- Script `scripts/cargar_workbook_modernizado.py`.
- Pruebas asociadas al workbook modernizado como flujo activo.

### Notas

- Esta versión no modifica ni guarda archivos Excel.
- Esta versión no implementa búsqueda, filtros, edición, guardado, vencimientos ni DOCX.
- `data/output/` queda reservado para copias, exportaciones o cambios futuros aprobados.

## [1.8.1] - 2026-04-26

### Agregado

- Modelo tabular de solo lectura en `app/ui/table_model.py`.
- Pestaña `Registros` en la GUI para visualizar filas cargadas.
- Conteos visuales de filas cargadas y columnas visibles.
- Pruebas del modelo tabular en `tests/test_gui_table_model.py`.

### Modificado

- Versión interna del paquete actualizada a `1.8.1`.
- La ventana mantiene el resumen y agrega visualización tabular de registros.
- La pestaña `Registros` queda antes de `Resumen`.
- La carga ocurre automáticamente al seleccionar un Control Cartera valido.
- Se elimina el botón visible `Cargar Control Cartera`.
- El flujo activo elimina columnas auxiliares visibles y muestra solo columnas originales.
- El lector carga solo filas útiles con contenido real e ignora filas vacías o solo formateadas.
- Documentación actualizada para reflejar tabla de solo lectura.

### Notas

- Esta versión no implementa búsqueda, filtros, edición ni guardado.
- Esta versión no modifica ni guarda archivos Excel.
- Los datos reales pueden verse solo dentro de la app local cuando el usuario carga su Control Cartera.

## [1.8.0] - 2026-04-25

### Agregado

- Dependencia `PySide6` para interfaz grafica.
- Paquete `app/ui/` con ventana principal inicial.
- GUI para seleccionar y cargar un `Control Cartera` modernizado.
- Panel visual de resumen de carga y advertencias.
- Modo técnico secundario `python -m app --check`.
- Pruebas GUI en `tests/test_gui_main_window.py` usando entorno offscreen.

### Modificado

- `python -m app` ahora abre la interfaz grafica.
- Versión interna del paquete actualizada a `1.8.0`.
- Titulo visible ajustado a `Gestor de Seguros- Dagoberto Quirós Madriz`.
- Terminologia visible ajustada de `workbook` a `Control Cartera`.
- Contraste visual reforzado para tema claro.
- Distribucion visual ajustada con scroll y areas legibles para listas largas.
- Validación previa de ruta y extensión `.xlsx` en la GUI.
- Documentación y manual de usuario actualizados con uso inicial de la GUI.

### Notas

- Esta versión no muestra registros completos.
- Esta versión no modifica ni guarda workbooks.
- Esta versión no implementa búsqueda, filtros, edición, bitácoras, SQLite, DOCX, dashboards ni vencimientos.
- Los scripts técnicos existentes se mantienen disponibles.

## [1.7.0] - 2026-04-25

### Agregado

- Contratos de lectura en `app/domain/workbook_records.py`.
- Servicio de carga controlada en `app/services/workbook_loader.py`.
- Script local `scripts/cargar_workbook_modernizado.py`.
- Pruebas con workbooks ficticios en `tests/test_workbook_loader.py`.
- Validación de hoja `CONTROLCARTERA` y carga de filas útiles sin exigir columnas auxiliares.

### Modificado

- Versión interna del paquete actualizada a `1.7.0`.
- Documentación actualizada con el flujo de lectura controlada del workbook modernizado.

### Notas

- Esta versión no modifica workbooks ni genera archivos de salida.
- Esta versión carga datos reales solo en memoria local cuando el usuario indica la ruta del workbook.
- Esta versión no implementa GUI, búsqueda funcional, edición, bitácoras, SQLite, DOCX, dashboards ni vencimientos.
- La salida por consola es un resumen técnico sin valores reales de filas.

## [1.6.1] - 2026-04-24

### Agregado

- Script local `scripts/limpiar_workbook_operativo.py` para mantenimiento controlado del workbook operativo.
- Respaldo automático previo en `data/backups/workbook_mantenimiento/`.
- Reportes locales de mantenimiento en `data/output/workbook_mantenimiento/`.
- Pruebas con workbooks ficticios en `tests/test_limpiar_workbook_operativo.py`.

### Modificado

- Documentación actualizada con el flujo de limpieza respaldada de la hoja obsoleta.

### Notas

- Esta versión puede modificar `data/input/CONTROLCARTERA_V2.xlsx` solo para eliminar la hoja `Reporte de vencimientos del mes`.
- Esta versión no elimina registros ni modifica datos de clientes, pólizas, identificaciones, placas, teléfonos ni datos operativos.
- Esta versión no implementa generación de vencimientos, GUI, búsqueda, edición, persistencia, DOCX ni dashboards.
- Los respaldos y reportes locales quedan bajo rutas ignoradas por Git.

## [1.6.0] - 2026-04-24

### Agregado

- `requirements.txt` con dependencias minimas de desarrollo y Excel.
- Reglas preliminares puras para workbook en `app/domain/workbook_rules.py`.
- Servicio de modernización local en `app/services/workbook_modernizer.py`.
- Script local `scripts/modernizar_workbook_local.py`.
- Pruebas con workbooks ficticios en `tests/test_workbook_modernizer.py`.
- Generación local de copias `*_modernizado_YYYYMMDD_HHMMSS.xlsx`.
- Reportes locales `resumen_modernizacion.md` y `resumen_modernizacion.json`.

### Modificado

- Versión del paquete actualizada a `1.6.0`.
- Documentación actualizada con uso técnico, arquitectura y pruebas de modernización.

### Notas

- Esta versión no modifica `data/input/CONTROLCARTERA_V2.xlsx`.
- Esta versión no borra registros ni corrige valores originales automáticamente.
- Esta versión no implementa GUI, búsqueda, edición, persistencia, DOCX ni avisos.
- Las salidas reales se generan bajo `data/output/`, ruta ignorada por Git.

## [1.5.0] - 2026-04-24

### Agregado

- Paquete Python base `app/` con entry point ejecutable mediante `python -m app`.
- Bootstrap técnico sin lectura del workbook, sin GUI y sin persistencia.
- Configuración centralizada para nombre, versión, rutas locales y logging.
- Resolucion de rutas del proyecto sin crear carpetas ni tocar datos reales.
- Logging básico en consola sin artefactos persistentes.
- Excepciones técnicas propias del proyecto.
- Contratos preliminares del dataset canónico con clasificación de origen, sensibilidad y editabilidad.
- Servicio de estado técnico no funcional para confirmar capacidades habilitadas.
- Utilidad pequeña para redacción segura de textos técnicos.
- Pruebas automatizadas para entry point, configuración, rutas, logging, excepciones, contratos y utilidad segura.

### Modificado

- `README.md` documenta ejecución técnica y pruebas de la base Python.
- `docs/proyecto/ARQUITECTURA.md` refleja el esqueleto real creado en `app/`.
- `docs/proyecto/DOCUMENTACION_TECNICA.md` documenta bootstrap, configuración, rutas, logging y contratos.
- `docs/proyecto/PLAN_DE_PRUEBAS.md` agrega criterios y pruebas base de `1.5.0`.
- `docs/proyecto/DECISIONES_IMPLEMENTACION_1_5_1_6.md` distingue decisiones cerradas en `1.5.0` y pendientes para `1.6.0`.

### Notas

- Esta versión no lee ni modifica el Excel real.
- Esta versión no implementa GUI, búsqueda, edición, bitácoras, exportaciones, DOCX ni persistencia funcional.
- Esta versión usa solo libreria esténdar de Python y no agrega dependencias.

## [1.4.0] - 2026-04-24

### Agregado

- `docs/proyecto/ESPECIFICACION_DATASET_CANONICO.md` con la especificacion del dataset canónico interno.
- `docs/proyecto/MAPA_ORIGEN_A_CANONICO.md` con el mapeo estructural seguro entre origen y modelo canónico.
- `docs/proyecto/ESTRATEGIA_MODERNIZACION_WORKBOOK.md` con la estrategia de convivencia y modernización gradual del workbook operativo.
- `docs/proyecto/DECISIONES_IMPLEMENTACION_1_5_1_6.md` con decisiones bloqueantes previas a implementación.

### Modificado

- `README.md` para reflejar la fase documental `1.4.0` y el enfoque workbook primero.
- `docs/proyecto/DOCUMENTACION_TECNICA.md` para incorporar el rol del dataset canónico, el mapeo y los límites de la fase.
- `docs/proyecto/ARQUITECTURA.md` para introducir la capa `origen workbook -> normalizacion -> dataset canonico -> app`.
- `docs/proyecto/DICCIONARIO_DE_DATOS.md` para clasificar campos por procedencia, sensibilidad y editabilidad futura.
- `docs/proyecto/PLAN_DE_PRUEBAS.md` para documentar pruebas futuras sobre mapeo, normalización, derivaciones y control de PII.
- `AGENTS.md` para reforzar la distincion entre campos originales, canónicos, derivados, operativos y sensibles.

### Notas

- Esta versión es solo de diseño y documentación.
- Esta versión no implementa lógica funcional de negocio.
- Esta versión no modifica el workbook real ni define aún persistencia operativa.
- Esta versión no introduce GUI, importación funcional ni automatización del workbook.

## [1.3.1] - 2026-04-23

### Corregido

- Saneamiento del reporte de auditoría para evitar exponer valores reales como encabezados.
- Deteccion de encabezados con criterio conservador de confianza.
- Uso de etiquetas técnicas seguras `COL_A`, `COL_B`, etc. cuando un encabezado no es confiable.
- Reportes JSON y Markdown sin almacenamiento de encabezados dudosos o valores de filas.

### Modificado

- Documentos internos movidos a `docs/proyecto/`.
- Referencias internas actualizadas a la nueva ubicacion documental.
- Pruebas reforzadas para casos sin encabezado confiable.
- `.gitignore` mantiene datos, salidas locales y caches fuera de Git.

### Eliminado

- Archivos `.gitkeep` de soporte.
- Referencia a configuración local asistida obsoleta.

## [1.3.2] - 2026-04-23

### Modificado

- Las pruebas de auditoría usan directorios temporales autocontenidos en lugar de `data/output/test_auditoria_unit/`.
- `README.md` y reglas del repositorio reflejan la estructura sobria actual.
- La documentación interna mantiene `docs/proyecto/` como contenedor único de documentos del proyecto.

### Eliminado

- `data/output/test_auditoria_unit/` como artefacto persistente de pruebas.
- `scripts/__pycache__/` y `tests/__pycache__/`.
- `templates/docx/` y `templates/` por no aportar valor en esta etapa.

## [1.3.0] - 2026-04-23

### Agregado

- Script seguro de auditoría local `scripts/auditar_base_local.py`.
- Reportes locales de auditoría en `data/output/auditoria/`, ruta ignorada por Git.
- Pruebas automatizadas con datos ficticios en `tests/test_auditar_base_local.py`.
- Deteccion estructural de hojas, encabezados, dimensiones y completitud por columna.
- Deteccion preliminar de vigencias/frecuencias observadas, incluyendo `D.M.`.
- Clasificacion preliminar de patrónes de número de póliza sin exponer pólizas completas.
- Verificación de campos separados de día, mes y año de vencimiento.

### Modificado

- `docs/proyecto/DOCUMENTACION_TECNICA.md` documenta la auditoría local segura.
- `docs/proyecto/DICCIONARIO_DE_DATOS.md` incorpora notas sobre frecuencias observadas.
- `docs/proyecto/PLAN_DE_PRUEBAS.md` incluye pruebas actuales de la auditoría.
- `README.md` agrega instrucciones de ejecución local.
- `.gitignore` ignora artefactos temporales locales de pytest.

### Notas

- Esta versión no modifica el Excel original.
- Esta versión no importa datos a una base operativa.
- Esta versión no genera interfaz, DOCX ni avisos.
- Los reportes locales no deben subirse a GitHub ni exponerse publicamente.

## [1.2.0] - 2026-04-23

### Agregado

- Estandar de versionado `X.Y.Z`.
- Reglas iniciales de commits, ramas y releases.
- Política de datos confidenciales.
- Política preliminar de anonimización para datos de prueba.
- Reglas de negocio conocidas documentadas como preliminares.
- Lineamientos para documentación del código principal.
- Lineamientos de calidad textual para futura GUI.
- Estrategia futura de revisión funcional, revisión de interfaz y consistencia de datos.

### Modificado

- `README.md` actualizado con versionado y política de confidencialidad.
- `docs/proyecto/DOCUMENTACION_TECNICA.md` fortalecido con esténdares de desarrollo.
- `docs/proyecto/DICCIONARIO_DE_DATOS.md` ampliado con notas preliminares sobre campos reales.
- `docs/proyecto/PLAN_DE_PRUEBAS.md` ampliado con criterios de revisión futura.
- `AGENTS.md` actualizado con reglas maduras para trabajo asistido.

### Notas

- Esta versión no implementa interfaz grafica funcional.
- Esta versión no crea base de datos operativa.
- Esta versión no importa ni modifica datos reales.
- Esta versión no convierte reglas preliminares en validaciones funcionales.

## [1.1.0] - 2026-04-22

### Agregado

- Estructura inicial del repositorio.
- Documentación base del proyecto.
- Arquitectura preliminar.
- Diccionario de datos preliminar.
- Plan de pruebas inicial.
- Reglas de trabajo para agentes y colaboradores.
- Configuración minima de `.gitignore`.

### Notas

- Esta versión no incluye interfaz grafica funcional.
- Esta versión no incluye base de datos operativa.
- Esta versión no incluye importación real de Excel.
- Esta versión no incluye generación real de documentos DOCX.
- Esta versión no incluye lógica de negocio definitiva.
