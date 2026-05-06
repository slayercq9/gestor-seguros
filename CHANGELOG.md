# Changelog

Todos los cambios relevantes del proyecto se documentaran en este archivo.

El formato seguira una estructura por versiones, con secciones para cambios agregados, modificados, corregidos y decisiones importantes cuando aplique.

## [v1.8.4-alpha] - 2026-05-06

### Agregado

- Primer documento de release tecnico inicial en `docs/releases/v1.8.4-alpha.md`.
- Checklist de validacion para publicar el release en GitHub.
- Release notes breves listas para copiar en GitHub.

### Notas

- La version interna de la app se mantiene en `1.8.4`.
- Este release no incluye ejecutable, instalador ni artefactos binarios.
- Este release no incluye datos reales ni archivos confidenciales.
- Esta preparacion no modifica logica funcional de la aplicacion.

## [1.8.4] - 2026-05-05

### Agregado

- Icono profesional propio en `assets/app_icon.svg`.
- Utilidad `app/ui/assets.py` para resolver assets en desarrollo y en futuros empaquetados con PyInstaller.
- Aplicacion del icono a `QApplication` y a la ventana principal.
- Pruebas para validar existencia, resolucion y carga del icono.

### Modificado

- Version interna del paquete actualizada a `1.8.4`.
- Documentacion actualizada para indicar que el icono no usa logos oficiales ni marcas externas.

### Notas

- Esta version no modifica ni guarda archivos Excel.
- Esta version no implementa busqueda, filtros, edicion, guardado, bitacoras, vencimientos, DOCX, instalador ni release.

## [1.8.3] - 2026-05-05

### Agregado

- Boton compacto para alternar tema claro/oscuro en la ventana principal.
- Persistencia local de la preferencia de tema mediante `QSettings`.
- Modulo `app/ui/theme.py` para centralizar estilos visuales de la GUI.

### Modificado

- Version interna del paquete actualizada a `1.8.3`.
- Estilos de ventana, botones, pestanas, tabla, encabezados y barra de estado ajustados para tema claro y oscuro.
- Pruebas GUI ampliadas para validar cambio de tema, persistencia local y conservacion de registros cargados.
- Documentacion actualizada con el uso del control de tema.

### Notas

- Esta version no modifica ni guarda archivos Excel.
- Esta version no implementa busqueda, filtros, edicion, guardado, bitacoras, icono profesional, vencimientos ni DOCX.

## [1.8.2] - 2026-05-05

### Agregado

- Accion `Cargar predeterminado` en la GUI para leer `data/input/CONTROLCARTERA_V2.xlsx`.
- Script `scripts/cargar_control_cartera.py` para carga tecnica directa del Control Cartera operativo.
- Ventanas emergentes amigables para errores de archivo, formato y carga.

### Modificado

- Version interna del paquete actualizada a `1.8.2`.
- La app deja de depender de `data/output/workbook_modernizado/` para visualizar datos.
- El lector se orienta al Control Cartera operativo de `data/input/`.
- La documentacion vigente define `data/input/CONTROLCARTERA_V2.xlsx` como fuente activa.
- Las pruebas cubren lectura directa, ruta predeterminada, filas utiles y dialogos de error.
- Cancelar la seleccion de archivo en la GUI conserva el estado anterior sin mostrar error ni limpiar registros.
- La pestana `Resumen` deja de mostrar una seccion visual de advertencias y conserva solo conteos, modo y estado de carga.
- La documentacion registra la necesidad futura de un modulo de bitacoras o pistas de auditoria para cambios sobre el Control Cartera.

### Retirado

- Flujo activo de modernizacion local del workbook.
- Servicio `app/services/workbook_modernizer.py`.
- Script `scripts/modernizar_workbook_local.py`.
- Script `scripts/cargar_workbook_modernizado.py`.
- Pruebas asociadas al workbook modernizado como flujo activo.

### Notas

- Esta version no modifica ni guarda archivos Excel.
- Esta version no implementa busqueda, filtros, edicion, guardado, vencimientos ni DOCX.
- `data/output/` queda reservado para copias, exportaciones o cambios futuros aprobados.

## [1.8.1] - 2026-04-26

### Agregado

- Modelo tabular de solo lectura en `app/ui/table_model.py`.
- Pestaña `Registros` en la GUI para visualizar filas cargadas.
- Conteos visuales de filas cargadas y columnas visibles.
- Pruebas del modelo tabular en `tests/test_gui_table_model.py`.

