# Plan de Pruebas

## Objetivo

Definir una estrategia de validación progresiva para asegurar que cada fase del proyecto sea revisable, mantenible y coherente con el alcance aprobado.

## Estrategia general

- Validar primero estructura, documentación y decisiones técnicas.
- Agregar pruebas automatizadas cuando exista código ejecutable.
- Mantener pruebas manuales por fase para flujos de usuario.
- Confirmar que no se introduzcan reglas de negocio no aprobadas.
- Verificar que cualquier eliminación futura exija confirmación explícita.
- Revisar código antes de integrar cambios funcionales.
- Revisar ortografia y consistencia textual cuando exista GUI.
- Verificar consistencia de datos con muestras anonimizadas antes de usar datos reales.

## Pruebas automatizadas futuras

Cuando exista código, se evaluará incorporar `pytest` para:

- validaciones de modelos de datos;
- transformaciones de información;
- reglas de importación;
- generación de reportes;
- generación de documentos;
- operaciones de respaldo;
- pruebas de regresion sobre errores corregidos.

## Pruebas automatizadas actuales

La auditoría local segura cuenta con pruebas en `tests/test_auditar_base_local.py`. La base técnica Python de `1.5.0` cuenta con pruebas en:

- `tests/test_app_entrypoint.py`;
- `tests/test_config_paths_logging.py`;
- `tests/test_contracts.py`;
- `tests/test_limpiar_workbook_operativo.py`.
- `tests/test_workbook_loader.py`.
- `tests/test_gui_main_window.py`.
- `tests/test_gui_table_model.py`.
- `tests/test_gui_filter_proxy_model.py`.
- `tests/test_gui_detail_model.py`.
- `tests/test_gui_detail_dialog.py`.
- `tests/test_gui_edit_dialog.py`.

Ejecución:

```powershell
python -m pytest tests -p no:cacheprovider
```

Las pruebas usan datos ficticios y validan:

- detección de vigencia `D.M.`;
- detección de categorías mensuales, trimestrales, semestrales y anuales;
- clasificación preliminar de pólizas por prefijos `01` y `02`;
- excepcion para pólizas completamente numéricas;
- detección de fecha separada en día, mes y año;
- clasificación conservadora de identificaciones diversas;
- ausencia de datos sensibles de filas en reportes generados;
- uso de etiquetas seguras cuando no hay encabezado confiable;
- utilidad minima del reporte aúnque no se muestren encabezados originales;
- uso de directorios temporales sin dejar salidas permanentes de prueba en el proyecto.

Las pruebas de `1.5.0` validan:

- importación del paquete `app`;
- ejecución de `python -m app`;
- bootstrap técnico sin flujos de negocio;
- configuración y resolucion de rutas sin crear artefactos;
- logging de consola sin archivos persistentes;
- excepciones técnicas propias;
- contratos preliminares del dataset canónico;
- utilidad de redacción segura para textos técnicos.

Las pruebas de `1.6.0` validan:

- decision documental de retirar la modernización como flujo activo desde `1.8.2`;
- reserva de `data/output/` para copias, exportaciones o cambios futuros aprobados;
- ausencia de dependencia de copias modernizadas para visualizar datos.

Las pruebas de `1.6.1` validan:

- creacion de respaldo antes de modificar un workbook ficticio;
- eliminación exclusiva de la hoja obsoleta cuando existe;
- conservacion de otras hojas y datos de la hoja principal;
- comportamiento no destructivo cuando la hoja obsoleta no existe;
- generación de reportes locales Markdown y JSON;
- ausencia de datos de filas en reportes de prueba.

Las pruebas de lectura controlada validan:

