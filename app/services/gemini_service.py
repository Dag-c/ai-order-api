import logging
import json
import httpx
from sqlalchemy.orm import Session

from app.schemas.chat_llm_schema import ChatLLM
from app.services.product_service import get_products_service
from app.core.config import GEMINI_API_KEY

logger = logging.getLogger(__name__)

URL = (
    "https://generativelanguage.googleapis.com/"
    "v1beta/models/gemini-3.1-flash-lite:generateContent"
)

# =========================================
# SYSTEM PROMPT
# =========================================

CHAT_SYSTEM_PROMPT = """
You are an AI assistant for a Mexican restaurant ordering system.

Your ONLY job is to convert user messages into structured JSON.

==================================================
STRICT OUTPUT RULES
==================================================

- Return ONLY valid JSON
- No markdown
- No explanations
- No extra text
- Never hallucinate products
- Use ONLY AVAILABLE PRODUCTS
- Always include "data"
- Always include "items"

If no items exist:
"items": []

==================================================
CRITICAL STATE MACHINE RULES
==================================================

CURRENT STATE controls EVERYTHING.

NEVER generate intents
that are not allowed
for CURRENT STATE.

STATE PRIORITY (HIGHEST RULE):

1. idle

Allowed intents:
- greeting
- ask_menu
- ask_availability
- add_to_cart
- unknown

--------------------------------------------------

2. building_order

Allowed intents:
- add_to_cart
- remove_from_cart
- review_order
- unknown

--------------------------------------------------

3. review_order

Allowed intents:
- review_order
- add_to_cart
- remove_from_cart
- checkout
- unknown

--------------------------------------------------

4. checkout

Allowed intents:
- checkout
- unknown

==================================================
IMPORTANT BEHAVIOR RULES
==================================================

- NEVER move to checkout
unless CURRENT STATE = review_order

- Words like:
  - sí
  - ok
  - va
  - simón
  - dale
  - arre

ONLY mean checkout
when CURRENT STATE = review_order

- NEVER extract customer data
unless user explicitly writes it

- DO NOT return cart items
during review_order or checkout
(system already manages cart)

==================================================
INTENTS
==================================================

- greeting
- ask_menu
- ask_availability
- add_to_cart
- remove_from_cart
- review_order
- checkout
- unknown

==================================================
MEXICAN SPANISH CONTEXT
==================================================

Users speak informal Mexican Spanish.

Understand expressions like:
- simón
- va
- órale
- arre
- con eso
- ya quedó
- mándalo
- cuánto sería
- dame dos
- agrégame otro
- ya estuvo

==================================================
INTENT DEFINITIONS
==================================================

1. greeting

Examples:
- hola
- buenas
- qué onda
- buen día
- hello

--------------------------------------------------

2. ask_menu

User wants to see the menu.

Examples:
- qué tienes
- pásame el menú
- qué venden
- qué hay de comer
- enséñame el menú

--------------------------------------------------

3. ask_availability

User asks if product exists.

Examples:
- tienes pozole
- hay tacos
- manejas enchiladas
- todavía hay quesadillas

--------------------------------------------------

4. add_to_cart

User wants MORE products.

Examples:
- dame 2 pozoles
- agrégame una enchilada
- también una coca
- ponme otros dos tacos
- agrega una quesadilla

IMPORTANT:
Use add_to_cart ONLY
when user increases products.

--------------------------------------------------

5. remove_from_cart

User wants FEWER products
or remove products.

Examples:
- quita un pozole
- elimina una enchilada
- ya no quiero tacos
- borra una quesadilla
- deja solo un pozole
- mejor quita una coca
- bájale un pozole
- solo quiero uno
- reduce a un pozole
- ponme solo una enchilada
- quita 2 tacos
- ya no quiero 3, solo 1
- mejor nada más un pozole

IMPORTANT:

If user wants fewer products:
use remove_from_cart

NEVER use add_to_cart
when user is reducing quantities.

--------------------------------------------------

6. review_order

User wants:
- see order
- see total
- finish selecting products

Examples:
- eso es todo
- cuánto es
- ya quedó
- quiero ver la orden
- cuánto voy pagando
- enséñame mi pedido
- con eso

--------------------------------------------------

7. checkout

ONLY if:
- CURRENT STATE = review_order
AND:
  - user confirms order
  OR
  - user provides customer information

Examples:
- sí
- adelante
- va
- ok
- simón
- dale

Examples with customer data:
- me llamo Juan
- mi nombre es Carlos
- mi número es 3334445555
- vivo en calle Hidalgo 20
- mi dirección es avenida Juárez 50

IMPORTANT:

In checkout state,
user may provide data gradually.

Examples:
- me llamo Juan
- 3334445555
- calle Hidalgo 20

Still use:
intent = "checkout"

If CURRENT STATE = checkout,
prioritize extracting:
- customer_name
- customer_phone
- delivery_address

==================================================
REQUIRED OUTPUT FORMAT
==================================================

{
  "intent": "string",
  "data": {
    "items": [
      {
        "product": "string",
        "quantity": number
      }
    ],
    "customer_name": null,
    "customer_phone": null,
    "delivery_address": null
  }
}

==================================================
JSON RULES
==================================================

- Always include "data"
- Always include "items"

If no items exist:
"items": []

If customer data does not exist:
use null

Never return text outside JSON.

==================================================
EXAMPLES
==================================================

User:
quiero 2 pozoles y una enchilada

Response:
{
  "intent": "add_to_cart",
  "data": {
    "items": [
      {
        "product": "Pozole blanco",
        "quantity": 2
      },
      {
        "product": "Enchiladas Rojas",
        "quantity": 1
      }
    ],
    "customer_name": null,
    "customer_phone": null,
    "delivery_address": null
  }
}

--------------------------------------------------

User:
quita un pozole

Response:
{
  "intent": "remove_from_cart",
  "data": {
    "items": [
      {
        "product": "Pozole blanco",
        "quantity": 1
      }
    ],
    "customer_name": null,
    "customer_phone": null,
    "delivery_address": null
  }
}

--------------------------------------------------

User:
eso sería todo

Response:
{
  "intent": "review_order",
  "data": {
    "items": [],
    "customer_name": null,
    "customer_phone": null,
    "delivery_address": null
  }
}

--------------------------------------------------

User:
sí, continuar

Response:
{
  "intent": "checkout",
  "data": {
    "items": [],
    "customer_name": null,
    "customer_phone": null,
    "delivery_address": null
  }
}

--------------------------------------------------

User:
me llamo Juan Pérez

Response:
{
  "intent": "checkout",
  "data": {
    "items": [],
    "customer_name": "Juan Pérez",
    "customer_phone": null,
    "delivery_address": null
  }
}
"""

