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

Desde `v1.8.0`, la ejecucion principal abre la interfaz grafica:

```powershell
python -m app
```

Chequeo tecnico sin abrir la interfaz:

```powershell
python -m app --check
```

Pruebas:

```powershell
python -m pytest tests -p no:cacheprovider
```

Esta base inicializa configuracion, rutas, logging, excepciones y contratos preliminares. No abre interfaz grafica, no lee ni escribe el workbook real, no crea persistencia y no ejecuta transformaciones de negocio.

## Fuente activa de datos

Desde `v1.8.2`, la fuente normal de lectura de la app es el Control Cartera operativo:

```text
data/input/CONTROLCARTERA_V2.xlsx
```

La app lo abre en modo de solo lectura para visualizar registros en memoria. No guarda cambios en Excel, no genera columnas tecnicas auxiliares y no depende de copias en `data/output/workbook_modernizado/`.

Instalacion de dependencias:

```powershell
python -m pip install -r requirements.txt
```

## Mantenimiento controlado del workbook

La version `v1.6.1` agrega un flujo local de mantenimiento para eliminar del workbook operativo la hoja obsoleta `Reporte de vencimientos del mes`, con respaldo automatico previo.

Ejecucion local:

```powershell
python scripts/limpiar_workbook_operativo.py data/input/CONTROLCARTERA_V2.xlsx data/backups/workbook_mantenimiento data/output/workbook_mantenimiento
```

Salidas locales:

- respaldo timestamped en `data/backups/workbook_mantenimiento/`;
- `data/output/workbook_mantenimiento/reporte_limpieza_workbook.md`;
- `data/output/workbook_mantenimiento/reporte_limpieza_workbook.json`.

El script solo elimina esa hoja si existe. No modifica registros de clientes, polizas, identificaciones, placas, telefonos ni otros datos operativos.

## Carga controlada del Control Cartera

Ejecucion local:

```powershell
python scripts/cargar_control_cartera.py data/input/CONTROLCARTERA_V2.xlsx
```

El script imprime solo un resumen tecnico: archivo, hoja, filas utiles, filas cargadas, filas omitidas, columnas visibles y advertencias. No imprime valores reales de clientes, cedulas, polizas, placas, telefonos ni detalle.

## Interfaz grafica inicial

La version `v1.8.0` incorpora la primera interfaz grafica real con PySide6. La version `v1.8.1` agrega visualizacion tabular de registros en modo solo lectura. La version `v1.8.2` cambia la fuente activa a `data/input/CONTROLCARTERA_V2.xlsx`. La version `v1.8.3` agrega control compacto de tema claro/oscuro.

Instalacion de dependencias:

```powershell
python -m pip install -r requirements.txt
```

Ejecucion:

```powershell
python -m app
```

La ventana muestra `Gestor de Seguros- Dagoberto Quirós Madriz`, deja lista la ruta predeterminada `data/input/CONTROLCARTERA_V2.xlsx`, permite cargarla con `Cargar predeterminado` y tambien permite seleccionar otro `.xlsx`. La pestana `Registros` queda primero y muestra solo columnas originales y filas utiles en una tabla de solo lectura. La pestana `Resumen` muestra conteos y estado de carga. El boton compacto de tema permite alternar entre claro y oscuro, recordando la preferencia localmente. No permite busqueda, filtros, edicion ni guardado de cambios en Excel.

## Funcionalidades futuras previstas

- Persistencia local, probablemente con SQLite.
- Importacion controlada desde Excel cuando exista la base real.
- Gestion de clientes, polizas, vencimientos y bitacoras o pistas de auditoria.
- Generacion de documentos de vencimiento por cliente.
- Soporte para polizas en colones y dolares.
- Reportes operativos y tableros de seguimiento.
- Respaldos locales y politicas de recuperacion.
- Distribucion portable y mediante instalador.

## Estructura del repositorio

```text
app/                 Paquete Python base de la aplicacion.
app/ui/              Interfaz grafica inicial con PySide6.
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

Proyecto en fase de visualizacion tabular de registros con lectura directa desde `data/input/CONTROLCARTERA_V2.xlsx`. La version `v1.1.0` creo la base inicial, `v1.2.0` fortalecio lineamientos tecnicos, `v1.3.x` dejo una auditoria local segura, `v1.4.0` formalizo el dataset canonico, `v1.5.0` creo la base tecnica modular, `v1.6.x` preparo el workbook operativo, `v1.7.0` agrego lectura controlada, `v1.8.0` muestra el resumen de carga en GUI, `v1.8.1` agrega tabla de registros de solo lectura, `v1.8.2` retira la dependencia de copias modernizadas y `v1.8.3` mejora el aspecto visual con tema claro/oscuro.

## Proximos pasos

1. Probar manualmente la GUI con `data/input/CONTROLCARTERA_V2.xlsx`.
2. Validar manualmente la tabla de solo lectura, las filas utiles detectadas, el resumen de carga y el cambio de tema.
3. Definir la politica inicial de IDs internos para cliente, poliza y vencimiento.
4. Definir el alcance de busqueda, filtros o persistencia para una fase futura.
5. Posponer edicion, guardado, exportaciones, DOCX y vencimientos hasta fases aprobadas.
