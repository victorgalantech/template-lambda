def suma(a: int, b: int) -> int:
    return a + b


def resta(a: int, b: int) -> int:
    return a - b


def multiplicacion(a: int, b: int) -> int:
    return a * b


def division(a: int, b: int) -> int:
    return a // b


def potencia(base: int, exponente: int) -> int:
    return base**exponente


def modulo(a: int, b: int) -> int:
    return a % b


def raiz_cuadrada(numero: float) -> float:
    return numero**0.5


def factorial(numero: int) -> int:
    if numero < 0:
        raise ValueError("El factorial no está definido para números negativos")
    if numero == 0 or numero == 1:
        return 1
    resultado = 1
    for i in range(2, numero + 1):
        resultado *= i
    return resultado


def promedio(numeros: list[int]) -> float:
    if not numeros:
        raise ValueError("La lista no puede estar vacía")
    return sum(numeros) / len(numeros)


def es_par(numero: int) -> bool:
    return numero % 2 == 0


def es_impar(numero: int) -> bool:
    return numero % 2 != 0


def es_primo(numero: int) -> bool:
    if numero < 2:
        return False
    return all(numero % i != 0 for i in range(2, int(numero**0.5) + 1))


def validar_rango(numero: int, minimo: int, maximo: int) -> bool:
    return minimo <= numero <= maximo


def es_positivo(numero: float) -> bool:
    return numero > 0


def es_negativo(numero: float) -> bool:
    return numero < 0


def es_cero(numero: float) -> bool:
    return numero == 0


def es_entero(numero: float) -> bool:
    return numero == int(numero)


def es_decimal(numero: float) -> bool:
    return numero != int(numero)


def es_racional(numero: float) -> bool:
    return isinstance(numero, (int, float)) and not isinstance(numero, bool)
