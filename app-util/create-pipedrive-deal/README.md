# Pipedrive Deal Creator

## Vue d'ensemble

Cette application est une API Flask qui permet de créer et gérer des opportunités (deals) dans Pipedrive CRM. Elle sert d'interface entre vos formulaires ou applications et Pipedrive, en automatisant la création de contacts et d'opportunités commerciales.

## Fonctionnalité principale

L'application expose une route principale `/deal-processing` qui traite les demandes de création ou de mise à jour d'opportunités dans Pipedrive. Cette route accepte des requêtes POST avec des données JSON et retourne des URLs Pipedrive pour accéder directement aux ressources créées.

### Route `/deal-processing`

Cette route accepte des données JSON et les traite différemment selon le type de transaction spécifié (`deal_type`):

#### Types de transactions

1. **Vente (`deal_type: "vente"`)** 
   - Recherche un contact existant par numéro de téléphone
   - Si le contact existe:
     - Recherche des opportunités existantes pour ce contact
     - Met à jour les opportunités existantes ou en crée une nouvelle
   - Si le contact n'existe pas:
     - Crée un nouveau contact
     - Crée une nouvelle opportunité associée à ce contact
   - Retourne l'URL Pipedrive de l'opportunité créée/mise à jour

2. **Suivi (`deal_type: "suivi"`)** 
   - Recherche un contact existant par numéro de téléphone
   - Si le contact existe:
     - Ajoute une note au contact
   - Si le contact n'existe pas:
     - Crée un nouveau contact
     - Ajoute une note au contact
   - Retourne l'URL Pipedrive du contact

## Exemple d'utilisation

Pour créer une nouvelle opportunité de vente:

```json
POST /deal-processing
Content-Type: application/json

{
  "deal_type": "vente",
  "name": "Jean Dupont",
  "phone": "+33612345678",
  "insurance_type": "Assurance Vie",
  "insurance_amount": "100000",
  "gender": "M",
  "birth_year": "1980"
}
```

Réponse:
```json
{
  "url": "https://comparermaprime.pipedrive.com/deal/123"
}
```

Pour ajouter une note de suivi à un contact:

```json
POST /deal-processing
Content-Type: application/json

{
  "deal_type": "suivi",
  "name": "Jean Dupont",
  "phone": "+33612345678",
  "message": "Le client souhaite être rappelé la semaine prochaine"
}
```

Réponse:
```json
{
  "url": "https://comparermaprime.pipedrive.com/person/456"
}
```

Cette API simplifie l'intégration avec Pipedrive en automatisant les opérations courantes et en fournissant un accès direct aux ressources créées via les URLs retournées.