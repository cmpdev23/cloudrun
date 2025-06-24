import re
import pandas as pd
import logging
logger = logging.getLogger(__name__)

def format_phone_number(phone_number):
    try:
        # Gestion des cas nuls ou vides
        if pd.isna(phone_number) or phone_number.strip() == '':
            return None  # Retourner None si le numéro de téléphone est NaN ou vide

        # Suppression des caractères non numériques
        phone_number = re.sub(r'\D', '', phone_number)

        if not phone_number.startswith('1'):
            phone_number = '1' + phone_number
        if len(phone_number) != 11:
            raise ValueError("Le numéro de téléphone doit être de 11 chiffres avec un '1' au début.")
        return phone_number
    except Exception as e:
        logger.error(f"Erreur lors du formatage du numéro de téléphone '{phone_number}': {e}")
        return None