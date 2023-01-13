# Intérprete de funciones FUNX

Este es una [Práctica de GEI-LP(2022-2023)](https://github.com/gebakx/lp-funcions).

En esta práctica se implementa un intérprete de un lenguaje de programación basado en expresiones y funciones.
La entrada y salida del intérprete será en una página web.

## FUNX

FUNX es un lenguaje orientado a expresiones y funciones. Con FUNX podemos definir y terminar, opcionalmente, con una expresión.
```
# Función que recibe dos nombres enteros y retorna la suma de los dos.
Suma x y
{
  x + y
}

Suma (2 * 3) 4 
```

```
Out: 10 
```

### Instrucciones
- Assignacion con `<-`.
```
a <- a - b
```
- Invocación de funciones.
```
Suma (2 * 3) 4 
```
```
Out: 10 
```
- Condicional con `if` y opcionalmente `else`.
```
if x = y { z <- 1 }
```
```
if x = y { z <- 1 } else { z <- 2 }
```

- Iteración con 'while'.
```
while a > 0 { a <- a / 2 }
```

- Operadores aritméticos ('+', '-', '*', '/', '%').

- Operadores relacionales ('=', '!=', '<', '&gt;', '<=', '&gt;=').


## USO

En este apartado se dará a conocer los requisitos y como invocar el intérprete.

### Requisitos

Para usar este intérprete se necesita tener:
- ANTLR4.10.1 https://www.antlr.org/download/antlr-4.10.1-complete.jar
- Python 3 https://www.python.org/downloads/
- Librería de python Flask.
```
pip install flask
```
- Librería de python Jinja.
```
pip install jinja2
```

### Parsers y Visitors

Generamos los parsers y visitors con el siguiente comando:
```
java -jar antlr-4.10.1-complete.jar -Dlanguage=Python3 -no-listener -visitor funx.g4
```

### Invocación del intérprete

Una vez generado los parsers y visitors, activamos la web con:

Bash:
```
export FLASK_APP=funx
flask run
```
cmd:
```
set FLASK_APP=funx
flask run
```
Powershell:
```
$env:FLASK_APP="funx"
flask run
```

Flask nos dará una ip con un puerto donde estará disponible el intérprete.

