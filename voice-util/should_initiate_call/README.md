# Service de Vérification d'Appels Automatiques

## Description

Ce service est une API REST qui détermine si un appel automatique peut être initié en fonction de plusieurs critères. Il est conçu pour être déployé sur Google Cloud Run et sert de point de décision central pour les systèmes d'appels automatisés.

## Fonctionnement

Le service vérifie trois conditions essentielles avant d'autoriser un appel:

1. **Heures de bureau**: Vérifie si la demande est effectuée pendant les heures d'ouverture définies (lundi-jeudi: 9h-17h, vendredi: 9h-12h)
2. **Activation des appels**: Vérifie si la fonctionnalité d'appels automatiques est activée via une API externe
3. **Disponibilité des agents**: Vérifie si au moins un agent est disponible pour prendre l'appel

## Endpoint Principal

- **URL**: `/`
- **Méthode**: GET
- **Authentification**: Requiert une clé API dans l'en-tête `X-API-KEY`

## Réponses

### Appel Autorisé (200 OK)
```json
{
  "allowed": true
}
```

### Appel Non Autorisé (200 OK)
```json
{
  "allowed": false,
  "reason": "out_of_hours" | "auto_call_disabled" | "no_available_agent"
}
```

### Erreur d'Authentification (403 Forbidden)
Retourné si la clé API est invalide ou manquante.

### Erreur Serveur (500 Internal Server Error)
```json
{
  "allowed": false,
  "error": "Description de l'erreur"
}
```

## Déploiement

Le service est conçu pour être déployé sur Google Cloud Run. Un script de déploiement (`deploy.sh`) est fourni pour faciliter ce processus.

```bash
# Rendre le script exécutable
chmod +x deploy.sh

# Exécuter le déploiement
./deploy.sh
```

## Variables d'Environnement

- `REQUEST_KEY`: Clé API requise pour l'authentification
- `AVAILABILITY_API_URL`: URL de l'API de vérification de disponibilité des agents
- `PORT`: Port sur lequel le serveur écoute (par défaut: 8080)

## Technologies Utilisées

- Python 3.11
- Flask
- Gunicorn
- Docker