- carga correcta de un Control Cartera ficticio;
- resolucion de la ruta predeterminada `data/input/CONTROLCARTERA_V2.xlsx`;
- validación de archivo inexistente y extensión incorrecta;
- detección de hoja `CONTROLCARTERA`;
- error controlado cuando falta la hoja principal;
- carga sin exigir columnas técnicas auxiliares;
- ocultamiento de columnas técnicas auxiliares si aparecen;
- conteo de filas útiles e ignorado de filas vacías o solo formateadas;
- salida de consola sin valores sensibles ficticios;
- ausencia de modificaciones al workbook fuente;
- ausencia de salidas permanentes innecesarias.

Las pruebas de `1.8.0` validan:

- importación e instanciacion de la ventana principal PySide6;
- titulo de ventana y versión visible;
- presencia de botónes principales;
- estado inicial;
- carga simulada con loader controlado;
- validación de archivo inexistente y extensión distinta de `.xlsx`;
- carga de la ruta predeterminada desde `data/input/`;
- carga automática al seleccionar una ruta `.xlsx` valida;
- ventanas emergentes amigables para errores de archivo y carga;
- area de resumen con soporte para texto largo;
- visualización de resumen sin registros completos;
- errores amigables por falta de archivo o error del loader;
- modo técnico `python -m app --check`.

Las pruebas de `1.8.1` validan:

- modelo tabular con registros ficticios;
- conteo correcto de filas y columnas;
- encabezados de columnas;
- valores convertidos a texto;
- flags de solo lectura;
- ausencia de columnas auxiliares en la tabla;
- pestaña `Registros` antes de `Resumen`;
- ausencia del botón `Cargar Control Cartera`;
- carga automática al seleccionar archivo valido;
- pestaña y tabla de registros en la GUI;
- tabla vacia antes de cargar datos;
- actualizacion de tabla tras carga simulada;
- conteos visuales de filas y columnas;
- ausencia de uso del Excel real.

Las pruebas de `1.8.2` validan:

- versión interna `1.8.2`;
- GUI con acción `Cargar predeterminado`;
- lectura directa de Control Cartera desde ruta de input;
- script `scripts/cargar_control_cartera.py`;
- ausencia de dependencia de `data/output/workbook_modernizado/`;
- ausencia de generación de archivos Excel o reportes de modernización.
- cancelacion del selector sin mensaje, sin error y sin limpiar datos cargados;
- ausencia de seccion visual `Advertencias` en la pestaña `Resumen`;
- mantenimiento de `QMessageBox` solo para errores reales de archivo o carga.

Las pruebas de `1.8.3` validan:

- versión interna `1.8.3`;
- existencia del botón compacto de tema;
- aplicación de tema claro y tema oscuro;
- persistencia local del tema con `QSettings`;
- cambio de tema sin limpiar registros cargados;
- mantenimiento de pestañas `Registros` y `Resumen` en el orden esperado;
- tabla en modo solo lectura;
- ausencia de seccion visual `Advertencias`;
- ausencia de modificaciones sobre archivos Excel.

Las pruebas de `1.8.4` validan:

- versión interna `1.8.4`;
- existencia de `assets/app_icon.svg`;
- resolucion de ruta del ícono mediante `app/ui/assets.py`;
- carga no nula del ícono con `QIcon`;
- ventana principal instanciada con ícono configurado;
- mantenimiento de `python -m app --check`;
- ausencia de modificaciones sobre archivos Excel.

Las pruebas de `1.9.0` validan:

- versión interna `1.9.0`;
- modelo proxy de búsqueda con datos ficticios;
- búsqueda general en todas las columnas;
- búsqueda por columna específica;
- búsqueda sin coincidencias;
- búsqueda vacía que muestra todos los registros;
- tolerancia básica a mayúsculas, minúsculas y tildes;
- manejo de valores vacíos o `None`;
- filtrado sin modificar los registros originales;
- presencia de campo `Buscar`, selector `Buscar en`, botón `Limpiar` y contador de resultados;
- actualización del contador al cargar, buscar y limpiar;
- limpieza de búsqueda al cargar un nuevo Control Cartera;
- conservación de búsqueda y registros al cambiar tema;
- mantenimiento de tabla en modo solo lectura y sin panel visual de advertencias.

