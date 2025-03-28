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
