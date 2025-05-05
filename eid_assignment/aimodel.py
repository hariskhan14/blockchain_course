class AIConfig:
    def __init__(self):
        # Replace with actual API key
        self.api_key = "please insert API Key here"
        self.model_name = "gemini-2.0-flash"
        self.temperature = 0.2
        self.max_tokens = 1024


class AIContractModifier:
    def __init__(self, ai_config):
        self.ai_config = ai_config
        genai.configure(api_key=ai_config.api_key)
        self.model = genai.GenerativeModel(
            model_name=ai_config.model_name,
            generation_config={
                "temperature": ai_config.temperature,
                "max_output_tokens": ai_config.max_tokens
            }
        )

    def create_prompt(self, current_contract, passenger_data):
        prompt = f"""
You are an AI that modifies Python smart contract code for a transportation fare system.
The current passenger count is {passenger_data['passenger_count']}.
The threshold for fare discount is 500 passengers.

Current contract code:
```python
{current_contract}
```

Please modify the code according to these rules:
1. If passenger count is below 500, set the discount_percentage to an appropriate value (10% for 400-499, 20% for 300-399, 30% for less than 300)
2. If passenger count is 500 or above, set discount_percentage to 0.0
3. Update only the discount_percentage and discount_threshold variables
4. Do not change any other part of the code

Return only the modified code with no explanations or markdown.
"""
        return prompt

    def modify_contract(self, current_contract, passenger_data):
        prompt = self.create_prompt(current_contract, passenger_data)
        response = self.model.generate_content(prompt)
        modified_code = response.text.strip()

        if "```python" in modified_code:
            modified_code = modified_code.split("```python")[1].split("```")[0].strip()
        elif "```" in modified_code:
            modified_code = modified_code.split("```")[1].split("```")[0].strip()

        return modified_code
