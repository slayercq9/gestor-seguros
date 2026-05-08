# Arquitectura

## Vision general

La aplicación se diseña como una herramienta de escritorio modular. Cada componente deberá tener una responsabilidad clara y comúnicarse mediante contratos simples para facilitar mantenimiento, pruebas y empaquetado.

Desde `1.4.0`, la arquitectura también contempla una capa de dataset canónico interno para desacoplar el modelo futuro de la app respecto del workbook operativo, sin reemplazarlo todavía.

## Modulos preliminares

### Interfaz

Responsable de presentar pantallas, formularios, acciones y mensajes al usuario. Desde `1.8.0` existe una primera ventana PySide6 para seleccionar y cargar visualmente un Control Cartera. Desde `1.8.1` esa ventana también muestra registros en una tabla de solo lectura. Desde `1.8.3` permite alternar entre tema claro y oscuro sin alterar datos cargados. Desde `1.8.4` aplica un ícono propio de la aplicación. Desde `1.9.0` permite búsqueda y filtros básicos en memoria sobre la tabla. Desde `1.9.1` abre una ventana de detalle con doble clic sobre un registro. Desde `1.10.0` permite edición controlada solo en memoria desde una ventana modal separada. Desde `1.10.1` muestra una pestaña `Bitácora` con cambios de la sesión. Desde `1.10.2` oculta visualmente coberturas sin eliminarlas de memoria. Desde `1.10.3` agrega controles por campo, errores bloqueantes y advertencias suaves antes de aplicar cambios en memoria.

### Lectura de origen

Responsable de leer el workbook operativo y otras fuentes controladas sin alterarlas. Esta capa debe preservar trazabilidad y no debe imponer cambios manuales sobre el archivo real.

### Dataset canónico

Responsable de representar internamente clientes, pólizas, vencimientos, relaciones y metadatos operativos en una forma trazable y consistente. Debe conservar distincion entre campos originales, normalizados, derivados y operativos.

### Datos

Responsable de persistir y recuperar información interna cuando exista una estrategia aprobada de almacenamiento. La persistencia local probable será SQLite, pero no se define una base operativa en esta fase.

### Lógica de aplicación

Responsable de coordinar casos de uso. No debe mezclarse con detalles de interfaz ni de almacenamiento.

### Reportes

Responsable de consultas, filtros, resúmenes y exportaciones futuras.

### Documentos

Responsable de preparar documentos a partir de plantillas. Los documentos de vencimiento deberán generarse por cliente, no por póliza. La estructura fisica de plantillas se incorporara cuando inicie la fase de generación DOCX.

### Respaldos

Responsable de crear, verificar y recuperar respaldos. No deberá borrar información automáticamente.

### Bitácoras o pistas de auditoría

Módulo futuro para registrar cambios aprobados sobre el Control Cartera cuando exista guardado persistente. Deberá conservar fecha y hora, campo modificado, valor anterior, valor nuevo, origen del cambio, usuario local si aplica, archivo afectado y resultado de la operación.

### Configuración

Responsable de rutas locales, preferencias y parametros operativos no sensibles.

## Flujo conceptual general

```text
Usuario
  -> Interfaz
  -> Logica de aplicacion
  -> Lectura controlada del workbook
  -> Normalizacion y dataset canonico
  -> Datos / Reportes / Documentos / Respaldos
  -> Resultado visible, archivo generado o registro operativo
```

## Separacion de responsabilidades

- La interfaz no debe contener reglas de negocio complejas.
- Los módulos de datos no deben depender de la interfaz.
- La capa canónica no debe ocultar ni sobrescribir silenciosamente el origen.
- La generación de documentos no debe modificar datos operativos por si misma.
- Los respaldos deben ser operaciones explícitas y verificables.
- Cualquier eliminación futura debe exigir confirmación explícita.
- La lectura del workbook debe ser compatible con operación manual y no intrusiva.

## Estructura preliminar

```text
app/
  __main__.py     Entry point tecnico para `python -m app`.
  main.py         Punto de entrada de proceso.
  bootstrap.py    Inicializacion tecnica sin flujos de negocio.
  config/         Configuracion central.
  core/           Rutas, logging y excepciones base.
  domain/         Contratos preliminares del dataset canonico.
  services/       Servicios tecnicos y flujos locales controlados.
  ui/             Interfaz grafica inicial con PySide6.
  utils/          Utilidades pequenas y seguras.
```

Los paquetes de GUI, lectura funcional, persistencia, reportes, documentos y respaldos se crearan solo cuando exista una fase especifica aprobada.

## Decision arquitectonica de 1.5.0

- El workbook operativo se mantiene como fuente manual vigente.
- El dataset canónico se define como capa interna futura, no como reemplazo inmedíato.
- El esqueleto técnico de `1.5.0` no ejecuta lectura, escritura ni transformaciones de datos reales.
- La implementación de `1.6.0` deberá respetar trazabilidad entre origen y modelo interno.

## Decision arquitectonica de 1.6.0

- El flujo de modernización local queda retirado como dependencia activa desde `1.8.2`.
- La app no requiere copias en `data/output/workbook_modernizado/` para visualizar datos.
- `data/output/` queda reservado para copias, exportaciones o cambios futuros aprobados.
- Las inferencias quedan reservadas para lógica interna futura y no deben agregarse como columnas técnicas al Excel.

## Decision arquitectonica de 1.7.0

- La lectura controlada se orienta al Control Cartera operativo.
- El servicio `app/services/workbook_loader.py` abre el archivo en modo de solo lectura y no guarda cambios.
- Los registros se cargan en estructuras internas preliminares en `app/domain/workbook_records.py`.
- La consola reporta solo resumen técnico y nombres técnicos seguros de columnas.
- El lector no exige columnas técnicas auxiliares para cargar registros.
- Las filas se cargan por contenido útil real para evitar mostrar filas vacías o solo formateadas.
- No se implementa todavía búsqueda, edición, persistencia ni normalización funcional definitiva.

