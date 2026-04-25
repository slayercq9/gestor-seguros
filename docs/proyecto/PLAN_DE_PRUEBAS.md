# Plan de Pruebas

## Objetivo

Definir una estrategia de validacion progresiva para asegurar que cada fase del proyecto sea revisable, mantenible y coherente con el alcance aprobado.

## Estrategia general

- Validar primero estructura, documentacion y decisiones tecnicas.
- Agregar pruebas automatizadas cuando exista codigo ejecutable.
- Mantener pruebas manuales por fase para flujos de usuario.
- Confirmar que no se introduzcan reglas de negocio no aprobadas.
- Verificar que cualquier eliminacion futura exija confirmacion explicita.
- Revisar codigo antes de integrar cambios funcionales.
- Revisar ortografia y consistencia textual cuando exista GUI.
- Verificar consistencia de datos con muestras anonimizadas antes de usar datos reales.

## Pruebas automatizadas futuras

Cuando exista codigo, se evaluara incorporar `pytest` para:

- validaciones de modelos de datos;
- transformaciones de informacion;
- reglas de importacion;
- generacion de reportes;
- generacion de documentos;
- operaciones de respaldo;
- pruebas de regresion sobre errores corregidos.

## Pruebas automatizadas actuales

La auditoria local segura cuenta con pruebas en `tests/test_auditar_base_local.py`. La base tecnica Python de `1.5.0` cuenta con pruebas en:

- `tests/test_app_entrypoint.py`;
- `tests/test_config_paths_logging.py`;
- `tests/test_contracts.py`;
- `tests/test_workbook_modernizer.py`.
- `tests/test_limpiar_workbook_operativo.py`.
- `tests/test_workbook_loader.py`.

Ejecucion:

```powershell
python -m pytest tests -p no:cacheprovider
```

Las pruebas usan datos ficticios y validan:

- deteccion de vigencia `D.M.`;
- deteccion de categorias mensuales, trimestrales, semestrales y anuales;
- clasificacion preliminar de polizas por prefijos `01` y `02`;
- excepcion para polizas completamente numericas;
- deteccion de fecha separada en dia, mes y ano;
- clasificacion conservadora de identificaciones diversas;
- ausencia de datos sensibles de filas en reportes generados;
- uso de etiquetas seguras cuando no hay encabezado confiable;
- utilidad minima del reporte aunque no se muestren encabezados originales;
- uso de directorios temporales sin dejar salidas permanentes de prueba en el proyecto.

Las pruebas de `1.5.0` validan:

- importacion del paquete `app`;
- ejecucion de `python -m app`;
- bootstrap tecnico sin flujos de negocio;
- configuracion y resolucion de rutas sin crear artefactos;
- logging de consola sin archivos persistentes;
- excepciones tecnicas propias;
- contratos preliminares del dataset canonico;
- utilidad de redaccion segura para textos tecnicos.

Las pruebas de `1.6.0` validan:

- generacion de copia modernizada sin alterar la fuente;
- columnas auxiliares `GS_*` esperadas;
- deteccion de `D.M.`;
- moneda preliminar por prefijos `01` y `02`;
- excepcion de polizas completamente numericas;
- consolidacion valida de fecha;
- marcas de revision para datos incompletos o ambiguos;
- reportes locales y `control_revision.csv` sin valores sensibles ficticios;
- formato visual basico y hoja de control;
- error controlado ante entrada inexistente.

Las pruebas de `1.6.1` validan:

- creacion de respaldo antes de modificar un workbook ficticio;
- eliminacion exclusiva de la hoja obsoleta cuando existe;
- conservacion de otras hojas y datos de la hoja principal;
- comportamiento no destructivo cuando la hoja obsoleta no existe;
- generacion de reportes locales Markdown y JSON;
- ausencia de datos de filas en reportes de prueba.

Las pruebas de `1.7.0` validan:

- carga correcta de un workbook modernizado ficticio;
- validacion de archivo inexistente y extension incorrecta;
- deteccion de hoja `CONTROLCARTERA`;
- error controlado cuando falta la hoja principal;
- deteccion de columnas auxiliares `GS_*`;
- advertencia y estructura incompleta cuando faltan columnas `GS_*`;
- salida de consola sin valores sensibles ficticios;
- ausencia de modificaciones al workbook fuente;
- ausencia de salidas permanentes innecesarias.

## Revision de codigo futura

Cuando exista codigo, cada cambio relevante debera revisar:

- claridad de nombres y responsabilidades;
- modularidad y separacion de capas;
- ausencia de dependencias innecesarias;
- comentarios o docstrings en codigo principal cuando aporten contexto;
- manejo conservador de datos;
- ausencia de datos reales en pruebas, capturas o archivos versionados.

## Revision de interfaz futura

Cuando exista GUI, cada fase debera validar:

- ortografia en textos visibles;
- consistencia de terminos;
- mensajes de error y confirmacion claros;
- confirmacion explicita antes de eliminar informacion;
- visualizacion consistente de colones y dolares;
- respeto por nombres originales de registros importados.

## Pruebas funcionales futuras

