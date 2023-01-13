#Interprete de funciones FUNX

Este es una practica de GEI-LP(2022-2023).
En esta practica se implementa un interprete de un lenguaje de programacion basado en expresiones y funciones.
La entrada y salida del interprete sera en una pagina web.


##FUNX

FUNX es un lenguaje orientado a expresiones y funciones. Con FUNX podemos definir y terminar, opcionalmente, con una expresion.


##USO
Para usar este interprete se necesita tener:

	- Python 3
	- Libreria de python Flask
	- Libreria de python Jinja	
	- ANTLR4.10.1
	
Para usarlo en el terminal pone los siguientes comandos:

'''
java -jar antlr-4.10.1-complete.jar -Dlanguage=Python3 -no-listener -visitor funx.g4
'''
'''
set FLASK_APP=funx
flask run
'''