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

La auditoria local segura cuenta con pruebas en `tests/test_auditar_base_local.py`.

Ejecucion:

```powershell
python -m pytest tests/test_auditar_base_local.py -p no:cacheprovider
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
- utilidad minima del reporte aunque no se muestren encabezados originales.

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

## Pruebas manuales por fase

Cada version debera contar con una lista de validaciones manuales alineadas al alcance. Ejemplos futuros:

- abrir la aplicacion;
- cargar datos de muestra;
- revisar listados;
- generar documentos por cliente;
- validar monedas CRC y USD;
- confirmar mensajes antes de operaciones destructivas;
- crear y verificar respaldos.

## Casos futuros especificos

Cuando se implemente la logica correspondiente, se deberan disenar pruebas para:

- polizas con vigencia `D.M.`;
- confirmacion de que `D.M.` se almacena aunque no genere avisos;
- multiples formatos de `Nº Poliza`;
- identificaciones fisicas, juridicas, pasaportes e identificaciones de extranjero;
- fechas de vencimiento separadas en dia, mes y ano;
- consistencia entre cliente, polizas y detalle;
- uso de `Nº Placa / Finca`;
- regla preliminar de moneda por prefijos `01` y `02`;
- excepcion de riesgos del trabajo para polizas completamente numericas;
- anonimizacion de datos de prueba.

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
- Las categorias de vigencia/frecuencia se documentan como observadas y preliminares.
- Las pruebas automatizadas usan datos ficticios.

## Criterios de salida de la fase

La fase se considera lista cuando la estructura y documentacion puedan ser revisadas por una persona responsable del proyecto y no existan cambios funcionales fuera del alcance.
