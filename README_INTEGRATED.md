# EventHub AI - Integrated API

This integrated API combines all the AI features of EventHub into a single FastAPI application:

1. **Chat Summary** - Summarize chat histories
2. **Search Agent** - Research and search capabilities
3. **Recommendation** - Event recommendations based on user preferences
4. **Dynamic Pricing** - Price adjustments based on user metadata clustering

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd eventhub-ai

# Install dependencies
pip install -r requirements.txt
```

## Running the Integrated Application

You can run the integrated API using the provided script:

```bash
# Run in development mode with auto-reload
python run_integrated.py --reload

# Run in production mode
python run_integrated.py
```

By default, the server will run on all interfaces (0.0.0.0) on port 8000.

## API Endpoints

The integrated API includes the following key endpoints:

- **Chat Summary**: `/chat/...`
- **Search Agent**: `/research/...`
- **Recommendation**: `/recommendation/...`
- **Dynamic Pricing**: `/pricing/adjust-price`

## Testing

You can test the integrated API using the provided test script:

```bash
python test_integrated.py
```

This script will test the Dynamic Pricing feature with different user profiles.

## API Documentation

The API documentation is available at:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Integration Details

This application integrates multiple AI features into a single FastAPI application:

1. The main API structure is defined in `main_integrated.py`
2. Each feature is organized into its own module with clear separation of concerns
3. All API routes are exposed under a single FastAPI instance

## Original Components

- The chat summary, search agent, and recommendation features were originally part of the eventhub-ai application
- The dynamic pricing feature was originally part of the backend application
- All features have been integrated into a unified API structure without modifying their core functionality
