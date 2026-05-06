# Arquitectura

## Vision general

La aplicacion se disena como una herramienta de escritorio modular. Cada componente debera tener una responsabilidad clara y comunicarse mediante contratos simples para facilitar mantenimiento, pruebas y empaquetado.

Desde `1.4.0`, la arquitectura tambien contempla una capa de dataset canonico interno para desacoplar el modelo futuro de la app respecto del workbook operativo, sin reemplazarlo todavia.

## Modulos preliminares

### Interfaz

Responsable de presentar pantallas, formularios, acciones y mensajes al usuario. Desde `1.8.0` existe una primera ventana PySide6 para seleccionar y cargar visualmente un Control Cartera. Desde `1.8.1` esa ventana tambien muestra registros en una tabla de solo lectura. Desde `1.8.3` permite alternar entre tema claro y oscuro sin alterar datos cargados. Desde `1.8.4` aplica un icono propio de la aplicacion.

### Lectura de origen

Responsable de leer el workbook operativo y otras fuentes controladas sin alterarlas. Esta capa debe preservar trazabilidad y no debe imponer cambios manuales sobre el archivo real.

### Dataset canonico

Responsable de representar internamente clientes, polizas, vencimientos, relaciones y metadatos operativos en una forma trazable y consistente. Debe conservar distincion entre campos originales, normalizados, derivados y operativos.

### Datos

Responsable de persistir y recuperar informacion interna cuando exista una estrategia aprobada de almacenamiento. La persistencia local probable sera SQLite, pero no se define una base operativa en esta fase.

### Logica de aplicacion

Responsable de coordinar casos de uso. No debe mezclarse con detalles de interfaz ni de almacenamiento.

### Reportes

Responsable de consultas, filtros, resumenes y exportaciones futuras.

### Documentos

Responsable de preparar documentos a partir de plantillas. Los documentos de vencimiento deberan generarse por cliente, no por poliza. La estructura fisica de plantillas se incorporara cuando inicie la fase de generacion DOCX.

### Respaldos

Responsable de crear, verificar y recuperar respaldos. No debera borrar informacion automaticamente.

### Bitacoras o pistas de auditoria

Modulo futuro para registrar cambios aprobados sobre el Control Cartera cuando existan edicion y guardado. Debera conservar fecha y hora, campo modificado, valor anterior, valor nuevo, origen del cambio, usuario local si aplica, archivo afectado y resultado de la operacion.

### Configuracion

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
- Los modulos de datos no deben depender de la interfaz.
- La capa canonica no debe ocultar ni sobrescribir silenciosamente el origen.
- La generacion de documentos no debe modificar datos operativos por si misma.
- Los respaldos deben ser operaciones explicitas y verificables.
- Cualquier eliminacion futura debe exigir confirmacion explicita.
- La lectura del workbook debe ser compatible con operacion manual y no intrusiva.

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
- El dataset canonico se define como capa interna futura, no como reemplazo inmediato.
- El esqueleto tecnico de `1.5.0` no ejecuta lectura, escritura ni transformaciones de datos reales.
- La implementacion de `1.6.0` debera respetar trazabilidad entre origen y modelo interno.

## Decision arquitectonica de 1.6.0

- El flujo de modernizacion local queda retirado como dependencia activa desde `1.8.2`.
- La app no requiere copias en `data/output/workbook_modernizado/` para visualizar datos.
- `data/output/` queda reservado para copias, exportaciones o cambios futuros aprobados.
- Las inferencias quedan reservadas para logica interna futura y no deben agregarse como columnas tecnicas al Excel.

## Decision arquitectonica de 1.7.0

- La lectura controlada se orienta al Control Cartera operativo.
- El servicio `app/services/workbook_loader.py` abre el archivo en modo de solo lectura y no guarda cambios.
- Los registros se cargan en estructuras internas preliminares en `app/domain/workbook_records.py`.
- La consola reporta solo resumen tecnico y nombres tecnicos seguros de columnas.
- El lector no exige columnas tecnicas auxiliares para cargar registros.
- Las filas se cargan por contenido util real para evitar mostrar filas vacias o solo formateadas.
- No se implementa todavia busqueda, edicion, persistencia ni normalizacion funcional definitiva.

## Decision arquitectonica de 1.8.0

- `python -m app` abre la interfaz grafica inicial.
- `python -m app --check` queda como modo tecnico secundario.
- La GUI vive en `app/ui/` y consume `app/services/workbook_loader.py`.
- La ventana prioriza la pestana `Registros`, mantiene un resumen de carga y muestra tabla de solo lectura.
- La seleccion de archivo es local y explicita; no se asume un nombre fijo con timestamp.
- No se implementa todavia busqueda, filtros, edicion ni persistencia.

## Decision arquitectonica de 1.8.1

- La tabla de registros usa un `QAbstractTableModel` propio para evitar carga manual celda por celda.
- La tabla vive en una pestana `Registros` y es de solo lectura.
- Los datos se muestran desde los registros cargados en memoria por `workbook_loader`.
- No se implementan busqueda, filtros, edicion, guardado ni persistencia.

## Decision arquitectonica de 1.8.2

- La fuente activa de lectura es `data/input/CONTROLCARTERA_V2.xlsx`.
- La GUI muestra esa ruta como predeterminada y ofrece una accion clara para cargarla.
- Se mantiene la seleccion manual de otro `.xlsx`, con carga automatica tras seleccion.
- Las ventanas emergentes de validacion usan mensajes amigables y sin trazas tecnicas crudas.
- Cancelar la seleccion de archivo conserva el estado anterior y no se trata como error.
- La pestana `Resumen` no muestra un panel visual de advertencias; conserva conteos, modo y estado de carga.
- Ningun flujo de visualizacion depende de `data/output/workbook_modernizado/`.

## Decision arquitectonica de 1.8.3

- Los estilos visuales se centralizan en `app/ui/theme.py`.
- El boton compacto de tema alterna entre tema claro y oscuro dentro de la ventana principal.
- La preferencia visual se guarda con `QSettings`, sin archivos de configuracion versionados.
- Cambiar el tema no recarga datos, no limpia registros y no modifica archivos Excel.

## Decision arquitectonica de 1.8.4

- Los assets visuales viven en `assets/`.
- El icono fuente del proyecto es `assets/app_icon.svg`.
- `app/ui/assets.py` resuelve rutas de assets en desarrollo y contempla `_MEIPASS` para futuros empaquetados con PyInstaller.
- El icono se aplica a `QApplication` y a la ventana principal sin introducir funcionalidad operativa nueva.
