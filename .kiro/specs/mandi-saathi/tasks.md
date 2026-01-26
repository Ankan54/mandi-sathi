# Implementation Plan

- [x] 1. Set up project structure and dependencies


  - Create directory structure: agents/, tools/, database/, frontend/, utils/
  - Set up Python virtual environment
  - Install dependencies: crewai, openai, streamlit, sqlite3, requests, hypothesis
  - Create requirements.txt with all dependencies
  - Initialize SQLite database with schema
  - _Requirements: 6.1, 6.3_

- [ ] 2. Implement database layer and session management
- [x] 2.1 Create database schema and connection utilities

  - Implement SQLite connection manager with connection pooling
  - Create tables: market_prices, districts, chat_sessions, chat_messages
  - Write database initialization script
  - _Requirements: 6.3, 6.6_

- [x] 2.2 Implement session management


  - Create SessionManager class with timestamp-based session ID generation
  - Implement store_chat_history method with JSON format storage
  - Implement retrieve_chat_history and get_all_sessions methods
  - _Requirements: 6.6, 6.7_

- [ ]* 2.3 Write property test for chat history persistence
  - **Property 18: Chat history persistence**
  - **Validates: Requirements 6.6**

- [x] 2.3 Implement cache manager for market prices


  - Create CacheManager class for price data storage and retrieval
  - Implement cache validity checking and automatic refresh logic
  - Add methods for storing and retrieving district validation data
  - _Requirements: 6.3, 6.4_

- [ ]* 2.4 Write property test for cache behavior
  - **Property 15: Cache behavior consistency**
  - **Validates: Requirements 6.3, 6.4**

- [ ] 3. Implement API integration layer
- [x] 3.1 Create data.gov.in API client


  - Implement API client with Resource ID 35985678-0d79-46b4-9ed6-6f13308a1d24
  - Add request formatting and response parsing
  - Implement retry logic with exponential backoff
  - _Requirements: 6.1, 6.2_

- [x] 3.2 Implement error handling and fallback mechanisms


  - Add network failure handling with graceful degradation
  - Implement fallback to cached data when API unavailable
  - Add data validation for API responses
  - _Requirements: 6.2, 6.5_

- [ ]* 3.3 Write property test for error handling robustness
  - **Property 14: Error handling robustness**
  - **Validates: Requirements 6.2**

- [ ] 4. Implement agent tools
- [x] 4.1 Create get_districts_for_state tool


  - Implement function to fetch and validate district names for a given state
  - Add fuzzy matching for state name variations
  - Integrate with cache for performance
  - _Requirements: 2.1_

- [x] 4.2 Create fetch_mandi_prices tool


  - Implement function to fetch prices from data.gov.in API
  - Add commodity name normalization logic
  - Implement nearby market fallback when primary location unavailable
  - _Requirements: 2.2, 2.3, 2.4, 2.5_

- [ ]* 4.3 Write property test for location validation
  - **Property 4: Location validation consistency**
  - **Validates: Requirements 2.1**

- [ ]* 4.4 Write property test for commodity normalization
  - **Property 5: Commodity normalization consistency**
  - **Validates: Requirements 2.3**

- [ ]* 4.5 Write property test for price data completeness
  - **Property 6: Price data completeness**
  - **Validates: Requirements 2.2, 2.4**

- [ ] 5. Implement Price Discovery Agent
- [x] 5.1 Create Price Discovery Agent with CrewAI


  - Define agent with role, goal, backstory
  - Assign get_districts_for_state and fetch_mandi_prices tools
  - Configure agent for information extraction from farmer messages
  - _Requirements: 1.1, 1.2, 1.3, 1.5, 2.1, 2.2_

- [x] 5.2 Implement deal details extraction logic

  - Create parser for extracting state, district, commodity, quantity, offered price
  - Handle multilingual input (Hindi, English, Hinglish)
  - Implement spelling variation handling
  - _Requirements: 1.1, 1.2, 1.3, 1.5_

- [ ]* 5.3 Write property test for multilingual input processing
  - **Property 1: Multilingual input processing**
  - **Validates: Requirements 1.1, 1.2**

- [ ]* 5.4 Write property test for information extraction
  - **Property 2: Information extraction consistency**
  - **Validates: Requirements 1.3, 1.5**

- [ ]* 5.5 Write property test for incomplete data handling
  - **Property 3: Graceful handling of incomplete data**
  - **Validates: Requirements 1.4**

- [ ] 6. Implement Negotiation Strategist Agent
- [x] 6.1 Create Negotiation Strategist Agent with CrewAI


  - Define agent with role, goal, backstory for deal analysis
  - Configure agent to receive price data and generate strategy
  - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5_

