# Mandi Saathi - Hackathon Quick Guide

## 🚀 Quick Start (5 minutes)

```bash
# 1. Setup
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python setup.py

# 2. Add API Key
# Edit .env file and add: OPENAI_API_KEY=sk-your-key-here

# 3. Run
streamlit run app.py
```

## 🎯 Demo Scenarios

### Scenario 1: Good Deal (English)
**Input:** "I have 10 quintals of onions, trader offering 2500 per quintal, I'm in Nashik"
**Expected:** System should recognize this as a good deal if market price is around 2500-2600

### Scenario 2: Bad Deal (Hinglish)
**Input:** "Mera 5 quintal tamatar hai, trader 1500 bol raha hai, Ballia mandi mein hoon"
**Expected:** System should identify low offer and suggest counter-offer around 2400-2600

### Scenario 3: Fair Deal (Hindi Romanized)
**Input:** "Bhai mere paas 20 quintal aalu hai, 1800 ka rate mil raha hai, Agra mein"
**Expected:** System should analyze and provide balanced advice

## 🎨 Demo Tips

### 1. Show Multilingual Capability
- Start with English query
- Follow with Hinglish
- Show romanized Hindi response matching

### 2. Highlight Key Features
- **Real-time prices**: Point out modal price from data.gov.in
- **Smart analysis**: Show percentage calculation
- **Practical advice**: Emphasize specific numbers and talking points
- **Chat history**: Demonstrate sidebar with previous conversations
- **Beautiful design**: Highlight the "Harvest Clarity" warm, earthy aesthetic

### 3. Explain the AI Agents
- **Agent 1**: "Extracts location and fetches prices"
- **Agent 2**: "Analyzes deal and creates strategy"
- **Agent 3**: "Delivers advice in farmer's language"

## 🐛 Quick Fixes

### If API fails:
- System has fallback to cached data
- Will try nearby markets automatically
- Show this resilience in demo

### If response is slow:
- First query initializes agents (30-60 seconds)
- Subsequent queries are faster
- Mention this is optimizable with better hosting

### If language detection fails:
- System defaults to English
- Can be improved with more training data
- Still functional for demo

## 📊 Presentation Points

### Problem Statement
"Farmers lose 15-20% of income due to information asymmetry in mandis"

### Solution
"AI-powered negotiation assistant that provides real-time market intelligence in farmer's own language"

### Innovation
1. **Three-agent architecture** for specialized tasks
2. **Multilingual NLP** handling Hindi/Hinglish/English
3. **Real-time data** from government APIs
4. **Practical advice** with specific numbers

### Impact
- Empowers 100M+ Indian farmers
- Reduces information gap
- Increases farmer income
- Accessible via simple chat interface

### Tech Stack Highlights
- **CrewAI**: Multi-agent orchestration
- **GPT-4**: Natural language understanding
- **Streamlit**: Rapid UI development
- **SQLite**: Lightweight data persistence
- **data.gov.in**: Official price data

## 🎤 Demo Script (3 minutes)

**[0:00-0:30] Introduction**
"Mandi Saathi helps farmers negotiate fair prices using AI. Let me show you..."

**[0:30-1:30] Live Demo**
1. Type Hinglish query: "Mera 5 quintal tamatar hai, trader 1500 bol raha hai, Ballia mein"
2. Show processing (agents working)
3. Highlight response in same language
4. Point out specific numbers and advice

**[1:30-2:00] Show Features**
1. Click sidebar to show chat history
2. Start new conversation
3. Try English query to show language flexibility

**[2:00-2:30] Explain Architecture**
Show diagram or explain:
- Price Discovery Agent → Negotiation Strategist → Communicator
- Real-time API integration
- Caching for performance

**[2:30-3:00] Impact & Future**
- Current: Works for major crops and states
- Future: Voice support, SMS, more languages
- Impact: Empowering millions of farmers

## 🏆 Judging Criteria Alignment

### Innovation (25%)
- Novel three-agent architecture
- Multilingual NLP for rural context
- Real-time government data integration

### Technical Implementation (25%)
- Clean, modular code structure
- Proper error handling and fallbacks
- Database design for scalability
- Agent orchestration with CrewAI

### User Experience (25%)
- Simple chat interface with beautiful design
- No learning curve
- Language flexibility
- Clear, actionable advice
- Warm, trustworthy aesthetic inspired by agriculture

### Social Impact (25%)
- Addresses real farmer problem
- Accessible to rural users
- Scalable solution
- Measurable impact on income

## 🔧 Last-Minute Checklist

- [ ] .env file has valid OPENAI_API_KEY
- [ ] Database initialized (run setup.py)
- [ ] Test with all three demo scenarios
- [ ] Prepare backup responses (screenshots)
- [ ] Have architecture diagram ready
- [ ] Know your impact numbers
- [ ] Practice 3-minute pitch
- [ ] Test on presentation laptop
- [ ] Have fallback plan if internet fails

## 💡 Backup Plan (No Internet)

If demo environment has no internet:
1. Show pre-recorded video
2. Use screenshots of successful runs
3. Walk through code architecture
4. Explain caching mechanism
5. Show database schema

## 🎯 Key Messages

1. **Simple**: "Just chat like you're talking to a friend"
2. **Smart**: "AI agents work together to analyze your deal"
3. **Practical**: "Get specific numbers, not vague advice"
4. **Accessible**: "Works in Hindi, English, or Hinglish"
5. **Impactful**: "Helps farmers earn 15-20% more"

## 📞 Q&A Preparation

**Q: How accurate are the prices?**
A: We use official data.gov.in API, updated daily. Plus we show neighboring markets for comparison.

**Q: What if farmer doesn't have smartphone?**
A: Future: SMS integration, voice calls, or village kiosk model.

**Q: How do you handle regional languages?**
A: Currently Hindi/English/Hinglish. Architecture supports adding more languages easily.

**Q: What about internet connectivity in villages?**
A: Caching allows offline operation. Can work with intermittent connectivity.

**Q: How do you monetize?**
A: Freemium model: Basic free, premium features for cooperatives/FPOs.

**Q: Scalability?**
A: Stateless architecture, can scale horizontally. Database can move to PostgreSQL/MongoDB.

## 🚀 Good Luck!

Remember:
- **Confidence**: You built something real and useful
- **Clarity**: Explain simply, avoid jargon
- **Passion**: Show you care about farmer welfare
- **Preparation**: Practice your demo multiple times

**You've got this! 🌾**