Las pruebas de `1.9.1` validan:

- versión interna `1.9.1`;
- modelo de detalle con campos y valores de registros ficticios;
- omisión de campos vacíos en la ventana de detalle;
- flags de solo lectura en el detalle;
- existencia de la ventana `Detalle del registro`;
- apertura del detalle con doble clic o método equivalente;
- compatibilidad del detalle con filtros activos;
- comportamiento seguro cuando no hay índice válido;
- mantenimiento de búsqueda, tabla de solo lectura y ausencia de modificaciones sobre archivos Excel.

Las pruebas de `1.10.0` validan:

- versión interna `1.10.0`;
- actualización controlada de valores en memoria desde el modelo tabular;
- conteo de cambios pendientes no guardados;
- conservación de encabezados y registros ajenos;
- ventana `Editar registro` con campos editables y confirmación previa;
- cancelación de edición sin aplicar cambios;
- aplicación de cambios con actualización de tabla en memoria;
- mantenimiento de búsqueda y filtros después de editar;
- indicador visual `Cambios pendientes: X`;
- advertencia antes de cargar otro Control Cartera cuando existen cambios pendientes;
- tabla principal en modo solo lectura;
- ausencia de guardado, eliminación y modificaciones sobre archivos Excel.

Para el release técnico `v1.8.4-alpha` se debe validar:

- ejecución completa de `python -m pytest tests -p no:cacheprovider`;
- apertura manual de la app con `python -m app`;
- carga manual del Control Cartera local;
- tabla en modo solo lectura;
- cambio de tema claro/oscuro;
- ícono aplicado a la ventana;
- ausencia de datos reales versionados;
- ausencia de archivos de `data/input/`, `data/output/` o `data/backups/` en Git;
- ausencia de ejecutables, instaladores o binarios de release.

Cuando se implemente guardado persistente, deberán agregarse pruebas especificas para bitácoras o pistas de auditoría: registro de fecha y hora, campo modificado, valor anterior, valor nuevo, origen del cambio, usuario local si aplica, archivo afectado y resultado de la operación.

## Revisión de código futura

Cuando exista código, cada cambio relevante deberá revisar:

- claridad de nombres y responsabilidades;
- modularidad y separacion de capas;
- ausencia de dependencias innecesarias;
- comentarios o docstrings en código principal cuando aporten contexto;
- manejo conservador de datos;
- ausencia de datos reales en pruebas, capturas o archivos versionados.

## Revisión de interfaz futura

Cuando exista GUI, cada fase deberá validar:

- ortografia en textos visibles;
- consistencia de terminos;
- mensajes de error y confirmación claros;
- confirmación explícita antes de eliminar información;
- visualización consistente de colones y dólares;
- respeto por nombres originales de registros importados.

## Pruebas funcionales futuras

Las pruebas funcionales se definirán por módulo y versión. Deberan cubrir flujos completos cuando existan pantallas, persistencia, importación, reportes o documentos.

## Consistencia de datos futura

La validación de datos deberá confirmar que:

- los registros importados conservan nombres originales;
- no se pierden registros con formatos no esperados;
- las relaciones entre clientes, pólizas y vencimientos son trazables;
- los datos anonimizados no contienen información sensible real;
- los respaldos no sustituyen ni borran información sin confirmación.

## Casos futuros sobre dataset canónico

Cuando se implemente la capa correspondiente, deberán definirse pruebas para:

- mapeo origen -> canónico sin pérdida de trazabilidad;
- separacion entre campos originales, normalizados, derivados y operativos;
- clasificación correcta de sensibilidad y editabilidad futura;
- consolidación de fecha de vencimiento desde fecha única o partes;
- normalización de frecuencia sin forzar reglas no aprobadas;
- derivacion preliminar de moneda con excepcion para riesgos del trabajo;
- preservacion del valor original aúnque exista versión normalizada;
- manejo conservador de `detalle` como campo potencialmente sensible;
- ausencia de PII en salidas documentales, técnicas y de depuracion.

