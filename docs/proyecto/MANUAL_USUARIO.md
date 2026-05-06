# Manual de Usuario

## Estado del sistema

El sistema se encuentra en construcción. La versión actual permite cargar el Control Cartera operativo desde `data/input/CONTROLCARTERA_V2.xlsx`, ver un resumen de carga, visualizar registros en una tabla de solo lectura, alternar entre tema claro y oscuro y mostrar un ícono propio de la aplicación. Aun no ofrece búsqueda, filtros, edición, guardado, documentos ni vencimientos.

El release técnico inicial `v1.8.4-alpha` se ejecuta mediante Python. Todavia no existe ejecutable, instalador ni paquete portable.

Este manual se actualizara en cada fase con instrucciones reales y verificadas. No se documentaran funciones que todavía no existan.

## Audiencia

Este manual está dirigido a usuarios operativos que utilizaran la aplicación para apoyar tareas relacionadas con clientes, pólizas, vencimientos, documentos y reportes.

## Secciones futuras

### 1. Instalación

Instrucciones para ejecutar la versión portable y, cuando exista, el instalador.

### 2. Inicio de la aplicación

Para abrir la interfaz grafica:

```powershell
python -m app
```

La ventana muestra el nombre `Gestor de Seguros- Dagoberto Quirós Madriz`, la versión actual, una seccion para seleccionar Control Cartera, la pestaña `Registros`, un resumen de carga y un botón compacto de tema.

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

Si se cancela el selector de archivo, la aplicación conserva el estado anterior sin mostrar error. Si el archivo no existe, no tiene extensión `.xlsx` o no puede cargarse, la aplicación mostrara un mensaje amigable y no intentara modificarlo.

La tabla permite revisar registros cargados dentro de la app local. No permite editar ni guardar cambios en esta versión.

### 2.2 Tema claro y oscuro

El botón compacto de tema permite cambiar entre tema claro y tema oscuro. La preferencia se conserva localmente para la siguiente apertura de la aplicación. Cambiar el tema no recarga el Control Cartera, no limpia registros y no modifica ningun archivo Excel.

### 2.3 ícono de aplicación

La ventana usa un ícono propio, sobrio y generico del proyecto. No corresponde a logos oficiales del INS ni a marcas externas.

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
- No hay base de datos operativa.
- No hay importación persistente de datos.
- No hay búsqueda ni filtros.
- No hay edición ni guardado.
- No hay generación de documentos.
- No hay reportes ni dashboards funcionales.
