# Travel Deal Management System

A cleanly-structured REST API for managing travel deals, built with Flask. You can add, browse, update, and delete deals; search, filter, and sort them; see which deals were recently viewed or are most popular; and check overall API usage statistics. Everything is served as JSON with proper status codes and meaningful error messages.

Built across three days for the W3 Engineers internship (Batch 11): Part 01 covered the core CRUD-style endpoints and validation; Part 02 added advanced search, filtering, sorting, logging, and recently-viewed tracking; Part 03 added update/delete, view-count tracking, a most-viewed (popular) endpoint, and app-wide usage statistics — all while keeping the architecture clean and the logic reusable.

## Table of Contents

- [What it does](#what-it-does)
- [How it's organized](#how-its-organized)
- [Getting it running](#getting-it-running)
- [The API](#the-api)
  - [Add a travel deal](#add-a-travel-deal)
  - [Get all deals](#get-all-deals)
  - [Get a single deal](#get-a-single-deal)
  - [Update a deal](#update-a-deal)
  - [Delete a deal](#delete-a-deal)
  - [Search deals](#search-deals)
  - [Filter deals by budget](#filter-deals-by-budget)
  - [Sort deals](#sort-deals)
  - [Recently viewed deals](#recently-viewed-deals)
  - [Most popular deals](#most-popular-deals)
  - [API usage statistics](#api-usage-statistics)
- [Validation rules](#validation-rules)
- [Logging](#logging)
- [Errors we might run into](#errors-we-might-run-into)
- [Testing with Postman](#testing-with-postman)
- [Tech used](#tech-used)
- [A few notes](#a-few-notes)

## What it does

At its core, the API lets us work with travel deals. Each deal has a destination, a price, the platform it was found on, an optional rating, and a travel type (like Budget or Luxury). What you can do:

- **Create a deal** by sending its details to the API
- **List every deal** that's been stored
- **Look up one specific deal** by its ID
- **Update a deal** in place, with the same validation as creating one
- **Delete a deal**, with related view records cleaned up safely
- **Search** deals by destination, platform, or travel type — partial and case-insensitive
- **Filter** deals by a price range
- **Sort** deals by any field, ascending or descending
- **See recently viewed deals** — the individual deals you've opened, newest first
- **See most popular deals** — ranked by how many times they've been viewed
- **Check API usage statistics** — request counts, the most-searched destination, and the most-viewed deal

Every response is JSON, with appropriate HTTP status codes and clear error messages when something goes wrong.

## How it's organized

The project is split into layers so each part has one job. This keeps the routes thin and the logic easy to test and reuse:

```
project/
├── app.py             # Creates the app, sets up the DB, registers blueprints, error handlers, request hook
├── routes/            # Defines the HTTP endpoints (request in, response out)
├── services/          # Business logic and database operations
├── utils/             # Reusable validation, logging, and stats helpers
├── database/          # Models / database setup
├── logs/              # Log files (created automatically at runtime)
├── config.py.sample   # Sample config — copy and rename to config.py
├── requirements.txt   # Python dependencies
└── README.md
```

The guiding idea: a route only accepts a request and returns a response. The real work — validating input, building queries, talking to the database — lives in `services/` and `utils/`. Two consequences worth highlighting: when the recently-viewed feature was switched from in-memory storage to the database, not a single route had to change, because the routes only call service functions; and request counting is handled by one app-wide hook rather than being repeated in every route.

## Getting it running

You'll need Python 3 installed. From there:

**1. Clone the repo**

```bash
git clone https://github.com/NaimurRahmannn/Travel-Deal-Management-System.git
cd Travel-Deal-Management-System
```

**2. Set up a virtual environment**

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

The server starts on `http://localhost:5000`, and the database tables are created automatically on first run.

## The API

Deal endpoints live under the `/deals` prefix. The statistics endpoint lives at the root (`/stats`).

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

On success you get the newly created deal with a `201 Created`. If validation fails or the body isn't valid JSON, you get a `400` explaining what's wrong.

### Get all deals

```
GET /deals
```

Returns a list of every deal stored, with `200 OK`. (Listing deals does not count as "viewing" any of them — only opening a single deal does.)

### Get a single deal

```
GET /deals/<id>
```

Returns the matching deal, or `404 Not Found` if no deal has that ID. A non-numeric ID returns a `400`. Opening a deal here records it as both recently viewed and a view event (used for popularity).

### Update a deal

```
PUT /deals/<id>
```

Replaces all fields of an existing deal. Send a full JSON body, the same shape as creating a deal:

```json
{
    "destination": "Singapore",
    "price": 7000,
    "platform": "Agoda",
    "rating": 4.8,
    "travel_type": "Luxury"
}
```

Update uses the exact same validation as create, so the rules are identical. Returns the updated deal with `200 OK`, a `400` if validation fails or the ID isn't numeric, or a `404` if no deal has that ID.

### Delete a deal

```
DELETE /deals/<id>
```

Deletes the deal and cleans up its recently-viewed record. Returns a `200 OK` confirmation message on success, a `404` if the deal doesn't exist (handled safely — deleting a missing deal never crashes), and a `400` if the ID isn't numeric.

### Search deals

```
GET /deals/search
```

Query parameters (provide at least one): `destination`, `platform`, `travel_type`.

```
GET /deals/search?destination=dubai
GET /deals/search?platform=booking&travel_type=luxury
```

Search is **partial** and **case-insensitive** — `dub` matches "Dubai", and `LUXURY` matches "Luxury". When multiple parameters are given, they combine: results must match all of them. Calling search with no parameters returns a `400`. Each search also records the destination, feeding the "most-searched destination" statistic.

### Filter deals by budget

```
GET /deals/filter
```

Query parameters: `min_price`, `max_price` (either or both).

```
GET /deals/filter?min_price=1000&max_price=5000
GET /deals/filter?min_price=2000
```

Prices are validated before querying: a non-numeric value, a negative price, or a `max_price` smaller than `min_price` all return a `400` with a clear message.

### Sort deals

```
GET /deals/sort
```

Query parameters: `sort_by` (defaults to `price`) and `order` (`asc` or `desc`, defaults to `asc`).

```
GET /deals/sort?sort_by=price&order=desc
GET /deals/sort?sort_by=rating&order=desc
```

`sort_by` accepts `price`, `rating`, `destination`, `travel_type`, `platform`, or `id`. An unknown field or an invalid order returns a `400`.

### Recently viewed deals

```
GET /deals/recent
```

Returns the deals you've opened via `GET /deals/<id>`, newest first, capped at the 10 most recent. Each deal appears only once — viewing a deal again moves it back to the front rather than adding a duplicate. Stored in the database, so the list survives app restarts.

### Most popular deals

```
GET /deals/popular
```

Returns deals ranked by how many times they've been viewed, most-viewed first. Each result includes a `views` count alongside the deal details. Popularity is computed from a log of view events, so it reflects total views over time, not just distinct deals.

### API usage statistics

```
GET /stats
```

Returns a snapshot of how the API has been used:

- **Request counts** — total, successful, and failed requests
- **Most-searched destination** — the destination searched most often
- **Most-viewed deal** — the deal with the highest view count

Request counts and search tracking are kept in memory and reset when the app restarts, while the most-viewed deal is derived from view events stored in the database.

## Validation rules

Validation lives in `utils/` so it's reusable across routes. For creating or updating a deal (both use the same rules):

- **`destination`** can't be empty
- **`platform`** can't be empty
- **`price`** must be a number and positive
- **`rating`** is optional, but if given must be a number between 1 and 5
- **`travel_type`** must be one of: `Budget`, `Luxury`, `Adventure`, or `Family`

For search, filter, and sort:

- A search with no parameters is rejected
- `min_price` and `max_price` can't be negative, and `max_price` can't be smaller than `min_price`
- Non-numeric price values are rejected with a clear message
- `sort_by` must be a known field and `order` must be `asc` or `desc`

Every validator follows the same pattern — it returns an error message string if something's wrong, or `None` if everything checks out — so the calling code stays consistent everywhere.

## Logging

The app logs activity at three levels using Python's `logging` module, configured once in `utils/logger.py`. Logs go to both the console and a file at `logs/app.log` (the folder is created automatically). The app tracks:

- **Successful operations** (`info`) — searches, filters, deal views, updates, and deletes that completed
- **Invalid requests** (`warning`) — rejected filters, bad sort parameters, missing deals on update/delete, and similar
- **Failures** (`error` / `warning`) — for example, a database error while saving or while recording a view

This makes it easy to trace what the API did and why a request was rejected.

## Errors we might run into

The API fails gracefully and tells us what happened:

- **400 Bad Request** — input didn't pass validation, the ID wasn't numeric, or the JSON body was malformed
- **404 Not Found** — the deal or route doesn't exist
- **405 Method Not Allowed** — wrong HTTP method for that endpoint
- **500 Internal Server Error** — something unexpected went wrong on the server
- **200 OK** / **201 Created** — your request worked

A quick note on malformed JSON: make sure your request body uses **double quotes** around keys and string values, and that you set the `Content-Type: application/json` header. Single quotes cause a JSON decode error.

## Testing with Postman

There's a Postman collection included in the repo (`Postman Collection.postman_collection.json`). Import it into Postman and you'll have all the endpoints ready to go, so you can try things out without typing requests by hand. A good flow to try: add a few deals, search and filter them, sort by price, open a couple by ID a few times, update and delete one, then check `/deals/recent`, `/deals/popular`, and `/stats`.

## Tech used

- **Python 3**
- **Flask** — the web framework
- **Flask-SQLAlchemy** — database models and queries
- **SQLite** — the database (lightweight, no setup needed)
- **Python `logging`** — request and activity logging

## A few notes

The architecture is built to grow. Search and budget filtering share a single reusable query-building helper, so adding a new filter is a matter of extending that one helper rather than duplicating logic. Recently-viewed deals are stored with one row per deal (deduplicated), while popularity is tracked separately as a log of individual view events — two different questions, two purpose-built tables. Request statistics are gathered by a single app-wide hook rather than being scattered across routes, keeping the counting logic in one place.

Built by [Naimur Rahman](https://github.com/NaimurRahmannn)