## Casos futuros especificos

Cuando se implemente la lógica correspondiente, se deberán diseñar pruebas para:

- pólizas con vigencia `D.M.`;
- confirmación de que `D.M.` se almacena aúnque no genere avisos;
- multiples formatos de `Numero de Poliza`;
- identificaciones fisicas, juridicas, pasaportes e identificaciones de extranjero;
- fechas de vencimiento separadas en día, mes y año;
- consistencia entre cliente, pólizas y `detalle`;
- uso de `Numero de Placa / Finca`;
- regla preliminar de moneda por prefijos `01` y `02`;
- excepcion de riesgos del trabajo para pólizas completamente numéricas;
- anonimización de datos de prueba.

## Pruebas manuales por fase

Cada versión deberá contar con una lista de validaciones manuales alineadas al alcance. Ejemplos futuros:

- abrir la aplicación;
- cargar datos de muestra;
- revisar listados;
- generar documentos por cliente;
- validar monedas CRC y USD;
- confirmar mensajes antes de operaciones destructivas;
- crear y verificar respaldos.

## Validaciones minimas de esta fase

- Existe la estructura base de carpetas solicitada.
- Existen los documentos base del proyecto.
- La documentación indica que el sistema está en construcción.
- No se implementa interfaz grafica funcional.
- No se implementa base de datos operativa.
- No se implementa importación real de Excel.
- No se implementa generación real de DOCX.
- No se implementa lógica de vencimientos.
- Se documentan supuestos conservadores.
- `.gitignore` excluye artefactos locales y temporales comunes.
- La política de confidencialidad queda documentada.
- Las reglas de negocio conocidas quedan documentadas sin implementación funcional.

## Validaciones minimas de auditoría local segura

- El script acepta ruta de entrada y ruta de salida.
- El Excel original no se modifica.
- Los reportes se generan en una ruta local ignorada por Git.
- Los reportes no incluyen muestras de filas ni valores sensibles.
- Los encabezados no confirmados se reportan como `COL_A`, `COL_B`, etc.
- Las categorías de vigencia o frecuencia se documentan como observadas y preliminares.
- Las pruebas automatizadas usan datos ficticios.
- Las pruebas no dejan artefactos permanentes en `data/output/`.

## Criterio de salida de 1.4.0

La fase `1.4.0` se considera lista cuando:

- el dataset canónico queda documentado de forma revisable;
- el mapeo origen -> canónico queda definido sin exponer datos sensibles;
- la estrategia de modernización del workbook queda explícita;
- las decisiones bloqueantes para `1.5.0` y `1.6.0` quedan identificadas;
- no existen cambios funcionales fuera del alcance.

## Criterio de salida de 1.5.0

La fase `1.5.0` se considera lista cuando:

- `python -m app` ejecuta correctamente;
- el paquete `app` es importable;
- existen pruebas automatizadas para configuración, rutas, logging, bootstrap y contratos;
- no se lee ni modifica el Excel real;
- no se implementa GUI, persistencia, búsqueda, edición, exportacion ni DOCX;
- la documentación técnica queda alineada con la estructura creada.

## Criterio de salida de 1.6.0

La fase `1.6.0` se considera lista cuando:

- el workbook original no cambia;
- se documenta que este flujo queda retirado como dependencia activa desde `1.8.2`;
- `data/output/` queda reservado para copias o exportaciones futuras;
- no se agregan columnas auxiliares visibles;
- las pruebas automatizadas pasan con datos ficticios;
- no se versionan salidas con datos reales.

## Criterio de salida de 1.6.1

La fase `1.6.1` se considera lista cuando:

- se crea un respaldo local antes de modificar el workbook operativo;
- solo se elimina la hoja `Reporte de vencimientos del mes`, si existe;
- no se modifican registros de la hoja principal;
- se generan reportes locales de mantenimiento;
- las pruebas automatizadas pasan con workbooks ficticios;
- no se versionan respaldos, reportes locales ni datos reales.

