# Diccionario de Datos

## Estado

Version preliminar ampliada. Este diccionario seguira refinandose cuando se valide mejor la base real y se apruebe la implementacion del modelo interno. Los campos listados no representan reglas de negocio definitivas.

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
- `Numero de Poliza` puede contener formatos diversos; no debe asumirse un unico patron todavia.
- Las polizas que inician en `01` corresponden preliminarmente a colones.
- Las polizas que inician en `02` corresponden preliminarmente a dolares.
- La regla de moneda por prefijo no aplica a riesgos del trabajo, identificados preliminarmente como polizas cuyo numero es completamente numerico.
- La fecha de vencimiento puede venir separada en dia, mes y ano.
- La columna `detalle` se usa para anotaciones o para relacionar polizas de un mismo dueno.
- `Numero de Placa / Finca` usualmente contiene numeros de placa de vehiculos, aunque debe validarse con la base real.

## Dimensiones de clasificacion

Cada campo debe evaluarse, segun aplique, en estas dimensiones:

- `Procedencia`: original, normalizado, derivado u operativo.
- `Sensible`: si o no.
- `Editable futuro`: si o no.
- `Entidad`: cliente, poliza, vencimiento, relacion o metadato.

## Cliente

| Campo tentativo | Descripcion | Procedencia | Sensible | Editable futuro | Notas |
| --- | --- | --- | --- | --- | --- |
| cliente_id | Identificador interno del cliente | Operativo | No | No | Futuro campo tecnico |
| nombre_original | Nombre o razon social tal como llega | Original | Si | No | Debe preservarse sin sobrescribir |
| tipo_identificacion_normalizado | Tipo de identificacion normalizado | Normalizado | Si | No | Cedula fisica, juridica, pasaporte o extranjero |
| identificacion_original | Identificacion tal como llega | Original | Si | No | Puede variar por tipo |
| identificacion_normalizada | Identificacion llevada a formato tecnico | Normalizado | Si | No | Pendiente de politica final |
| telefono_original | Telefono de contacto | Original | Si | No | Opcional |
| correo_original | Correo electronico | Original | Si | No | Opcional |
| direccion_original | Direccion de contacto | Original | Si | No | Opcional |
| requiere_revision_cliente | Indicador de revision del registro | Derivado | No | No | Para conflictos o ambiguedades |
| observacion_revision_cliente | Nota operativa interna | Operativo | No | Si | No reemplaza al origen |

## Poliza

| Campo tentativo | Descripcion | Procedencia | Sensible | Editable futuro | Notas |
| --- | --- | --- | --- | --- | --- |
| poliza_id | Identificador interno de poliza | Operativo | No | No | Futuro campo tecnico |
| cliente_id | Relacion con cliente | Operativo | No | No | Una persona puede tener varias polizas |
| numero_poliza_original | Numero de poliza original | Original | Si | No | Respetar valor original |
| numero_poliza_normalizado | Numero de poliza para clasificacion tecnica | Normalizado | Si | No | No sustituye al original |
| aseguradora_original | Entidad aseguradora | Original | No | No | Pendiente de catalogo |
| tipo_seguro_original | Tipo de seguro | Original | No | No | Pendiente de catalogo |
| vigencia_original | Vigencia registrada | Original | No | No | Puede incluir `D.M.` |
| frecuencia_normalizada | Frecuencia normalizada | Normalizado | No | No | Mensual, trimestral, semestral, anual u otra |
| frecuencia_observada | Categoria observada en auditoria | Derivado | No | No | Preliminar |
| es_dm | Indicador de deduccion mensual | Derivado | No | No | No implica logica funcional aun |
| genera_aviso | Indicador futuro de aviso | Derivado | No | No | Solo documentado en esta fase |
| moneda_normalizada | Moneda inferida o validada | Derivado | No | No | Regla `01` y `02` es preliminar |
| es_riesgo_trabajo_probable | Excepcion preliminar para polizas numericas | Derivado | No | No | Requiere validacion posterior |
| numero_placa_finca_original | Valor de placa o finca | Original | Si | No | Usualmente placa de vehiculo |
| detalle_original | Anotacion o relacion entre polizas | Original | Si | No | Puede requerir revision manual |
| requiere_revision_poliza | Indicador de conflicto o ambiguedad | Derivado | No | No | Para soporte operativo futuro |
| observacion_revision_poliza | Nota operativa interna | Operativo | No | Si | Separada del origen |

