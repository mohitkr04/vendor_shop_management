# 🏪 Vendor and Shop Management System

A modern FastAPI-based web application that enables vendors to register and manage their shops, featuring a powerful API for searching nearby shops.

---

## ✨ Features

### 🔐 Vendor Management
- Secure vendor registration with email and password
- JWT token-based authentication
- Protected vendor profile management

### 🏬 Shop Operations
- **Create:** Add new shops with detailed information
- **Read:** Access comprehensive shop details
- **Update:** Modify existing shop information
- **Delete:** Remove shops from the platform
- **Multi-Shop Support:** Vendors can manage multiple shops

### 📍 Location Services
- Search nearby shops using latitude and longitude
- Customizable search radius
- Distance-based shop filtering

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/mohitkr04/vendor_shop_management
   cd vendor-shop-management
   ```
2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   ```
   - **On Windows:**
     ```bash
     venv\Scripts\activate
     ```
   - **On macOS/Linux:**
     ```bash
     source venv/bin/activate
     ```
3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

---

## 💻 Usage

### Starting the Server
```bash
uvicorn app.main:app --reload
```
The server will start at `http://localhost:8000`

### API Documentation
Access the interactive API documentation at:
- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

---

## 📡 API Endpoints

### Vendor Routes
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST   | `/vendors/` | Register new vendor |
| POST   | `/vendors/token` | Login and get access token |
| GET    | `/vendors/me` | Get current vendor profile |

### Shop Routes
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST   | `/shops/` | Create new shop |
| GET    | `/shops/` | List all shops |
| GET    | `/shops/{shop_id}` | Get specific shop details |
| PUT    | `/shops/{shop_id}` | Update shop information |
| DELETE | `/shops/{shop_id}` | Delete shop |
| GET    | `/shops/nearby/` | Search nearby shops |

---

## 🔒 Security Features

- **Password Security:** Bcrypt hashing for password storage
- **Authentication:** JWT token-based authentication
- **Authorization:** Role-based access control
- **Data Protection:** Secure data transmission and storage

---

## 🗄️ Database Schema

### Vendor Model
```python
class Vendor:
    id: int
    name: str
    email: str
    hashed_password: str
```

### Shop Model
```python
class Shop:
    id: int
    name: str
    owner: str
    business_type: str
    latitude: float
    longitude: float
    vendor_id: int
```

---

## 🧪 Testing

Run the comprehensive test suite:
```bash
pytest
```
The test suite includes:
- Vendor authentication tests
- Shop CRUD operation tests
- Nearby shop search tests
- Integration tests

---

## 🛠️ Technology Stack

- **Framework:** FastAPI
- **Database:** SQLite with SQLAlchemy ORM
- **Authentication:** JWT tokens
- **Testing:** pytest
- **Documentation:** Swagger/OpenAPI

---

## 📝 Development Notes

### Project Structure
```
vendor_shop_management/
├── app/                 # Main application directory
│   ├── __init__.py
│   ├── database.py      # Database connection and setup
│   ├── models.py        # Pydantic models for data validation
│   ├── schemas.py       # Pydantic schemas for request/response data
│   ├── auth.py          # Authentication logic (JWT)
│   ├── crud.py          # Database CRUD operations
│   ├── routers/         # API route handlers (organized by resource)
│   │   ├── __init__.py
│   │   ├── vendors.py    # Vendor registration/authentication routes
│   │   └── shops.py      # Shop management routes
│   └── main.py          # Main application entry point (FastAPI instance)
├── tests/               # Unit tests
│   ├── __init__.py
│   ├── conftest.py      # Fixtures for tests
│   ├── test_vendors.py  # Tests for vendor routes
│   └── test_shops.py    # Tests for shop routes
├── README.md            # Project documentation
├── requirements.txt     # Dependencies
└── .gitignore           # Files to ignore in Git
```

---

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 👥 Authors

- Mohit Kumar - *Initial work*

---

## 🙏 Acknowledgments

- FastAPI documentation
- SQLAlchemy community
- Python community

---

⭐️ Star this repository if you find it helpful! 🚀

