# Travel Deal Management System

A small but cleanly-structured REST API for managing travel deals, built with Flask. We can add new deals, browse everything that's been added, and pull up the details of a single deal — all through simple JSON endpoints.

This was built as the Part 01 backend assignment using Flask for the W3 Engineers internship.

## Table of Contents

- [What it does](#what-it-does)
- [How it's organized](#how-its-organized)
- [Getting it running](#getting-it-running)
- [The API](#the-api)
  - [Add a travel deal](#add-a-travel-deal)
  - [Get all deals](#get-all-deals)
  - [Get a single deal](#get-a-single-deal)
- [Validation rules](#validation-rules)
- [Errors we might run into](#errors-you-might-run-into)
- [Testing with Postman](#testing-with-postman)
- [Tech used](#tech-used)
- [A few notes](#a-few-notes)

## What it does

At its core, the API lets us work with travel deals. Each deal has a destination, a price, the platform it was found on, an optional rating, and a travel type (like Budget or Luxury). The three things you can do:

- **Create a deal** by sending its details to the API
- **List every deal** that's been stored
- **Look up one specific deal** by its ID

Everything comes back as JSON, with proper HTTP status codes and friendly error messages when something goes wrong.

## How it's organized

The project is split into layers so each part has one job. This keeps the routes thin and the logic easy to test and reuse:

```
project/
├── app.py             # Creates the app, sets up the DB, registers routes
├── routes/            # Defines the HTTP endpoints (request in, response out)
├── services/          # The actual business logic and database operations
├── utils/             # Reusable validation helpers
├── database/          # Models / database setup
├── config.py.sample   # Sample config — copy and rename to config.py
├── requirements.txt   # Python dependencies
└── README.md
```

The idea: a route's only job is to accept a request and hand back a response. The real work — validating input, talking to the database — happens in `services/` and `utils/`. That separation is intentional and makes the whole thing easier to extend later.

## Getting it running

You'll need Python 3 installed. From there:

**1. Clone the repo**

```bash
git clone https://github.com/NaimurRahmannn/Travel-Deal-Management-System.git
cd Travel-Deal-Management-System
```

**2. Set up a virtual environment** (recommended, keeps dependencies isolated)

```bash
python -m venv venv
source venv/bin/activate 
```

**3. Install the dependencies**

```bash
pip install -r requirements.txt
```

**4. Set up your config**

There's a `config.py.sample` file in the repo. Copy it and rename the copy to `config.py`, then fill in your own values.

**5. Run the app**

```bash
python3 app.py
```

The server will start on `http://localhost:5000`.

## The API

### Add a travel deal

```
POST /deals
```

Send a JSON body like this:

```json
{
    "destination": "Dubai",
    "price": 5000,
    "platform": "Booking",
    "rating": 4.5,
    "travel_type": "Luxury"
}
```

If everything checks out, you get back the newly created deal with a `201 Created`. If something's off, you get a `400` with a message telling you what went wrong.

### Get all deals

```
GET /deals
```

Returns a list of every deal stored, with a `200 OK`.

### Get a single deal

```
GET /deals/<id>
```

Returns the matching deal, or a `404 Not Found` if there's no deal with that ID.

## Validation rules

Before a deal gets saved, it has to pass a few checks. These live in `utils/` so they can be reused anywhere:

- **`destination`** can't be empty
- **`price`** must be a positive number
- **`rating`** must be between 1 and 5 (it's optional, so it can be left out)
- **`travel_type`** has to be one of: `Budget`, `Luxury`, `Adventure`, or `Family`

If any of these fail, the API responds with a clear `400 Bad Request` explaining the problem instead of crashing or silently accepting bad data.

## Errors you might run into

The API tries to fail gracefully and tell us what happened:

- **400 Bad Request** — our input didn't pass validation, or the JSON body was malformed
- **404 Not Found** —We asked for a deal (or a route) that doesn't exist
- **201 Created** — our deal was added successfully
- **200 OK** — our request worked

A quick note on malformed JSON: make sure your request body uses **double quotes** around keys and string values, and that you set the `Content-Type: application/json` header. Single quotes will cause a JSON decode error.

## Testing with Postman

There's a Postman collection included in the repo (`Postman Collection.postman_collection.json`). Import it into Postman and you'll have all three endpoints ready to go, so you can try things out without typing requests by hand.

## Tech used

- **Python 3**
- **Flask** — the web framework
- **Flask-SQLAlchemy** — for the database models and queries
- **SQLite** — the database (lightweight, no setup needed)

## A few notes

This is just the first part of a bigger assignment, so I kept it focused on the main backend basics instead of adding too many features at once. The project is structured in a way that makes it easy to improve later, like adding filters, new endpoints, or API versioning such as an /api/v1 prefix, without changing the existing setup too much.

---
