# Gestor Seguros

Aplicación de escritorio en Python para apoyar la gestión operativa de seguros. El proyecto busca organizar información de clientes, pólizas, vencimientos, documentos, respaldos y reportes en una herramienta local, portable y mantenible.

## Problema que resuelve

La gestión operativa de seguros suele depender de archivos dispersos, controles manuales y documentos preparados caso por caso. Esto aumenta el riesgo de omisiones, duplicidad de información, dificultad para dar seguimiento a vencimientos y poca trazabilidad sobre cambios o respaldos.

## Objetivo general

Construir una aplicación de escritorio modular que permita gestionar información operativa de seguros de forma ordenada, trazable y preparada para crecer por fases.

## Alcance inicial

Las primeras fases establecen la base profesional del repositorio:

- estructura inicial de carpetas;
- documentación formal del proyecto;
- arquitectura preliminar;
- reglas iniciales de trabajo;
- supuestos, riesgos y decisiones técnicas conservadoras.

No se implementa interfaz grafica funcional, base de datos operativa, importación real de Excel, generación real de documentos ni lógica de vencimientos.

## Versionado

El proyecto usa versionado `X.Y.Z`:

- `X`: cambios mayores o incompatibles.
- `Y`: nuevas fases, módulos o capacidades relevantes.
- `Z`: correcciones, ajustes documentales menores o mantenimiento.

Cada versión relevante debe quedar registrada en `CHANGELOG.md` y acompanarse de notas de release cuando exista entregable revisable.

## Release técnico actual

Release técnico actual: `v1.8.4-alpha`.

Estado del proyecto: alpha técnico. La aplicación se ejecuta mediante Python y todavía no cuenta con ejecutable, instalador ni paquete portable.

Documento de release:

- `docs/releases/v1.8.4-alpha.md`

Este release no debe incluir datos reales, archivos confidenciales ni capturas con información sensible.

## Política de datos confidenciales

La base real de seguros es confidencial y no debe subirse a GitHub. Los archivos reales de entrada, salida y respaldo deben permanecer fuera del control de versiones.

Para pruebas se podrán usar datos ficticios o copias anonimizadas, sin nombres, identificaciones, teléfonos, correos, placas, fincas, números de póliza u otros datos sensibles reales.

## Auditoría local segura

La versión `v1.3.0` incorpora un script para auditar la estructura del Excel local confidencial sin modificarlo y sin exponer valores sensibles de filas. La versión `v1.3.1` refuerza el saneamiento para usar etiquetas seguras cuando un encabezado no es confiable.

Ejecución local:

```powershell
python scripts/auditar_base_local.py data/input/CONTROLCARTERA_V2.xlsx data/output/auditoria
```

Salidas locales:

- `data/output/auditoria/resumen_auditoria.md`
- `data/output/auditoria/resumen_auditoria.json`

Estas salidas estén en una ruta ignorada por Git y deben tratarse como información local de trabajo.

## Dataset canónico y workbook

La versión `v1.4.0` define, a nivel documental, como conviviran el workbook operativo actual y el futuro dataset canónico interno de la aplicación.

El enfoque de esta fase es `workbook primero`:

- el workbook sigue siendo la herramienta operativa principal;
- el dataset canónico se diseña como capa interna, gradual y trazable;
- el mapeo origen -> canónico se documenta sin exponer datos sensibles;
- la modernización del workbook se planifica por pasos pequeños y reversibles;
- no se implementa todavía importación funcional, persistencia operativa ni automatización del archivo real.

Los documentos principales de esta fase se encuentran en:

- `docs/proyecto/ESPECIFICACION_DATASET_CANONICO.md`
- `docs/proyecto/MAPA_ORIGEN_A_CANONICO.md`
- `docs/proyecto/ESTRATEGIA_MODERNIZACION_WORKBOOK.md`
- `docs/proyecto/DECISIONES_IMPLEMENTACION_1_5_1_6.md`

## Base técnica Python

La versión `v1.5.0` crea el esqueleto técnico mínimo de la aplicación como paquete Python importable.

Desde `v1.8.0`, la ejecución principal abre la interfaz grafica:

```powershell
python -m app
```

Chequeo técnico sin abrir la interfaz:

```powershell
python -m app --check
```

Pruebas:

```powershell
python -m pytest tests -p no:cacheprovider
```

Esta base inicializa configuración, rutas, logging, excepciones y contratos preliminares. No abre interfaz grafica, no lee ni escribe el workbook real, no crea persistencia y no ejecuta transformaciones de negocio.

## Fuente activa de datos

Desde `v1.8.2`, la fuente normal de lectura de la app es el Control Cartera operativo:

```text
data/input/CONTROLCARTERA_V2.xlsx
```

La app lo abre en modo de solo lectura para visualizar registros en memoria. No guarda cambios en Excel, no genera columnas técnicas auxiliares y no depende de copias en `data/output/workbook_modernizado/`.

Instalación de dependencias:

```powershell
python -m pip install -r requirements.txt
```

## Mantenimiento controlado del workbook

La versión `v1.6.1` agrega un flujo local de mantenimiento para eliminar del workbook operativo la hoja obsoleta `Reporte de vencimientos del mes`, con respaldo automático previo.

