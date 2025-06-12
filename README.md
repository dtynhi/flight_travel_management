# Flight Management System (QLMB) – Quick Start

## 1. Clone Project

```bash
git clone https://github.com/dtynhi/flight_travel_management
cd flight_travel_management
```

## 2. Install Dependencies

Make sure you have **Python 3.10+** installed:

```bash
python --version
```

Then install the required libraries:

```bash
pip install -r requirements.txt
```

## 3. Run the App

Start the application by running:

```bash
python main.py
```

The API will be available at http://localhost:5000.

## 4. Debugging in VS Code

To debug and set breakpoints easily in VS Code:

### Step 1: Create .vscode/launch.json

Create a file at .vscode/launch.json with the following content:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: Run main.py",
      "type": "python",
      "request": "launch",
      "program": "${workspaceFolder}/main.py",
      "console": "integratedTerminal",
      "justMyCode": false
    }
  ]
}
```

### Step 2: Start Debugging

1. Open the project in VS Code.

2. Set breakpoints in main.py or any other file.

3. Press F5 or click "Run > Start Debugging".

## Notes

- Make sure .env.dev is present for environment variables.

- You can edit main.py or app_config.py to log values or disable token expiration during debugging.

- No virtual environment is required for local development.

---

For full documentation, see the [document](https://deepwiki.com/dtynhi/flight_travel_management_app) below or contact: duongthaiynhi@gmail.com
