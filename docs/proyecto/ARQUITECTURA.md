# Arquitectura

## Vision general

La aplicacion se disena como una herramienta de escritorio modular. Cada componente debera tener una responsabilidad clara y comunicarse mediante contratos simples para facilitar mantenimiento, pruebas y empaquetado.

Desde `1.4.0`, la arquitectura tambien contempla una capa de dataset canonico interno para desacoplar el modelo futuro de la app respecto del workbook operativo, sin reemplazarlo todavia.

## Modulos preliminares

### Interfaz

Responsable de presentar pantallas, formularios, acciones y mensajes al usuario. Desde `1.8.0` existe una primera ventana PySide6 para seleccionar y cargar visualmente un workbook modernizado.

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

- La modernizacion del workbook se ejecuta mediante script explicito, no desde el arranque de la app.
- El archivo original en `data/input/` no se modifica.
- La copia modernizada y reportes se generan en `data/output/workbook_modernizado/`.
- Las columnas auxiliares se agregan al final de la hoja principal y no reemplazan datos originales.
- Las inferencias siguen siendo preliminares y orientadas a revision humana.

## Decision arquitectonica de 1.7.0

- La lectura del workbook modernizado se ejecuta mediante script explicito, no desde el arranque de la app.
- El servicio `app/services/workbook_loader.py` abre el archivo en modo de solo lectura y no guarda cambios.
- Los registros se cargan en estructuras internas preliminares en `app/domain/workbook_records.py`.
- La consola reporta solo resumen tecnico y nombres tecnicos seguros de columnas.
- La ausencia de columnas `GS_*` no destruye la carga; marca la estructura como incompleta y genera advertencias.
- No se implementa todavia busqueda, edicion, persistencia ni normalizacion funcional definitiva.

## Decision arquitectonica de 1.8.0

- `python -m app` abre la interfaz grafica inicial.
- `python -m app --check` queda como modo tecnico secundario.
- La GUI vive en `app/ui/` y consume `app/services/workbook_loader.py`.
- La ventana muestra solo resumen de carga y advertencias, no registros completos.
- La seleccion de archivo es local y explicita; no se asume un nombre fijo con timestamp.
- No se implementa todavia tabla completa, busqueda, filtros, edicion ni persistencia.
