## Demystified Journal


A journal Web application developer using Django

---
## Table of Contents

---

# Purpose of project


# User Experience Design

## Typography and Fonts used

## Color Palette

# Wireframes

## Mobile Wireframes

## Tablet Wireframes

## Desktop Wireframes

# User Stories

# Features

# Entity Relationship Diagram (ERD)

```mermaid
erDiagram
USER ||--o{ ENTRY : "writes"
    ENTRY ||--o{ GRATITUDE_ITEM : "contains"
    ADMIN ||--o{ QUOTE : "manages"

    USER {
        int id PK
        string username
        string email
        string password
    }

    ENTRY {
        int id PK
        int user_id FK
        datetime date
        string mood
        int rating
        string title
        text content
        datetime created_at
    }

    GRATITUDE_ITEM {
        int id PK
        int entry_id FK
        string item_text
    }

    QUOTE {
        int id PK
        string text
        string author
    }
```

# Testing

# Bugs

# Deployment

# Technologies used

# Development Process
