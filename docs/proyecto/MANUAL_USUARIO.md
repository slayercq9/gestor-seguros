# Manual de Usuario

## Estado del sistema

El sistema se encuentra en construccion. La version actual permite cargar el Control Cartera operativo desde `data/input/CONTROLCARTERA_V2.xlsx`, ver un resumen de carga, visualizar registros en una tabla de solo lectura y alternar entre tema claro y oscuro. Aun no ofrece busqueda, filtros, edicion, guardado, documentos ni vencimientos.

Este manual se actualizara en cada fase con instrucciones reales y verificadas. No se documentaran funciones que todavia no existan.

## Audiencia

Este manual esta dirigido a usuarios operativos que utilizaran la aplicacion para apoyar tareas relacionadas con clientes, polizas, vencimientos, documentos y reportes.

## Secciones futuras

### 1. Instalacion

Instrucciones para ejecutar la version portable y, cuando exista, el instalador.

### 2. Inicio de la aplicacion

Para abrir la interfaz grafica:

```powershell
python -m app
```

La ventana muestra el nombre `Gestor de Seguros- Dagoberto Quirós Madriz`, la version actual, una seccion para seleccionar Control Cartera, la pestana `Registros`, un resumen de carga y un boton compacto de tema.

### 2.1 Carga visual de Control Cartera

Para cargar la fuente predeterminada:

1. Presionar `Cargar predeterminado`.
2. Revisar la pestana `Registros` y la tabla de solo lectura.
3. Abrir la pestana `Resumen` para revisar conteos, modo de solo lectura y estado de carga.

Para cargar otro archivo:

1. Presionar `Seleccionar Control Cartera`.
2. Elegir un archivo `.xlsx`.
3. La aplicacion carga automaticamente el archivo seleccionado.
4. Revisar la pestana `Registros` y la tabla de solo lectura.
5. Abrir la pestana `Resumen` para revisar conteos, modo de solo lectura y estado de carga.

Si se cancela el selector de archivo, la aplicacion conserva el estado anterior sin mostrar error. Si el archivo no existe, no tiene extension `.xlsx` o no puede cargarse, la aplicacion mostrara un mensaje amigable y no intentara modificarlo.

La tabla permite revisar registros cargados dentro de la app local. No permite editar ni guardar cambios en esta version.

### 2.2 Tema claro y oscuro

El boton compacto de tema permite cambiar entre tema claro y tema oscuro. La preferencia se conserva localmente para la siguiente apertura de la aplicacion. Cambiar el tema no recarga el Control Cartera, no limpia registros y no modifica ningun archivo Excel.

### 3. Gestion de clientes

Instrucciones para consultar, crear, editar o revisar informacion de clientes cuando esta funcion exista.

### 4. Gestion de polizas

Instrucciones para trabajar con polizas en colones y dolares cuando el modulo este implementado.

### 5. Vencimientos

Instrucciones para revisar vencimientos y generar documentos por cliente, no por poliza, cuando esta funcion este disponible.

### 6. Documentos

Uso de plantillas y generacion de documentos cuando el modulo DOCX este implementado.

### 7. Respaldos

Procedimientos de respaldo, restauracion y verificacion cuando sean definidos.

### 8. Reportes

Consulta de reportes operativos y exportaciones cuando existan.

### 9. Confirmaciones y seguridad operativa

El sistema no debera borrar informacion automaticamente. Cualquier eliminacion futura debera requerir confirmacion explicita del usuario.

## Limitaciones de la version actual

- La interfaz muestra resumen de carga y tabla de solo lectura.
- No hay base de datos operativa.
- No hay importacion persistente de datos.
- No hay busqueda ni filtros.
- No hay edicion ni guardado.
- No hay generacion de documentos.
- No hay reportes ni dashboards funcionales.
