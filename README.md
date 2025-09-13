QR Flask App - Documentación
Objetivo del proyecto

Este proyecto consiste en crear una aplicación web para registrar y monitorear choferes mediante códigos QR, facilitando la gestión de la entrada y salida de personal dentro de una planta o instalación de manera eficiente.

Los objetivos principales son:

Registrar los movimientos de los choferes a través de códigos QR.

Gestionar usuarios con distintos roles (administrador y normal).

Monitorear la actividad de los choferes en tiempo real.

Ejecutar la aplicación automáticamente en un servidor virtualizado, garantizando que esté siempre disponible.

Flujo de trabajo

Inicio de sesión:
Los usuarios ingresan con sus credenciales. Según su rol, acceden a diferentes funcionalidades.

Roles de usuario:

Administrador: puede gestionar usuarios, estaciones y contraseñas.

Usuario normal (caseta, chofer, etc.): registra movimientos mediante códigos QR en las estaciones correspondientes.

Generación y escaneo de QR:
La aplicación crea códigos QR dinámicos y reutilizables, permitiendo un registro rápido y confiable de cada evento.

Registro en la base de datos:
Cada acción queda almacenada para generar un historial completo y mantener el control sobre la actividad de los choferes.

Visualización y monitoreo:
La interfaz permite consultar en tiempo real el estado de los choferes y de las estaciones.

Despliegue en Proxmox

La aplicación está hosteada en un servidor virtualizado Proxmox, lo que ofrece varias ventajas:

Mantener la misma IP que el host, utilizando redirección de puertos para que la app sea accesible desde el puerto 5000.

Automatizar el arranque de la aplicación mediante un servicio del sistema, asegurando que Flask se inicie automáticamente cada vez que el servidor se reinicia.

Exponer la app a la red interna usando un bridge en la VM, evitando conflictos de IP y permitiendo el acceso desde cualquier máquina de la LAN.

Beneficios de esta arquitectura

Disponibilidad continua: la aplicación se inicia automáticamente y se mantiene activa incluso tras reinicios del servidor.

Control de acceso: los distintos roles limitan el acceso a funciones críticas.

Monitoreo en tiempo real: facilita supervisar el flujo de choferes y estaciones en todo momento.

Flexibilidad de red: funciona bien en entornos virtualizados, usando port forwarding y bridge, sin necesidad de cambiar la IP del host.

Login
<img width="531" height="459" alt="image" src="https://github.com/user-attachments/assets/a0ab52a0-8fd4-40f7-aa5e-8630b1605591" />
dashboard
<img width="1873" height="904" alt="image" src="https://github.com/user-attachments/assets/0767fbb4-c146-4826-9cf4-d5617084bc28" />
Main menu
<img width="1354" height="474" alt="image" src="https://github.com/user-attachments/assets/c79ed6b9-9417-4be9-996f-029e21963a8a" />
register of drivers
<img width="604" height="747" alt="image" src="https://github.com/user-attachments/assets/75dcaafa-409a-400c-b56a-af04375cc2f5" />
baneed drivers
<img width="1904" height="754" alt="image" src="https://github.com/user-attachments/assets/b65858b2-c043-4181-94b6-367bae215f51" />
follow drivers
<img width="736" height="673" alt="image" src="https://github.com/user-attachments/assets/2de92846-5bc6-463a-aef7-58df77afca27" />
active drivers
<img width="943" height="930" alt="image" src="https://github.com/user-attachments/assets/734b44f9-f002-4a9f-b51b-3bf345fdf67b" />
history 
<img width="940" height="931" alt="image" src="https://github.com/user-attachments/assets/c3080efc-f42b-4a03-bc45-a5e50a6c5968" />
