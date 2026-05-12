# Manual de Usuario

## Estado del sistema

El sistema se encuentra en construcción. La versión actual permite cargar el Control Cartera operativo desde `data/input/CONTROLCARTERA_V2.xlsx`, ver un resumen de carga, visualizar registros en una tabla de solo lectura, buscar registros, filtrar por columna, revisar el detalle del registro seleccionado, aplicar ediciones controladas solo en memoria con controles por campo, errores bloqueantes y advertencias suaves, consultar una bitácora de cambios de la sesión, ocultar visualmente columnas de coberturas, alternar entre tema claro y oscuro y mostrar un ícono propio de la aplicación. Aún no ofrece guardado, documentos ni vencimientos.

El release técnico inicial `v1.8.4-alpha` se ejecuta mediante Python. Todavía no existe ejecutable, instalador ni paquete portable.

Este manual se actualizará en cada fase con instrucciones reales y verificadas. No se documentarán funciones que todavía no existan.

## Audiencia

Este manual está dirigido a usuarios operativos que utilizaran la aplicación para apoyar tareas relacionadas con clientes, pólizas, vencimientos, documentos y reportes.

## Secciones futuras

### 1. Instalación

Instrucciones para ejecutar la versión portable y, cuando exista, el instalador.

### 2. Inicio de la aplicación

Para abrir la interfaz gráfica:

```powershell
python -m app
```

La ventana muestra el nombre `Gestor de Seguros- Dagoberto Quirós Madriz`, la versión actual, una sección para seleccionar Control Cartera, la pestaña `Registros`, un resumen de carga y un botón compacto de tema.

### 2.1 Carga visual de Control Cartera

Para cargar la fuente predeterminada:

1. Presionar `Cargar predeterminado`.
2. Revisar la pestaña `Registros` y la tabla de solo lectura.
3. Abrir la pestaña `Resumen` para revisar conteos, modo de solo lectura y estado de carga.

Para cargar otro archivo:

1. Presionar `Seleccionar Control Cartera`.
2. Elegir un archivo `.xlsx`.
3. La aplicación carga automáticamente el archivo seleccionado.
4. Revisar la pestaña `Registros` y la tabla de solo lectura.
5. Abrir la pestaña `Resumen` para revisar conteos, modo de solo lectura y estado de carga.

Si se cancela el selector de archivo, la aplicación conserva el estado anterior sin mostrar error. Si el archivo no existe, no tiene extensión `.xlsx` o no puede cargarse, la aplicación mostrará un mensaje amigable y no intentará modificarlo.

La tabla permite revisar registros cargados dentro de la app local. Ajusta automáticamente anchos de columnas importantes, conserva el scroll horizontal y permite consultar valores largos con tooltip al pasar el cursor. No permite editar ni guardar cambios directamente en esta versión.

Las columnas de coberturas se conservan en memoria, pero no se muestran en la tabla, el detalle, la edición ni el selector `Buscar en`.

### 2.2 Búsqueda y filtros básicos

La pestaña `Registros` incluye una sección `Búsqueda` encima de la tabla.

Para buscar en todas las columnas:

1. Cargar un Control Cartera.
2. Mantener `Buscar en` con la opción `Todas las columnas`.
3. Escribir el texto en el campo `Buscar`.
4. Revisar el contador `Mostrando X de Y registros`.

Para buscar en una columna específica:

1. Cargar un Control Cartera.
2. Abrir el selector `Buscar en`.
3. Elegir una columna real del archivo cargado.
4. Escribir el texto buscado.

El botón `Limpiar` borra el texto de búsqueda, vuelve a `Todas las columnas` y muestra nuevamente todos los registros cargados. La búsqueda no modifica el archivo Excel ni los registros originales; solo cambia la visualización temporal en la tabla.

### 2.3 Detalle del registro

La pestaña `Registros` permite abrir una ventana `Detalle del registro`.

Para revisar un registro:

1. Cargar un Control Cartera.
2. Hacer doble clic sobre una fila en la tabla.
3. Revisar los campos y valores mostrados en la ventana de detalle.
4. Cerrar la ventana con el botón `Cerrar`.

El detalle respeta la búsqueda y los filtros activos. Los campos vacíos no se muestran. La vista de detalle es de consulta: permite abrir la edición controlada, pero no modifica el archivo Excel por sí misma.

### 2.4 Edición controlada en memoria

La ventana `Detalle del registro` incluye la acción `Editar registro`.

Para editar un registro en memoria:

1. Cargar un Control Cartera.
2. Hacer doble clic sobre una fila de la tabla.
3. Presionar `Editar registro`.
4. Modificar los campos necesarios en la ventana `Editar registro`.
5. Presionar `Aplicar cambios`.
6. Confirmar que los cambios se aplicarán solo en memoria.

La edición usa controles específicos cuando aplica: `Vigencia`, `DÍA` y `MES` usan listas controladas no editables, y `Detalle` usa un área multilínea. El resto de campos se mantiene como texto para conservar formatos originales.

Antes de aplicar, la app valida los campos editados. Los errores bloqueantes no permiten aplicar cambios: por ejemplo `Nº Póliza`, `Nombre del Asegurado` o `Vigencia` vacíos, una `Vigencia` fuera de catálogo, una `Emisión` con texto libre o fecha inválida, una fecha de vencimiento imposible o incompleta cuando aplica, o montos con formato inválido. Las advertencias suaves permiten revisar y cancelar, o aplicar de todos modos. Ninguna validación guarda nada en Excel ni cambia el archivo original.

El botón `Cancelar` cierra la ventana sin aplicar cambios. Al aplicar cambios, la tabla se actualiza en memoria y la aplicación muestra `Cambios pendientes: X`.

### 2.5 Guardar sobre el archivo cargado

