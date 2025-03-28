```mermaid

classDiagram
    class User {
        +UUID userId
        +String firstName
        +String lastName
        +String email
        +String password
        +DateTime createdAt
        +DateTime updatedAt
        +register()
        +updateProfile()
        +deleteUser()
    }

    class Place {
        +UUID placeId
        +String title
        +String description
        +double price
        +double latitude
        +double longitude
        +DateTime createdAt
        +DateTime updatedAt
        +createPlace()
        +updatePlace()
        +deletePlace()
        +listAmenities()
    }

    class Review {
        +UUID reviewId
        +String comment
        +int rating
        +DateTime createdAt
        +DateTime updatedAt
        +createReview()
        +updateReview()
        +deleteReview()
    }

    class Amenity {
        +UUID amenityId
        +String name
        +String description
        +DateTime createdAt
        +DateTime updatedAt
        +addAmenity()
        +updateAmenity()
        +deleteAmenity()
    }

    User "1" --> "*" Place : owns
    Place "1" --> "*" Review : has
    Place "*" --> "*" Amenity : has
