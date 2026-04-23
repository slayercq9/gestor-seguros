# Plan de Pruebas

## Objetivo

Definir una estrategia de validacion progresiva para asegurar que cada fase del proyecto sea revisable, mantenible y coherente con el alcance aprobado.

## Estrategia general

- Validar primero estructura, documentacion y decisiones tecnicas.
- Agregar pruebas automatizadas cuando exista codigo ejecutable.
- Mantener pruebas manuales por fase para flujos de usuario.
- Confirmar que no se introduzcan reglas de negocio no aprobadas.
- Verificar que cualquier eliminacion futura exija confirmacion explicita.

## Pruebas automatizadas futuras

Cuando exista codigo, se evaluara incorporar `pytest` para:

- validaciones de modelos de datos;
- transformaciones de informacion;
- reglas de importacion;
- generacion de reportes;
- generacion de documentos;
- operaciones de respaldo;
- pruebas de regresion sobre errores corregidos.

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

## Criterios de salida de la fase

La fase se considera lista cuando la estructura y documentacion puedan ser revisadas por una persona responsable del proyecto y no existan cambios funcionales fuera del alcance.
