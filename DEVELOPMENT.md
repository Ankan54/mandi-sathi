# Mandi Saathi - Development Guide

## Project Structure

```
mandi-saathi/
├── agents/                    # AI agents
│   ├── price_discovery_agent.py
│   ├── negotiation_strategist_agent.py
│   ├── communicator_agent.py
│   └── crew_manager.py       # Orchestrates all agents
├── tools/                     # Agent tools
│   ├── location_tools.py     # State/district validation
│   └── price_tools.py        # Price fetching and normalization
├── database/                  # Data persistence
│   ├── db_manager.py         # SQLite connection manager
│   ├── session_manager.py    # Chat history management
│   ├── cache_manager.py      # Price caching
│   └── schema.sql            # Database schema
├── utils/                     # Utilities
│   ├── api_client.py         # data.gov.in API client
│   └── price_service.py      # Price service with fallback
├── app.py                     # Streamlit frontend
├── config.py                  # Configuration management
├── requirements.txt           # Python dependencies
├── setup.py                   # Setup script
└── test_setup.py             # Verification tests
```

## Architecture

### Three-Agent System

1. **Price Discovery Agent**
   - Extracts location and commodity from farmer's message
   - Handles Hindi/Hinglish/English input
   - Validates locations against official data
   - Fetches current market prices
   - Gets neighboring district prices

2. **Negotiation Strategist Agent**
   - Analyzes offered price vs market rate
   - Calculates percentage differences
   - Classifies deals (good/fair/bad)
   - Generates counter-offers
   - Provides walk-away prices

3. **Communicator Agent**
   - Matches farmer's language and tone
   - Delivers advice in simple terms
   - Keeps responses concise (max 5 sentences)
   - Includes specific numbers and talking points

### Data Flow

```
Farmer Message
    ↓
Price Discovery Agent (extracts info + fetches prices)
    ↓
Negotiation Strategist Agent (analyzes + creates strategy)
    ↓
Communicator Agent (formats response in farmer's language)
    ↓
Response to Farmer
```

### Database Schema

**market_prices**: Caches price data from API
**districts**: Stores validated location data
**chat_sessions**: Tracks conversation sessions
**chat_messages**: Stores individual messages with JSON format

## Key Features

### Multilingual Support
- Detects Hindi, English, Hinglish automatically
- Handles romanized Hindi (e.g., "tamatar" for tomato)
- Matches farmer's tone (formal/casual)

### Price Intelligence
- Real-time data from data.gov.in API
- Caching for performance (24-hour validity)
- Fallback to nearby markets if data unavailable
- Neighboring district price comparison

### Smart Negotiation
- Percentage-based deal classification
- Counter-offer calculation (90-95% of modal price)
- Walk-away price (minimum 80% of modal)
- Contextual factors (variety, grade, quantity)

### Chat History
- Unique timestamp-based session IDs
- JSON storage format
- Sidebar display of previous conversations
- Session persistence across page refreshes

## Configuration

### Environment Variables (.env)

```
OPENAI_API_KEY=sk-...          # Required
DATA_GOV_API_KEY=              # Optional
DATABASE_PATH=mandi_saathi.db  # Default
CACHE_VALIDITY_HOURS=24        # Default
```

### Agent Configuration (config.py)

```python
AGENT_MODEL = "gpt-4"          # LLM model
AGENT_TEMPERATURE = 0.7        # Response creativity
DATA_GOV_RESOURCE_ID = "35985678-0d79-46b4-9ed6-6f13308a1d24"
```

## Testing

### Run Verification Tests
```bash
python test_setup.py
```

Tests include:
- Module imports
- Database initialization
- Session management
- Agent tools

### Manual Testing

Test with various inputs:

**English:**
"I have 5 quintals of tomatoes, trader is offering 1500, I'm in Ballia, UP"

**Hinglish:**
"Mera 5 quintal tamatar hai, trader 1500 bol raha hai, Ballia mandi mein hoon"

**Hindi (romanized):**
"Bhai mere paas 10 quintal pyaz hai, 2000 ka bhav mil raha hai, Nashik mein"

## Troubleshooting

### Common Issues

**1. Import Errors**
```bash
pip install -r requirements.txt
```

**2. Database Errors**
```bash
rm mandi_saathi.db
python setup.py
```

**3. API Errors**
- Check OPENAI_API_KEY in .env
- Verify internet connection
- Check API rate limits

**4. CrewAI Errors**
- Ensure crewai version 0.28.8
- Check agent tool definitions
- Verify task context dependencies

### Debug Mode

Enable verbose output in agents:
```python
verbose=True  # Already enabled in all agents
```

## Development Tips

### Adding New Commodities

Edit `tools/price_tools.py`:
```python
COMMODITY_MAPPINGS = {
    "new_hindi_name": "English Name",
    # ...
}
```

### Adding New States/Districts

Edit `tools/location_tools.py`:
```python
INDIAN_STATES = {
    "new_state": ["District1", "District2"],
    # ...
}
```

### Modifying Agent Behavior

Edit agent backstories in:
- `agents/price_discovery_agent.py`
- `agents/negotiation_strategist_agent.py`
- `agents/communicator_agent.py`

### Customizing UI

Edit `app.py`:
- Modify page config
- Change sidebar layout
- Update welcome message
- Adjust chat display

## Performance Optimization

### Caching
- Price data cached for 24 hours
- Streamlit resource caching for DB and crew
- Session state for conversation context

### Database
- Indexes on frequently queried columns
- Automatic cleanup of old cache data
- Connection pooling via db_manager

## Deployment

### Local Development
```bash
streamlit run app.py
```

### Production Deployment

**Option 1: Streamlit Cloud**
1. Push to GitHub
2. Connect to Streamlit Cloud
3. Add secrets (OPENAI_API_KEY)
4. Deploy

**Option 2: Docker**
```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["streamlit", "run", "app.py"]
```

**Option 3: VPS/Cloud Server**
```bash
# Install dependencies
pip install -r requirements.txt

# Run with nohup
nohup streamlit run app.py --server.port 8501 &
```

## Future Enhancements

- [ ] Support for more regional languages
- [ ] Voice input/output
- [ ] SMS integration for feature phones
- [ ] Historical price trends visualization
- [ ] Weather-based price predictions
- [ ] Direct trader connections
- [ ] Mobile app version

## Contributing

For hackathon participants:
1. Focus on core functionality first
2. Test with real farmer scenarios
3. Optimize for speed (hackathon time constraints)
4. Document any API limitations
5. Prepare demo scenarios

## License

[Add your license here]

## Support

For issues or questions:
- Check DEVELOPMENT.md (this file)
- Review test_setup.py output
- Check Streamlit logs
- Verify .env configuration
