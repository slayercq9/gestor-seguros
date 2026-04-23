# Changelog

Todos los cambios relevantes del proyecto se documentaran en este archivo.

El formato seguira una estructura por versiones, con secciones para cambios agregados, modificados, corregidos y decisiones importantes cuando aplique.

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
