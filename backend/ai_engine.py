# ==========================================
# KEYRADDIIN PERSONAL AI V2.0
# AI ENGINE + JSON MEMORY
# ==========================================

import os
import time

from google import genai

from memory import recall_all, remember


class KeyraddiinAI:

    def __init__(self):

        self.api_key = os.getenv("GEMINI_API_KEY")

        self.model = os.getenv(
            "GEMINI_MODEL",
            "gemini-2.5-flash"
        )

        self.client = (
            genai.Client(api_key=self.api_key)
            if self.api_key else None
        )

        self.system_instruction = """
You are KEYRADDIIN PERSONAL AI.

You are a professional, intelligent
and helpful personal assistant.

YOUR RESPONSIBILITIES:

1. Answer questions accurately.
2. Help students learn.
3. Explain science and technology.
4. Support Afaan Oromo and English.
5. Give clear and useful explanations.
6. Remember useful information provided by the user.
7. Use saved memories when relevant.

LANGUAGE:

- Support Afaan Oromo.
- Support English.
- Understand both languages.
- Respond in the language used by the user.

BEHAVIOUR:

- Be respectful and educational.
- Do not invent information.
- Explain difficult topics clearly.
- Use saved memory only when relevant.
- Never claim to remember something
  that is not present in the supplied memory.

You are KEYRADDIIN PERSONAL AI V2.0.
"""


    # ======================================
    # GET SAVED MEMORY
    # ======================================

    def get_memory_context(self):

        try:

            memories = recall_all()

            if not memories:

                return "No saved memories available."

            if isinstance(memories, dict):

                return "\n".join(
                    f"{key}: {value}"
                    for key, value in memories.items()
                )

            return str(memories)

        except Exception as error:

            print("MEMORY READ ERROR:", error)

            return "Memory is temporarily unavailable."


    # ======================================
    # CHECK EXPLICIT MEMORY REQUEST
    # ======================================

    def should_remember(self, message):

        text = message.lower()

        triggers = [

            "remember that",
            "remember this",
            "please remember",
            "save this",
            "don't forget",

            "kana yaadadhu",
            "na yaadadhu",
            "yaadadhu",
            "hin dagatin",
            "kuusi",

        ]

        return any(
            trigger in text
            for trigger in triggers
        )


    # ======================================
    # SAVE USER MEMORY
    # ======================================

    def save_user_memory(self, message):

        if not self.should_remember(message):

            return False

        try:

            memory_key = (
                "user_note_" + str(int(time.time()))
            )

            remember(
                memory_key,
                message
            )

            print("MEMORY SAVED:", memory_key)

            return True

        except Exception as error:

            print("MEMORY SAVE ERROR:", error)

            return False


    # ======================================
    # GENERATE AI RESPONSE
    # ======================================

    async def generate_response(self, message):

        if not self.client:

            return (
                "AI is not configured yet. "
                "Please configure GEMINI_API_KEY."
            )

        try:

            # READ SAVED MEMORY
            memory_context = self.get_memory_context()


            # SAVE EXPLICIT MEMORY REQUEST
            memory_saved = self.save_user_memory(message)


            # BUILD AI PROMPT
            full_prompt = f"""

{self.system_instruction}


SAVED USER MEMORY:

{memory_context}


CURRENT USER MESSAGE:

{message}


IMPORTANT:

Use the saved memory when relevant.

If the user asks you to remember something
and it has been saved, confirm that it was saved.

Answer the user's current question clearly.

"""


            # GEMINI API REQUEST
            response = self.client.models.generate_content(

                model=self.model,

                contents=full_prompt

            )


            # GET RESPONSE TEXT
            answer = response.text

            if not answer:

                return (
                    "Sorry, I could not generate "
                    "a response. Please try again."
                )

            return answer


        except Exception as error:

            print("AI ERROR:", error)

            return (
                "Sorry, I could not process "
                "your request. Please try again."
            )


# ==========================================
# INITIALIZE AI
# ==========================================

ai = KeyraddiinAI()


print("KEYRADDIIN PERSONAL AI ENGINE LOADED")