Ejecución local:

```powershell
python scripts/limpiar_workbook_operativo.py data/input/CONTROLCARTERA_V2.xlsx data/backups/workbook_mantenimiento data/output/workbook_mantenimiento
```

Salidas locales:

- respaldo timestamped en `data/backups/workbook_mantenimiento/`;
- `data/output/workbook_mantenimiento/reporte_limpieza_workbook.md`;
- `data/output/workbook_mantenimiento/reporte_limpieza_workbook.json`.

El script solo elimina esa hoja si existe. No modifica registros de clientes, pólizas, identificaciones, placas, teléfonos ni otros datos operativos.

## Carga controlada del Control Cartera

Ejecución local:

```powershell
python scripts/cargar_control_cartera.py data/input/CONTROLCARTERA_V2.xlsx
```

El script imprime solo un resumen técnico: archivo, hoja, filas útiles, filas cargadas, filas omitidas, columnas visibles y advertencias. No imprime valores reales de clientes, cédulas, pólizas, placas, teléfonos ni detalle.

## Interfaz grafica inicial

La versión `v1.8.0` incorpora la primera interfaz gráfica real con PySide6. La versión `v1.8.1` agrega visualización tabular de registros en modo solo lectura. La versión `v1.8.2` cambia la fuente activa a `data/input/CONTROLCARTERA_V2.xlsx`. La versión `v1.8.3` agrega control compacto de tema claro/oscuro. La versión `v1.8.4` agrega ícono profesional propio. La versión `v1.9.0` agrega búsqueda y filtros básicos en la pestaña `Registros`. La versión `v1.9.1` agrega una ventana de detalle del registro seleccionado. La versión `v1.10.0` agrega edición controlada de registros solo en memoria.

Instalación de dependencias:

```powershell
python -m pip install -r requirements.txt
```

Ejecución:

```powershell
python -m app
```

La ventana muestra `Gestor de Seguros- Dagoberto Quirós Madriz`, deja lista la ruta predeterminada `data/input/CONTROLCARTERA_V2.xlsx`, permite cargarla con `Cargar predeterminado` y también permite seleccionar otro `.xlsx`. La pestaña `Registros` queda primero y muestra solo columnas originales y filas útiles en una tabla de solo lectura. También permite buscar en todas las columnas o en una columna específica, limpiar la búsqueda y ver el contador `Mostrando X de Y registros`. Al hacer doble clic sobre una fila, se abre `Detalle del registro` con los campos que contienen información. Desde ese detalle se puede abrir `Editar registro` para aplicar cambios únicamente en memoria. La pestaña `Resumen` muestra conteos y estado de carga. El botón compacto de tema permite alternar entre claro y oscuro, recordando la preferencia localmente. No guarda cambios en Excel, no elimina registros y marca visualmente los cambios pendientes sin guardar.

El ícono de la aplicación es un asset propio y generico ubicado en `assets/app_icon.svg`. No usa marcas oficiales ni logos de terceros. En una fase futura de empaquetado se podrá convertir o referenciar para PyInstaller.

## Funcionalidades futuras previstas

- Persistencia local, probablemente con SQLite.
- Importacion controlada desde Excel cuando exista la base real.
- Gestión de clientes, pólizas, vencimientos y bitácoras o pistas de auditoría.
- Generación de documentos de vencimiento por cliente.
- Soporte para pólizas en colones y dólares.
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
assets/              Icono propio y futuros recursos visuales de la app.
scripts/             Utilidades de desarrollo y mantenimiento.
tests/               Pruebas automatizadas futuras.
```

## Estado actual

Proyecto en fase de búsqueda, filtros, detalle y edición controlada en memoria con lectura directa desde `data/input/CONTROLCARTERA_V2.xlsx`. La versión `v1.1.0` creó la base inicial, `v1.2.0` fortaleció lineamientos técnicos, `v1.3.x` dejó una auditoría local segura, `v1.4.0` formalizó el dataset canónico, `v1.5.0` creó la base técnica modular, `v1.6.x` preparó el workbook operativo, `v1.7.0` agregó lectura controlada, `v1.8.0` muestra el resumen de carga en GUI, `v1.8.1` agrega tabla de registros de solo lectura, `v1.8.2` retira la dependencia de copias modernizadas, `v1.8.3` mejora el aspecto visual con tema claro/oscuro, `v1.8.4` agrega identidad visual básica con ícono propio, `v1.9.0` agrega búsqueda y filtros básicos, `v1.9.1` agrega ventana de detalle del registro seleccionado y `v1.10.0` agrega edición controlada solo en memoria.

## Próximos pasos

1. Probar manualmente la GUI con `data/input/CONTROLCARTERA_V2.xlsx`.
2. Validar manualmente la tabla de solo lectura, las filas útiles detectadas, el resumen de carga, el cambio de tema y la edición en memoria.
3. Definir la política inicial de IDs internos para cliente, póliza y vencimiento.
4. Definir el alcance de guardado seguro, persistencia y bitácoras para una fase futura.
5. Posponer exportaciones, DOCX y vencimientos hasta fases aprobadas.
