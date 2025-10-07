# SimpleCalendarEx\BackendService_Ver1.0

A Python FastAPI web service for managing calendar day-off records with PostgreSQL database.

## Quick Start

### Prerequisites
- Python 3.8+
- PostgreSQL database
- pip (Python package manager)

### Installation & Setup

1. **Clone and navigate to the project:**
   ```bash
   cd BackendService_Ver1.0
   ```

2. **Set up environment variables:**
   ```bash
   copy .env.example .env
   ```
   Edit `.env` file with your database credentials:
   ```
   DATABASE_URL=postgresql://username:password@localhost:5432/your_database
   HOST=0.0.0.0
   PORT=8000
   DEBUG=True
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   python main.py
   ```
   Or use the startup script:
   ```bash
   # Windows
   start.bat
   
   # Linux/Mac
   chmod +x start.sh
   ./start.sh
   ```

5. **Access the API:**
   - API Base URL: http://localhost:8000
   - Interactive API Documentation: http://localhost:8000/docs
   - Alternative docs: http://localhost:8000/redoc

## API Endpoints

### 1. Create & Edit Day Off
**POST** `/api/dayoff/create`

**Request Body:**
```json
{
  "dayoff": "25/12/2023",
  "isOffDay": true,
  "description": "Christmas Day",
  "creator": "admin",
  "organid": "ORG001"
}
```

**Response:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "organid": "ORG001",
  "dayoff": "2023-12-25",
  "year": 2023,
  "description": "Christmas Day",
  "creator": "admin",
  "createdate": "2023-10-05",
  "modifier": null,
  "modifydate": null,
  "delflag": 0
}
```

### 2. Delete Day Off
**DELETE** `/api/dayoff/delete`

**Request Body:**
```json
{
  "dayoff": "25/12/2023",
  "organid": "ORG001"
}
```

**Response:** DayOffDto with updated delflag

### 3. Search Day Offs
**POST** `/api/dayoff/search`

**Request Body:**
```json
{
  "dayoffFrom": "01/12/2023",
  "dayoffTo": "31/12/2023",
  "organid": "ORG001"
}
```

**Response:** Array of DayOffDto objects

### 4. Check Day Off
**POST** `/api/dayoff/check`

**Request Body:**
```json
{
  "dayoff": "25/12/2023",
  "organid": "ORG001"
}
```

**Response:**
```json
{
  "is_off_day": true
}
```

## Project Structure

```
BackendService_Ver1.0/
├── app/
│   ├── __init__.py
│   ├── config.py              # Application configuration
│   ├── api/
│   │   ├── __init__.py
│   │   └── dayoff.py          # Day off endpoints
│   ├── db/
│   │   ├── __init__.py
│   │   └── database.py        # Database connection
│   └── models/
│       ├── __init__.py
│       ├── dayoff.py          # SQLAlchemy models
│       └── schemas.py         # Pydantic models
├── database/
├── main.py                    # FastAPI application entry point
├── requirements.txt           # Python dependencies
├── .env.example              # Environment variables template
├── .gitignore                # Git ignore rules
├── start.bat                 # Windows startup script
├── start.sh                  # Linux/Mac startup script
└── readme.md                 # This file
```

## Database Schema

### Table: daysoffyear

-- Drop table

-- DROP TABLE public.daysoffyear;

CREATE TABLE public.daysoffyear (
	id uuid NOT NULL,
	organid varchar(250),
	dayoff date NULL,
	"year" int4 NULL,
	description text NULL,
	creator varchar(250) NULL,
	createdate date NULL,
	modifier varchar(250) NULL,
	modifydate date NULL,
	delflag int4 NULL,
	CONSTRAINT daysoffyear_pkey PRIMARY KEY (id)
);

-- Permissions

ALTER TABLE public.daysoffyear OWNER TO postgres;
GRANT ALL ON TABLE public.daysoffyear TO postgres;