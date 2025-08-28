# Zulu AI App Builder Service

## Overview

This is a FastAPI-based service that generates structured app starter code based on user-provided app ideas. The service analyzes natural language descriptions of app concepts and automatically creates complete project scaffolding with appropriate files, structure, and boilerplate code. It uses pattern matching to identify common app types (todo, blog, ecommerce, etc.) and generates corresponding code templates using Jinja2 templating engine.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Backend Framework
- **FastAPI**: Chosen for its automatic API documentation, type validation, and async support
- **Pydantic Models**: Used for request/response validation and data structure definition
- **CORS Middleware**: Configured to allow cross-origin requests for frontend integration

### Code Generation Engine
- **Pattern Matching System**: Maps user descriptions to predefined app types (todo, blog, ecommerce, social, dashboard, portfolio, calculator, weather, note)
- **Template Engine**: Jinja2 used for generating code files from templates with dynamic content injection
- **Metadata Extraction**: Analyzes app ideas to determine app type, required features, database needs, and API structure

### Data Models
- **AppIdeaRequest**: Input validation for user app ideas (5-1000 characters) with optional complexity level
- **GeneratedFile**: Represents individual code files with path, content, and type information
- **GeneratedAppResponse**: Complete response structure including success status, files, and directory structure
- **AppMetadata**: Internal model for storing extracted app characteristics

### API Design
- **RESTful Structure**: Single primary endpoint `/generate_app` for code generation
- **Health Check**: Root endpoint for service monitoring
- **Error Handling**: HTTP exceptions for invalid requests with appropriate status codes

### Template System
- **File-based Templates**: Templates stored in `/templates` directory for code generation
- **Multiple File Types**: Support for Python, JavaScript, HTML, and Markdown file generation
- **Dynamic Content**: Template variables populated based on analyzed app metadata

## External Dependencies

### Core Libraries
- **FastAPI**: Web framework for building APIs
- **Pydantic**: Data validation and settings management
- **Jinja2**: Template engine for code generation
- **uvicorn**: ASGI server for running the FastAPI application (implied)

### Development Tools
- **Python Logging**: Built-in logging for request tracking and debugging
- **Type Hints**: Extensive use of Python typing for code clarity and IDE support

### Template Storage
- **File System**: Templates stored locally in `/templates` directory
- **No Database**: Current architecture is stateless with no persistent storage requirements

Note: The service is designed to be lightweight and stateless, focusing on rapid code generation without requiring complex infrastructure or external service dependencies.