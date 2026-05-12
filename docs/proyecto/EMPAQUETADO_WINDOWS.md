# Empaquetado Windows futuro

## Propósito

Este documento deja una guía inicial para empaquetar la aplicación en Windows en una fase posterior. La versión `1.11.3` prepara un spec preliminar de PyInstaller, pero no genera ejecutables finales, instaladores, archivos `.zip` ni releases.

## Alcance futuro

Cuando se apruebe el empaquetado, se deberá validar:

- ejecución de `python -m app` antes de empaquetar;
- pruebas automatizadas completas;
- inclusión de `assets/app_icon.svg`;
- manejo de rutas locales `data/input/`, `data/output/` y `data/backups/`;
- exclusión de datos reales del repositorio y de artefactos públicos;
- verificación manual de `Guardar`, `Guardar como`, respaldos, tema claro/oscuro, ayuda y acerca de.

## PyInstaller

`requirements.txt` contempla PyInstaller como dependencia de empaquetado. El archivo `GestorSeguros.spec` usa `app/__main__.py` como entrypoint y agrega `assets/app_icon.svg` como asset.

Build preliminar para revisión local futura:

```powershell
python -m PyInstaller .\GestorSeguros.spec
```

Este comando no debe ejecutarse como parte de la verificación automatizada de esta fase. Antes de usarlo, se debe confirmar manualmente que no existan datos reales dentro de artefactos de salida.

El spec debe mantener:

- paquete `app`;
- `assets/app_icon.svg`;
- dependencias de PySide6;
- rutas de trabajo locales fuera del ejecutable;
- exclusión de `data/input/`, `data/output/` y `data/backups/`.

## Restricciones vigentes

- No incluir el Control Cartera real.
- No incluir archivos en `data/input/`, `data/output/` ni `data/backups/`.
- No publicar capturas con datos reales.
- No crear instalador sin revisión manual.
