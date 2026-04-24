# Especificacion Dataset Canonico

## Proposito

Definir el dataset canonico interno de la aplicacion como una representacion estable, trazable y extensible de la operacion de seguros, sin sustituir todavia la utilidad manual del workbook operativo.

Esta fase es solo de diseno. No introduce importacion funcional, persistencia operativa ni automatizacion del workbook.

## Principio rector

El enfoque del proyecto en `1.4.0` es `workbook primero`:

- el workbook sigue siendo la herramienta operativa principal;
- el dataset canonico se disena como capa interna gradual;
- la futura app debera poder entender, mapear y normalizar el origen sin romper el flujo manual actual.

## Objetivos del dataset canonico

- dar estabilidad interna a la app aunque el workbook mantenga formatos heredados;
- separar campos originales, normalizados, derivados y operativos;
- permitir trazabilidad desde origen hasta valor interno;
- aislar datos sensibles para su tratamiento seguro;
- preparar la base para implementacion controlada en `1.5.0` y `1.6.0`.

## Entidades minimas futuras

### Cliente

Representa la identidad operativa principal de una persona o entidad asegurada.

| Campo canonico | Procedencia esperada | Tipo | Sensible | Editable futuro |
| --- | --- | --- | --- | --- |
| cliente_id | Operativo interno | Operativo | No | No |
| nombre_original | Workbook | Original | Si | No |
| tipo_identificacion_normalizado | Workbook | Normalizado | Si | No |
| identificacion_original | Workbook | Original | Si | No |
| identificacion_normalizada | Workbook | Normalizado | Si | No |
| telefono_original | Workbook | Original | Si | No |
| correo_original | Workbook | Original | Si | No |
| direccion_original | Workbook | Original | Si | No |
| requiere_revision_cliente | Derivado | Derivado | No | No |
| observacion_revision_cliente | Operativo interno | Operativo | No | Si |

### Poliza

Representa una poliza tal como existe en origen, mas sus normalizaciones y clasificaciones internas.

| Campo canonico | Procedencia esperada | Tipo | Sensible | Editable futuro |
| --- | --- | --- | --- | --- |
| poliza_id | Operativo interno | Operativo | No | No |
| cliente_id | Relacion interna | Operativo | No | No |
| numero_poliza_original | Workbook | Original | Si | No |
| numero_poliza_normalizado | Workbook | Normalizado | Si | No |
| tipo_seguro_original | Workbook | Original | No | No |
| aseguradora_original | Workbook | Original | No | No |
| vigencia_original | Workbook | Original | No | No |
| frecuencia_normalizada | Workbook | Normalizado | No | No |
| frecuencia_observada | Derivado | Derivado | No | No |
| es_dm | Derivado | Derivado | No | No |
| genera_aviso | Derivado | Derivado | No | No |
| moneda_normalizada | Derivado | Derivado | No | No |
| es_riesgo_trabajo_probable | Derivado | Derivado | No | No |
| numero_placa_finca_original | Workbook | Original | Si | No |
| detalle_original | Workbook | Original | Si | No |
| requiere_revision_poliza | Derivado | Derivado | No | No |
| observacion_revision_poliza | Operativo interno | Operativo | No | Si |

### Vencimiento

Representa la informacion de vencimiento asociada a una poliza o relacion operativa, incluyendo consolidacion de fecha.

| Campo canonico | Procedencia esperada | Tipo | Sensible | Editable futuro |
| --- | --- | --- | --- | --- |
| vencimiento_id | Operativo interno | Operativo | No | No |
| poliza_id | Relacion interna | Operativo | No | No |
| dia_vencimiento_original | Workbook | Original | No | No |
| mes_vencimiento_original | Workbook | Original | No | No |
| ano_vencimiento_original | Workbook | Original | No | No |
| fecha_vencimiento_original | Workbook | Original | No | No |
| fecha_vencimiento_normalizada | Derivado | Derivado | No | No |
| requiere_revision_fecha | Derivado | Derivado | No | No |
| estado_gestion_vencimiento | Operativo interno | Operativo | No | Si |

### Relacion Cliente-Poliza

Representa relaciones operativas que no siempre quedan claras solo con clave de cliente o numero de poliza.

| Campo canonico | Procedencia esperada | Tipo | Sensible | Editable futuro |
| --- | --- | --- | --- | --- |
| relacion_cliente_poliza_id | Operativo interno | Operativo | No | No |
| cliente_id | Relacion interna | Operativo | No | No |
| poliza_id | Relacion interna | Operativo | No | No |
| rol_relacion | Derivado o revision | Operativo | No | Si |
| relacion_detectada_desde_detalle | Derivado | Derivado | No | No |
| requiere_revision_relacion | Derivado | Derivado | No | No |

### Metadatos Operativos

Representan trazabilidad, validacion y control del proceso futuro de lectura o sincronizacion.

| Campo canonico | Procedencia esperada | Tipo | Sensible | Editable futuro |
| --- | --- | --- | --- | --- |
| fuente_origen | Operativo interno | Operativo | No | No |
| hoja_origen | Operativo interno | Operativo | No | No |
| columna_origen | Operativo interno | Operativo | No | No |
| fila_origen | Operativo interno | Operativo | No | No |
| sincronizado_en | Operativo interno | Operativo | No | No |
| estado_validacion | Operativo interno | Operativo | No | Si |
| conflicto_detectado | Derivado | Derivado | No | No |

