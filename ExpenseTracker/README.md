# Expense Analyzer

A multi-part expense tracking and analysis system with:
- Java backend API (Spring Boot, coming soon)
- Python analysis engine with data visualization
- Frontend UI (coming soon)

## Project Structure

```
.
├── backend-java/           # Java API server
│   ├── pom.xml           # Maven configuration
│   └── src/main/java/    # Java source files
│       └── com/expensetracker/
│           └── Main.java # Entry point
│
├── Python Backend/        # Python analysis engine
│   ├── analyze.py        # Expense analysis & charts
│   ├── requirements.txt  # Python dependencies
│   ├── README.md        # Python setup guide
│   └── static/          # Generated charts
│
├── frontend/             # Web UI (coming soon)
│
└── shared-data/          # Shared data files
    ├── expenses.csv     # Expense records
    └── user-profile.json # User settings
```

## Quick Start

### Python Analysis Engine

1. Set up Python environment:
```powershell
cd "Python Backend"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

2. Run analysis:
```powershell
python analyze.py
```
Charts will be generated in the `static/` directory.

### Java Backend

1. Build with Maven:
```powershell
cd backend-java
mvn clean install
```

2. Run the server (coming soon):
```powershell
mvn spring-boot:run  # Once Spring Boot is added
```

## Development

- Java: JDK 17+ recommended
- Python: 3.8+ with pandas, matplotlib, numpy
- IDE: VS Code with Java & Python extensions

## Contributing

1. Create a feature branch
2. Make changes
3. Run tests (coming soon)
4. Submit PR

## License

MIT (or your preferred license)