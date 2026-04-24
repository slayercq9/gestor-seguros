# Decisiones Implementacion 1.5.0 y 1.6.0

## Proposito

Listar las decisiones que deben quedar aprobadas antes de pasar a implementacion tecnica en `1.5.0` y `1.6.0`.

## Decisiones bloqueantes

### 1. Unidad canonica principal

Debe quedar aprobado el rol de:

- cliente;
- poliza;
- vencimiento;
- relacion cliente-poliza;
- metadatos operativos.

### 2. Regla de autoridad

Debe quedar definido:

- que campos seguiran siendo reflejo fiel del origen;
- que campos podran tener valor propio dentro de la app;
- en que momento un dato operativo editable dejaria de depender exclusivamente del workbook.

### 3. Politica de IDs internos

Debe definirse:

- como se identificaran clientes, polizas y vencimientos internamente;
- como se evitara depender solo de nombres o texto libre;
- como se mantendra trazabilidad con el origen sin exponer PII.

### 4. Tratamiento de duplicados y relaciones

Debe quedar aprobado:

- como manejar una persona con multiples polizas;
- como interpretar `detalle` cuando sugiera relacion entre polizas;
- como tratar conflicto entre nombre, identificacion y numero de poliza;
- como distinguir casos que requieren revision manual.

### 5. Politica de normalizacion

Debe definirse para:

- frecuencia;
- moneda;
- fechas;
- identificaciones;
- placas o finca;
- numero de poliza para clasificacion tecnica.

### 6. Politica de sensibilidad

Debe quedar decidido:

- que puede mostrarse en interfaz;
- que puede salir en reportes locales;
- que debe permanecer solo en entorno controlado;
- que no debe aparecer nunca en documentacion ni artefactos versionados.

### 7. Criterio de edicion futura

Debe quedar definido:

- que campos seran solo lectura;
- que campos admitiran correccion operativa;
- que campos requeriran historial o trazabilidad;
- que campos nunca se deberan sobrescribir sobre el origen.

### 8. Limites por version futura

#### 1.5.0

Debe enfocarse en:

- modelo interno;
- definicion tecnica de entidades;
- capa preliminar de lectura y normalizacion;
- persistencia o contratos tecnicos minimos, si ya estan aprobados.

#### 1.6.0

Debe enfocarse en:

- primeros flujos controlados sobre dataset canonico;
- validaciones de integridad iniciales;
- soporte operativo sin reemplazar aun el workbook salvo decision explicita posterior.

## Riesgos a monitorear antes de implementar

- ambiguedades de encabezados o significado real de columnas;
- exceso de rigidez del modelo canonico;
- perdida de trazabilidad entre origen y app;
- interpretacion apresurada de `detalle`;
- falsa unicidad de identificacion o numero de poliza;
- mezcla entre campos originales, corregidos y derivados sin distincion clara.

## Criterio de salida de 1.4.0

La fase `1.4.0` estara lista cuando estas decisiones queden documentadas y revisables, aunque todavia no esten implementadas en codigo funcional.
