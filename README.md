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

La version `v1.3.0` incorpora un script para auditar la estructura del Excel local confidencial sin modificarlo y sin exponer valores sensibles de filas. La version `v1.3.1` refuerza el saneamiento para usar etiquetas seguras cuando un encabezado no es confiable.

Ejecucion local:

```powershell
python scripts/auditar_base_local.py data/input/CONTROLCARTERA_V2.xlsx data/output/auditoria
```

Salidas locales:

- `data/output/auditoria/resumen_auditoria.md`
- `data/output/auditoria/resumen_auditoria.json`

Estas salidas estan en una ruta ignorada por Git y deben tratarse como informacion local de trabajo.

## Dataset canonico y workbook

La version `v1.4.0` define, a nivel documental, como conviviran el workbook operativo actual y el futuro dataset canonico interno de la aplicacion.

El enfoque de esta fase es `workbook primero`:

- el workbook sigue siendo la herramienta operativa principal;
- el dataset canonico se disena como capa interna, gradual y trazable;
- el mapeo origen -> canonico se documenta sin exponer datos sensibles;
- la modernizacion del workbook se planifica por pasos pequenos y reversibles;
- no se implementa todavia importacion funcional, persistencia operativa ni automatizacion del archivo real.

Los documentos principales de esta fase se encuentran en:

- `docs/proyecto/ESPECIFICACION_DATASET_CANONICO.md`
- `docs/proyecto/MAPA_ORIGEN_A_CANONICO.md`
- `docs/proyecto/ESTRATEGIA_MODERNIZACION_WORKBOOK.md`
- `docs/proyecto/DECISIONES_IMPLEMENTACION_1_5_1_6.md`

## Base tecnica Python

La version `v1.5.0` crea el esqueleto tecnico minimo de la aplicacion como paquete Python importable.

Ejecucion tecnica:

```powershell
python -m app
```

Pruebas:

```powershell
python -m pytest tests -p no:cacheprovider
```

Esta base inicializa configuracion, rutas, logging, excepciones y contratos preliminares. No abre interfaz grafica, no lee ni escribe el workbook real, no crea persistencia y no ejecuta transformaciones de negocio.

## Modernizacion local del workbook

La version `v1.6.0` agrega un flujo controlado para generar una copia modernizada local del workbook operativo, sin sobrescribir el archivo original.

Instalacion de dependencias:

```powershell
pip install -r requirements.txt
```

Ejecucion local:

```powershell
python scripts/modernizar_workbook_local.py data/input/CONTROLCARTERA_V2.xlsx data/output/workbook_modernizado
```

Salidas locales:

- `data/output/workbook_modernizado/CONTROLCARTERA_V2_modernizado_YYYYMMDD_HHMMSS.xlsx`
- `data/output/workbook_modernizado/resumen_modernizacion.md`
- `data/output/workbook_modernizado/resumen_modernizacion.json`
- `data/output/workbook_modernizado/control_revision.csv`

Estas salidas pueden contener datos reales o estadisticas reales y permanecen fuera de Git por estar en `data/output/`.

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
app/                 Paquete Python base de la aplicacion.
data/input/          Archivos de entrada locales no versionados.
data/output/         Archivos generados localmente.
data/backups/        Respaldos locales no versionados.
data/samples/        Datos de muestra anonimizados o ficticios.
docs/capturas/       Capturas para documentacion.
docs/diagramas/      Diagramas de arquitectura y flujo.
docs/proyecto/       Documentacion interna del proyecto.
docs/releases/       Notas y evidencias por version.
scripts/             Utilidades de desarrollo y mantenimiento.
tests/               Pruebas automatizadas futuras.
```

## Estado actual

Proyecto en fase de modernizacion local controlada del workbook operativo. La version `v1.1.0` creo la base inicial, `v1.2.0` fortalecio lineamientos tecnicos, `v1.3.x` dejo una auditoria local segura, `v1.4.0` formalizo el dataset canonico, `v1.5.0` creo la base tecnica modular y `v1.6.0` genera una copia modernizada local sin modificar el workbook original.

## Proximos pasos

1. Revisar la copia modernizada local y los reportes de control.
2. Validar manualmente columnas auxiliares y registros marcados para revision.
3. Confirmar si la copia modernizada sera base de la lectura controlada futura.
4. Confirmar la politica inicial de IDs internos para cliente, poliza y vencimiento.
5. Posponer GUI, persistencia funcional, busqueda, edicion, exportaciones y DOCX hasta fases aprobadas.
