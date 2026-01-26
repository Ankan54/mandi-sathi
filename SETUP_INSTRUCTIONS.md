# Mandi Saathi - Setup Instructions

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- OpenAI API key
- Internet connection (for API calls)

## Step-by-Step Setup

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- crewai (0.28.8) - Multi-agent framework
- openai (1.12.0) - OpenAI API client
- streamlit (1.31.0) - Web interface
- requests (2.31.0) - HTTP library
- hypothesis (6.98.0) - Property-based testing
- python-dotenv (1.0.1) - Environment management

### 2. Run Setup Script

```bash
python setup.py
```

This will:
- Create `.env` file if it doesn't exist
- Check if dependencies are installed
- Initialize SQLite database with schema
- Create necessary tables

### 3. Configure Environment Variables

Edit the `.env` file and add your OpenAI API key:

```env
OPENAI_API_KEY=sk-your-actual-api-key-here
DATA_GOV_API_KEY=
DATABASE_PATH=mandi_saathi.db
CACHE_VALIDITY_HOURS=24
```

**Important**: Replace `sk-your-actual-api-key-here` with your real OpenAI API key.

### 4. Verify Setup (Optional but Recommended)

```bash
python test_setup.py
```

This will test:
- ✅ All module imports
- ✅ Database initialization
- ✅ Session management
- ✅ Agent tools

Expected output:
```
🌾 Mandi Saathi Setup Verification

Testing imports...
✅ All imports successful

Testing database...
✅ Database initialized

Testing session manager...
  Generated session ID: 20240126123456789012
✅ Session manager working

Testing tools...
  Location tool: Districts in Uttar Pradesh: Ballia, Varanasi...
  Commodity tool: Normalized 'tamatar' to 'Tomato'
✅ Tools working

==================================================
✅ All tests passed! System is ready.

To start the application:
  streamlit run app.py
==================================================
```

### 5. Run the Application

```bash
streamlit run app.py
```

Or use the quick start scripts:

**Linux/Mac:**
```bash
chmod +x run.sh
./run.sh
```

**Windows:**
```cmd
run.bat
```

### 6. Access the Application

The application will automatically open in your default browser at:
```
http://localhost:8501
```

If it doesn't open automatically, manually navigate to that URL.

## Troubleshooting

### Issue: "ModuleNotFoundError"

**Solution:**
```bash
pip install -r requirements.txt
```

### Issue: "OPENAI_API_KEY not found"

**Solution:**
1. Check if `.env` file exists
2. Open `.env` and verify OPENAI_API_KEY is set
3. Make sure there are no spaces around the `=` sign
4. Restart the application

### Issue: "Database initialization failed"

**Solution:**
```bash
# Delete existing database
rm mandi_saathi.db  # Linux/Mac
del mandi_saathi.db  # Windows

# Re-run setup
python setup.py
```

### Issue: "API request failed"

**Possible causes:**
1. No internet connection
2. Invalid API key
3. API rate limit exceeded
4. data.gov.in API is down

**Solution:**
- Check internet connection
- Verify API key in `.env`
- Wait a few minutes and try again
- System will use cached data as fallback

### Issue: "Streamlit not found"

**Solution:**
```bash
pip install streamlit==1.31.0
```

### Issue: "CrewAI import error"

**Solution:**
```bash
pip install crewai==0.28.8
```

## Getting OpenAI API Key

1. Go to https://platform.openai.com/
2. Sign up or log in
3. Navigate to API Keys section
4. Click "Create new secret key"
5. Copy the key (starts with `sk-`)
6. Paste it in your `.env` file

**Note**: OpenAI API is paid, but new accounts get free credits.

## Project Structure After Setup

```
mandi-saathi/
├── agents/              ✅ Created
├── database/            ✅ Created
├── tools/               ✅ Created
├── utils/               ✅ Created
├── .env                 ✅ Created by setup.py
├── mandi_saathi.db      ✅ Created by setup.py
├── app.py               ✅ Ready to run
└── ...
```

## Verification Checklist

Before running the app, verify:

- [ ] Python 3.8+ installed (`python --version`)
- [ ] All dependencies installed (`pip list | grep crewai`)
- [ ] `.env` file exists and has OPENAI_API_KEY
- [ ] Database file created (`ls mandi_saathi.db`)
- [ ] Test script passes (`python test_setup.py`)

## First Run

When you run the app for the first time:

1. **Initialization**: Takes 10-15 seconds to load
2. **First Query**: Takes 30-60 seconds (agents initialize)
3. **Subsequent Queries**: Much faster (10-20 seconds)

This is normal! The agents need to initialize on first use.

## Demo Mode

For quick demo without API calls:

1. Comment out API calls in `utils/api_client.py`
2. Use mock data in `tools/price_tools.py`
3. Or prepare screenshots of successful runs

## Production Deployment

### Streamlit Cloud

1. Push code to GitHub
2. Go to https://streamlit.io/cloud
3. Connect your repository
4. Add secrets:
   - Key: `OPENAI_API_KEY`
   - Value: Your API key
5. Deploy!

### Docker

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501"]
```

Build and run:
```bash
docker build -t mandi-saathi .
docker run -p 8501:8501 mandi-saathi
```

## Support

If you encounter issues:

1. Check this file (SETUP_INSTRUCTIONS.md)
2. Run `python test_setup.py`
3. Check `.env` configuration
4. Review error messages in terminal
5. Check Streamlit logs

## Quick Commands Reference

```bash
# Setup
python setup.py

# Test
python test_setup.py

# Run
streamlit run app.py

# Quick start (Linux/Mac)
./run.sh

# Quick start (Windows)
run.bat

# Clean database
rm mandi_saathi.db && python setup.py

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

## Success!

If you see the Streamlit interface with "🌾 Mandi Saathi" title, you're all set! 

Try a test message:
```
Mera 5 quintal tamatar hai, trader 1500 bol raha hai, Ballia mandi mein hoon
```

Happy farming! 🌾
