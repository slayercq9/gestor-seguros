# Manual de Usuario

## Estado del sistema

El sistema se encuentra en construccion. La version actual ofrece una primera interfaz grafica para seleccionar un Control Cartera modernizado y ver un resumen de carga seguro. Aun no ofrece consulta completa de registros, busqueda, edicion, guardado, documentos ni vencimientos.

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

La ventana muestra el nombre `Gestor de Seguros- Dagoberto Quirós Madriz`, la version actual, una seccion para seleccionar Control Cartera, un boton de carga, un resumen y un area de advertencias.

### 2.1 Carga visual de Control Cartera modernizado

1. Presionar `Seleccionar Control Cartera`.
2. Elegir un archivo `.xlsx` modernizado generado localmente.
3. Presionar `Cargar Control Cartera`.
4. Revisar el resumen de carga y las advertencias.

Si el archivo no existe o no tiene extension `.xlsx`, la aplicacion mostrara un mensaje amigable y no intentara cargarlo.

La pantalla no muestra registros completos de clientes, polizas, cedulas, placas, telefonos ni detalle.

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

- La interfaz solo muestra resumen de carga.
- No hay base de datos operativa.
- No hay importacion persistente de datos.
- No hay busqueda ni filtros.
- No hay edicion ni guardado.
- No hay generacion de documentos.
- No hay reportes ni dashboards funcionales.
