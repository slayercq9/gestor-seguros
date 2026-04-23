# Gestor Seguros

Aplicacion de escritorio en Python para apoyar la gestion operativa de seguros. El proyecto busca organizar informacion de clientes, polizas, vencimientos, documentos, respaldos y reportes en una herramienta local, portable y mantenible.

## Problema que resuelve

La gestion operativa de seguros suele depender de archivos dispersos, controles manuales y documentos preparados caso por caso. Esto aumenta el riesgo de omisiones, duplicidad de informacion, dificultad para dar seguimiento a vencimientos y poca trazabilidad sobre cambios o respaldos.

## Objetivo general

Construir una aplicacion de escritorio modular que permita gestionar informacion operativa de seguros de forma ordenada, trazable y preparada para crecer por fases.

## Alcance inicial

Esta fase establece la base profesional del repositorio:

- estructura inicial de carpetas;
- documentacion formal del proyecto;
- arquitectura preliminar;
- reglas iniciales de trabajo;
- supuestos, riesgos y decisiones tecnicas conservadoras.

No se implementa interfaz grafica funcional, base de datos operativa, importacion real de Excel, generacion real de documentos ni logica de vencimientos.

## Funcionalidades futuras previstas

- Interfaz grafica de escritorio, probablemente con PySide6.
- Persistencia local, probablemente con SQLite.
- Importacion controlada desde Excel cuando exista la base real.
- Gestion de clientes, polizas, vencimientos y bitacoras.
- Generacion de documentos de vencimiento por cliente.
- Soporte para polizas en colones y dolares.
- Reportes operativos y tableros de seguimiento.
- Respaldos locales y politicas de recuperacion.
- Distribucion portable y mediante instalador.

## Estructura del repositorio

```text
app/                 Codigo fuente de la aplicacion.
data/input/          Archivos de entrada locales no versionados.
data/output/         Archivos generados localmente.
data/backups/        Respaldos locales no versionados.
data/samples/        Datos de muestra anonimizados o ficticios.
docs/capturas/       Capturas para documentacion.
docs/diagramas/      Diagramas de arquitectura y flujo.
docs/releases/       Notas y evidencias por version.
scripts/             Utilidades de desarrollo y mantenimiento.
templates/docx/      Plantillas futuras para documentos.
tests/               Pruebas automatizadas futuras.
.codex/              Configuracion minima de trabajo asistido.
```

## Estado actual

Version inicial documental `v0.1.0`. El proyecto esta listo para revision humana de estructura, alcance, supuestos y criterios de trabajo antes de iniciar implementacion funcional.

## Proximos pasos

1. Revisar y aprobar la documentacion base.
2. Definir el alcance funcional de la siguiente version.
3. Recibir o acordar una muestra representativa del Excel real.
4. Refinar el diccionario de datos.
5. Disenar el modelo inicial de persistencia local.
6. Crear el esqueleto tecnico de la aplicacion solo cuando el alcance este validado.