La acción `Guardar` escribe los cambios pendientes sobre el Control Cartera cargado.

Reglas de uso:

- el botón permanece deshabilitado si no hay cambios pendientes;
- antes de guardar, la app solicita confirmación;
- antes de modificar el archivo cargado, la app crea un respaldo automático en `data/backups/guardado_control_cartera/`;
- si el respaldo falla, no se guarda nada;
- si el archivo está abierto en Excel o no se puede escribir, los cambios pendientes se mantienen en memoria;
- las columnas ocultas de coberturas, hojas existentes, filas no modificadas y columnas no modificadas se conservan;
- después de guardar correctamente se limpian los cambios pendientes, pero la pestaña `Bitácora` sigue visible durante la sesión.

### 2.6 Guardar como copia

La acción `Guardar como` permite crear una copia `.xlsx` del Control Cartera con los cambios aplicados en memoria.

Campos obligatorios como `Nº Póliza` y `Nombre del Asegurado` pueden editarse y exportarse, siempre que no queden vacíos y pasen las validaciones. La app guarda esos cambios en la copia usando la ubicación real de la fila y la columna, no el valor de la póliza o del nombre como identificador.

Reglas de uso:

- el archivo cargado no se sobrescribe;
- si se elige una ruta sin extensión, la app usa `.xlsx`;
- si se elige una ruta con otra extensión, se muestra un error;
- si la ruta destino ya existe, la app solicita confirmación antes de sobrescribir esa copia;
- las columnas ocultas de coberturas se conservan en la copia;
- al guardar correctamente se limpian los cambios pendientes, pero la pestaña `Bitácora` sigue visible durante la sesión.

Si no hay cambios pendientes, `Guardar como` puede crear una copia equivalente del archivo cargado.

Cada campo realmente modificado genera una entrada en la pestaña `Bitácora`. Si existen cambios pendientes y se intenta cargar otro Control Cartera o cerrar la aplicación, el sistema muestra una advertencia para continuar descartando los cambios en memoria o cancelar la acción.

### 2.7 Ayuda y Acerca de

El botón `Ayuda` abre una guía rápida de uso. También puede abrirse con `F1`.

La ayuda integrada resume:

- cómo cargar el Control Cartera;
- cómo buscar registros;
- cómo abrir el detalle con doble clic;
- cómo editar desde el detalle;
- cómo usar `Guardar`;
- cómo usar `Guardar como`;
- dónde se crean los respaldos automáticos;
- qué hacer si el archivo está abierto en Excel y no se puede guardar.

El botón `Acerca de` muestra el nombre de la aplicación, versión, autor, descripción breve y una nota sobre el respaldo automático previo al guardado.

Atajos disponibles:

- `F1`: abrir ayuda;
- `Ctrl+S`: ejecutar `Guardar`;
- `Ctrl+Shift+S`: ejecutar `Guardar como`.

### 2.8 Bitácora en memoria

La pestaña `Bitácora` muestra los cambios registrados durante la sesión actual.

La tabla de bitácora incluye:

- fecha y hora;
- registro técnico modificado;
- campo;
- valor anterior;
- valor nuevo;
- origen;
- estado.

La bitácora es de solo lectura y no se guarda en archivos, base de datos ni Excel. Si se carga otro Control Cartera descartando cambios, o si se cierra la aplicación descartando cambios pendientes, la bitácora en memoria se pierde.

### 2.7 Coberturas ocultas visualmente

Las columnas de coberturas quedan ocultas en esta versión para simplificar la operación diaria. No se eliminan del registro cargado en memoria y se reservan para futuras exportaciones, depuración o controles específicos.

Esta fase no implementa edición de coberturas ni guardado persistente.

### 2.8 Tema claro y oscuro

El botón compacto de tema permite cambiar entre tema claro y tema oscuro. La preferencia se conserva localmente para la siguiente apertura de la aplicación. Cambiar el tema no recarga el Control Cartera, no limpia registros y no modifica ningún archivo Excel.

### 2.9 Ícono de aplicación

La ventana usa un ícono propio, sobrio y genérico del proyecto. No corresponde a logos oficiales del INS ni a marcas externas.

### 3. Gestión de clientes

Instrucciones para consultar, crear, editar o revisar información de clientes cuando esta función exista.

### 4. Gestión de pólizas

Instrucciones para trabajar con pólizas en colones y dólares cuando el módulo este implementado.

### 5. Vencimientos

Instrucciones para revisar vencimientos y generar documentos por cliente, no por póliza, cuando esta función este disponible.

### 6. Documentos

Uso de plantillas y generación de documentos cuando el módulo DOCX este implementado.

### 7. Respaldos

Procedimientos de respaldo, restauracion y verificacion cuando sean definidos.

### 8. Reportes

Consulta de reportes operativos y exportaciones cuando existan.

### 9. Confirmaciones y seguridad operativa

El sistema no deberá borrar información automáticamente. Cualquier eliminación futura deberá requerir confirmación explícita del usuario.

## Limitaciones de la versión actual

- La interfaz muestra resumen de carga y tabla de solo lectura.
- Hay búsqueda y filtros básicos sobre los registros cargados.
- Hay vista de detalle para el registro seleccionado.
- Hay edición controlada solo en memoria.
- Hay controles por campo, errores bloqueantes y advertencias suaves confirmables.
- Hay bitácora de cambios solo en memoria durante la sesión.
- Las columnas de coberturas se ocultan visualmente, pero se conservan en memoria.
- No hay base de datos operativa.
- No hay importación persistente de datos.
- No hay guardado persistente en Excel.
- No hay exportación persistente de bitácora.
- No hay eliminación de registros.
- No hay guardado persistente ni validaciones definitivas de negocio.
- No hay generación de documentos.
- No hay reportes ni dashboards funcionales.
