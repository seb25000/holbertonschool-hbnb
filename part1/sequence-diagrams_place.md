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