## Decision arquitectonica de 1.8.0

- `python -m app` abre la interfaz grafica inicial.
- `python -m app --check` queda como modo técnico secundario.
- La GUI vive en `app/ui/` y consume `app/services/workbook_loader.py`.
- La ventana prioriza la pestaña `Registros`, mantiene un resumen de carga y muestra tabla de solo lectura.
- La selección de archivo es local y explícita; no se asume un nombre fijo con timestamp.
- No se implementa todavía búsqueda, filtros, edición ni persistencia.

## Decision arquitectonica de 1.8.1

- La tabla de registros usa un `QAbstractTableModel` propio para evitar carga manual celda por celda.
- La tabla vive en una pestaña `Registros` y es de solo lectura.
- Los datos se muestran desde los registros cargados en memoria por `workbook_loader`.
- No se implementan edición, guardado ni persistencia.

## Decision arquitectonica de 1.8.2

- La fuente activa de lectura es `data/input/CONTROLCARTERA_V2.xlsx`.
- La GUI muestra esa ruta como predeterminada y ofrece una acción clara para cargarla.
- Se mantiene la selección manual de otro `.xlsx`, con carga automática tras selección.
- Las ventanas emergentes de validación usan mensajes amigables y sin trazas técnicas crudas.
- Cancelar la selección de archivo conserva el estado anterior y no se trata como error.
- La pestaña `Resumen` no muestra un panel visual de advertencias; conserva conteos, modo y estado de carga.
- Ningun flujo de visualización depende de `data/output/workbook_modernizado/`.

## Decision arquitectonica de 1.8.3

- Los estilos visuales se centralizan en `app/ui/theme.py`.
- El botón compacto de tema alterna entre tema claro y oscuro dentro de la ventana principal.
- La preferencia visual se guarda con `QSettings`, sin archivos de configuración versionados.
- Cambiar el tema no recarga datos, no limpia registros y no modifica archivos Excel.

## Decision arquitectonica de 1.8.4

- Los assets visuales viven en `assets/`.
- El ícono fuente del proyecto es `assets/app_icon.svg`.
- `app/ui/assets.py` resuelve rutas de assets en desarrollo y contempla `_MEIPASS` para futuros empaquetados con PyInstaller.
- El ícono se aplica a `QApplication` y a la ventana principal sin introducir funcionalidad operativa nueva.

## Decision arquitectonica de 1.9.0

- La búsqueda vive en `app/ui/filter_proxy_model.py` como un `QSortFilterProxyModel`.
- El filtro trabaja sobre registros ya cargados en memoria y no modifica el modelo fuente.
- La GUI permite buscar en todas las columnas o en una columna visible específica.
- El selector de columnas se actualiza cada vez que se carga un nuevo Control Cartera.
- Cambiar tema no limpia búsqueda, tabla ni registros.
- No se implementan edición, guardado ni persistencia.

## Decision arquitectonica de 1.9.1

- La vista de detalle vive en `app/ui/detail_dialog.py` como ventana modal abierta por doble clic.
- El detalle usa `app/ui/detail_model.py` para exponer campos y valores en modo solo lectura.
- La fila visible de la tabla se mapea desde el proxy de búsqueda hacia el modelo fuente para mostrar el registro correcto aunque existan filtros activos.
- Los campos vacíos se omiten para mejorar lectura sin modificar los datos originales.
- No se implementan edición, guardado, bitácoras ni persistencia.

## Decision arquitectonica de 1.10.0

- La edición controlada vive en `app/ui/edit_dialog.py` como ventana modal abierta desde `Detalle del registro`.
- La tabla principal conserva flags de solo lectura; no se edita directamente en celdas.
- `app/ui/table_model.py` permite actualizar registros en memoria mediante un método controlado y mantiene conteo de cambios pendientes.
- Los cambios se aplican al modelo en memoria, refrescan la tabla y conservan búsqueda o filtros activos cuando es posible.
- La GUI muestra `Cambios pendientes: X` y advierte antes de cargar otro archivo o cerrar la app si existen cambios no guardados.
- No se implementan guardado en Excel, eliminación de registros, bitácoras persistentes ni persistencia.

## Decision arquitectonica de 1.10.1

- La bitácora de sesión vive en memoria y no escribe archivos ni bases de datos.
- `app/domain/audit_log.py` define entradas de bitácora independientes de la interfaz.
- `app/ui/audit_table_model.py` expone la bitácora a Qt en una tabla de solo lectura.
- La pestaña `Bitácora` se ubica después de `Resumen`.
- Cada campo realmente modificado desde `Editar registro` genera una entrada con fecha y hora, registro, campo, valor anterior, valor nuevo, origen y estado.
- Al descartar cambios para cargar otro Control Cartera, se limpian los cambios en memoria y la bitácora de sesión.
- No se implementa exportación, persistencia ni guardado de bitácora.

## Decision arquitectonica de 1.10.2

- Los estándares funcionales de columnas se documentan en `docs/proyecto/ESTANDARES_COLUMNAS_CONTROL_CARTERA.md`.
- `app/domain/column_standards.py` clasifica columnas de cobertura con criterio conservador.
- El lector conserva valores de coberturas en `WorkbookRowRecord.values_by_column`.
- Las coberturas se excluyen de `visible_columns`, por lo que no aparecen en tabla, detalle, edición ni selector de búsqueda.
- No se eliminan columnas, no se modifica Excel y no se implementan ComboBox ni validaciones fuertes.
