# Backend Processor System - Pre-Processing Static Template Generation

## Overview

The new **Backend Processor System** transforms the FastAPI template generation from a dynamic, conditional approach to a **pre-processed static template system**. This system performs all conditional logic and configuration during template generation, producing completely static templates with no runtime conditionals.

## Key Features

### 1. **Pre-Processing Architecture**
- **All conditional logic is evaluated during template creation**
- **No conditional statements remain in generated templates**
- **Static files contain only finalized content**
- **Configuration is processed upfront, not at runtime**

### 2. **User Configuration Collection**
- **Single-pass configuration collection** via CLI
- **All decisions made before template generation begins**
- **Configuration validated and processed upfront**

### 3. **Static Template Generation**
- **Requirements files generated with exact dependencies**
- **Database configurations pre-processed for selected backend**
- **Environment files created with finalized values**
- **Model files contain only backend-specific implementations**

## Architecture Components

### BackendProcessor Class

The `BackendProcessor` class handles all pre-processing logic:

```python
from fastapi_template.backend_processor import BackendProcessor

processor = BackendProcessor(template_path, target_path)
processor.process_template(user_config)
```

### Configuration Processing Flow

1. **User Input Collection**
   - Template type selection (minimal, api_only, fullstack)
   - Backend selection (sqlalchemy, beanie)
   - Feature flags (auth, database, docker, tests)

2. **Configuration Validation**
   - Default value assignment
   - Feature dependency resolution
   - Backend-specific settings

3. **Static Content Generation**
   - Requirements.txt with exact dependencies
   - Database configuration files
   - Environment configuration
   - Application models and code

4. **File Processing**
   - Conditional file inclusion/exclusion
   - Backend-specific file generation
   - Static content replacement

## Usage Examples

### CLI Usage

```bash
# Create fullstack project with SQLAlchemy
fastapi-template new myapp --template fullstack --backend sqlalchemy

# Create minimal project
fastapi-template new myapp --template minimal

# Interactive mode
fastapi-template new myapp
```

### Programmatic Usage

```python
from fastapi_template.backend_processor import BackendProcessor

config = {
    "template_type": "fullstack",
    "backend": "beanie",
    "include_auth": True,
    "include_database": True,
    "include_docker": True
}

processor = BackendProcessor(template_path, target_path)
processor.process_template(config)
```

## Configuration Schema

```json
{
  "template_type": "fullstack",
  "backend": "sqlalchemy",
  "include_auth": true,
  "include_database": true,
  "include_docker": true,
  "include_tests": true
}
```

## Generated File Structure

### SQLAlchemy Backend
```
myapp/
├── requirements.txt          # SQLAlchemy + PostgreSQL deps
├── alembic.ini              # Migration configuration
├── alembic/
│   ├── env.py               # SQLAlchemy migration env
│   └── versions/
├── docker-compose.yml        # PostgreSQL setup
├── .env.example             # SQLAlchemy env vars
├── app/
│   ├── db/database.py       # SQLAlchemy configuration
│   ├── models/user.py       # SQLAlchemy User model
│   └── models/item.py       # SQLAlchemy Item model
└── ... (other static files)
```

### Beanie Backend
```
myapp/
├── requirements.txt          # Beanie + MongoDB deps
├── docker-compose.yml      # MongoDB setup
├── .env.example            # MongoDB env vars
├── app/
│   ├── db/database.py      # Beanie configuration
│   ├── models/user.py      # Beanie User model
│   └── models/item.py      # Beanie Item model
└── ... (other static files)
```

## Benefits

### 1. **Performance**
- No runtime conditional evaluation
- Faster startup times
- Reduced memory usage

### 2. **Maintainability**
- Single source of truth for configurations
- No conditional logic in templates
- Easier debugging and testing

### 3. **Consistency**
- All files contain only relevant content
- No unused dependencies
- Consistent file structure

### 4. **Testing**
- Predictable output for given inputs
- Easier integration testing
- Simplified CI/CD pipelines

## Testing

Run the test suite to verify the backend processor:

```bash
python test_backend_processor.py
```

This will test:
- All template types (minimal, api_only, fullstack)
- Both backend types (sqlalchemy, beanie)
- Static content generation
- File structure validation
- Configuration processing

## Migration Guide

### From Dynamic to Static Templates

1. **Remove conditional logic** from template files
2. **Add BackendProcessor** for pre-processing
3. **Update CLI** to use new system
4. **Test generated templates** for correctness

### Template File Updates

**Before (Dynamic):**
```python
# Conditional imports based on backend
if os.getenv("BACKEND_TYPE") == "sqlalchemy":
    from sqlalchemy import Column, String
else:
    from beanie import Document
```

**After (Static):**
```python
# Static import for SQLAlchemy backend
from sqlalchemy import Column, String
```

## Development

### Adding New Backend Types

1. **Update BackendProcessor** with new backend logic
2. **Add configuration options** in CLI
3. **Create backend-specific content generators**
4. **Update test suite**

### Adding New Template Types

1. **Define configuration schema** in BackendProcessor
2. **Create template-specific content generators**
3. **Update CLI options**
4. **Add test cases**

## Troubleshooting

### Common Issues

1. **Missing dependencies**: Check requirements.txt generation
2. **Wrong backend configuration**: Verify BackendProcessor settings
3. **Conditional logic in templates**: Ensure all templates are static

### Debug Mode

Enable debug logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

processor = BackendProcessor(template_path, target_path)
processor.process_template(config)
```

## API Reference

### BackendProcessor

- `__init__(template_path, target_path)` - Initialize processor
- `process_template(config)` - Process template with configuration
- `BackendProcessorError` - Exception for processing errors

### Configuration Options

| Option | Type | Description |
|--------|------|-------------|
| `template_type` | string | Type of template (minimal, api_only, fullstack) |
| `backend` | string | Database backend (sqlalchemy, beanie) |
| `include_auth` | boolean | Include authentication features |
| `include_database` | boolean | Include database configuration |
| `include_docker` | boolean | Include Docker configuration |
| `include_tests` | boolean | Include test files |