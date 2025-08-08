# Guía de instalación de Android-x86 en VirtualBox con Vagrant

## Requisitos previos

- Instalar **VirtualBox** en el host.
- Instalar **Vagrant** en el host.
- Instalar **adb** en el host (por ejemplo, en Ubuntu:  
  ```sh
  sudo apt install adb
  ```

- Descargar la ISO de Android-x86 desde [https://www.android-x86.org/download.html](https://www.android-x86.org/download.html).

**Recomendado:**
- **Versión:** `android-x86_9.0-r2.iso`
- **Formato:** ISO (no RPM ni tar.gz)

Guardar la ISO en una ruta accesible desde el `Vagrantfile`.

---

## 1. Configurar la VM manualmente (opcional / referencia)

Si no usas Vagrant, crea la máquina en VirtualBox con estos parámetros:

- **Tipo:** Linux
- **Versión:** Other Linux (64-bit)
- **RAM:** mínimo 2 GB
- **Disco:** 25 GB (VDI, dinámico)
- **Tarjeta de red:** NAT o Adaptador puente
- **Controlador gráfico:** VBoxVGA (importante)
- **Aceleración 3D:** desactivada
- **Memoria de video:** al menos 64 MB

💡 Si usas Vagrant, el `Vagrantfile` (ubicado en la raíz del proyecto) lo configurará automáticamente.

---

## 2. Instalación de Android

Al bootear desde la ISO:

1. Elegir **Installation – Install Android-x86 to harddisk**
2. Crear partición con `cfdisk` (no GPT):
   - Crear partición primaria, tipo Linux, y marcarla como bootable
3. Seleccionar sistema de archivos: **ext4**
4. Instalar GRUB → Yes
5. Marcar `/system` como read-write → Yes
6. Elegir "auto-boot to GUI" → Yes (si está disponible)

---

## 3. Activar el modo desarrollador

Una vez en la interfaz de Android:

1. Ir a **Configuración > Acerca del teléfono**
2. Tocar **Número de compilación** 7 veces para activar el modo desarrollador
3. Volver a **Configuración > Sistema > Opciones para desarrolladores** y activar:
   - **Depuración USB**
   - **Depuración de ADB** (necesario para conectar con adb)

---

## 4. Solución para modo consola

Si después del reinicio solo aparece una terminal:

```sh
startx
```

Si no funciona, editar GRUB (presionar `e` al arrancar) y quitar parámetros como `quiet` o `console=tty0`.

---

## 5. Preparar el sistema para mitmproxy

### Generar y copiar el certificado

Para que Android confíe en el proxy, necesitas instalar el certificado raíz de mitmproxy.

#### Opción 1: Descargar desde el navegador

1. **Conéctate a Internet usando el proxy de mitmproxy** (asegúrate de que el tráfico pase por el proxy).
2. Abre el navegador en el dispositivo y visita:  
   [http://mitm.it](http://mitm.it)
3. Descarga el certificado para Android desde esa página.

> **Nota:** Solo podrás acceder a `http://mitm.it` si el dispositivo está usando el proxy de mitmproxy.

#### Opción 2: Generar el certificado en el host

En el host, ejecuta:

```sh
mitmproxy --export-cert ./mitmproxy-ca-cert.pem
```

El nombre del archivo que Android requiere depende de un hash generado a partir del certificado. Para obtener el nombre correcto y convertirlo:

```sh
hash=$(openssl x509 -inform PEM -subject_hash_old -in mitmproxy-ca-cert.pem | head -1)
openssl x509 -inform PEM -subject_hash_old -in mitmproxy-ca-cert.pem -outform DER -out ${hash}.0
```

Esto generará un archivo llamado, por ejemplo, `9a5ba575.0`.  
**El nombre real puede variar según el hash generado.**

Copia el archivo a la VM (por ejemplo con `adb push`, carpeta compartida o `scp`).

En Android (como root):

```sh
mount -o remount,rw /system
cp <hash>.0 /system/etc/security/cacerts/
chmod 644 /system/etc/security/cacerts/<hash>.0
reboot
```

Reemplaza `<hash>.0` por el nombre real generado en el paso

---

## 6. Vagrantfile (ejemplo base)

```ruby
Vagrant.configure("2") do |config|
  config.vm.box = "generic/linux"
  config.vm.provider "virtualbox" do |vb|
    vb.name = "android-x86"
    vb.memory = 2048
    vb.cpus = 2
    vb.customize ["modifyvm", :id, "--graphicscontroller", "vboxvga"]
    vb.customize ["modifyvm", :id, "--vram", "64"]
    vb.customize ["storageattach", :id, "--storagectl", "IDE Controller", "--port", 1, "--device", 0, "--type", "dvddrive", "--medium", "ruta/a/android-x86_9.0-r2.iso"]
  end
end
```

⚠️ Reemplazar `"ruta/a/android-x86_9.0-r2.iso"` por la ruta real al archivo.

---

## 7. Notas adicionales

- A veces es necesario desactivar el Touchpad y USB Tablet desde la configuración de VirtualBox.
- Puedes usar `tcpdump` o `mitmproxy` en la red del host y configurar Android para que use el proxy manualmente.
- Si necesitas capturar tráfico, asegúrate de que la red esté configurada correctamente (NAT o puente según el caso).
- Para compartir archivos entre host y VM, puedes usar carpetas compartidas de VirtualBox, `adb push/pull` o `scp
