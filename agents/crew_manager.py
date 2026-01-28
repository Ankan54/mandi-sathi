from datetime import date
from datetime import date
from crewai import Crew, Task
from agents.price_discovery_agent import create_price_discovery_agent
from agents.negotiation_strategist_agent import create_negotiation_strategist_agent
from agents.communicator_agent import create_communicator_agent

class MandiSaathiCrew:
    """Manages the three-agent workflow for Mandi Saathi"""
    
    def __init__(self):
        # Create agents
        self.price_discovery_agent = create_price_discovery_agent()
        self.negotiation_strategist_agent = create_negotiation_strategist_agent()
        self.communicator_agent = create_communicator_agent()
        
        # Store farmer message for context
        self.farmer_message = ""
    
    def _format_chat_history(self, chat_history: list) -> str:
        """Format chat history into a readable string for agent context"""
        if not chat_history:
            return ""

        lines = []
        for msg in chat_history:
            lines.append(f"Farmer: {msg['user']}")
            lines.append(f"Assistant: {msg['assistant']}")
        return "\n".join(lines)

    def create_tasks(self, farmer_message: str, chat_history: list = None):
        """Create tasks for the crew based on farmer's message"""
        self.farmer_message = farmer_message

        history_text = self._format_chat_history(chat_history)
        history_block = ""
        if history_text:
            history_block = f"""
            PREVIOUS CONVERSATION HISTORY (use this for context, the farmer may be referring to details mentioned earlier):
            ---
            {history_text}
            ---
            """

        # Task 1: Price Discovery
        price_discovery_task = Task(
            description=f"""Analyze this farmer's message and extract deal information:
            {history_block}
            Farmer's CURRENT Message: "{farmer_message}"

            Your tasks:
            1. Identify the state, district, and commodity mentioned
            2. Extract the quantity and offered price if mentioned
            3. Validate and correct location names using your tools
            4. Normalize commodity name (handle Hindi/Hinglish)
            5. Fetch current market prices for the commodity in that location
            6. Get prices from neighboring districts for comparison
            
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
        
        today = date.today().strftime("%d %B %Y")

        # Task 2: Negotiation Strategy
        negotiation_strategy_task = Task(
            description=f"""Today's Date: {today}
            
            Analyze the conversation till now:
            {history_block}
            Farmer's CURRENT Message: "{farmer_message}"

            Based on the given context and price discovery results, create a negotiation strategy.
            Use the Calculator tool for ALL calculations - do not do mental math.

            Your tasks:
            1. Calculate percentage difference between offered price and market rate
            2. Classify the deal as Good/Fair/Bad
            3. Generate specific counter-offer amount (aim for 90-95% of modal price)
            4. provide some counter argument along with counter offer price to help user back his claim
            5. Calculate walk-away price (minimum 80% of modal price)
            6. Determine maximum concession farmer should make
            7. Create 2-3 practical talking points for negotiation
            8. Provide clear justification based on market data
            9. Walking away from a bad deal is also crucial in negotiations. so if you think the user should walk away from the deal, then advise accordingly with reasoning.
            
            Consider:
            - Variety and grade differences if mentioned
            - Quantity (bulk discounts for large quantities)
            - Market urgency and seasonal factors
            """,
            expected_output="""Negotiation strategy with:
            - Deal Assessment: [Good/Fair/Bad]
            - Percentage Difference: [X]% below/above market
            - Counter-Offer: ₹[specific amount] per quintal . Not Required if Offer Price is not mentioned
            - Walk-Away Price: ₹[specific amount] per quintal
            - Maximum Concession: ₹[amount]
            - Talking Points: [2-3 specific points]. Not Required if Offer Price is not mentioned.
            - Justification: [One clear reason based on market data]

            Point TO NOTE: 
            -You will never assume Trader's offer if the offered price is not mentioned by user.
            - You will never repeat the same negotiation tactics from conversation history if the User comes back with negative response from the Trader.
            - If user only asks about the price then answer with only the price details and what are the prices in nearby mandis (if data available). No other information needed in that case.
            """,
            agent=self.negotiation_strategist_agent,
            context=[price_discovery_task]
        )
        
        # Task 3: Communication
        communication_task = Task(
            description=f"""Today's Date: {today}

            Deliver the negotiation advice to the farmer in their language and style:
            CONVERSATION HISTORY: {history_block}
            Farmer's CURRENT Message: "{farmer_message}"
            
            Your tasks:
            1. Detect the farmer's language (Hindi/English/Hinglish/romanized Hindi)
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
            - Assesses their deal (good/bad/fair). Not Required if offered price is not mentioned
            - Gives specific counter-offer with reason. Not Required if offered price is not mentioned
            - States minimum acceptable price. Not Required if offered price is not mentioned
            - do not repeat the same negotiation tactics again from conversation history in case of negative response from the Trader.
            
            Example format (adapt to farmer's language):
            "[Greeting], abhi [location] mein [commodity] ka bhav ₹[market_price] chal raha hai. 
            Trader [assessment]. Tum ₹[counter_offer] maango, aur batao ki [reason]. 
            ₹[walk_away] se neeche mat bechna."
            """,
            agent=self.communicator_agent,
            context=[price_discovery_task, negotiation_strategy_task]
        )
        
        return [price_discovery_task, negotiation_strategy_task, communication_task]
    
    def run(self, farmer_message: str, chat_history: list = None) -> str:
        """Execute the crew workflow and return final response"""
        try:
            # Create tasks
            tasks = self.create_tasks(farmer_message, chat_history)
            
            # Create crew
            crew = Crew(
                agents=[
                    self.price_discovery_agent,
                    self.negotiation_strategist_agent,
                    self.communicator_agent
                ],
                tasks=tasks,
                verbose=True
            )
            
            # Execute workflow
            result = crew.kickoff()
            
            # Return the final communication task output
            return str(result)
            
        except Exception as e:
            return f"Error processing request: {str(e)}. Please try again or rephrase your message."
