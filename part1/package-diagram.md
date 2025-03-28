```mermaid

classDiagram
    class PresentationLayer {
        <<Interface>>
        +ServiceAPI
        +UserService
        +PlaceService
        +ReviewService
    }

    class BusinessLogicLayer {
        +UserModel
        +PlaceModel
        +ReviewModel
        +AmenityModel
    }

    class PersistenceLayer {
        +UserRepository
        +PlaceRepository
        +ReviewRepository
        +AmenityRepository
    }

    PresentationLayer --> BusinessLogicLayer : Facade Pattern
    BusinessLogicLayer --> PersistenceLayer : Database Operations
