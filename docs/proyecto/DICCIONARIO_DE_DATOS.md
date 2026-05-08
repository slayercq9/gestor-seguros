# Diccionario de Datos

## Estado

Versión preliminar ampliada. Este diccionario seguirá refinándose cuando se valide mejor la base real y se apruebe la implementación del modelo interno. Los campos listados no representan reglas de negocio definitivas.

## Criterios generales

- Registrar moneda cuando aplique, contemplando colones y dólares.
- Mantener identificadores internos cuando exista persistencia local.
- Evitar asumir formatos finales hasta revisar datos reales.
- No borrar información automáticamente.
- Registrar cambios relevantes en bitácoras futuras cuando corresponda.
- Respetar los nombres originales de registros provenientes de la base.
- Tratar las reglas conocidas como preliminares hasta validarlas con datos reales.

## Notas preliminares de la base

- Los formatos de identificación pueden incluir cédula fisica, cédula juridica, pasaporte o identificación de extranjero.
- Las vigencias `D.M.` significan deduccion mensual.
- Las pólizas con vigencia `D.M.` no generan avisos, pero si deben almacenarse.
- Tambien pueden observarse frecuencias mensuales, trimestrales, semestrales y anuales.
- Las frecuencias observadas se documentan como categorías preliminares, no como reglas rigidas.
- `Numero de Poliza` puede contener formatos diversos; no debe asumirse un único patrón todavía.
- Las pólizas que inician en `01` corresponden preliminarmente a colones.
- Las pólizas que inician en `02` corresponden preliminarmente a dólares.
- La regla de moneda por prefijo no aplica a riesgos del trabajo, identificados preliminarmente como pólizas cuyo número es completamente numerico.
- La fecha de vencimiento puede venir separada en día, mes y año.
- La columna `detalle` se usa para anotaciones o para relacionar pólizas de un mismo dueño.
- `Numero de Placa / Finca` usualmente contiene números de placa de vehiculos, aúnque debe validarse con la base real.

## Dimensiones de clasificación

Cada campo debe evaluarse, segun aplique, en estas dimensiones:

- `Procedencia`: original, normalizado, derivado u operativo.
- `Sensible`: si o no.
- `Editable futuro`: si o no.
- `Entidad`: cliente, póliza, vencimiento, relación o metadato.

## Vista de detalle en GUI

La vista de detalle agregada en `1.9.1` no introduce campos nuevos al modelo de datos ni modifica el Control Cartera. Presenta, en modo solo lectura, los encabezados visibles de la tabla y los valores con información del registro seleccionado. Los campos vacíos se omiten para mejorar lectura, sin cambiar el valor original en memoria ni en Excel.

## Estándares de columnas del Control Cartera

Desde `1.10.2`, los estándares funcionales de columnas se documentan en `docs/proyecto/ESTANDARES_COLUMNAS_CONTROL_CARTERA.md`.

Las columnas de coberturas se conservan en memoria, pero quedan ocultas visualmente en tabla, detalle, edición y búsqueda. Esta decisión no elimina columnas, no elimina datos y no modifica el Excel. Desde `1.10.3`, la edición incorpora controles por campo y validaciones suaves no bloqueantes; el guardado persistente y las validaciones fuertes quedan para una fase posterior.

## Cliente

| Campo tentativo | Descripcion | Procedencia | Sensible | Editable futuro | Notas |
| --- | --- | --- | --- | --- | --- |
| cliente_id | Identificador interno del cliente | Operativo | No | No | Futuro campo técnico |
| nombre_original | Nombre o razon social tal como llega | Original | Si | No | Debe preservarse sin sobrescribir |
| tipo_identificacion_normalizado | Tipo de identificación normalizado | Normalizado | Si | No | Cédula fisica, juridica, pasaporte o extranjero |
| identificacion_original | Identificacion tal como llega | Original | Si | No | Puede variar por tipo |
| identificacion_normalizada | Identificacion llevada a formato técnico | Normalizado | Si | No | Pendiente de política final |
| telefono_original | Telefono de contacto | Original | Si | No | Opcional |
| correo_original | Correo electronico | Original | Si | No | Opcional |
| direccion_original | Direccion de contacto | Original | Si | No | Opcional |
| requiere_revision_cliente | Indicador de revisión del registro | Derivado | No | No | Para conflictos o ambigüedades |
| observacion_revision_cliente | Nota operativa interna | Operativo | No | Si | No reemplaza al origen |

## Póliza