- [x] 6.2 Implement deal analysis logic

  - Create function to calculate percentage difference between offered and market price
  - Implement deal classification (good/fair/bad) based on thresholds
  - Add logic for counter-offer generation with justification
  - Calculate walk-away price and maximum concession
  - _Requirements: 3.1, 3.2, 3.3, 3.4_

- [x] 6.3 Implement contextual factor analysis

  - Add consideration for variety differences, grade quality
  - Implement quantity discount calculations
  - Add market urgency assessment
  - _Requirements: 3.5_

- [ ]* 6.4 Write property test for percentage calculation
  - **Property 7: Percentage calculation accuracy**
  - **Validates: Requirements 3.1**

- [ ]* 6.5 Write property test for deal classification
  - **Property 8: Deal classification consistency**
  - **Validates: Requirements 3.2**

- [ ]* 6.6 Write property test for strategy completeness
  - **Property 9: Strategy completeness**
  - **Validates: Requirements 3.3, 3.4**

- [ ] 7. Implement Communicator Agent
- [x] 7.1 Create Communicator Agent with CrewAI


  - Define agent with role, goal, backstory for farmer communication
  - Configure agent to match farmer's language and style
  - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5_

- [x] 7.2 Implement language detection and matching

  - Create function to detect input language (Hindi/English/Hinglish/regional)
  - Implement tone and formality level detection
  - Add romanized Hindi detection and response formatting
  - _Requirements: 4.1, 4.2, 4.3_

- [x] 7.3 Implement response generation logic

  - Create response formatter with 5-sentence maximum constraint
  - Implement simple language conversion (avoid jargon)
  - Add specific number inclusion and talking points generation
  - _Requirements: 4.4, 4.5, 5.1, 5.2, 5.3, 5.4_

- [ ]* 7.4 Write property test for language matching
  - **Property 10: Language matching consistency**
  - **Validates: Requirements 4.1, 4.3**

- [ ]* 7.5 Write property test for response length
  - **Property 11: Response length constraint**
  - **Validates: Requirements 4.4**

- [ ]* 7.6 Write property test for advice completeness
  - **Property 12: Advice completeness**
  - **Validates: Requirements 5.1, 5.2, 5.3, 5.4**

- [ ] 8. Implement CrewAI workflow orchestration
- [x] 8.1 Create agent tasks and crew


  - Define Task for Price Discovery Agent with description and expected output
  - Define Task for Negotiation Strategist Agent
  - Define Task for Communicator Agent
  - Create Crew with all three agents and tasks in sequence
  - _Requirements: 5.5_

- [x] 8.2 Implement workflow execution

  - Create workflow controller to execute crew with farmer input
  - Add error handling for agent failures
  - Implement result extraction and formatting
  - _Requirements: 5.5_

- [ ]* 8.3 Write property test for single interaction completeness
  - **Property 13: Single interaction completeness**
  - **Validates: Requirements 5.5**

- [ ] 9. Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 10. Implement Streamlit frontend
- [x] 10.1 Create basic chat interface


  - Set up Streamlit app with single-page layout
  - Create chat input widget for farmer messages
  - Implement message display area with formatting
  - Add session state management for conversation context
  - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5_

- [x] 10.2 Integrate chat history display

  - Create sidebar or section to show previous chat sessions
  - Implement session list retrieval from database
  - Add click handlers to load previous conversations
  - Display chat history with user/assistant message formatting
  - _Requirements: 6.7, 7.4_

- [x] 10.3 Connect frontend to agent workflow

  - Integrate crew execution with chat input
  - Display agent responses in real-time
  - Add loading indicators during processing
  - Implement error message display for failures
  - _Requirements: 7.2, 7.3_

- [x] 10.4 Implement session persistence in UI

  - Generate session ID on first message
  - Store each interaction to database via SessionManager
  - Maintain session context across page refreshes
  - _Requirements: 6.6, 7.4_

- [ ]* 10.5 Write property test for real-time processing
  - **Property 16: Real-time processing**
  - **Validates: Requirements 7.2**

- [ ]* 10.6 Write property test for context preservation
  - **Property 17: Context preservation**
  - **Validates: Requirements 7.4**

- [ ]* 10.7 Write property test for chat history retrieval
  - **Property 19: Chat history retrieval**
  - **Validates: Requirements 6.7**

- [ ] 11. Configuration and environment setup
- [x] 11.1 Create configuration management

  - Create config.py for API keys, database paths, cache intervals
  - Add environment variable support for sensitive data
  - Implement configuration validation
  - _Requirements: 6.1, 6.4_

- [x] 11.2 Create deployment documentation

  - Write README with setup instructions
  - Document API key requirements and setup
  - Add usage examples and troubleshooting guide
  - _Requirements: All_

- [x] 12. Final checkpoint - Ensure all tests pass


  - Ensure all tests pass, ask the user if questions arise.