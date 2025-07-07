# URL Shortener

A simple and efficient URL shortener built with [Flask](https://flask.palletsprojects.com/en/stable/) and [SQLite](https://sqlite.org), using [SQLAlchemy](https://sqlalchemy.org) as the ORM. This API allows users to shorten URLs, retrieve them, track usage statistics, update, or delete them.

## Features

* Generate short codes for long URLs
* Retrieve original URL using short code
* Track the number of times each short URL is accessed
* Update or delete existing short URLs
* View statistics for individual short URLs (e.g., creation date, access count)

## Modules Used

* [Python](https://python.org)
* [Flask](https://flask.palletsprojects.com/en/stable/)
* [SQLAlchemy](https://sqlalchemy.org)
* [SQLite](https://sqlite.org)
* datetime, secrets, string modules for utility tasks

## Endpoints

### `POST /shorten`

Create a shortened URL.

**Request**

* Form Data: `url=<your_long_url>`

**Response**

```json
{
  "id": 1,
  "url": "https://example.com",
  "shortCode": "a1B2c3",
  "createdAt": "2025-07-07T18:00:00.000Z",
  "updated": "null",
  "accessCount": 0
}
```

---

### `GET /shorten/<short_code>`

Retrieve the original URL and increment the access count.

**Response**

```json
{
  "id": 1,
  "url": "https://example.com",
  "shortCode": "a1B2c3",
  "createdAt": "...",
  "updated": "...",
  "accessCount": 1
}
```

---

### `PUT /shorten/<short_code>`

Update the original URL.

**Request**

* Form Data: `url=<new_url>`

**Response**
```json
{
  "id": 1,
  "url": "https://example.com",
  "shortCode": "a1B2c3",
  "createdAt": "...",
  "updated": "...",
  "accessCount": 1
}
```
---

### `DELETE /shorten/<short_code>`

Delete the URL record.

**Response:**

* `204 No Content` on success

---

### `GET /shorten/<short_code>/stats`

Get metadata about the short URL including creation time and access count.

**Response**

```json
{
  "id": 1,
  "url": "https://www.example.com",
  "shortCode": "AXC2a3",
  "createdAt": "...",
  "updated": "...",
  "accessCount": 3
}
```

## Setup Instructions

1. **Clone the Repository**

   ```bash
   git clone https://github.com/DragonSenseiGuy/url-shortener.git
   cd url-shortener
   ```

2. **Create a Virtual Environment (Optional but Recommended)**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # on Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**

   ```bash
   pip3 install requirements.txt
   ```

4. **Run the App**

   ```bash
   python main.py
   ```

5. **Visit**:
   Your API will run at `http://127.0.0.1:5000`

## Notes

* Short codes are generated using cryptographically secure randomness (`secrets` module).
* The app uses ISO 8601 format for all datetime fields.
* Database is created automatically in the project root (`url_database.db`).

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.