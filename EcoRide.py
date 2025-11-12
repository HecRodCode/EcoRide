# Parámetros base
costo_estandar = 300.0
costo_premium  = 600.0
penalizacion = 0.35        # 35%
descuento_tarjeta = 0.10   # 10%
recargo_fin_semana = 0.05  # 5%

# Tipos de bici y su precio por minuto
tarifas = {"1": ("Estándar", costo_estandar), "2": ("Premium", costo_premium)}

valor_pendiente = 0.0      # Deuda acumulada
continuar = True           # Control del bucle principal

while continuar:
    print("Menu Principal\n1. Alquilar una bicicleta\n2. Consultar tarifas\n3. Pagar\n4. Salir")
    opcion = input("Elige una opción (1-4): ").strip()

    if opcion == "4":  # Salir del sistema
        print("¡Hasta luego!")
        continuar = False
        continue

    elif opcion == "2":
        print(f"\nTarifas por minuto: Estándar = {costo_estandar:.2f}, Premium = {costo_premium:.2f}\n")
        continue

    elif opcion == "3":  # Pago de pendientes
        print("\n/--- Menú de pagos ---/")
        if valor_pendiente <= 0:
            print("No tienes pagos pendientes.\n")
        else:
            print(f"Monto pendiente: {valor_pendiente:.2f}")
            confirmar = input("¿Deseas pagar ahora? (si/no): ").lower().strip()
            if confirmar in ("si", "s"):
                metodo_pago = input("Método de pago (efectivo/tarjeta/puntos): ").lower().strip()
                if metodo_pago in ("efectivo", "tarjeta", "puntos"):
                    print("¡Pago completado!")
                    valor_pendiente = 0.0
                else:
                    print("Método de pago inválido. No se procesó el pago.")
            else:
                print("Puedes pagar más tarde.")
        continue
        
    elif opcion != "1":
        print("Opción inválida.\n")
        continue

    print("\nTipos de bicicleta:\n1. Estándar\n2. Premium")
    tipo = input("Seleccione el tipo (1/2): ").strip()
    if tipo not in tarifas:  # Validación de tipo
        print("Tipo inválido.\n")
        continue

    # Minutos > 0
    while True:
        m = input("Ingrese el tiempo de uso (minutos): ").strip()
        if m.isdigit() and int(m) > 0:
            m = int(m)
            break
        print("Tiempo inválido. Debe ser un entero > 0.")

    metodo = input("Método de pago (efectivo/tarjeta/puntos): ").lower().strip()
    if metodo not in ("efectivo", "tarjeta", "puntos"):  # Validación de método
        print("Método de pago inválido.\n")
        continue

    finde = input("¿Es fin de semana? (si/no): ").lower().strip() in ("si", "s")
    retraso = input("¿Hubo retraso en la entrega? (si/no): ").lower().strip() in ("si", "s")

    tipo_bici, costo_minuto = tarifas[tipo]

    # Cálculo base
    base = m * costo_minuto
    total = base
    detalles = []

    # Descuento con tarjeta si > 60 (anidado)
    if metodo == "tarjeta":
        if m > 60:
            total *= (1 - descuento_tarjeta)
            detalles.append("Descuento 10% por tarjeta (>60 min)")

    # Puntos <10: sin descuento (recargos/penalización pueden aplicar)
    if metodo == "puntos" and m < 10:
        detalles.append("Pago con puntos <10 min: sin descuento")

    # Recargo fin de semana
    if finde:
        total *= (1 + recargo_fin_semana)
        detalles.append("Recargo 5% fin de semana")

    # Penalización por retraso
    if retraso:
        total *= (1 + penalizacion)
        detalles.append("Penalización 35% por retraso")
        
    # Resumen
    print("\n--- Resumen del servicio ---")
    print(f"Tipo de bicicleta: {tipo_bici}")
    print(f"Método de pago utilizado: {metodo}")
    print(f"Tiempo de uso: {m} min")
    print(f"Precio base: {base:.2f}")
    if detalles:
        print("Ajustes: " + " | ".join(detalles))
    print(f"Precio final a pagar: {total:.2f}")

    # Acumula para pagar luego
    valor_pendiente += total
    print(f"Se agregó a pagos pendientes. Pendiente actual: {valor_pendiente:.2f}\n")

    # Controla repetición del bucle
    continuar = input("¿Deseas realizar otro alquiler? (si/no): ").lower().strip() in ("si", "s")
    if not continuar:
        print("\nCerrando sistema. ¡Gracias por usar EcoRide!\n")