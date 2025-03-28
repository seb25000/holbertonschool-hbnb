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

