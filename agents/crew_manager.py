from datetime import date
from crewai import Crew, Task
from agents.price_discovery_agent import create_price_discovery_agent
from agents.negotiation_strategist_agent import create_negotiation_strategist_agent
from agents.communicator_agent import create_communicator_agent
from agents.supervisor_agent import SupervisorAgent


class MandiSaathiCrew:
    """
    Manages the intelligent agent workflow for Mandi Saathi.

    Uses a Supervisor Agent to route queries to appropriate agents:
    - GREETING: Direct response from supervisor
    - PRICE_ONLY: Price Discovery -> Communicator
    - NEGOTIATION_WITH_CONTEXT: Negotiation -> Communicator
    - FULL_WORKFLOW: Price Discovery -> Negotiation -> Communicator
    - MISSING_INFO: Direct response asking for details
    - GENERAL_QUERY: Direct response with service info
    """

    def __init__(self):
        # Initialize supervisor for intelligent routing
        self.supervisor = SupervisorAgent()

        # Create agents (lazy initialization - only when needed)
        self._price_discovery_agent = None
        self._negotiation_strategist_agent = None
        self._communicator_agent = None

        # Store context
        self.farmer_message = ""

    @property
    def price_discovery_agent(self):
        """Lazy load price discovery agent"""
        if self._price_discovery_agent is None:
            self._price_discovery_agent = create_price_discovery_agent()
        return self._price_discovery_agent

    @property
    def negotiation_strategist_agent(self):
        """Lazy load negotiation strategist agent"""
        if self._negotiation_strategist_agent is None:
            self._negotiation_strategist_agent = create_negotiation_strategist_agent()
        return self._negotiation_strategist_agent

    @property
    def communicator_agent(self):
        """Lazy load communicator agent"""
        if self._communicator_agent is None:
            self._communicator_agent = create_communicator_agent()
        return self._communicator_agent

    def _format_chat_history(self, chat_history: list) -> str:
        """Format chat history into a readable string for agent context"""
        if not chat_history:
            return ""

        lines = []
        for msg in chat_history:
            lines.append(f"Farmer: {msg.get('user', '')}")
            lines.append(f"Assistant: {msg.get('assistant', '')}")
        return "\n".join(lines)

    def _create_price_only_tasks(self, farmer_message: str, chat_history: list, context_data: dict) -> list:
        """Create tasks for price-only workflow: Price Discovery -> Communicator"""
        history_text = self._format_chat_history(chat_history)
        history_block = self._get_history_block(history_text)
        extracted = context_data.get("extracted_info", {})

        # Task 1: Price Discovery
        price_discovery_task = Task(
            description=f"""Analyze this farmer's message and fetch price information:
            {history_block}
            Farmer's CURRENT Message: "{farmer_message}"

            Pre-extracted info (verify and use):
            - State: {extracted.get('state', 'Not specified')}
            - District: {extracted.get('district', 'Not specified')}
            - Commodity: {extracted.get('commodity', 'Not specified')}

            Your tasks:
            1. Validate the location using your tools
            2. Normalize commodity name (handle Hindi/Hinglish)
            3. Fetch current market prices for the commodity
            4. Get prices from neighboring districts for comparison

            Provide a structured summary with:
            - Validated location (state, district)
            - Normalized commodity name
            - Current modal market price
            - Price range (min-max)
            - Neighboring district prices
            """,
            expected_output="""Structured price data including:
            - Location: [State], [District]
            - Commodity: [Normalized Name]
            - Market Modal Price: ₹[amount] per quintal
            - Price Range: ₹[min] - ₹[max]
            - Nearby Markets: [District1]: ₹[price], [District2]: ₹[price]
            """,
            agent=self.price_discovery_agent
        )

        # Task 2: Communication (price info only)
        communication_task = Task(
            description=f"""Deliver the price information to the farmer in their language:
            CONVERSATION HISTORY: {history_block}
            Farmer's CURRENT Message: "{farmer_message}"

            Your tasks:
            1. Detect the farmer's language (Hindi/English/Hinglish)
            2. Match their tone (formal vs casual)
            3. Provide the price information clearly
            4. Mention nearby market prices for comparison
            5. Keep it concise (maximum 3-4 sentences)

            NOTE: This is a price inquiry only - do NOT provide negotiation advice.
            """,
            expected_output="""A concise, farmer-friendly response that:
            - Matches the farmer's language and tone
            - States current market price clearly
            - Mentions price range
            - Includes nearby market prices for reference
            """,
            agent=self.communicator_agent,
            context=[price_discovery_task]
        )

        return [price_discovery_task, communication_task]

    def _create_negotiation_with_context_tasks(self, farmer_message: str, chat_history: list, context_data: dict) -> list:
        """Create tasks when price context is available: Negotiation -> Communicator"""
        history_text = self._format_chat_history(chat_history)
        history_block = self._get_history_block(history_text)
        extracted = context_data.get("extracted_info", {})
        price_context = context_data.get("price_from_history", {})
        today = date.today().strftime("%d %B %Y")

        # Build price context string for negotiation
        price_info = f"""
        PRICE DATA FROM PREVIOUS CONVERSATION:
        - Commodity: {price_context.get('commodity', 'Unknown')}
        - Location: {price_context.get('location', 'Unknown')}
        - Modal Market Price: ₹{price_context.get('modal_price', 'Unknown')} per quintal
        """

        # Task 1: Negotiation Strategy (using context from history)
        negotiation_strategy_task = Task(
            description=f"""Today's Date: {today}

            Analyze the conversation and create a negotiation strategy:
            {history_block}
            Farmer's CURRENT Message: "{farmer_message}"

            {price_info}

            Extracted from current message:
            - Offered Price: ₹{extracted.get('offered_price', 'Not mentioned')}
            - Quantity: {extracted.get('quantity', 'Not mentioned')}

            Use the Calculator tool for ALL calculations.

            Your tasks:
            1. Calculate percentage difference between offered price and market rate
            2. Classify the deal as Good/Fair/Bad
            3. Generate specific counter-offer amount (aim for 90-95% of modal price)
            4. Provide counter arguments to help user back their claim
            5. Calculate walk-away price (minimum 80% of modal price)
            6. Create 2-3 practical talking points
            7. If the deal is really bad, advise walking away with reasoning
            """,
            expected_output="""Negotiation strategy with:
            - Deal Assessment: [Good/Fair/Bad]
            - Percentage Difference: [X]% below/above market
            - Counter-Offer: ₹[specific amount] per quintal
            - Walk-Away Price: ₹[specific amount] per quintal
            - Talking Points: [2-3 specific points]
            - Justification: [Clear reason based on market data]
            """,
            agent=self.negotiation_strategist_agent
        )

        # Task 2: Communication
        communication_task = Task(
            description=f"""Today's Date: {today}

            Deliver the negotiation advice to the farmer in their language:
            CONVERSATION HISTORY: {history_block}
            Farmer's CURRENT Message: "{farmer_message}"

            Your tasks:
            1. Detect the farmer's language (Hindi/English/Hinglish)
            2. Match their tone (formal vs casual)
            3. Craft a response in their exact language style
            4. Keep it concise (maximum 5 sentences)
            5. Include specific counter-offer amount
            6. Include walk-away price
            7. Give one simple reason they can tell the trader
            """,
            expected_output="""A concise, farmer-friendly response (max 5 sentences) that:
            - Matches the farmer's language and tone
            - Assesses their deal (good/bad/fair)
            - Gives specific counter-offer with reason
            - States minimum acceptable price
            """,
            agent=self.communicator_agent,
            context=[negotiation_strategy_task]
        )

        return [negotiation_strategy_task, communication_task]

    def _create_full_workflow_tasks(self, farmer_message: str, chat_history: list, context_data: dict) -> list:
        """Create tasks for full workflow: Price Discovery -> Negotiation -> Communicator"""
        history_text = self._format_chat_history(chat_history)
        history_block = self._get_history_block(history_text)
        extracted = context_data.get("extracted_info", {})
        today = date.today().strftime("%d %B %Y")

        # Task 1: Price Discovery
        price_discovery_task = Task(
            description=f"""Analyze this farmer's message and extract deal information:
            {history_block}
            Farmer's CURRENT Message: "{farmer_message}"

            Pre-extracted info (verify and use):
            - State: {extracted.get('state', 'Not specified')}
            - District: {extracted.get('district', 'Not specified')}
            - Commodity: {extracted.get('commodity', 'Not specified')}
            - Offered Price: {extracted.get('offered_price', 'Not specified')}

            Your tasks:
            1. Validate and correct location names using your tools
            2. Normalize commodity name (handle Hindi/Hinglish)
            3. Fetch current market prices for the commodity
            4. Get prices from neighboring districts for comparison

            Provide a structured summary with:
            - Validated location (state, district)
            - Normalized commodity name
            - Offered price (if mentioned)
            - Current modal market price
            - Price range (min-max)
            - Neighboring district prices
            """,
            expected_output="""Structured price data including:
            - Location: [State], [District]
            - Commodity: [Normalized Name]
            - Offered Price: ₹[amount] per quintal (if mentioned)
            - Market Modal Price: ₹[amount] per quintal
            - Price Range: ₹[min] - ₹[max]
            - Nearby Markets: [District1]: ₹[price], [District2]: ₹[price]
            """,
            agent=self.price_discovery_agent
        )

        # Task 2: Negotiation Strategy
        negotiation_strategy_task = Task(
            description=f"""Today's Date: {today}

            Analyze the conversation and price data:
            {history_block}
            Farmer's CURRENT Message: "{farmer_message}"

            Based on the price discovery results, create a negotiation strategy.
            Use the Calculator tool for ALL calculations.

            Your tasks:
            1. Calculate percentage difference between offered price and market rate
            2. Classify the deal as Good/Fair/Bad
            3. Generate specific counter-offer amount (aim for 90-95% of modal price)
            4. Provide counter arguments to help user back their claim
            5. Calculate walk-away price (minimum 80% of modal price)
            6. Determine maximum concession farmer should make
            7. Create 2-3 practical talking points
            8. If deal is really bad, advise walking away with reasoning

            Consider:
            - Variety and grade differences if mentioned
            - Quantity (bulk discounts for large quantities)
            - Market urgency and seasonal factors
            """,
            expected_output="""Negotiation strategy with:
            - Deal Assessment: [Good/Fair/Bad]
            - Percentage Difference: [X]% below/above market
            - Counter-Offer: ₹[specific amount] per quintal (Not Required if Offer Price not mentioned)
            - Walk-Away Price: ₹[specific amount] per quintal
            - Maximum Concession: ₹[amount]
            - Talking Points: [2-3 specific points] (Not Required if Offer Price not mentioned)
            - Justification: [Clear reason based on market data]

            NOTE: Never assume trader's offer if not mentioned by user.
            If user only asks about price, answer with only price details.
            """,
            agent=self.negotiation_strategist_agent,
            context=[price_discovery_task]
        )

        # Task 3: Communication
        communication_task = Task(
            description=f"""Today's Date: {today}

            Deliver the negotiation advice to the farmer in their language:
            CONVERSATION HISTORY: {history_block}
            Farmer's CURRENT Message: "{farmer_message}"

            Your tasks:
            1. Detect the farmer's language (Hindi/English/Hinglish)
            2. Match their tone (formal vs casual)
            3. Craft a response in their exact language style
            4. Keep it concise (maximum 5 sentences)
            5. Include specific counter-offer amount
            6. Include walk-away price
            7. Give one simple reason they can tell the trader
            8. Avoid all technical jargon

            Language matching rules:
            - If they used "tamatar", use "tamatar" (not "tomato")
            - If they used "bhai", respond with "bhai"
            - If romanized Hindi, respond in romanized Hindi
            - Match their formality level exactly
            """,
            expected_output="""A concise, farmer-friendly response (max 5 sentences) that:
            - Matches the farmer's language and tone exactly
            - States current market price
            - Assesses their deal (good/bad/fair) if offered price mentioned
            - Gives specific counter-offer with reason if applicable
            - States minimum acceptable price
            - Does not repeat same negotiation tactics from history if trader rejected
            """,
            agent=self.communicator_agent,
            context=[price_discovery_task, negotiation_strategy_task]
        )

        return [price_discovery_task, negotiation_strategy_task, communication_task]

    def _get_history_block(self, history_text: str) -> str:
        """Create formatted history block for task descriptions"""
        if not history_text:
            return ""
        return f"""
        PREVIOUS CONVERSATION HISTORY (use this for context):
        ---
        {history_text}
        ---
        """

    def run(self, farmer_message: str, chat_history: list = None) -> str:
        """Execute the intelligent workflow based on supervisor's routing decision"""
        try:
            self.farmer_message = farmer_message

            # Step 1: Supervisor analyzes the query
            print("\n" + "="*50)
            print("SUPERVISOR: Analyzing query...")
            print("="*50)

            analysis = self.supervisor.analyze_query(farmer_message, chat_history)
            intent, direct_response, context_data = self.supervisor.get_workflow_decision(analysis)

            print(f"SUPERVISOR DECISION:")
            print(f"  Intent: {intent}")
            print(f"  Confidence: {analysis.get('confidence', 'N/A')}")
            print(f"  Reasoning: {analysis.get('reasoning', 'N/A')}")
            print("="*50 + "\n")

            # Step 2: Handle direct responses (no agents needed)
            if direct_response and intent in [
                SupervisorAgent.INTENT_GREETING,
                SupervisorAgent.INTENT_MISSING_INFO,
                SupervisorAgent.INTENT_GENERAL_QUERY
            ]:
                print(f"SUPERVISOR: Handling directly ({intent})")
                return direct_response

            # Step 3: Route to appropriate workflow
            tasks = []
            agents = []

            if intent == SupervisorAgent.INTENT_PRICE_ONLY:
                print("SUPERVISOR: Routing to PRICE_ONLY workflow")
                print("  Agents: Price Discovery -> Communicator")
                tasks = self._create_price_only_tasks(farmer_message, chat_history, context_data)
                agents = [self.price_discovery_agent, self.communicator_agent]

            elif intent == SupervisorAgent.INTENT_NEGOTIATION_WITH_CONTEXT:
                print("SUPERVISOR: Routing to NEGOTIATION_WITH_CONTEXT workflow")
                print("  Agents: Negotiation -> Communicator (using price from history)")
                tasks = self._create_negotiation_with_context_tasks(farmer_message, chat_history, context_data)
                agents = [self.negotiation_strategist_agent, self.communicator_agent]

            else:  # FULL_WORKFLOW or fallback
                print("SUPERVISOR: Routing to FULL_WORKFLOW")
                print("  Agents: Price Discovery -> Negotiation -> Communicator")
                tasks = self._create_full_workflow_tasks(farmer_message, chat_history, context_data)
                agents = [
                    self.price_discovery_agent,
                    self.negotiation_strategist_agent,
                    self.communicator_agent
                ]

            # Step 4: Create and execute crew
            crew = Crew(
                agents=agents,
                tasks=tasks,
                verbose=True
            )

            result = crew.kickoff()
            return str(result)

        except Exception as e:
            print(f"Error in MandiSaathiCrew: {e}")
            return f"Maaf kijiye, kuch gadbad ho gayi. Kripya dobara koshish karein. (Error: {str(e)})"
