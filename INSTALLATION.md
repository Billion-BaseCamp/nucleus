# Installation Guide for Nucleus Package

This guide explains how to install the `nucleus` package in other projects.

## Installation Methods

### Method 1: Local Development (Editable Install) ✅ Recommended for Development

If the other project is on the same machine or accessible:

```bash
pip install -e /path/to/nucleus
```

Or using a relative path:
```bash
pip install -e ../nucleus
```

### Method 2: From Git Repository

If your package is version controlled:

```bash
# Public repository
pip install git+https://github.com/yourusername/nucleus.git

# Specific branch
pip install git+https://github.com/yourusername/nucleus.git@main

# Specific version/tag
pip install git+https://github.com/yourusername/nucleus.git@v0.1.0

# Private repository (SSH)
pip install git+ssh://git@github.com/yourusername/nucleus.git
```

Add to `requirements.txt`:
```txt
git+https://github.com/yourusername/nucleus.git@main
```

### Method 3: Build and Install Distribution

Build the package:
```bash
cd nucleus
python -m build
```

Install from built wheel:
```bash
pip install dist/nucleus-0.1.0-py3-none-any.whl
```

### Method 4: Using requirements.txt

In your other project's `requirements.txt`:
```txt
# Option 1: Local path (editable)
-e /absolute/path/to/nucleus

# Option 2: Git repository
git+https://github.com/yourusername/nucleus.git@main

# Option 3: Local wheel file
# nucleus @ file:///path/to/nucleus/dist/nucleus-0.1.0-py3-none-any.whl
```

Then install:
```bash
pip install -r requirements.txt
```

## Dependency Groups

The package has minimal core dependencies and optional extras:

### Core Dependencies (Always Installed)
- `SQLAlchemy` - Required for all models
- `python-dotenv` - For database configuration
- `pytz` - For timezone constants

### Optional Dependencies

Install additional extras only if needed:

```bash
# For running migrations (Alembic)
pip install nucleus[migrations]

# For web frameworks (FastAPI, Uvicorn)
pip install nucleus[web]

# For database drivers (PostgreSQL)
pip install nucleus[database]

# For development tools
pip install nucleus[dev]

# Install all optional dependencies
pip install nucleus[full]
```

**In other projects that only query the database:**
```bash
pip install -e /path/to/nucleus
# or
pip install git+https://github.com/yourusername/nucleus.git
```
This installs only the core dependencies (SQLAlchemy, python-dotenv, pytz).

**For the nucleus project itself** (where you run migrations):
```bash
pip install -e .[migrations,database]
```

## Usage After Installation

Once installed, import and use the models:

```python
# Import models
from nucleus.models import Client, Advisor, CapitalGains, FinancialYear
from nucleus.models.common_models.client import Client
from nucleus.models.advance_tax_models.capital_gains import CapitalGains

# Import database components
from nucleus.db.database import Base, SessionLocal, engine

# Import constants
from nucleus.core.constants import UserRole, ResidenceType, CapitalGainsCategory
```

## Verify Installation

Check if the package is installed:
```bash
pip show nucleus
```

Test imports:
```python
python -c "from nucleus.models import Client; print('Success!')"
```

