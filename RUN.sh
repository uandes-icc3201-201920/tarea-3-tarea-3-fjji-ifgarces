#!/bin/bash
# archivo para probar condición de carrera: ejecución paralela de instrucciones de varios clientes
for i in {1..5}
do
	python3 client.py < "test_input.txt" > "client_$i_output.txt" 2>&1 &
done

echo Type enter to exit
read _stop_

# no sé qué pasa que no funciona al leer el archivo, seguro tengo el Ubuntu medio mal instalado. Al copiarlo a la terminal, funciona, pero dada la estructura del input del cliente, pensado para que los saltos de línea sean enter, como que no funciona porque todo se mete en la primera línea, cuando dice "  > " el cliente. Luego trata de leer de nuevo pero ya no hay archivo, lee caracter EOF.