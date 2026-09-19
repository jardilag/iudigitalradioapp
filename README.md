# iudigitalradioapp

Arquitectura: UDF con estado elevado y servicios separados.
Una sola actividad: MainActivity.
UI completamente en Jetpack Compose.
Audio real mediante Media3 ExoPlayer.
Emisoras definidas inicialmente en una lista local.
Flujos HTTPS para evitar problemas de seguridad con HTTP.
minSdk 29, que ya está configurado.
Cámara con TakePicturePreview.
Estado simple con rememberSaveable.
Ramas por funcionalidad y Pull Requests.

## Equipo de trabajo

| Integrante | Rol principal | Rama | Revisor |
| --- | --- | --- | --- |
| Juan Ardila | Líder técnico, arquitectura e integración | `main` y ramas `chore/...` | Yeison Padron |
| Juan Pablo Gonzalez | Diseño UI y componentes Compose | `feature/ui-compose` | Juan Ardila |
| Luisa Gomez | Estado, emisoras y lista dinámica | `feature/stations` | Juan Pablo Gonzalez |
| Edwin Ruiz | Cámara, permisos y vibración | `feature/hardware` | Luisa Gomez |
| Jorge Echavarría | Reproductor Media3 ExoPlayer | `feature/audioPlayer` | Juan Ardila |
| Yeison Padron | Pruebas, documentación y evidencias | `feature/test` y `docs` | Edwin Ruiz |
