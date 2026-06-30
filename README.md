# Anti-Fraud Rule Engine

An asynchronous business rule engine designed for validating financial transactions, accounts, and devices. This project demonstrates an architectural approach to building anti-fraud and compliance systems where validation rules are managed dynamically rather than hardcoded.

## Description

A core engine that allows administrators to create, modify, and delete validation rules in real-time (such as amount limits or IP/country blocks). Incoming business objects are checked against active rules before being persisted to the database.

## Tech Stack

| Component | Technology |
|-----------|------------|
| Language | Python 3.10+ |
| Validation | Pydantic v2 |
| Framework | Django & Django REST Framework |
| Async Support | asyncio |
| Pattern | Repository Pattern, Dependency Injection |
| Configuration | python-dotenv |

## Architecture

```
anti-fraud-rule-engine/
├── src/
│   ├── main.py           # Demo simulation and API mock
│   ├── service.py        # Core rule engine business logic
│   ├── database.py       # Data access layer (Repository Pattern)
│   ├── schemas.py        # Pydantic validation schemas
│   ├── models.py         # Django models
│   └── config.py         # Application configuration
├── requirements.txt      # Python dependencies
├── .env.example         # Environment variables template
└── README.md
```

## Key Features

- **Dynamic Rule Management**: Create, update, and delete validation rules without code deployment
- **Multi-Object Support**: Validate transactions, accounts, and devices with unified rule engine
- **Real-time Validation**: Immediate rule application to incoming requests
- **Type Safety**: Strict validation with Pydantic schemas
- **Async Architecture**: Simulated database I/O delays for realistic performance testing
- **Repository Pattern**: Clean separation between data access and business logic
- **Operator Support**: Multiple comparison operators (>, <, ==, !=, in)

## How It Works

1. **Rule Creation**: Administrator defines a rule (e.g., `Target: Transaction, Field: amount, Operator: >, Value: 10000`)
2. **Object Validation**: User initiates a transaction with amount `15000`
3. **Schema Validation**: API validates data through Pydantic
4. **Rule Application**: `RuleEngineService` dynamically loads active rules for `Transaction` type
5. **Decision Making**: Engine applies operators and blocks transaction, returning `errors` array with rule violations
6. **Data Persistence**: Legitimate objects (passing all checks) are sent to DAL for storage

## Installation & Setup

### Prerequisites

- Python 3.10+
- pip

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `ADMIN_SECRET_KEY` | Secret key for admin operations | Yes |
| `DEBUG` | Enable debug mode | No (default: True) |

### Quick Start

1. Clone the repository:
```bash
git clone https://github.com/OniSku/anti-fraud-rule-engine.git
cd anti-fraud-rule-engine
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment:
```bash
cp .env.example .env
# Edit .env with your values
```

4. Run the demonstration:
```bash
python -m src.main
```

The simulation will demonstrate:
- Loading active rules from the database
- Processing various transaction and account validation scenarios
- Dynamic rule creation by administrators
- Real-time rule application and decision making

## Design Patterns

- **Repository Pattern**: Data access layer is isolated from business logic, enabling easy database migration
- **Dependency Injection**: Rule engine operates through interfaces, accepting prepared data
- **Schema Validation**: Pydantic ensures type safety and data integrity before processing

## Example Rules

- Block transactions over $10,000
- Restrict accounts from specific countries
- Block untrusted devices
- Age verification for account creation
- Custom business logic through configurable operators

⚠️ **Disclaimer**: This repository serves as a code showcase for demonstration purposes. It does not contain a fully runnable production environment or all proprietary backend dependencies.