### Modificado

- Version interna del paquete actualizada a `1.8.1`.
- La ventana mantiene el resumen y agrega visualizacion tabular de registros.
- La pestana `Registros` queda antes de `Resumen`.
- La carga ocurre automaticamente al seleccionar un Control Cartera valido.
- Se elimina el boton visible `Cargar Control Cartera`.
- El flujo activo elimina columnas auxiliares visibles y muestra solo columnas originales.
- El lector carga solo filas utiles con contenido real e ignora filas vacias o solo formateadas.
- Documentacion actualizada para reflejar tabla de solo lectura.

### Notas

- Esta version no implementa busqueda, filtros, edicion ni guardado.
- Esta version no modifica ni guarda archivos Excel.
- Los datos reales pueden verse solo dentro de la app local cuando el usuario carga su Control Cartera.

## [1.8.0] - 2026-04-25

### Agregado

- Dependencia `PySide6` para interfaz grafica.
- Paquete `app/ui/` con ventana principal inicial.
- GUI para seleccionar y cargar un `Control Cartera` modernizado.
- Panel visual de resumen de carga y advertencias.
- Modo tecnico secundario `python -m app --check`.
- Pruebas GUI en `tests/test_gui_main_window.py` usando entorno offscreen.

### Modificado

- `python -m app` ahora abre la interfaz grafica.
- Version interna del paquete actualizada a `1.8.0`.
- Titulo visible ajustado a `Gestor de Seguros- Dagoberto Quirós Madriz`.
- Terminologia visible ajustada de `workbook` a `Control Cartera`.
- Contraste visual reforzado para tema claro.
- Distribucion visual ajustada con scroll y areas legibles para listas largas.
- Validacion previa de ruta y extension `.xlsx` en la GUI.
- Documentacion y manual de usuario actualizados con uso inicial de la GUI.

### Notas

- Esta version no muestra registros completos.
- Esta version no modifica ni guarda workbooks.
- Esta version no implementa busqueda, filtros, edicion, bitacoras, SQLite, DOCX, dashboards ni vencimientos.
- Los scripts tecnicos existentes se mantienen disponibles.

## [1.7.0] - 2026-04-25

### Agregado

- Contratos de lectura en `app/domain/workbook_records.py`.
- Servicio de carga controlada en `app/services/workbook_loader.py`.
- Script local `scripts/cargar_workbook_modernizado.py`.
- Pruebas con workbooks ficticios en `tests/test_workbook_loader.py`.
- Validacion de hoja `CONTROLCARTERA` y carga de filas utiles sin exigir columnas auxiliares.

### Modificado

- Version interna del paquete actualizada a `1.7.0`.
- Documentacion actualizada con el flujo de lectura controlada del workbook modernizado.

### Notas

- Esta version no modifica workbooks ni genera archivos de salida.
- Esta version carga datos reales solo en memoria local cuando el usuario indica la ruta del workbook.
- Esta version no implementa GUI, busqueda funcional, edicion, bitacoras, SQLite, DOCX, dashboards ni vencimientos.
- La salida por consola es un resumen tecnico sin valores reales de filas.

## [1.6.1] - 2026-04-24

### Agregado

- Script local `scripts/limpiar_workbook_operativo.py` para mantenimiento controlado del workbook operativo.
- Respaldo automatico previo en `data/backups/workbook_mantenimiento/`.
- Reportes locales de mantenimiento en `data/output/workbook_mantenimiento/`.
- Pruebas con workbooks ficticios en `tests/test_limpiar_workbook_operativo.py`.

### Modificado

- Documentacion actualizada con el flujo de limpieza respaldada de la hoja obsoleta.

### Notas

- Esta version puede modificar `data/input/CONTROLCARTERA_V2.xlsx` solo para eliminar la hoja `Reporte de vencimientos del mes`.
- Esta version no elimina registros ni modifica datos de clientes, polizas, identificaciones, placas, telefonos ni datos operativos.
- Esta version no implementa generacion de vencimientos, GUI, busqueda, edicion, persistencia, DOCX ni dashboards.
- Los respaldos y reportes locales quedan bajo rutas ignoradas por Git.

## [1.6.0] - 2026-04-24

### Agregado

