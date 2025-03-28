# Documentation Technique du Projet HBnB

## Introduction

### Objectif du Document
Ce document technique décrit l'architecture et la conception du système HBnB. Il présente les principaux diagrammes, ainsi que des notes explicatives pour chaque élément, afin de guider l'implémentation du projet. Ce document doit être utilisé comme référence pendant toute la phase de développement.

### Aperçu du Projet
HBnB est une application de location de logements où les utilisateurs peuvent créer des annonces pour leurs propriétés, soumettre des avis, et réserver des logements. Le système est structuré en trois couches principales : **Présentation**, **Logique Métier**, et **Persistence**. Cette architecture est conçue pour faciliter la gestion des données et assurer une évolutivité optimale.

---

## 1. Architecture de Haut Niveau

### Diagramme de Package

Le diagramme suivant représente l'architecture en couches du système HBnB, en mettant en évidence les principales couches : **Présentation**, **Logique Métier**, et **Persistence**.

```mermaid
classDiagram
    class PresentationLayer {
        <<Interface>>
        +API
        +Service
    }

    class BusinessLogicLayer {
        +User
        +Place
        +Review
        +Amenity
    }

    class PersistenceLayer {
        +DatabaseAccess
    }

    PresentationLayer --> BusinessLogicLayer : Facade Pattern
    BusinessLogicLayer --> PersistenceLayer : Database Operations
```

### Business Logic Layer - Diagramme de Classe

Le diagramme suivant présente les principales classes de la couche Logique Métier, avec leurs attributs et leurs relations.

```mermaid
classDiagram
    class User {
        +UUID userId
        +String firstName
        +String lastName
        +String email
        +register()
        +updateProfile()
    }

    class Place {
        +UUID placeId
        +String name
        +String location
        +String description
        +createPlace()
        +updatePlace()
    }

    class Review {
        +UUID reviewId
        +String content
        +int rating
        +submitReview()
    }

    class Amenity {
        +UUID amenityId
        +String name
        +addAmenity()
    }

    User --> Place : creates
    User --> Review : writes
    Place --> Amenity : contains
```
### Sequence Diagrams for API Calls

Voici les diagrammes représentant les interactions entre les différentes couches lors de certains appels API dans l'application HBnB.

**User Registration**
```mermaid
sequenceDiagram
    participant User
    participant API
    participant BusinessLogic
    participant Database

    User->>API: POST /register (user data)
    API->>BusinessLogic: validateUserData(user data)
    BusinessLogic->>Database: saveUser(user data)
    Database-->>BusinessLogic: return userId
    BusinessLogic-->>API: return success (userId)
    API-->>User: return success message
```
**Place Creation**
```mermaid
sequenceDiagram
    participant User
    participant API
    participant BusinessLogic
    participant Database

    User->>API: POST /place/create (place data)
    API->>BusinessLogic: validatePlaceData(place data)
    BusinessLogic->>Database: savePlace(place data)
    Database-->>BusinessLogic: return placeId
    BusinessLogic-->>API: return success (placeId)
    API-->>User: return success message
```
**Review Submission**
```mermaid
sequenceDiagram
    participant User
    participant API
    participant BusinessLogic
    participant Database
    User->>API: POST /review/submit (review data)
    API->>BusinessLogic: validateReviewData(review data)
    BusinessLogic->>Database: saveReview(review data)
    Database-->>BusinessLogic: return reviewId
    BusinessLogic-->>API: return success (reviewId)
    API-->>User: return success message
```
**Fetching a List of Places**
```mermaid
sequenceDiagram
    participant User
    participant API
    participant BusinessLogic
    participant Database
    User->>API: GET /places (search criteria)
    API->>BusinessLogic: fetchPlaces(criteria)
    BusinessLogic->>Database: getPlaces(criteria)
    Database-->>BusinessLogic: return list of places
    BusinessLogic-->>API: return list of places
    API-->>User: return list of places
```
