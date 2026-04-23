# Diccionario de Datos

## Estado

Version preliminar. Este diccionario sera refinado cuando se reciba y analice la base real en Excel. Los campos listados son tentativos y no representan reglas de negocio definitivas.

## Criterios generales

- Registrar moneda cuando aplique, contemplando colones y dolares.
- Mantener identificadores internos cuando exista persistencia local.
- Evitar asumir formatos finales hasta revisar datos reales.
- No borrar informacion automaticamente.
- Registrar cambios relevantes en bitacoras futuras cuando corresponda.

## Cliente

| Campo tentativo | Descripcion | Notas |
| --- | --- | --- |
| cliente_id | Identificador interno del cliente | Futuro campo tecnico |
| tipo_identificacion | Tipo de identificacion | Pendiente de catalogo |
| numero_identificacion | Numero de identificacion | Formato pendiente |
| nombre_completo | Nombre o razon social | Campo principal visible |
| telefono | Telefono de contacto | Opcional |
| correo | Correo electronico | Opcional |
| direccion | Direccion de contacto | Opcional |
| estado | Estado operativo del cliente | Pendiente de definir |

## Poliza

| Campo tentativo | Descripcion | Notas |
| --- | --- | --- |
| poliza_id | Identificador interno de poliza | Futuro campo tecnico |
| cliente_id | Relacion con cliente | Una persona puede tener varias polizas |
| numero_poliza | Numero de poliza | Formato pendiente |
| aseguradora | Entidad aseguradora | Pendiente de catalogo |
| tipo_seguro | Tipo de seguro | Pendiente de catalogo |
| moneda | Moneda de la poliza | CRC o USD tentativo |
| prima | Monto de prima | Reglas pendientes |
| fecha_inicio | Inicio de vigencia | Formato pendiente |
| fecha_fin | Fin de vigencia | Base para vencimientos futuros |
| estado | Estado operativo de poliza | Pendiente de definir |

## Vencimiento

| Campo tentativo | Descripcion | Notas |
| --- | --- | --- |
| vencimiento_id | Identificador interno | Futuro campo tecnico |
| cliente_id | Cliente asociado | Los documentos se generan por cliente |
| fecha_vencimiento | Fecha relevante de vencimiento | Reglas pendientes |
| moneda | Moneda relacionada | CRC o USD segun corresponda |
| monto | Monto relacionado | Pendiente de definicion |
| estado_gestion | Estado de seguimiento | Pendiente de definir |
| observaciones | Notas operativas | Opcional |

## Bitacora

| Campo tentativo | Descripcion | Notas |
| --- | --- | --- |
| bitacora_id | Identificador interno | Futuro campo tecnico |
| fecha_hora | Momento del evento | Con zona horaria local |
| usuario | Usuario o responsable | Pendiente de modelo de usuarios |
| accion | Accion realizada | Pendiente de catalogo |
| entidad | Tipo de informacion afectada | Cliente, poliza, documento, etc. |
| entidad_id | Identificador relacionado | Opcional |
| detalle | Descripcion del evento | Debe ser clara y auditable |

## Respaldo

| Campo tentativo | Descripcion | Notas |
| --- | --- | --- |
| respaldo_id | Identificador interno | Futuro campo tecnico |
| fecha_hora | Momento del respaldo | Con zona horaria local |
| ruta_archivo | Ubicacion del respaldo | Local |
| tipo_respaldo | Tipo de respaldo | Manual o futuro automatico controlado |
| estado | Resultado del respaldo | Exitoso, fallido, pendiente |
| observaciones | Detalle operativo | Opcional |
