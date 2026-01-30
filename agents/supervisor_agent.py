from openai import OpenAI
import config
import json
import re
from typing import Tuple, Dict, Any, Optional


class SupervisorAgent:
    """
    Supervisor Agent that intelligently routes user queries to appropriate agents.

    Routing Logic:
    - GREETING: Respond directly with a friendly greeting
    - PRICE_ONLY: Price Discovery -> Communicator
    - NEGOTIATION_WITH_CONTEXT: Negotiation -> Communicator (prices from history)
    - FULL_WORKFLOW: Price Discovery -> Negotiation -> Communicator
    - MISSING_INFO: Respond directly asking for required details
    - GENERAL_QUERY: Respond directly with helpful information
    """

    # Intent categories
    INTENT_GREETING = "GREETING"
    INTENT_PRICE_ONLY = "PRICE_ONLY"
    INTENT_NEGOTIATION_WITH_CONTEXT = "NEGOTIATION_WITH_CONTEXT"
    INTENT_FULL_WORKFLOW = "FULL_WORKFLOW"
    INTENT_MISSING_INFO = "MISSING_INFO"
    INTENT_GENERAL_QUERY = "GENERAL_QUERY"

    def __init__(self):
        self.client = OpenAI(api_key=config.OPENAI_API_KEY)
        self.model = config.SUPERVISOR_MODEL

    def analyze_query(self, farmer_message: str, chat_history: list = None) -> Dict[str, Any]:
        """
        Analyze the farmer's query and determine the appropriate workflow.

        Returns:
            Dict containing:
            - intent: The classified intent
            - direct_response: Response if supervisor handles directly (for GREETING, MISSING_INFO, GENERAL_QUERY)
            - price_context: Extracted price data from history if available
            - extracted_info: Any extracted location, commodity, price info
        """

        history_text = self._format_chat_history(chat_history)

        analysis_prompt = f"""You are a supervisor agent for Mandi Saathi, a farming price advisory system.
Analyze the farmer's message and determine the appropriate action.

CONVERSATION HISTORY:
---
{history_text if history_text else "No previous conversation"}
---

FARMER'S CURRENT MESSAGE: "{farmer_message}"

TASK: Analyze the intent and extract relevant information.

INTENT CATEGORIES:
1. GREETING - Simple greetings like "hello", "hi", "namaste", "thanks", "dhanyavaad", casual conversation
2. PRICE_ONLY - User only wants to know the current market price (not negotiating)
3. NEGOTIATION_WITH_CONTEXT - User wants negotiation advice AND price data is already available in chat history
4. FULL_WORKFLOW - User wants negotiation advice but needs price discovery first
5. MISSING_INFO - User wants help but hasn't provided essential info (location OR commodity)
6. GENERAL_QUERY - General questions about the service, how it works, etc.

CONTEXT DETECTION RULES:
- For NEGOTIATION_WITH_CONTEXT: Check if chat history already contains:
  * Market price for the commodity user is asking about
  * The same location context
  * If user mentions an offered price AND history has market price -> NEGOTIATION_WITH_CONTEXT

- For PRICE_ONLY: User asks things like:
  * "What's the price of wheat in Delhi?"
  * "Tamatar ka bhav kya hai Ballia mein?"
  * No mention of trader's offer or negotiation

- For FULL_WORKFLOW: User mentions:
  * A trader's offered price AND
  * Needs price discovery (no recent price in history for same commodity/location)

- For MISSING_INFO: User wants price/negotiation help but:
  * Missing location (state/district) AND can't be inferred from history
  * OR missing commodity name AND can't be inferred from history

EXTRACTION RULES:
- Extract state, district, commodity, offered_price if mentioned
- Check chat history for previously mentioned info
- Look for Hindi/Hinglish terms (tamatar=tomato, aloo=potato, pyaz=onion, gehu=wheat)

Respond in this exact JSON format:
{{
    "intent": "<GREETING|PRICE_ONLY|NEGOTIATION_WITH_CONTEXT|FULL_WORKFLOW|MISSING_INFO|GENERAL_QUERY>",
    "confidence": <0.0-1.0>,
    "reasoning": "<brief explanation of why this intent>",
    "extracted_info": {{
        "state": "<extracted state or null>",
        "district": "<extracted district or null>",
        "commodity": "<extracted commodity in English or null>",
        "offered_price": <extracted offered price as number or null>,
        "quantity": "<extracted quantity or null>"
    }},
    "price_from_history": {{
        "available": <true|false>,
        "commodity": "<commodity if available>",
        "modal_price": <price if available or null>,
        "location": "<location if available>"
    }},
    "missing_fields": ["<list of missing required fields if MISSING_INFO>"],
    "direct_response": "<response text if GREETING, MISSING_INFO, or GENERAL_QUERY, else null>"
}}

IMPORTANT for direct_response:
- For GREETING: Respond warmly in the same language as the farmer (Hindi/English/Hinglish)
- For MISSING_INFO: Politely ask for the missing information in farmer's language
- For GENERAL_QUERY: Explain Mandi Saathi's capabilities in farmer's language
- Keep responses concise and friendly

Examples of direct_response:
- GREETING (Hindi): "Namaste! Mein Mandi Saathi hoon. Aap apni fasal ka bhav jaanne ya mandi mein saudebazi mein madad ke liye mujhse pooch sakte hain."
- MISSING_INFO: "Bhai, kaunsi mandi ka bhav chahiye? State aur district bata do."
- GENERAL_QUERY: "Mein aapko mandi ke bhav batata hoon aur trader se accha dam dilwane mein madad karta hoon."
"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a routing supervisor for an agricultural advisory system. Respond only in valid JSON format."},
                    {"role": "user", "content": analysis_prompt}
                ],
                temperature=0.3,  # Lower temperature for consistent routing
                max_completion_tokens=1000
            )

            response_text = response.choices[0].message.content

            # Extract JSON from response
            json_match = re.search(r'\{[\s\S]*\}', response_text)
            if json_match:
                analysis = json.loads(json_match.group())
                return analysis
            else:
                # Fallback if JSON parsing fails
                return self._fallback_analysis(farmer_message, chat_history)

        except Exception as e:
            print(f"Supervisor analysis error: {e}")
            return self._fallback_analysis(farmer_message, chat_history)

    def _fallback_analysis(self, farmer_message: str, chat_history: list = None) -> Dict[str, Any]:
        """Fallback analysis when LLM fails"""
        # Simple keyword-based fallback
        msg_lower = farmer_message.lower()

        greeting_words = ['hello', 'hi', 'namaste', 'namaskar', 'thanks', 'thank', 'dhanyavaad', 'shukriya']
        if any(word in msg_lower for word in greeting_words) and len(farmer_message.split()) < 5:
            return {
                "intent": self.INTENT_GREETING,
                "confidence": 0.7,
                "reasoning": "Greeting detected via keyword matching",
                "extracted_info": {"state": None, "district": None, "commodity": None, "offered_price": None, "quantity": None},
                "price_from_history": {"available": False, "commodity": None, "modal_price": None, "location": None},
                "missing_fields": [],
                "direct_response": "Namaste! Mein Mandi Saathi hoon. Aapki fasal ka bhav jaanne ya mandi saudebazi mein madad ke liye poochein."
            }

        # Default to full workflow
        return {
            "intent": self.INTENT_FULL_WORKFLOW,
            "confidence": 0.5,
            "reasoning": "Fallback - assuming full workflow needed",
            "extracted_info": {"state": None, "district": None, "commodity": None, "offered_price": None, "quantity": None},
            "price_from_history": {"available": False, "commodity": None, "modal_price": None, "location": None},
            "missing_fields": [],
            "direct_response": None
        }

    def _format_chat_history(self, chat_history: list) -> str:
        """Format chat history into a readable string"""
        if not chat_history:
            return ""

        lines = []
        for msg in chat_history:
            lines.append(f"Farmer: {msg.get('user', '')}")
            lines.append(f"Assistant: {msg.get('assistant', '')}")
        return "\n".join(lines)

    def get_workflow_decision(self, analysis: Dict[str, Any]) -> Tuple[str, Optional[str], Dict[str, Any]]:
        """
        Based on analysis, return the workflow decision.

        Returns:
            Tuple of (intent, direct_response_or_none, context_data)
        """
        intent = analysis.get("intent", self.INTENT_FULL_WORKFLOW)
        direct_response = analysis.get("direct_response")

        context_data = {
            "extracted_info": analysis.get("extracted_info", {}),
            "price_from_history": analysis.get("price_from_history", {}),
            "reasoning": analysis.get("reasoning", "")
        }

        # For intents that need direct response
        if intent in [self.INTENT_GREETING, self.INTENT_MISSING_INFO, self.INTENT_GENERAL_QUERY]:
            return (intent, direct_response, context_data)

        # For intents that need agent workflow
        return (intent, None, context_data)


def create_supervisor_agent() -> SupervisorAgent:
    """Factory function to create a SupervisorAgent instance"""
    return SupervisorAgent()