# =========================================
# MAIN SERVICE
# =========================================

async def analyze_chat_message(
    message: str,
    session,
    db: Session
):

    # =========================================
    # GET PRODUCTS
    # =========================================

    try:

        products = get_products_service(db)

    except Exception as e:

        return {
            "success": False,
            "error": (
                "Could not load products"
            ),
            "details": str(e)
        }

    menu_text = "\n".join(
        [
            f"- {product.name}"
            for product in products
        ]
    )

    # =========================================
    # BUILD PROMPT
    # =========================================

    full_prompt = f"""
{CHAT_SYSTEM_PROMPT}

==================================================
CURRENT STATE
==================================================

{session.current_state}

==================================================
AVAILABLE PRODUCTS
==================================================

{menu_text}

==================================================
USER MESSAGE
==================================================

{message}
"""

    # =========================================
    # REQUEST BODY
    # =========================================

    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": full_prompt
                    }
                ]
            }
        ]
    }

    headers = {
        "Content-Type": "application/json"
    }

    params = {
        "key": GEMINI_API_KEY
    }

    # =========================================
    # CALL GEMINI
    # =========================================

    try:

        async with httpx.AsyncClient(timeout=30) as client:

            response = await client.post(
                URL,
                headers=headers,
                params=params,
                json=payload
            )

    except httpx.ReadTimeout:

        return {
            "success": False,
            "error": "Gemini timeout"
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }

    # =========================================
    # VALIDATE STATUS CODE
    # =========================================

    if response.status_code != 200:

      return {
          "success": False,
          "error": (
              f"Gemini API error: "
              f"{response.status_code}"
          ),
          "details": response.text
      }

    # =========================================
    # DEBUG
    # =========================================

    logger.debug("STATUS: %s", response.status_code)
    logger.debug("RAW RESPONSE: %s", response.text)

    # =========================================
    # PARSE RESPONSE
    # =========================================

    try:

        response_json = response.json()

    except Exception:

        return {
            "success": False,
            "error": "Invalid JSON from Gemini"
        }

   # =========================================
    # VALIDATE CANDIDATES
    # =========================================

    candidates = response_json.get(
        "candidates",
        []
    )

    if not candidates:

        return {
            "success": False,
            "error": "No candidates returned"
        }

    # =========================================
    # EXTRACT PARTS
    # =========================================

    parts = (
        candidates[0]
        .get("content", {})
        .get("parts", [])
    )

    if not parts:

        return {
            "success": False,
            "error": "No parts returned"
        }

    # =========================================
    # EXTRACT TEXT
    # =========================================

    text = parts[0].get("text")

    if not text:

        return {
            "success": False,
            "error": "No text returned"
        }
    # =========================================
    # PARSE MODEL JSON
    # =========================================

    try:

        parsed = json.loads(text)

        validated = ChatLLM.model_validate(parsed)

        return {
            "success": True,
            "data": validated
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e),
            "raw_response": text
        }