- `requirements.txt` con dependencias minimas de desarrollo y Excel.
- Reglas preliminares puras para workbook en `app/domain/workbook_rules.py`.
- Servicio de modernizacion local en `app/services/workbook_modernizer.py`.
- Script local `scripts/modernizar_workbook_local.py`.
- Pruebas con workbooks ficticios en `tests/test_workbook_modernizer.py`.
- Generacion local de copias `*_modernizado_YYYYMMDD_HHMMSS.xlsx`.
- Reportes locales `resumen_modernizacion.md` y `resumen_modernizacion.json`.

### Modificado

- Version del paquete actualizada a `1.6.0`.
- Documentacion actualizada con uso tecnico, arquitectura y pruebas de modernizacion.

### Notas

- Esta version no modifica `data/input/CONTROLCARTERA_V2.xlsx`.
- Esta version no borra registros ni corrige valores originales automaticamente.
- Esta version no implementa GUI, busqueda, edicion, persistencia, DOCX ni avisos.
- Las salidas reales se generan bajo `data/output/`, ruta ignorada por Git.

## [1.5.0] - 2026-04-24

### Agregado

- Paquete Python base `app/` con entry point ejecutable mediante `python -m app`.
- Bootstrap tecnico sin lectura del workbook, sin GUI y sin persistencia.
- Configuracion centralizada para nombre, version, rutas locales y logging.
- Resolucion de rutas del proyecto sin crear carpetas ni tocar datos reales.
- Logging basico en consola sin artefactos persistentes.
- Excepciones tecnicas propias del proyecto.
- Contratos preliminares del dataset canonico con clasificacion de origen, sensibilidad y editabilidad.
- Servicio de estado tecnico no funcional para confirmar capacidades habilitadas.
- Utilidad pequena para redaccion segura de textos tecnicos.
- Pruebas automatizadas para entry point, configuracion, rutas, logging, excepciones, contratos y utilidad segura.

### Modificado

- `README.md` documenta ejecucion tecnica y pruebas de la base Python.
- `docs/proyecto/ARQUITECTURA.md` refleja el esqueleto real creado en `app/`.
- `docs/proyecto/DOCUMENTACION_TECNICA.md` documenta bootstrap, configuracion, rutas, logging y contratos.
- `docs/proyecto/PLAN_DE_PRUEBAS.md` agrega criterios y pruebas base de `1.5.0`.
- `docs/proyecto/DECISIONES_IMPLEMENTACION_1_5_1_6.md` distingue decisiones cerradas en `1.5.0` y pendientes para `1.6.0`.

### Notas

- Esta version no lee ni modifica el Excel real.
- Esta version no implementa GUI, busqueda, edicion, bitacoras, exportaciones, DOCX ni persistencia funcional.
- Esta version usa solo libreria estandar de Python y no agrega dependencias.

## [1.4.0] - 2026-04-24

### Agregado

- `docs/proyecto/ESPECIFICACION_DATASET_CANONICO.md` con la especificacion del dataset canonico interno.
- `docs/proyecto/MAPA_ORIGEN_A_CANONICO.md` con el mapeo estructural seguro entre origen y modelo canonico.
- `docs/proyecto/ESTRATEGIA_MODERNIZACION_WORKBOOK.md` con la estrategia de convivencia y modernizacion gradual del workbook operativo.
- `docs/proyecto/DECISIONES_IMPLEMENTACION_1_5_1_6.md` con decisiones bloqueantes previas a implementacion.

### Modificado

- `README.md` para reflejar la fase documental `1.4.0` y el enfoque workbook primero.
- `docs/proyecto/DOCUMENTACION_TECNICA.md` para incorporar el rol del dataset canonico, el mapeo y los limites de la fase.
- `docs/proyecto/ARQUITECTURA.md` para introducir la capa `origen workbook -> normalizacion -> dataset canonico -> app`.
- `docs/proyecto/DICCIONARIO_DE_DATOS.md` para clasificar campos por procedencia, sensibilidad y editabilidad futura.
- `docs/proyecto/PLAN_DE_PRUEBAS.md` para documentar pruebas futuras sobre mapeo, normalizacion, derivaciones y control de PII.
- `AGENTS.md` para reforzar la distincion entre campos originales, canonicos, derivados, operativos y sensibles.

### Notas

- Esta version es solo de diseno y documentacion.
- Esta version no implementa logica funcional de negocio.
- Esta version no modifica el workbook real ni define aun persistencia operativa.
- Esta version no introduce GUI, importacion funcional ni automatizacion del workbook.

## [1.3.1] - 2026-04-23

### Corregido

