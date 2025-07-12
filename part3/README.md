# [HBnB - Auth and DB](https://intranet.hbtn.io/projects/3212)
**Part 3: Implementation of tokens and database**

## Database Diagrams
Due to database being unfinished, here is what it could have been.
```mermaid
erDiagram
    USERS {
        uuid id
        string first_name
        string last_name
        string email
        string password
        boolean is_admin
    }

    PLACES {
        uuid id
        string title
        string description
        float price
        float latitude
        float longitude
        uuid owner_id
    }

    REVIEWS {
        uuid id
        string text
        int rating
        uuid user_id
        uuid place_id
    }

    AMENITIES {
        uuid id
        string name
    }

    USERS ||--o{ PLACES : owns
    USERS ||--o{ REVIEWS : writes
    PLACES ||--o{ REVIEWS : receives
    PLACES }o--o{ AMENITIES : contains-contained
```