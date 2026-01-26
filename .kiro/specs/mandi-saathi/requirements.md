# Requirements Document

## Introduction

Mandi Saathi is a chat-based negotiation assistant that helps farmers get fair prices for their produce in mandis (agricultural markets). The system uses three AI agents working together to understand the farmer's situation, fetch real market prices, create negotiation strategy, and respond in the farmer's own language.

## Glossary

- **Mandi_Saathi_System**: The complete chat-based negotiation assistant application
- **Price_Discovery_Agent**: AI agent responsible for extracting location and commodity details and fetching market prices
- **Negotiation_Strategist_Agent**: AI agent that analyzes deals and creates actionable negotiation advice
- **Communicator_Agent**: AI agent that delivers responses to farmers in their own language and style
- **Farmer**: User of the system who needs assistance with produce price negotiations
- **Trader**: Market participant offering to buy produce from farmers
- **Mandi**: Agricultural wholesale market where farmers sell their produce
- **Modal_Price**: The most frequently occurring price in the market
- **Quintal**: Unit of measurement equal to 100 kilograms, commonly used for agricultural produce

## Requirements

### Requirement 1

**User Story:** As a farmer, I want to describe my deal situation in natural language, so that I can get negotiation assistance without learning complex interfaces.

#### Acceptance Criteria

1. WHEN a farmer sends a message describing their deal situation, THE Mandi_Saathi_System SHALL accept input in Hindi, English, Hinglish, or regional languages
2. WHEN a farmer uses romanized Hindi text, THE Mandi_Saathi_System SHALL process and understand the input correctly
3. WHEN a farmer mentions location and commodity details informally, THE Mandi_Saathi_System SHALL extract the relevant information accurately
4. WHEN a farmer provides incomplete information, THE Mandi_Saathi_System SHALL work with available data and make reasonable assumptions
5. WHEN processing farmer input, THE Mandi_Saathi_System SHALL handle spelling variations and colloquial terms correctly

### Requirement 2

**User Story:** As a farmer, I want accurate current market prices for my commodity, so that I can make informed negotiation decisions.

#### Acceptance Criteria

1. WHEN the Price_Discovery_Agent receives location and commodity information, THE Price_Discovery_Agent SHALL validate state and district names against official data.gov.in records
2. WHEN fetching market prices, THE Price_Discovery_Agent SHALL retrieve current and recent prices from the specified mandi and nearby markets
3. WHEN commodity names have spelling variations, THE Price_Discovery_Agent SHALL normalize them to standard names for API queries
4. WHEN price data is retrieved, THE Price_Discovery_Agent SHALL return modal price, minimum price, maximum price, and prices from neighboring districts
5. WHEN API data is unavailable for a specific location, THE Price_Discovery_Agent SHALL fetch prices from the nearest available markets

### Requirement 3

**User Story:** As a farmer, I want strategic negotiation advice based on market analysis, so that I can maximize my profit from produce sales.

#### Acceptance Criteria

1. WHEN the Negotiation_Strategist_Agent receives offered price and market data, THE Negotiation_Strategist_Agent SHALL calculate the percentage difference between offered price and market rate
2. WHEN analyzing a deal, THE Negotiation_Strategist_Agent SHALL classify the offer as good, fair, or bad based on market comparison
3. WHEN generating counter-offers, THE Negotiation_Strategist_Agent SHALL provide specific amounts with clear justification
4. WHEN determining negotiation strategy, THE Negotiation_Strategist_Agent SHALL calculate walk-away price and maximum acceptable concession
5. WHEN considering deal factors, THE Negotiation_Strategist_Agent SHALL account for variety differences, grade quality, quantity discounts, and market urgency

### Requirement 4

**User Story:** As a farmer, I want responses in my own language and communication style, so that I can easily understand and act on the advice.

#### Acceptance Criteria

1. WHEN the Communicator_Agent prepares responses, THE Communicator_Agent SHALL match the farmer's input language automatically
2. WHEN responding to farmers, THE Communicator_Agent SHALL maintain the same tone and formality level as the farmer's input
3. WHEN farmers use romanized Hindi, THE Communicator_Agent SHALL respond in the same romanized format
4. WHEN delivering advice, THE Communicator_Agent SHALL keep responses concise with maximum five sentences
5. WHEN providing recommendations, THE Communicator_Agent SHALL avoid technical jargon and use simple, practical language

### Requirement 5

**User Story:** As a farmer, I want specific actionable advice with clear numbers, so that I know exactly what to say and do during negotiations.

#### Acceptance Criteria

1. WHEN providing negotiation advice, THE Mandi_Saathi_System SHALL include specific counter-offer amounts in the response
2. WHEN recommending strategy, THE Mandi_Saathi_System SHALL provide simple talking points the farmer can use with traders
3. WHEN delivering final advice, THE Mandi_Saathi_System SHALL clearly state the recommended asking price and minimum acceptable price
4. WHEN explaining recommendations, THE Mandi_Saathi_System SHALL provide one clear reason the farmer can share with the trader
5. WHEN processing requests, THE Mandi_Saathi_System SHALL complete the entire analysis and response cycle within a single chat interaction

### Requirement 6

**User Story:** As a system administrator, I want reliable data integration with government APIs, so that farmers receive accurate and up-to-date market information.

#### Acceptance Criteria

1. WHEN accessing market data, THE Mandi_Saathi_System SHALL integrate with data.gov.in API using Resource ID 35985678-0d79-46b4-9ed6-6f13308a1d24
2. WHEN API calls are made, THE Mandi_Saathi_System SHALL handle network failures gracefully and provide fallback responses
3. WHEN storing retrieved data, THE Mandi_Saathi_System SHALL cache market prices in SQLite database for performance optimization
4. WHEN data becomes stale, THE Mandi_Saathi_System SHALL refresh cached prices automatically based on configured intervals
5. WHEN API responses are received, THE Mandi_Saathi_System SHALL validate data completeness before processing
6. The chat history of each sessions to be stored in database against an unique session id which will comprise of timestamp upto milliseconds. the chat history will be stored as json as user and assistant key.
7. the frontend will show the chat history sessions from DB

### Requirement 7

**User Story:** As a farmer, I want to interact through a simple chat interface, so that I can get help without technical complexity.

#### Acceptance Criteria

1. WHEN farmers access the application, THE Mandi_Saathi_System SHALL present a single chat interface without requiring navigation
2. WHEN farmers type messages, THE Mandi_Saathi_System SHALL process input in real-time without requiring form submissions
3. WHEN displaying responses, THE Mandi_Saathi_System SHALL show advice clearly formatted for easy reading
4. WHEN farmers send new messages, THE Mandi_Saathi_System SHALL maintain conversation context for follow-up questions
5. WHEN the interface loads, THE Mandi_Saathi_System SHALL be ready to accept farmer input immediately without setup steps