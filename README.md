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
docs/proyecto/       Documentacion interna del proyecto.
docs/releases/       Notas y evidencias por version.
scripts/             Utilidades de desarrollo y mantenimiento.
tests/               Pruebas automatizadas futuras.
```

## Estado actual

Proyecto en fase de diseno documental del dataset canonico y de la convivencia con el workbook operativo. La version `v1.1.0` creo la base inicial, `v1.2.0` fortalecio lineamientos tecnicos, `v1.3.x` dejo una auditoria local segura y `v1.4.0` formaliza el marco para pasar a una futura implementacion controlada sin romper la operacion manual.

## Proximos pasos

1. Revisar y aprobar el diseno del dataset canonico y el mapeo origen -> canonico.
2. Confirmar las decisiones bloqueantes para `1.5.0` y `1.6.0`.
3. Validar con criterio humano las ambiguedades de frecuencia, identificacion, fechas y relaciones detectadas en la auditoria.
4. Definir el modelo interno preliminar y la politica de trazabilidad antes de implementar lectura controlada.
5. Mantener el workbook operativo sin cambios disruptivos mientras maduran las fases tecnicas.
6. Crear la estructura de plantillas DOCX solo cuando inicie esa fase.
