from app.services.gemini_service import analyze_chat_message
from app.core.chat_state_machine import handle_chat_state
from app.core.session_store import sessions
from app.schemas.chat_session_schema import ChatSessionSchema

async def process_chat(session_id, message, db):

    if session_id not in sessions:
        sessions[session_id] = ChatSessionSchema()
    
    session = sessions[session_id]

    llm_response = await analyze_chat_message(
        message,
        session,
        db
    )

    # =====================================
    # HANDLE LLM ERRORS
    # =====================================

    if not llm_response["success"]:

        return {
            "type": "message",
            "message": (
                "Ocurrió un problema procesando "
                "tu mensaje, intenta nuevamente"
            ),
            "data": {
                "error": llm_response["error"]
            }
        }

    llm_data = llm_response["data"]

    response = await handle_chat_state(
        llm_data,
        session,
        db
    )

    return response