- Saneamiento del reporte de auditoria para evitar exponer valores reales como encabezados.
- Deteccion de encabezados con criterio conservador de confianza.
- Uso de etiquetas tecnicas seguras `COL_A`, `COL_B`, etc. cuando un encabezado no es confiable.
- Reportes JSON y Markdown sin almacenamiento de encabezados dudosos o valores de filas.

### Modificado

- Documentos internos movidos a `docs/proyecto/`.
- Referencias internas actualizadas a la nueva ubicacion documental.
- Pruebas reforzadas para casos sin encabezado confiable.
- `.gitignore` mantiene datos, salidas locales y caches fuera de Git.

### Eliminado

- Archivos `.gitkeep` de soporte.
- Referencia a configuracion local asistida obsoleta.

## [1.3.2] - 2026-04-23

### Modificado

- Las pruebas de auditoria usan directorios temporales autocontenidos en lugar de `data/output/test_auditoria_unit/`.
- `README.md` y reglas del repositorio reflejan la estructura sobria actual.
- La documentacion interna mantiene `docs/proyecto/` como contenedor unico de documentos del proyecto.

### Eliminado

- `data/output/test_auditoria_unit/` como artefacto persistente de pruebas.
- `scripts/__pycache__/` y `tests/__pycache__/`.
- `templates/docx/` y `templates/` por no aportar valor en esta etapa.

## [1.3.0] - 2026-04-23

### Agregado

- Script seguro de auditoria local `scripts/auditar_base_local.py`.
- Reportes locales de auditoria en `data/output/auditoria/`, ruta ignorada por Git.
- Pruebas automatizadas con datos ficticios en `tests/test_auditar_base_local.py`.
- Deteccion estructural de hojas, encabezados, dimensiones y completitud por columna.
- Deteccion preliminar de vigencias/frecuencias observadas, incluyendo `D.M.`.
- Clasificacion preliminar de patrones de numero de poliza sin exponer polizas completas.
- Verificacion de campos separados de dia, mes y ano de vencimiento.

### Modificado

- `docs/proyecto/DOCUMENTACION_TECNICA.md` documenta la auditoria local segura.
- `docs/proyecto/DICCIONARIO_DE_DATOS.md` incorpora notas sobre frecuencias observadas.
- `docs/proyecto/PLAN_DE_PRUEBAS.md` incluye pruebas actuales de la auditoria.
- `README.md` agrega instrucciones de ejecucion local.
- `.gitignore` ignora artefactos temporales locales de pytest.

### Notas

- Esta version no modifica el Excel original.
- Esta version no importa datos a una base operativa.
- Esta version no genera interfaz, DOCX ni avisos.
- Los reportes locales no deben subirse a GitHub ni exponerse publicamente.

## [1.2.0] - 2026-04-23

### Agregado

- Estandar de versionado `X.Y.Z`.
- Reglas iniciales de commits, ramas y releases.
- Politica de datos confidenciales.
- Politica preliminar de anonimizacion para datos de prueba.
- Reglas de negocio conocidas documentadas como preliminares.
- Lineamientos para documentacion del codigo principal.
- Lineamientos de calidad textual para futura GUI.
- Estrategia futura de revision funcional, revision de interfaz y consistencia de datos.

### Modificado

- `README.md` actualizado con versionado y politica de confidencialidad.
- `docs/proyecto/DOCUMENTACION_TECNICA.md` fortalecido con estandares de desarrollo.
- `docs/proyecto/DICCIONARIO_DE_DATOS.md` ampliado con notas preliminares sobre campos reales.
- `docs/proyecto/PLAN_DE_PRUEBAS.md` ampliado con criterios de revision futura.
- `AGENTS.md` actualizado con reglas maduras para trabajo asistido.

### Notas

- Esta version no implementa interfaz grafica funcional.
- Esta version no crea base de datos operativa.
- Esta version no importa ni modifica datos reales.
- Esta version no convierte reglas preliminares en validaciones funcionales.

## [1.1.0] - 2026-04-22

### Agregado

- Estructura inicial del repositorio.
- Documentacion base del proyecto.
- Arquitectura preliminar.
- Diccionario de datos preliminar.
- Plan de pruebas inicial.
- Reglas de trabajo para agentes y colaboradores.
- Configuracion minima de `.gitignore`.

### Notas

- Esta version no incluye interfaz grafica funcional.
- Esta version no incluye base de datos operativa.
- Esta version no incluye importacion real de Excel.
- Esta version no incluye generacion real de documentos DOCX.
- Esta version no incluye logica de negocio definitiva.
