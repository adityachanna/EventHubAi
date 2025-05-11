"""
Script to start the integrated EventHub AI FastAPI server.

Usage:
    python run_integrated.py [--host HOST] [--port PORT] [--reload]

Options:
    --host HOST     Host to listen on, default is 0.0.0.0 (all interfaces)
    --port PORT     Port to listen on, default is 8000
    --reload        Whether to reload the server on file changes (development mode)

Examples:
    # Run in development mode with auto-reload
    python run_integrated.py --reload
    
    # Run in production mode on a specific host and port
    python run_integrated.py --host 127.0.0.1 --port 5000
"""

import argparse
import uvicorn

def main():
    parser = argparse.ArgumentParser(description="Start the integrated EventHub AI server.")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Host to listen on")
    parser.add_argument("--port", type=int, default=8000, help="Port to listen on")
    parser.add_argument("--reload", action="store_true", help="Reload on file changes")
    
    args = parser.parse_args()
    
    print(f"Starting EventHub AI server on {args.host}:{args.port}")
    print(f"{'Development' if args.reload else 'Production'} mode")
    print(f"API documentation available at http://{args.host}:{args.port}/docs")
    
    uvicorn.run(
        "main_integrated:app",
        host=args.host,
        port=args.port,
        reload=args.reload
    )

if __name__ == "__main__":
    main()
