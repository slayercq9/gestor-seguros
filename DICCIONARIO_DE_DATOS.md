# Diccionario de Datos

## Estado

Version preliminar. Este diccionario sera refinado cuando se reciba y analice la base real en Excel. Los campos listados son tentativos y no representan reglas de negocio definitivas.

## Criterios generales

- Registrar moneda cuando aplique, contemplando colones y dolares.
- Mantener identificadores internos cuando exista persistencia local.
- Evitar asumir formatos finales hasta revisar datos reales.
- No borrar informacion automaticamente.
- Registrar cambios relevantes en bitacoras futuras cuando corresponda.
- Respetar los nombres originales de registros provenientes de la base.
- Tratar las reglas conocidas como preliminares hasta validarlas con datos reales.

## Notas preliminares de la base

- Los formatos de identificacion pueden incluir cedula fisica, cedula juridica, pasaporte o identificacion de extranjero.
- Las vigencias `D.M.` significan deduccion mensual.
- Las polizas con vigencia `D.M.` no generan avisos, pero si deben almacenarse.
- Tambien pueden observarse frecuencias mensuales, trimestrales, semestrales y anuales.
- Las frecuencias observadas se documentan como categorias preliminares, no como reglas rigidas.
- `Nº Poliza` puede contener formatos diversos; no debe asumirse un unico patron todavia.
- Las polizas que inician en `01` corresponden preliminarmente a colones.
- Las polizas que inician en `02` corresponden preliminarmente a dolares.
- La regla de moneda por prefijo no aplica a riesgos del trabajo, identificados preliminarmente como polizas cuyo numero es completamente numerico.
- La fecha de vencimiento puede venir separada en dia, mes y ano.
- La columna `detalle` se usa para anotaciones o para relacionar polizas de un mismo dueno.
- `Nº Placa / Finca` usualmente contiene numeros de placa de vehiculos, aunque debe validarse con la base real.

## Cliente

| Campo tentativo | Descripcion | Notas |
| --- | --- | --- |
| cliente_id | Identificador interno del cliente | Futuro campo tecnico |
| tipo_identificacion | Tipo de identificacion | Cedula fisica, cedula juridica, pasaporte o extranjero |
| numero_identificacion | Numero de identificacion | Puede variar por tipo de identificacion |
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
| numero_poliza | Numero de poliza | Formatos diversos; respetar valor original |
| aseguradora | Entidad aseguradora | Pendiente de catalogo |
| tipo_seguro | Tipo de seguro | Pendiente de catalogo |
| vigencia | Vigencia registrada | `D.M.` significa deduccion mensual |
| frecuencia_observada | Categoria preliminar de frecuencia | D.M., mensual, trimestral, semestral, anual u otros formatos |
| moneda | Moneda de la poliza | CRC o USD; prefijos `01`/`02` son regla preliminar con excepcion |
| prima | Monto de prima | Reglas pendientes |
| fecha_inicio | Inicio de vigencia | Formato pendiente |
| fecha_fin | Fin de vigencia | Puede derivarse de dia, mes y ano separados |
| numero_placa_finca | Nº Placa / Finca | Usualmente placa de vehiculo; pendiente validar |
| detalle | Detalle | Anotaciones o relacion entre polizas de un mismo dueno |
| estado | Estado operativo de poliza | Pendiente de definir |

## Vencimiento

| Campo tentativo | Descripcion | Notas |
| --- | --- | --- |
| vencimiento_id | Identificador interno | Futuro campo tecnico |
| cliente_id | Cliente asociado | Los documentos se generan por cliente |
| fecha_vencimiento | Fecha relevante de vencimiento | Puede venir separada en dia, mes y ano |
| dia_vencimiento | Dia de vencimiento | Campo posible de origen |
| mes_vencimiento | Mes de vencimiento | Campo posible de origen |
| ano_vencimiento | Ano de vencimiento | Campo posible de origen |
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
