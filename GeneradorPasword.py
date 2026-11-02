
import secrets
import string
import time
import sys

# Definición de alternancias
alternances = {
    '1': string.digits,
    'M': string.ascii_uppercase,
    'm': string.ascii_lowercase
}


def get_pattern():
    while True:
        pattern = input(
            "\nIntroduce el patrón (1, M, m): "
        ).replace("-", "").replace(" ", "")

        if not pattern:
            print("El patrón no puede estar vacío.")
            continue

        if not all(c in alternances for c in pattern):
            print("Utiliza únicamente 1, M y m.")
            continue

        return pattern


def calculate_possibilities(pattern):
    total = 1

    for char in pattern:
        total *= len(alternances[char])

    return total


def generate_password(pattern):
    return ''.join(
        secrets.choice(alternances[char])
        for char in pattern
    )


def show_progress(current, total, start_time):
    percentage = current / total * 100
    elapsed = time.time() - start_time

    bar_length = 35
    filled = int(bar_length * current / total)

    bar = (
        "#" * filled +
        "-" * (bar_length - filled)
    )

    sys.stdout.write(
        f"\r[{bar}] {percentage:6.2f}% "
        f"| Únicas: {current}/{total} "
        f"| Tiempo: {elapsed:.1f}s"
    )

    sys.stdout.flush()


def generate_wordlist(pattern, quantity):
    total_possible = calculate_possibilities(pattern)

    if quantity <= 0:
        raise ValueError("La cantidad debe ser positiva.")

    if quantity > total_possible:
        raise ValueError(
            f"Solo existen {total_possible:,} combinaciones."
        )

    passwords = set()
    start_time = time.time()

    print("\nGenerando contraseñas...\n")

    while len(passwords) < quantity:
        password = generate_password(pattern)
        passwords.add(password)

        show_progress(
            len(passwords),
            quantity,
            start_time
        )

    elapsed = time.time() - start_time

    print("\n\nGeneración completada.")
    print(f"Resultados únicos: {len(passwords)}")
    print(f"Tiempo transcurrido: {elapsed:.2f} segundos")

    return passwords


def save_to_file(passwords):
    filename = input(
        "\nNombre del archivo TXT: "
    ).strip()

    if not filename.endswith(".txt"):
        filename += ".txt"

    with open(filename, "w", encoding="utf-8") as file:
        for password in passwords:
            file.write(password + "\n")

    print(f"\nArchivo guardado: {filename}")


def main():
    try:
        pattern = get_pattern()

        total = calculate_possibilities(pattern)

        print("\n--- INFORMACIÓN DEL PATRÓN ---")
        print(f"Longitud: {len(pattern)}")
        print(f"Combinaciones posibles: {total:,}")

        quantity = int(
            input(
                "\n¿Cuántas contraseñas únicas quieres generar?: "
            )
        )

        passwords = generate_wordlist(
            pattern,
            quantity
        )

        print("\n--- OPCIONES DE RESULTADO ---")
        print("1. Mostrar en terminal")
        print("2. Guardar en TXT")
        print("3. Mostrar y guardar")

        option = input("\nSelecciona una opción: ")

        if option in ("1", "3"):
            print("\n--- CONTRASEÑAS ---")

            for password in passwords:
                print(password)

        if option in ("2", "3"):
            save_to_file(sorted(passwords))

        if option not in ("1", "2", "3"):
            print("Opción no válida.")

    except ValueError as error:
        print(f"\nError: {error}")

    except OSError as error:
        print(f"\nError de archivo: {error}")


if __name__ == "__main__":
    main()
