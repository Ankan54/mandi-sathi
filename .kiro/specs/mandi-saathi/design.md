# Design Document

## Overview

Mandi Saathi is a multi-agent chat-based system that provides farmers with intelligent negotiation assistance for agricultural produce sales. The system employs three specialized AI agents working in a coordinated pipeline: Price Discovery Agent for market data retrieval, Negotiation Strategist Agent for deal analysis, and Communicator Agent for farmer-friendly response generation.

The architecture follows a microservices pattern with agent orchestration, real-time data processing, and multilingual natural language understanding capabilities.

## Architecture

The system uses a layered architecture with the following components:

### Presentation Layer
- **Streamlit Web Interface**: Single-page chat application providing real-time farmer interaction
- **Chat Handler**: Manages conversation flow and user session state
- **Session Manager**: Handles unique session ID generation and chat history persistence
- **History Display**: Shows previous chat sessions retrieved from database
- **Response Formatter**: Ensures consistent message display and formatting

### Agent Orchestration Layer
- **CrewAI Framework**: Coordinates the three-agent workflow with defined roles and responsibilities
- **Agent Manager**: Handles agent lifecycle, communication, and error recovery
- **Workflow Controller**: Manages the sequential execution of Price Discovery → Negotiation Strategy → Communication

### Business Logic Layer
- **Price Discovery Agent**: Extracts location/commodity data and fetches market prices
- **Negotiation Strategist Agent**: Analyzes deals and generates strategic recommendations
- **Communicator Agent**: Adapts responses to farmer's language and communication style

### Data Access Layer
- **API Gateway**: Manages external calls to data.gov.in with rate limiting and retry logic
- **Cache Manager**: SQLite-based caching for market prices and location data
- **Session Repository**: Handles chat history storage and retrieval with unique session IDs
- **Data Validator**: Ensures data quality and handles API response validation

### External Integrations
- **Data.gov.in API**: Official government source for daily mandi prices
- **OpenAI API**: Large language model for natural language processing and generation

## Components and Interfaces

### Price Discovery Agent
```python
class PriceDiscoveryAgent:
    def extract_deal_details(self, farmer_message: str) -> DealDetails
    def validate_location(self, state: str, district: str) -> LocationData
    def fetch_market_prices(self, location: LocationData, commodity: str) -> PriceData
    def normalize_commodity_name(self, commodity: str) -> str
```

**Tools:**
- `get_districts_for_state(state_name: str) -> List[District]`
- `fetch_mandi_prices(state: str, district: str, commodity: str) -> PriceRecords`

### Negotiation Strategist Agent
```python
class NegotiationStrategistAgent:
    def analyze_deal(self, offered_price: float, market_data: PriceData) -> DealAnalysis
    def calculate_price_difference(self, offered: float, market: float) -> float
    def generate_counter_offer(self, analysis: DealAnalysis) -> NegotiationStrategy
    def determine_walk_away_price(self, market_data: PriceData) -> float
```

### Communicator Agent
```python
class CommunicatorAgent:
    def detect_language(self, farmer_message: str) -> LanguageInfo
    def match_communication_style(self, farmer_message: str) -> StyleProfile
    def generate_response(self, strategy: NegotiationStrategy, style: StyleProfile) -> str
    def format_final_advice(self, response: str) -> FormattedAdvice

### Session Manager
```python
class SessionManager:
    def generate_session_id(self) -> str  # timestamp-based unique ID
    def store_chat_history(self, session_id: str, user_message: str, assistant_response: str) -> None
    def retrieve_chat_history(self, session_id: str) -> List[ChatMessage]
    def get_all_sessions(self) -> List[SessionSummary]
```

### Data Models

```python
@dataclass
class DealDetails:
    state: str
    district: str
    commodity: str
    quantity: float
    offered_price: float
    unit: str

@dataclass
class PriceData:
    modal_price: float
    min_price: float
    max_price: float
    neighboring_prices: List[DistrictPrice]
    last_updated: datetime

@dataclass
class NegotiationStrategy:
    deal_assessment: str  # "good" | "fair" | "bad"
    counter_offer: float
    walk_away_price: float
    max_concession: float
    talking_points: List[str]
    justification: str

