import re
import sys
from pathlib import Path
from core.config import config
from core.db_ops import (
    get_order_details,
    get_demand_details,
    get_project_details,
    get_resource_details,
    update_order_status,
    update_demand_status,
)

class BotReplyGenerator:
    def __init__(self):
        self.provider = config.ACTIVE_PROVIDER
        self.fallback_responses = {
            "Greeting": "Hello! How can I help you today?",
            "Track_Order": "Please provide your order ID to check the status.",
            "Track_Demand": "Please provide your demand ID to check the status.",
            "Project_Status": "Please provide your project ID to check the status.",
            "Resource_Availability": "Please provide the resource ID to check availability.",
            "Update_Order_Status": "Please provide your order ID and the new status to update.",
            "Update_Demand_Status": "Please provide your demand ID and the new status to update.",
            "Refund": "I can help you with a refund. What is the reason for the return?",
        }

    def _inject_dynamic_data(self, intent: str, system_prompt: str, user_text: str, context_history: list) -> str:
        """
        Dynamically calls the corresponding handler method for the intent if it exists.
        To add a new intent condition, simply add a new method named `_handle_{intent.lower()}`.
        """
        method_name = f"_handle_{intent.lower()}"
        handler = getattr(self, method_name, None)
        
        if handler:
            # Concat the previous user messages with current input to capture context if missing from current turn
            search_text = " ".join([msg["content"] for msg in context_history if msg["role"] == "user"]) + " " + user_text
            return handler(system_prompt, search_text)
            
        return system_prompt

    def _handle_track_order(self, system_prompt: str, user_text: str) -> str:
        match = re.search(r'(?i)(ORD-\d{4})', user_text)
        if match:
            extracted_id = match.group(1).upper()
            order_data = get_order_details(extracted_id)
            if order_data:
                system_prompt += (
                    f"\n\n[SYSTEM DATABASE INFO]\n"
                    f"Order Found: {extracted_id}\n"
                    f"Customer: {order_data['customer_name']}\n"
                    f"Item: {order_data['item_name']}\n"
                    f"Status: {order_data['status']}\n"
                    f"Amount: ${order_data['amount']}\n\n"
                    f"Use this EXACT database information to answer the user's question about their tracking status."
                )
            else:
                system_prompt += f"\n\n[SYSTEM INFO] The user asked about order '{extracted_id}', but it was NOT FOUND in the database. Apologize and say the order ID is invalid."
        else:
            system_prompt += "\n\n[SYSTEM INFO] The user wants to track an order. Ask them to provide their Order ID in the format 'ORD-XXXX'."
        return system_prompt

    def _handle_track_demand(self, system_prompt: str, user_text: str) -> str:
        match = re.search(r'(?i)(DEM-\d{3})', user_text)
        if match:
            extracted_id = match.group(1).upper()
            demand_data = get_demand_details(extracted_id)
            if demand_data:
                system_prompt += (
                    f"\n\n[SYSTEM DATABASE INFO]\n"
                    f"Demand Found: {extracted_id}\n"
                    f"Requestor: {demand_data['requestor_name']}\n"
                    f"Department: {demand_data['department']}\n"
                    f"Status: {demand_data['status']}\n"
                    f"Priority: {demand_data['priority']}\n"
                    f"Budget: ${demand_data['estimated_budget']}\n\n"
                    f"Use this EXACT database information to answer the user's question about their demand status."
                )
            else:
                system_prompt += f"\n\n[SYSTEM INFO] The user asked about demand '{extracted_id}', but it was NOT FOUND in the database. Apologize and say the demand ID is invalid."
        else:
            system_prompt += "\n\n[SYSTEM INFO] The user wants to track a demand. Ask them to provide their Demand ID in the format 'DEM-XXX'."
        return system_prompt

    def _handle_project_status(self, system_prompt: str, user_text: str) -> str:
        match = re.search(r'(?i)(PRJ-\d{3})', user_text)
        if match:
            extracted_id = match.group(1).upper()
            project_data = get_project_details(extracted_id)
            if project_data:
                system_prompt += (
                    f"\n\n[SYSTEM DATABASE INFO]\n"
                    f"Project Found: {extracted_id}\n"
                    f"Name: {project_data['project_name']}\n"
                    f"Manager: {project_data['manager']}\n"
                    f"Status: {project_data['status']}\n"
                    f"Start Date: {project_data['start_date']}\n\n"
                    f"Use this EXACT database information to answer the user's question about the project status."
                )
            else:
                system_prompt += f"\n\n[SYSTEM INFO] The user asked about project '{extracted_id}', but it was NOT FOUND in the database. Apologize and say the project ID is invalid."
        else:
            system_prompt += "\n\n[SYSTEM INFO] The user wants to track a project. Ask them to provide their Project ID in the format 'PRJ-XXX'."
        return system_prompt

    def _handle_resource_availability(self, system_prompt: str, user_text: str) -> str:
        match = re.search(r'(?i)(RES-\d{3})', user_text)
        if match:
            extracted_id = match.group(1).upper()
            resource_data = get_resource_details(extracted_id)
            if resource_data:
                system_prompt += (
                    f"\n\n[SYSTEM DATABASE INFO]\n"
                    f"Resource Found: {extracted_id}\n"
                    f"Name: {resource_data['resource_name']}\n"
                    f"Role: {resource_data['role']}\n"
                    f"Availability: {resource_data['availability_status']}\n\n"
                    f"Use this EXACT database information to answer the user's question about the resource availability."
                )
            else:
                system_prompt += f"\n\n[SYSTEM INFO] The user asked about resource '{extracted_id}', but it was NOT FOUND in the database. Apologize and say the resource ID is invalid."
        else:
            system_prompt += "\n\n[SYSTEM INFO] The user wants to check resource availability. Ask them to provide the Resource ID in the format 'RES-XXX'."
        return system_prompt

    def _handle_update_order_status(self, system_prompt: str, user_text: str) -> str:
        match_id = re.search(r'(?i)(ORD-\d{4})', user_text)
        match_status = re.search(r'(?i)(shipped|processing|delivered|cancelled|pending)', user_text)
        if match_id and match_status:
            extracted_id = match_id.group(1).upper()
            new_status = match_status.group(1).capitalize()
            success = update_order_status(extracted_id, new_status)
            if success:
                system_prompt += f"\n\n[SYSTEM DATABASE INFO]\nSuccessfully updated order {extracted_id} to {new_status}.\nInform the user that the modification was successful."
            else:
                system_prompt += f"\n\n[SYSTEM DATABASE INFO]\nFailed to update order {extracted_id}. It might not exist.\nInform the user about the failure."
        else:
            system_prompt += "\n\n[SYSTEM INFO] The user wants to update an order. Ask them to provide the Order ID in the format 'ORD-XXXX' and the new status (Shipped, Processing, Delivered, Cancelled, Pending)."
        return system_prompt

    def _handle_update_demand_status(self, system_prompt: str, user_text: str) -> str:
        match_id = re.search(r'(?i)(DEM-\d{3})', user_text)
        match_status = re.search(r'(?i)(approved|rejected|draft|under review)', user_text)
        if match_id and match_status:
            extracted_id = match_id.group(1).upper()
            new_status = match_status.group(1).title()
            success = update_demand_status(extracted_id, new_status)
            if success:
                system_prompt += f"\n\n[SYSTEM DATABASE INFO]\nSuccessfully updated demand {extracted_id} to {new_status}.\nInform the user that the modification was successful."
            else:
                system_prompt += f"\n\n[SYSTEM DATABASE INFO]\nFailed to update demand {extracted_id}. It might not exist.\nInform the user about the failure."
        else:
            system_prompt += "\n\n[SYSTEM INFO] The user wants to update a demand. Ask them to provide the Demand ID in the format 'DEM-XXX' and the new status (Approved, Rejected, Draft, Under Review)."
        return system_prompt

    def _handle_refund(self, system_prompt: str, user_text: str) -> str:
        system_prompt += "\n\n[SYSTEM INFO] Processing standard refund queries. Inform the user they can return items within 30 days."
        return system_prompt

    def _call_llm(self, system_prompt: str, user_text: str, context_history: list, provider_override: str = None) -> str:
        full_prompt = f"{system_prompt}\n\nChat History:\n"
        full_prompt += "\n".join([f"{msg['role'].capitalize()}: {msg['content']}" for msg in context_history])
        full_prompt += f"\n\nUser: {user_text}\nAssistant:"

        active_provider = provider_override if provider_override else self.provider

        try:
            if active_provider == "groq":
                from groq import Groq
                client = Groq(api_key=config.GROQ_API_KEY)
                model = config.GROQ_MODEL 
                response = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": system_prompt},
                        *context_history,
                        {"role": "user", "content": user_text}
                    ],
                    model=model,
                    temperature=0.7,
                    max_tokens=250,
                )
                return response.choices[0].message.content
                
            elif active_provider == "gemini":
                from google import genai
                client = genai.Client(api_key=config.GEMINI_API_KEY)
                model = config.GEMINI_MODEL
                
                contents = [f"{msg['role']}: {msg['content']}" for msg in context_history]
                contents.append(f"system: {system_prompt}")
                contents.append(f"user: {user_text}")
                
                response = client.models.generate_content(
                    model=model,
                    contents="\n".join(contents),
                )
                return response.text
                
            elif active_provider in ["huggingface", "local_transformers"]:
                import requests
                API_URL = f"https://api-inference.huggingface.co/models/{config.HF_MODEL}"
                headers = {"Authorization": f"Bearer {config.HF_API_KEY}"}
                payload = {
                    "inputs": full_prompt,
                    "parameters": {"max_new_tokens": 100, "return_full_text": False}
                }
                res = requests.post(API_URL, headers=headers, json=payload)
                res.raise_for_status()
                
                result_data = res.json()
                if isinstance(result_data, list) and "generated_text" in result_data[0]:
                     return result_data[0]["generated_text"].strip()
                return str(result_data)
                
        except Exception as e:
            print(f"Reply Generation Error: {e}")
            return None

    def generate_reply(self, intent: str, user_text: str, context_history: list, provider: str = None) -> str:
        system_prompt = (
            f"You are a helpful customer support agent. "
            f"The user's query has been classified as the intent: {intent}. "
            f"Answer the user's question politely and concisely."
        )
        
        system_prompt = self._inject_dynamic_data(intent, system_prompt, user_text, context_history)
        
        reply = self._call_llm(system_prompt, user_text, context_history, provider_override=provider)
        
        if reply is None:
            return self.fallback_responses.get(intent, "I'm sorry, I didn't quite catch that. How can I help you?")
            
        return reply

# For backward compatibility, keep the function wrapper
_default_generator = BotReplyGenerator()

def generate_bot_reply(intent: str, user_text: str, context_history: list) -> str:
    return _default_generator.generate_reply(intent, user_text, context_history)
