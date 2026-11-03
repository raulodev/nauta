# nauta

Línea de comandos para el nauta hogar Cuba

> Nota: El nombre del proyecto en PyPI fue donado, por lo que el proyecto cambió su nombre a `nauta-cli`.

## Instalación con pipx

Para instalar `pipx` siga las [instrucciones](https://github.com/pypa/pipx#install-pipx) según su sistema operativo

```bash
pipx install nauta-cli --force
```

## Guía

1. Agregar un usuario

```console
nauta add micorreo@nauta.com.cu contraseña
```

1. Iniciar sesión

```console
nauta login
```

1. Cerrar sesión

```console
nauta logout
```

## Ayuda

```bash
nauta --help
```

## Desinstalación

```bash
pipx uninstall nauta-cli
```

## Actualización

```bash
pipx upgrade nauta-cli
```