## Clasificacion de campos

### Originales

Se copian del workbook y mantienen semantica de origen:

- nombres originales de columnas y registros para trazabilidad interna;
- numero de poliza tal como viene;
- identificacion tal como viene;
- detalle;
- `Numero de Placa / Finca`;
- dia, mes y ano de vencimiento si vienen separados;
- frecuencia o vigencia tal como venga en origen.

### Normalizados

Reexpresan el origen en forma mas consistente para la app:

- tipo de identificacion normalizado;
- identificacion normalizada;
- frecuencia normalizada;
- moneda normalizada;
- fecha de vencimiento consolidada;
- numero de poliza normalizado para clasificacion tecnica;
- marca de riesgo del trabajo probable.

### Derivados

Se calculan desde otros campos y reglas aprobadas:

- moneda inferida por prefijo `01` o `02` cuando aplique;
- bandera `genera_aviso` futura, solo documentada;
- bandera `es_dm`;
- bandera `requiere_revision`;
- fecha consolidada desde dia, mes y ano;
- categoria de frecuencia observada.

### Operativos

Dan soporte a control, trazabilidad y revision:

- ids internos canonicos;
- estado de validacion;
- observaciones internas de revision;
- fuente de origen;
- fecha y hora de sincronizacion futura;
- trazabilidad del mapeo;
- indicadores de completitud o conflicto.

### Sensibles

Deben tratarse como PII o informacion restringida:

- nombre completo;
- identificacion completa;
- telefono;
- correo;
- direccion;
- numero completo de poliza cuando salga de entorno controlado;
- placa o finca;
- texto libre de `detalle` cuando pueda incluir informacion personal.

## Editabilidad futura

### Editables

- observaciones operativas;
- estados de gestion;
- clasificaciones manuales aprobadas;
- notas internas separadas del origen.

### No editables

- campos originales importados;
- campos derivados automaticos;
- metadatos de trazabilidad;
- consolidaciones calculadas desde origen mientras no exista politica explicita de sobrescritura.

## Reglas conocidas a reflejar en el modelo

- `D.M.` significa deduccion mensual.
- Las polizas `D.M.` no generan avisos, pero si se almacenan.
- Existen frecuencias mensuales, trimestrales, semestrales y anuales.
- `01` implica preliminarmente colones.
- `02` implica preliminarmente dolares.
- La regla de moneda no aplica a riesgos del trabajo, identificados preliminarmente como polizas completamente numericas.
- `Numero de Placa / Finca` normalmente contiene placas.
- La fecha de vencimiento puede venir separada en dia, mes y ano.
- `detalle` puede contener anotaciones o relacion entre polizas de un mismo dueno.

## Reglas preliminares de transformacion

- preservar siempre el valor original cuando un campo provenga del workbook;
- generar campos normalizados solo como capa interna complementaria;
- derivar moneda por prefijo `01` o `02` unicamente como regla preliminar y con excepcion para polizas completamente numericas;
- consolidar fecha de vencimiento cuando existan dia, mes y ano separados, sin perder las partes originales;
- clasificar `D.M.` como deduccion mensual y reflejarla como categoria observada, sin convertirla aun en comportamiento automatico definitivo;
- marcar casos ambiguos como `requiere_revision_*` en lugar de forzar una interpretacion.

## Reglas preliminares de validacion

- no asumir unicidad de numero de poliza sin aprobacion posterior;
- no asumir unicidad de identificacion sin revisar conflictos y duplicados;
- no sobrescribir campos originales con valores normalizados o corregidos;
- tratar `detalle` como campo potencialmente sensible y semiestructurado;
- distinguir entre ausencia de dato y dato no interpretable;
- registrar relaciones probables como preliminares cuando dependan de inferencia.

## Riesgos y supuestos

### Riesgos

- el workbook real puede contener excepciones adicionales a las observadas en auditoria;
- `detalle` puede mezclar notas libres con relaciones de negocio;
- la regla de moneda por prefijo puede tener mas excepciones;
- pueden existir conflictos entre nombre, identificacion y numero de poliza;
- un modelo demasiado rigido podria afectar la convivencia con el flujo manual.

### Supuestos

- el workbook seguira siendo importante para trabajo manual y respaldo en el corto y mediano plazo;
- el dataset canonico sera interno y no necesita replicar exactamente el layout visual del workbook;
- la app futura operara sobre un modelo mas consistente, manteniendo trazabilidad con el origen;
- esta fase solo documenta el modelo, no lo implementa.

## Decisiones abiertas

- politica definitiva de ids internos canonicos;
- criterio de unicidad de cliente y poliza;
- tratamiento exacto de duplicados y relaciones sugeridas por `detalle`;
- catalogos finales de tipo de seguro, aseguradora y estados operativos;
- politica definitiva de exportacion y sincronizacion entre app y workbook.

## Limites de esta fase

- No se define aun esquema fisico de base de datos.
- No se define aun API de importacion funcional.
- No se decide aun persistencia operativa.
- No se redefine el workbook ni se alteran sus columnas.
- No se implementa logica funcional.