Las pruebas funcionales se definiran por modulo y version. Deberan cubrir flujos completos cuando existan pantallas, persistencia, importacion, reportes o documentos.

## Consistencia de datos futura

La validacion de datos debera confirmar que:

- los registros importados conservan nombres originales;
- no se pierden registros con formatos no esperados;
- las relaciones entre clientes, polizas y vencimientos son trazables;
- los datos anonimizados no contienen informacion sensible real;
- los respaldos no sustituyen ni borran informacion sin confirmacion.

## Casos futuros sobre dataset canonico

Cuando se implemente la capa correspondiente, deberan definirse pruebas para:

- mapeo origen -> canonico sin perdida de trazabilidad;
- separacion entre campos originales, normalizados, derivados y operativos;
- clasificacion correcta de sensibilidad y editabilidad futura;
- consolidacion de fecha de vencimiento desde fecha unica o partes;
- normalizacion de frecuencia sin forzar reglas no aprobadas;
- derivacion preliminar de moneda con excepcion para riesgos del trabajo;
- preservacion del valor original aunque exista version normalizada;
- manejo conservador de `detalle` como campo potencialmente sensible;
- ausencia de PII en salidas documentales, tecnicas y de depuracion.

## Casos futuros especificos

Cuando se implemente la logica correspondiente, se deberan disenar pruebas para:

- polizas con vigencia `D.M.`;
- confirmacion de que `D.M.` se almacena aunque no genere avisos;
- multiples formatos de `Numero de Poliza`;
- identificaciones fisicas, juridicas, pasaportes e identificaciones de extranjero;
- fechas de vencimiento separadas en dia, mes y ano;
- consistencia entre cliente, polizas y `detalle`;
- uso de `Numero de Placa / Finca`;
- regla preliminar de moneda por prefijos `01` y `02`;
- excepcion de riesgos del trabajo para polizas completamente numericas;
- anonimizacion de datos de prueba.

## Pruebas manuales por fase

Cada version debera contar con una lista de validaciones manuales alineadas al alcance. Ejemplos futuros:

- abrir la aplicacion;
- cargar datos de muestra;
- revisar listados;
- generar documentos por cliente;
- validar monedas CRC y USD;
- confirmar mensajes antes de operaciones destructivas;
- crear y verificar respaldos.

## Validaciones minimas de esta fase

- Existe la estructura base de carpetas solicitada.
- Existen los documentos base del proyecto.
- La documentacion indica que el sistema esta en construccion.
- No se implementa interfaz grafica funcional.
- No se implementa base de datos operativa.
- No se implementa importacion real de Excel.
- No se implementa generacion real de DOCX.
- No se implementa logica de vencimientos.
- Se documentan supuestos conservadores.
- `.gitignore` excluye artefactos locales y temporales comunes.
- La politica de confidencialidad queda documentada.
- Las reglas de negocio conocidas quedan documentadas sin implementacion funcional.

## Validaciones minimas de auditoria local segura

- El script acepta ruta de entrada y ruta de salida.
- El Excel original no se modifica.
- Los reportes se generan en una ruta local ignorada por Git.
- Los reportes no incluyen muestras de filas ni valores sensibles.
- Los encabezados no confirmados se reportan como `COL_A`, `COL_B`, etc.
- Las categorias de vigencia o frecuencia se documentan como observadas y preliminares.
- Las pruebas automatizadas usan datos ficticios.
- Las pruebas no dejan artefactos permanentes en `data/output/`.

## Criterio de salida de 1.4.0

La fase `1.4.0` se considera lista cuando:

- el dataset canonico queda documentado de forma revisable;
- el mapeo origen -> canonico queda definido sin exponer datos sensibles;
- la estrategia de modernizacion del workbook queda explicita;
- las decisiones bloqueantes para `1.5.0` y `1.6.0` quedan identificadas;
- no existen cambios funcionales fuera del alcance.

## Criterio de salida de 1.5.0

La fase `1.5.0` se considera lista cuando:

- `python -m app` ejecuta correctamente;
- el paquete `app` es importable;
- existen pruebas automatizadas para configuracion, rutas, logging, bootstrap y contratos;
- no se lee ni modifica el Excel real;
- no se implementa GUI, persistencia, busqueda, edicion, exportacion ni DOCX;
- la documentacion tecnica queda alineada con la estructura creada.

## Criterio de salida de 1.6.0

La fase `1.6.0` se considera lista cuando:

- el workbook original no cambia;
- se genera una copia `*_modernizado_YYYYMMDD_HHMMSS.xlsx` en `data/output/workbook_modernizado/`;
- se generan reportes locales de modernizacion;
- las columnas auxiliares `GS_*` quedan agregadas al final;
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

- el lector carga un workbook modernizado indicado por ruta;
- la estructura se valida sin guardar cambios en Excel;
- se reportan columnas `GS_*` presentes y faltantes;
- los registros se cargan solo en memoria;
- el script no imprime valores reales de filas;
- las pruebas automatizadas pasan con datos ficticios;
- no se generan salidas permanentes innecesarias.
