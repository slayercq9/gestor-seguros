# Gestor Seguros

Aplicacion de escritorio en Python para apoyar la gestion operativa de seguros. El proyecto busca organizar informacion de clientes, polizas, vencimientos, documentos, respaldos y reportes en una herramienta local, portable y mantenible.

## Problema que resuelve

La gestion operativa de seguros suele depender de archivos dispersos, controles manuales y documentos preparados caso por caso. Esto aumenta el riesgo de omisiones, duplicidad de informacion, dificultad para dar seguimiento a vencimientos y poca trazabilidad sobre cambios o respaldos.

## Objetivo general

Construir una aplicacion de escritorio modular que permita gestionar informacion operativa de seguros de forma ordenada, trazable y preparada para crecer por fases.

## Alcance inicial

Las primeras fases establecen la base profesional del repositorio:

- estructura inicial de carpetas;
- documentacion formal del proyecto;
- arquitectura preliminar;
- reglas iniciales de trabajo;
- supuestos, riesgos y decisiones tecnicas conservadoras.

No se implementa interfaz grafica funcional, base de datos operativa, importacion real de Excel, generacion real de documentos ni logica de vencimientos.

## Versionado

El proyecto usa versionado `X.Y.Z`:

- `X`: cambios mayores o incompatibles.
- `Y`: nuevas fases, modulos o capacidades relevantes.
- `Z`: correcciones, ajustes documentales menores o mantenimiento.

Cada version relevante debe quedar registrada en `CHANGELOG.md` y acompanarse de notas de release cuando exista entregable revisable.

## Politica de datos confidenciales

La base real de seguros es confidencial y no debe subirse a GitHub. Los archivos reales de entrada, salida y respaldo deben permanecer fuera del control de versiones.

Para pruebas se podran usar datos ficticios o copias anonimizadas, sin nombres, identificaciones, telefonos, correos, placas, fincas, numeros de poliza u otros datos sensibles reales.

## Auditoria local segura

La version `v1.3.0` incorpora un script para auditar la estructura del Excel local confidencial sin modificarlo y sin exponer valores sensibles de filas.

Ejecucion local:

```powershell
python scripts/auditar_base_local.py data/input/CONTROLCARTERA_V2.xlsx data/output/auditoria
```

Salidas locales:

- `data/output/auditoria/resumen_auditoria.md`
- `data/output/auditoria/resumen_auditoria.json`

Estas salidas estan en una ruta ignorada por Git y deben tratarse como informacion local de trabajo.

## Funcionalidades futuras previstas

- Interfaz grafica de escritorio, probablemente con PySide6.
- Persistencia local, probablemente con SQLite.
- Importacion controlada desde Excel cuando exista la base real.
- Gestion de clientes, polizas, vencimientos y bitacoras.
- Generacion de documentos de vencimiento por cliente.
- Soporte para polizas en colones y dolares.
- Reportes operativos y tableros de seguimiento.
- Respaldos locales y politicas de recuperacion.
- Distribucion portable y mediante instalador.

## Estructura del repositorio

```text
app/                 Codigo fuente de la aplicacion.
data/input/          Archivos de entrada locales no versionados.
data/output/         Archivos generados localmente.
data/backups/        Respaldos locales no versionados.
data/samples/        Datos de muestra anonimizados o ficticios.
docs/capturas/       Capturas para documentacion.
docs/diagramas/      Diagramas de arquitectura y flujo.
docs/releases/       Notas y evidencias por version.
scripts/             Utilidades de desarrollo y mantenimiento.
templates/docx/      Plantillas futuras para documentos.
tests/               Pruebas automatizadas futuras.
.codex/              Configuracion minima de trabajo asistido.
```

## Estado actual

Proyecto en fase de auditoria local segura. La version `v1.1.0` creo la base inicial, `v1.2.0` fortalecio lineamientos tecnicos y `v1.3.0` agrega auditoria estructural segura del workbook local antes de disenar el dataset funcional.

## Proximos pasos

1. Revisar los reportes locales de auditoria sin publicarlos.
2. Confirmar la hoja principal y las columnas criticas.
3. Refinar el diccionario de datos con base en hallazgos aprobados.
4. Disenar el dataset mejorado conservando columnas originales.
5. Definir reglas de validacion preliminares antes de implementar importacion funcional.