## Vencimiento

| Campo tentativo | Descripcion | Procedencia | Sensible | Editable futuro | Notas |
| --- | --- | --- | --- | --- | --- |
| vencimiento_id | Identificador interno | Operativo | No | No | Futuro campo tecnico |
| poliza_id | Poliza asociada | Operativo | No | No | Los documentos futuros se generan por cliente |
| fecha_vencimiento_original | Fecha relevante de vencimiento | Original | No | No | Puede venir completa |
| dia_vencimiento_original | Dia de vencimiento | Original | No | No | Campo posible de origen |
| mes_vencimiento_original | Mes de vencimiento | Original | No | No | Campo posible de origen |
| ano_vencimiento_original | Ano de vencimiento | Original | No | No | Campo posible de origen |
| fecha_vencimiento_normalizada | Fecha consolidada | Derivado | No | No | Derivada de fecha unica o partes |
| requiere_revision_fecha | Indicador de inconsistencia de fecha | Derivado | No | No | Para validacion futura |
| estado_gestion_vencimiento | Estado operativo de seguimiento | Operativo | No | Si | Pendiente de definir |

## Relacion Cliente-Poliza

| Campo tentativo | Descripcion | Procedencia | Sensible | Editable futuro | Notas |
| --- | --- | --- | --- | --- | --- |
| relacion_cliente_poliza_id | Identificador interno | Operativo | No | No | Futuro campo tecnico |
| cliente_id | Cliente asociado | Operativo | No | No | Relacion interna |
| poliza_id | Poliza asociada | Operativo | No | No | Relacion interna |
| rol_relacion | Clasificacion operativa de la relacion | Operativo | No | Si | Pendiente de definicion |
| relacion_detectada_desde_detalle | Marca de relacion sugerida | Derivado | No | No | Debe revisarse con cautela |
| requiere_revision_relacion | Indicador de revision | Derivado | No | No | Casos ambiguos o incompletos |

## Bitacora

| Campo tentativo | Descripcion | Procedencia | Sensible | Editable futuro | Notas |
| --- | --- | --- | --- | --- | --- |
| bitacora_id | Identificador interno | Operativo | No | No | Futuro campo tecnico |
| fecha_hora | Momento del evento | Operativo | No | No | Con zona horaria local |
| usuario | Usuario o responsable | Operativo | No | No | Pendiente de modelo de usuarios |
| accion | Accion realizada | Operativo | No | No | Pendiente de catalogo |
| entidad | Tipo de informacion afectada | Operativo | No | No | Cliente, poliza, documento, etc. |
| entidad_id | Identificador relacionado | Operativo | No | No | Opcional |
| detalle_evento | Descripcion del evento | Operativo | No | Si | Debe ser clara y auditable |

## Respaldo

| Campo tentativo | Descripcion | Procedencia | Sensible | Editable futuro | Notas |
| --- | --- | --- | --- | --- | --- |
| respaldo_id | Identificador interno | Operativo | No | No | Futuro campo tecnico |
| fecha_hora | Momento del respaldo | Operativo | No | No | Con zona horaria local |
| ruta_archivo | Ubicacion del respaldo | Operativo | Si | No | Local |
| tipo_respaldo | Tipo de respaldo | Operativo | No | No | Manual o futuro automatico controlado |
| estado | Resultado del respaldo | Operativo | No | No | Exitoso, fallido, pendiente |
| observaciones | Detalle operativo | Operativo | No | Si | Opcional |

## Referencias de diseno relacionadas

- `docs/proyecto/ESPECIFICACION_DATASET_CANONICO.md`
- `docs/proyecto/MAPA_ORIGEN_A_CANONICO.md`
- `docs/proyecto/ESTRATEGIA_MODERNIZACION_WORKBOOK.md`

## Columnas tecnicas auxiliares

Desde `1.8.2`, el sistema retira definitivamente las columnas tecnicas auxiliares del flujo activo. La aplicacion lee el Control Cartera operativo desde `data/input/CONTROLCARTERA_V2.xlsx` y muestra solo columnas reales del archivo.

Las reglas preliminares de frecuencia, moneda, identificacion y revision podran mantenerse como logica interna en fases futuras, pero no deben generar columnas visibles ni mezclarse con los datos originales sin una decision aprobada.