@dataclass
class FormattedAdvice:
    response_text: str
    language: str
    counter_offer_amount: float
    key_reason: str

@dataclass
class ChatMessage:
    user_message: str
    assistant_response: str
    timestamp: datetime

@dataclass
class SessionSummary:
    session_id: str
    first_message: str
    last_updated: datetime
    message_count: int
```

## Data Models

### Database Schema (SQLite)

```sql
-- Market prices cache
CREATE TABLE market_prices (
    id INTEGER PRIMARY KEY,
    state TEXT NOT NULL,
    district TEXT NOT NULL,
    commodity TEXT NOT NULL,
    modal_price REAL,
    min_price REAL,
    max_price REAL,
    variety TEXT,
    grade TEXT,
    market_date DATE,
    cached_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Location validation cache
CREATE TABLE districts (
    id INTEGER PRIMARY KEY,
    state TEXT NOT NULL,
    district TEXT NOT NULL,
    normalized_name TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Conversation history with enhanced structure
CREATE TABLE chat_sessions (
    session_id TEXT PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    first_message TEXT,
    message_count INTEGER DEFAULT 0
);

CREATE TABLE chat_messages (
    id INTEGER PRIMARY KEY,
    session_id TEXT NOT NULL,
    user_message TEXT NOT NULL,
    assistant_response TEXT NOT NULL,
    chat_data JSON, -- stores full conversation as {"user": "...", "assistant": "..."}
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES chat_sessions(session_id)
);
```

### API Integration Models

```python
# Data.gov.in API Response Structure
@dataclass
class MandiPriceRecord:
    state: str
    district: str
    market: str
    commodity: str
    variety: str
    grade: str
    min_price: str
    max_price: str
    modal_price: str
    price_date: str
```
## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system-essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

After reviewing all testable properties from the prework analysis, the following properties provide unique validation value:

**Property 1: Multilingual input processing**
*For any* farmer message in Hindi, English, Hinglish, or regional languages, the system should process the input without errors and extract available information
**Validates: Requirements 1.1, 1.2**

**Property 2: Information extraction consistency**
*For any* farmer message containing location and commodity details, the system should extract the same information regardless of informal phrasing or spelling variations
**Validates: Requirements 1.3, 1.5**

**Property 3: Graceful handling of incomplete data**
*For any* farmer message with missing information, the system should continue processing without errors and make reasonable assumptions based on available data
**Validates: Requirements 1.4**

**Property 4: Location validation consistency**
*For any* state and district combination, validation against official records should always return the same result for the same input
**Validates: Requirements 2.1**

**Property 5: Commodity normalization consistency**
*For any* commodity name with spelling variations, normalization should always produce the same standard name for equivalent inputs
**Validates: Requirements 2.3**

**Property 6: Price data completeness**
*For any* successful price retrieval, the response should always include modal price, min price, max price, and neighboring district data
**Validates: Requirements 2.2, 2.4**

**Property 7: Percentage calculation accuracy**
*For any* offered price and market price combination, the percentage difference calculation should be mathematically correct and consistent
**Validates: Requirements 3.1**

**Property 8: Deal classification consistency**
*For any* price difference percentage, the deal classification (good/fair/bad) should be consistent across similar percentage ranges
**Validates: Requirements 3.2**

**Property 9: Strategy completeness**
*For any* negotiation analysis, the strategy should always include counter-offer amount, walk-away price, max concession, and justification
**Validates: Requirements 3.3, 3.4**

**Property 10: Language matching consistency**
*For any* farmer input, the response language should always match the detected input language
**Validates: Requirements 4.1, 4.3**

**Property 11: Response length constraint**
*For any* system response, the text should contain no more than five sentences
**Validates: Requirements 4.4**

**Property 12: Advice completeness**
*For any* negotiation advice response, it should always include specific counter-offer amount, asking price, minimum price, talking points, and justification reason
**Validates: Requirements 5.1, 5.2, 5.3, 5.4**

**Property 13: Single interaction completeness**
*For any* farmer message, the system should provide a complete response without requiring additional interactions
**Validates: Requirements 5.5**

**Property 14: Error handling robustness**
*For any* network failure or API error, the system should handle the error gracefully without crashing and provide meaningful fallback responses
**Validates: Requirements 6.2**

**Property 15: Cache behavior consistency**
*For any* retrieved market data, the system should store it in the SQLite cache and retrieve cached data for subsequent identical requests within the cache validity period
**Validates: Requirements 6.3, 6.4**

**Property 16: Real-time processing**
*For any* farmer message input, the system should begin processing immediately without requiring form submissions or additional user actions
**Validates: Requirements 7.2**

**Property 17: Context preservation**
*For any* conversation session, sending multiple messages should maintain conversation history and context across all interactions
**Validates: Requirements 7.4**

**Property 18: Chat history persistence**
*For any* chat interaction, the system should store the conversation in the database with a unique timestamp-based session ID and JSON format containing user and assistant messages
**Validates: Requirements 6.6**

**Property 19: Chat history retrieval**
*For any* stored chat session, the frontend should be able to retrieve and display the complete chat history from the database
**Validates: Requirements 6.7**

## Error Handling

### Input Validation Errors
- **Invalid Location**: When state/district cannot be validated, system falls back to nearest available markets
- **Unrecognized Commodity**: System attempts fuzzy matching and provides suggestions for similar commodities
- **Missing Price Data**: System uses cached data or nearby market prices with clear disclaimers

### API Integration Errors
- **Network Timeouts**: Implement exponential backoff with maximum 3 retry attempts
- **Rate Limiting**: Queue requests and implement request throttling to stay within API limits
- **Invalid API Responses**: Validate response structure and handle malformed data gracefully

### Agent Processing Errors
- **Language Detection Failures**: Default to English with multilingual fallback capabilities
- **Price Analysis Errors**: Provide conservative advice when market analysis is uncertain
- **Response Generation Failures**: Use template-based fallback responses

### Database Errors
- **Cache Unavailable**: Continue with direct API calls and log cache issues
- **Data Corruption**: Implement data integrity checks and cache refresh mechanisms
- **Storage Limits**: Implement automatic cleanup of old cached data

## Testing Strategy

### Unit Testing Approach
Unit tests will focus on individual component functionality:
- **Agent Tools**: Test each tool function (get_districts_for_state, fetch_mandi_prices) with mock data
- **Data Validation**: Test location validation, commodity normalization, and price calculation functions
- **Response Formatting**: Test language detection, style matching, and response generation
- **Database Operations**: Test cache storage, retrieval, and cleanup operations
- **Session Management**: Test session ID generation, chat history storage, and retrieval operations
- **API Integration**: Test request formatting, response parsing, and error handling

### Property-Based Testing Approach
Property-based tests will verify universal behaviors across all inputs using **Hypothesis** for Python:
- **Minimum 100 iterations** per property test to ensure comprehensive coverage
- **Smart generators** that create realistic farmer messages, location data, and price scenarios
- **Invariant testing** to ensure system behavior remains consistent across input variations
- **Round-trip testing** for data serialization and API request/response cycles

Each property-based test will be tagged with comments referencing the specific correctness property:
```python
# **Feature: mandi-saathi, Property 1: Multilingual input processing**
def test_multilingual_input_processing(farmer_message):
    # Test implementation
```

### Integration Testing
- **End-to-End Workflow**: Test complete farmer message → price discovery → strategy → response cycle
- **API Integration**: Test actual data.gov.in API calls with real data
- **Database Integration**: Test cache operations and chat history storage with actual SQLite database
- **Session Management**: Test session creation, history storage, and retrieval across multiple interactions
- **Agent Coordination**: Test CrewAI workflow execution and agent communication

### Performance Testing
- **Response Time**: Ensure complete workflow completes within 10 seconds
- **Concurrent Users**: Test system behavior with multiple simultaneous farmer requests
- **Cache Efficiency**: Verify cache hit rates and performance improvements
- **Memory Usage**: Monitor memory consumption during extended operation

The testing strategy emphasizes both concrete examples through unit tests and universal correctness through property-based testing, ensuring comprehensive validation of system behavior.