| Campo tentativo | Descripcion | Procedencia | Sensible | Editable futuro | Notas |
| --- | --- | --- | --- | --- | --- |
| poliza_id | Identificador interno de póliza | Operativo | No | No | Futuro campo técnico |
| cliente_id | Relacion con cliente | Operativo | No | No | Una persona puede tener varias pólizas |
| numero_poliza_original | Número de póliza original | Original | Si | No | Respetar valor original |
| numero_poliza_normalizado | Número de póliza para clasificación técnica | Normalizado | Si | No | No sustituye al original |
| aseguradora_original | Entidad aseguradora | Original | No | No | Pendiente de catalogo |
| tipo_seguro_original | Tipo de seguro | Original | No | No | Pendiente de catalogo |
| vigencia_original | Vigencia registrada | Original | No | No | Puede incluir `D.M.` |
| frecuencia_normalizada | Frecuencia normalizada | Normalizado | No | No | Mensual, trimestral, semestral, anual u otra |
| frecuencia_observada | Categoria observada en auditoría | Derivado | No | No | Preliminar |
| es_dm | Indicador de deduccion mensual | Derivado | No | No | No implica lógica funcional aún |
| genera_aviso | Indicador futuro de aviso | Derivado | No | No | Solo documentado en esta fase |
| moneda_normalizada | Moneda inferida o validada | Derivado | No | No | Regla `01` y `02` es preliminar |
| es_riesgo_trabajo_probable | Excepcion preliminar para pólizas numéricas | Derivado | No | No | Requiere validación posterior |
| numero_placa_finca_original | Valor de placa o finca | Original | Si | No | Usualmente placa de vehiculo |
| detalle_original | Anotacion o relación entre pólizas | Original | Si | No | Puede requerir revisión manual |
| requiere_revision_poliza | Indicador de conflicto o ambigüedad | Derivado | No | No | Para soporte operativo futuro |
| observacion_revision_poliza | Nota operativa interna | Operativo | No | Si | Separada del origen |

## Vencimiento

| Campo tentativo | Descripcion | Procedencia | Sensible | Editable futuro | Notas |
| --- | --- | --- | --- | --- | --- |
| vencimiento_id | Identificador interno | Operativo | No | No | Futuro campo técnico |
| poliza_id | Póliza asociada | Operativo | No | No | Los documentos futuros se generan por cliente |
| fecha_vencimiento_original | Fecha relevante de vencimiento | Original | No | No | Puede venir completa |
| día_vencimiento_original | Día de vencimiento | Original | No | No | Campo posible de origen |
| mes_vencimiento_original | Mes de vencimiento | Original | No | No | Campo posible de origen |
| ano_vencimiento_original | Ano de vencimiento | Original | No | No | Campo posible de origen |
| fecha_vencimiento_normalizada | Fecha consolidada | Derivado | No | No | Derivada de fecha única o partes |
| requiere_revision_fecha | Indicador de inconsistencia de fecha | Derivado | No | No | Para validación futura |
| estado_gestion_vencimiento | Estado operativo de seguimiento | Operativo | No | Si | Pendiente de definir |

## Relacion Cliente-Póliza

| Campo tentativo | Descripcion | Procedencia | Sensible | Editable futuro | Notas |
| --- | --- | --- | --- | --- | --- |
| relacion_cliente_poliza_id | Identificador interno | Operativo | No | No | Futuro campo técnico |
| cliente_id | Cliente asociado | Operativo | No | No | Relacion interna |
| poliza_id | Póliza asociada | Operativo | No | No | Relacion interna |
| rol_relacion | Clasificacion operativa de la relación | Operativo | No | Si | Pendiente de definicion |
| relacion_detectada_desde_detalle | Marca de relación sugerida | Derivado | No | No | Debe revisarse con cautela |
| requiere_revision_relacion | Indicador de revisión | Derivado | No | No | Casos ambiguos o incompletos |

## Bitacora

| Campo tentativo | Descripcion | Procedencia | Sensible | Editable futuro | Notas |
| --- | --- | --- | --- | --- | --- |
| bitacora_id | Identificador interno | Operativo | No | No | Futuro campo técnico |
| fecha_hora | Momento del evento | Operativo | No | No | Con zona horaria local |
| usuario | Usuario o responsable | Operativo | No | No | Pendiente de modelo de usuarios |
| acción | Accion realizada | Operativo | No | No | Pendiente de catalogo |
| entidad | Tipo de información afectada | Operativo | No | No | Cliente, póliza, documento, etc. |
| entidad_id | Identificador relacionado | Operativo | No | No | Opcional |
| detalle_evento | Descripcion del evento | Operativo | No | Si | Debe ser clara y auditable |

## Respaldo

| Campo tentativo | Descripcion | Procedencia | Sensible | Editable futuro | Notas |
| --- | --- | --- | --- | --- | --- |
| respaldo_id | Identificador interno | Operativo | No | No | Futuro campo técnico |
| fecha_hora | Momento del respaldo | Operativo | No | No | Con zona horaria local |
| ruta_archivo | Ubicacion del respaldo | Operativo | Si | No | Local |
| tipo_respaldo | Tipo de respaldo | Operativo | No | No | Manual o futuro automático controlado |
| estado | Resultado del respaldo | Operativo | No | No | Exitoso, fallido, pendiente |
| observaciones | Detalle operativo | Operativo | No | Si | Opcional |

## Referencias de diseño relacionadas

- `docs/proyecto/ESPECIFICACION_DATASET_CANONICO.md`
- `docs/proyecto/MAPA_ORIGEN_A_CANONICO.md`
- `docs/proyecto/ESTRATEGIA_MODERNIZACION_WORKBOOK.md`

## Columnas técnicas auxiliares

Desde `1.8.2`, el sistema retira definitivamente las columnas técnicas auxiliares del flujo activo. La aplicación lee el Control Cartera operativo desde `data/input/CONTROLCARTERA_V2.xlsx` y muestra solo columnas reales del archivo.

Las reglas preliminares de frecuencia, moneda, identificación y revisión podrán mantenerse como lógica interna en fases futuras, pero no deben generar columnas visibles ni mezclarse con los datos originales sin una decision aprobada.
