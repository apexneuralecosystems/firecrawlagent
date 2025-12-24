# Backend Troubleshooting Guide

## Common Issues and Solutions

### Error: "Can't patch loop of type <class 'uvloop.Loop'>"

**Problem**: This error occurs when `nest_asyncio` tries to patch a `uvloop` event loop. `nest_asyncio` only works with standard asyncio loops.

**Solution**: The backend is configured to use standard asyncio instead of uvloop. This is already set in:
- `main.py` - Sets `loop="asyncio"` in uvicorn.run()
- `run.sh` - Uses `--loop asyncio` flag
- `run_dev.sh` - Uses `--loop asyncio` flag

**Why**: `nest_asyncio` is only needed for Streamlit (which runs in a synchronous context). FastAPI is fully async and doesn't need it.

### Error: "Attribute 'app' not found in module 'main'"

**Problem**: When running `python main.py` directly, uvicorn can't find the app.

**Solution**: Use one of these methods:
1. Run from project root: `uvicorn backend.main:app --reload`
2. Use the script: `./backend/run.sh`
3. The direct `python main.py` now passes the app object directly

### Import Errors

**Problem**: Module not found errors when importing from parent directory.

**Solution**: 
- Make sure you've installed all dependencies from root: `pip install -r requirements.txt`
- The backend adds the project root to `sys.path` automatically
- Run from the correct directory

### CORS Errors

**Problem**: Frontend can't connect to backend.

**Solution**: 
- Check CORS origins in `main.py` match your frontend URL
- Default includes: localhost:3000, localhost:5173
- Add your frontend URL if different

## Best Practices

1. **Always run backend from project root** when using uvicorn directly:
   ```bash
   uvicorn backend.main:app --reload
   ```

2. **Use the scripts** for convenience:
   ```bash
   ./backend/run.sh        # Production
   ./backend/run_dev.sh    # Development with reload
   ```

3. **Check environment variables**:
   ```bash
   echo $FIRECRAWL_API_KEY
   echo $OPENROUTER_API_KEY
   ```

4. **Verify API is running**:
   ```bash
   curl http://localhost:8000/api/health
   ```

