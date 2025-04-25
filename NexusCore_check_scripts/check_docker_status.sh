#!/bin/bash
echo "Verificando estado de Docker..."

if docker version > /dev/null 2>&1; then
    echo " Docker está activo y accesible desde WSL."
else
    echo " Docker no está accesible desde WSL."
fi

