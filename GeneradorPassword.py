
import secrets
import string
import time
import sys
import os

# Definición de alternancias
alternances = {
    '1': string.digits,
    'M': string.ascii_uppercase,
    'm': string.ascii_lowercase,
    '.': "!¡@#$€%&*+-_=¿?.:,;<>[]/{}ºª"
}
# ? representa cualquier carácter de las alternancias
alternances['?'] = ''.join(alternances.values())

def show_title():
    print("============================")
    print("     GeneradorPasswords")
    print("----------------------------")
    print(" By:Valbef         v1.1.0")
    print("============================")

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')


def get_pattern():
    while True:
        pattern = input(
            "\nIntroduce el patrón (1, M, m, ., ?, (caracter)): "
        ).replace("-", "").replace(" ", "")

        if not pattern:
            print("El patrón no puede estar vacío.")
            continue

        i = 0
        valid = True

        while i < len(pattern):

            if pattern[i] == '(':
                end = pattern.find(')', i)

                if end == -1:
                    valid = False
                    break

                fixed = pattern[i + 1:end]

                if len(fixed) != 1:
                    valid = False
                    break

                i = end + 1

            elif pattern[i] in alternances:
                i += 1

            else:
                valid = False
                break

        if not valid:
            print("Patrón inválido. Utiliza 1, M, m, ., ?, o (caracter).")
            continue

        return pattern


def calculate_possibilities(pattern):
    total = 1
    i = 0

    while i < len(pattern):

        if pattern[i] == '(':
            end = pattern.find(')', i)
            i = end + 1

        else:
            total *= len(alternances[pattern[i]])
            i += 1

    return total

def calculate_password_length(pattern):
    length = 0
    i = 0

    while i < len(pattern):

        if pattern[i] == '(':
            end = pattern.find(')', i)
            length += 1
            i = end + 1

        else:
            length += 1
            i += 1

    return length

def calculate_estimated_size(pattern, quantity):

    # Calcular el tamaño máximo posible de una contraseña
    # teniendo en cuenta UTF-8.
    password_size = 0
    i = 0

    while i < len(pattern):

        if pattern[i] == '(':
            end = pattern.find(')', i)
            fixed = pattern[i + 1:end]

            password_size += len(fixed.encode("utf-8"))

            i = end + 1

        else:
            password_size += max(
                len(char.encode("utf-8"))
                for char in alternances[pattern[i]]
            )

            i += 1

    # Un salto de línea por contraseña (1 byte en Linux).
    total_bytes = quantity * (password_size + 1)

    size_kb = total_bytes / 1024
    size_mb = size_kb / 1024
    size_gb = size_mb / 1024

    print("\n--- ESPACIO ESTIMADO EN DISCO ---")
    print(f"Contraseñas: {quantity:,}")
    print(f"Espacio máximo estimado: {size_kb:.2f} KB")
    print(f"Espacio máximo estimado: {size_mb:.4f} MB")
    print(f"Espacio máximo estimado: {size_gb:.6f} GB")

    return total_bytes

def generate_password(pattern):
    password = []
    i = 0

    while i < len(pattern):

        if pattern[i] == '(':
            end = pattern.find(')', i)

            fixed = pattern[i + 1:end]

            password.append(fixed)

            i = end + 1

        else:
            password.append(
                secrets.choice(alternances[pattern[i]])
            )

            i += 1

    return ''.join(password)

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

def calculate_file_size(passwords):
    total_bytes = 0

    for password in passwords:
        total_bytes += len(
            (password + "\n").encode("utf-8")
        )

    size_kb = total_bytes / 1024
    size_mb = size_kb / 1024
    size_gb = size_mb / 1024

    print("\n--- TAMAÑO ESTIMADO DEL ARCHIVO ---")
    print(f"Kilobytes: {size_kb:.2f} KB")
    print(f"Megabytes: {size_mb:.4f} MB")
    print(f"Gigabytes: {size_gb:.6f} GB")

    return total_bytes

def save_to_file(passwords):

    filename = input(
        "\nNombre del archivo TXT: "
    ).strip()

    if not filename:
        filename = "contraseñas.txt"

    if not filename.endswith(".txt"):
        filename += ".txt"

    # Calcular tamaño antes de crear el archivo
    total_bytes = calculate_file_size(passwords)

    print("\n--- CONFIRMACIÓN ---")
    print(f"Archivo: {filename}")
    print(f"Tamaño estimado: {total_bytes:,} bytes")

    confirmation = input(
        "\n¿Quieres crear el archivo? (S/N): "
    ).strip().lower()

    if confirmation not in ("s", "si", "sí"):
        print("\nCreación del archivo cancelada.")
        return

    # Crear archivo únicamente si el usuario confirma
    with open(filename, "w", encoding="utf-8") as file:
        for password in passwords:
            file.write(password + "\n")

    print(f"\nArchivo guardado correctamente: {filename}")

def main():
    pattern = get_pattern()

    total = calculate_possibilities(pattern)

    print("\n--- INFORMACIÓN DEL PATRÓN ---")
    print(f"Longitud: {calculate_password_length(pattern)}")
    print(f"Combinaciones posibles: {total:,}")

    # Mostrar cuánto ocuparía generar todas las combinaciones
    calculate_estimated_size(pattern, total)

    quantity = int(
        input(
            "\n¿Cuántas contraseñas únicas quieres generar?: "
        )
    )

    # Mostrar cuánto ocuparía la cantidad seleccionada
    if quantity > 0 and quantity <= total:
        calculate_estimated_size(pattern, quantity)


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

        for password in sorted(passwords):
            print(password)

    if option in ("2", "3"):
        save_to_file(sorted(passwords))

    if option not in ("1", "2", "3"):
        print("Opción no válida.")
    return passwords



def program_menu():
    last_passwords = None

    while True:
        try:
            last_passwords = main()

        except ValueError as error:
            print(f"\nError: {error}")

        except OSError as error:
            print(f"\nError de archivo: {error}")

        except KeyboardInterrupt:
            print("\n\nOperación interrumpida.")

        print("\n" + "=" * 40)
        print("         MENÚ PRINCIPAL")
        print("=" * 40)
        print("1. Limpiar terminal y reiniciar")
        print("2. Guardar contraseñas en TXT")
        print("3. Salir")
        print("=" * 40)

        option = input("\nSelecciona una opción: ").strip()

        if option == "1":
            clear_terminal()
            print("Reiniciando generador...\n")
            continue

        elif option == "2":
            if last_passwords is not None:
                save_to_file(sorted(last_passwords))
            else:
                print("\nNo hay contraseñas disponibles para guardar.")

        elif option == "3":
            print("\nSaliendo del generador. ¡Hasta pronto!")
            break

        else:
            print("\nOpción no válida. Inténtalo de nuevo.")

if __name__ == "__main__":
    clear_terminal()
    show_title()
    program_menu()