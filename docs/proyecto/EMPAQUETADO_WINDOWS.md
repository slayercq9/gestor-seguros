# Empaquetado Windows futuro

## Propósito

Este documento deja una guía inicial para empaquetar la aplicación en Windows en una fase posterior. La versión `1.11.2` no genera ejecutables, instaladores, archivos `.zip` ni releases.

## Alcance futuro

Cuando se apruebe el empaquetado, se deberá validar:

- ejecución de `python -m app` antes de empaquetar;
- pruebas automatizadas completas;
- inclusión de `assets/app_icon.svg`;
- manejo de rutas locales `data/input/`, `data/output/` y `data/backups/`;
- exclusión de datos reales del repositorio y de artefactos públicos;
- verificación manual de `Guardar`, `Guardar como`, respaldos, tema claro/oscuro, ayuda y acerca de.

## PyInstaller

`requirements.txt` ya contempla PyInstaller como dependencia de empaquetado, pero esta fase no crea configuración ni comando definitivo.

Un futuro empaquetado deberá revisar cómo incluir:

- paquete `app`;
- carpeta `assets`;
- dependencias de PySide6;
- ícono de aplicación;
- rutas de trabajo locales fuera del ejecutable;
- documentación mínima para usuario final.

## Restricciones vigentes

- No incluir el Control Cartera real.
- No incluir archivos en `data/input/`, `data/output/` ni `data/backups/`.
- No publicar capturas con datos reales.
- No crear instalador sin revisión manual.
