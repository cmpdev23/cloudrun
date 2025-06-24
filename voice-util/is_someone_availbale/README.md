# Service de vérification de disponibilité

Ce service fournit une API permettant de vérifier la disponibilité des agents dans un espace de travail Twilio TaskRouter.

## Route principale: Vérification de disponibilité

### Endpoint

```
GET /
```

### Description

Cette route vérifie si au moins un agent (worker) est disponible dans l'espace de travail Twilio configuré. Un agent est considéré comme disponible lorsque son `activity_sid` correspond à l'identifiant d'activité "Disponible" défini dans la configuration.

### Authentification

Toutes les requêtes doivent inclure un en-tête `X-API-KEY` avec la clé API valide.

Exemple:
```
X-API-KEY: votre_clé_api
```

### Réponse

La route retourne un objet JSON avec les informations suivantes:

#### Succès (200 OK)

```json
{
  "available": true|false,
  "twilio_raw": [
    {
      "friendly_name": "Nom de l'agent",
      "sid": "WKxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
      "activity_sid": "WAxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
      "activity_name": "Nom de l'activité"
    },
    ...
  ]
}
```

- `available`: Booléen indiquant si au moins un agent est disponible
- `twilio_raw`: Tableau contenant les détails de tous les agents, incluant:
  - `friendly_name`: Nom convivial de l'agent
  - `sid`: Identifiant unique de l'agent
  - `activity_sid`: Identifiant de l'activité actuelle de l'agent
  - `activity_name`: Nom de l'activité actuelle de l'agent

#### Erreur (500 Internal Server Error)

En cas d'erreur lors de la communication avec Twilio:

```json
{
  "available": false,
  "error": "Description de l'erreur"
}
```

### Exemple d'utilisation

```bash
curl -H "X-API-KEY: votre_clé_api" https://votre-service.com/