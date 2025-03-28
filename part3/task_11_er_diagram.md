erDiagram
    User {
        string id PK
        string first_name
        string last_name
        string email
        string password
        boolean is_admin
    }

    Place {
        string id PK
        string title
        string description
        float price
        float latitude
        float longitude
        string owner_id FK
    }

    Review {
        string id PK
        string text
        int rating
        string user_id FK
        string place_id FK
    }

    Amenity {
        string id PK
        string name
    }

    Place_Amenity {
        string place_id FK
        string amenity_id FK
    }

    Reservation {
        string id PK
        string start_date
        string end_date
        int number_of_guests
        string user_id FK
        string place_id FK
    }

    User ||--o{ Place : owns
    User ||--o{ Review : writes
    Place ||--o{ Review : has
    Place ||--o{ Place_Amenity : has
    Amenity ||--o{ Place_Amenity : is part of
    User ||--o{ Reservation : books
    Place ||--o{ Reservation : available for