## Criterio de salida de 1.7.0

La fase `1.7.0` se considera lista cuando:

- el lector carga un Control Cartera indicado por ruta;
- la estructura se valida sin guardar cambios en Excel;
- no se exigen columnas auxiliares para cargar;
- se ignoran filas vacías o solo formateadas;
- los registros se cargan solo en memoria;
- el script no imprime valores reales de filas;
- las pruebas automatizadas pasan con datos ficticios;
- no se generan salidas permanentes innecesarias.

## Criterio de salida de 1.8.0

La fase `1.8.0` se considera lista cuando:

- `python -m app` abre la interfaz grafica;
- la ventana permite seleccionar y cargar un Control Cartera;
- el resumen visual no muestra registros completos ni valores sensibles de filas;
- los errores se muestran de forma amigable;
- no se modifica ningun workbook;
- las pruebas automatizadas pasan en modo offscreen;
- la documentación y el manual de usuario quedan actualizados.

## Criterio de salida de 1.8.1

La fase `1.8.1` se considera lista cuando:

- la GUI conserva carga de Control Cartera;
- después de cargar, los registros se muestran en tabla;
- la tabla es solo lectura;
- la tabla permite desplazamiento vertical y horizontal;
- se muestran conteos de filas cargadas y columnas visibles;
- no se modifica ningun Excel;
- no se implementa búsqueda, filtros, edición ni guardado;
- las pruebas automatizadas pasan.

## Criterio de salida de 1.8.2

La fase `1.8.2` se considera lista cuando:

- la app puede cargar `data/input/CONTROLCARTERA_V2.xlsx`;
- la app no depende de `data/output/workbook_modernizado/`;
- no se generan columnas técnicas auxiliares;
- los errores de archivo y carga muestran mensajes amigables;
- solo se cargan filas útiles;
- no se modifica ni guarda ningun Excel;
- no se implementa búsqueda, filtros, edición ni guardado;
- las pruebas automatizadas pasan.

## Criterio de salida de 1.9.0

La fase `1.9.0` se considera lista cuando:

- la GUI permite buscar en todas las columnas visibles;
- la GUI permite buscar en una columna específica del Control Cartera cargado;
- el botón `Limpiar` restaura todos los registros cargados;
- el contador `Mostrando X de Y registros` refleja el filtro activo;
- cargar un nuevo Control Cartera limpia la búsqueda y actualiza el selector de columnas;
- cambiar tema conserva datos y búsqueda activa;
- la tabla se mantiene en modo solo lectura;
- no se modifica ni guarda ningún Excel;
- no se implementa edición, guardado ni vista de detalle;
- las pruebas automatizadas pasan.

## Criterio de salida de 1.9.1

La fase `1.9.1` se considera lista cuando:

- la GUI mantiene búsqueda y filtros de `1.9.0`;
- al hacer doble clic sobre una fila se abre `Detalle del registro`;
- el detalle corresponde al registro correcto incluso con filtros activos;
- los campos vacíos no se muestran en el detalle;
- el detalle se mantiene en modo solo lectura;
- no se modifica ni guarda ningún Excel;
- no se implementa edición ni guardado;
- las pruebas automatizadas pasan.

## Criterio de salida de 1.10.0

La fase `1.10.0` se considera lista cuando:

- la GUI mantiene búsqueda, filtros y detalle de fases anteriores;
- desde `Detalle del registro` se puede abrir `Editar registro`;
- cancelar la edición no modifica datos en memoria;
- aplicar cambios actualiza la tabla solo en memoria;
- se muestra indicador de cambios pendientes;
- cargar otro Control Cartera o cerrar la app con cambios pendientes muestra advertencia;
- la tabla principal se mantiene en modo solo lectura;
- no se modifica ni guarda ningún Excel;
- no se implementa eliminación de registros;
- las pruebas automatizadas pasan.
