def format_insurance_amount(amount):
    try:
        # Convertir en entier si c'est une chaîne
        amount = int(amount)
        # Formater avec des espaces comme séparateur de milliers
        return f"{amount:,}".replace(",", " ") + "$"
    except (ValueError, TypeError):
        return "Montant invalide"

