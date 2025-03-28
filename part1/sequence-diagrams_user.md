```mermaid
sequenceDiagram
    participant U as User
    participant API as API Layer
    participant BL as Business Logic Layer
    participant DB as Persistence Layer

    U->>API: POST /register (user data)
    API->>BL: validateUserData(user data)
    BL->>BL: hashPassword(user password)
    BL->>DB: saveUser(user data)
    DB-->>BL: return userId
    BL-->>API: 201 Created (userId)
    API-->>U: return success message with userId
