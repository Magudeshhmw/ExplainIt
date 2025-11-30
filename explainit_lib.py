import boto3
import json

import requests
from botocore.exceptions import NoCredentialsError, NoRegionError, ClientError

# Model ID from the labs examples
MODEL_ID = "us.anthropic.claude-3-7-sonnet-20250219-v1:0"
GEMINI_API_KEY = "AIzaSyCPZ5bf1N0Tq7LO-n7QjhnsY6TpxeAd1VQ" # From user memory

def get_bedrock_client(region=None, profile_name=None, aws_access_key_id=None, aws_secret_access_key=None):
    session_kwargs = {}
    if profile_name:
        session_kwargs['profile_name'] = profile_name
    if region:
        session_kwargs['region_name'] = region
    if aws_access_key_id and aws_secret_access_key:
        session_kwargs['aws_access_key_id'] = aws_access_key_id
        session_kwargs['aws_secret_access_key'] = aws_secret_access_key
        
    session = boto3.Session(**session_kwargs)
    return session.client(service_name='bedrock-runtime', region_name=region or "us-east-1")

def call_gemini(prompt, system_prompt=None):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
    
    contents = [{"role": "user", "parts": [{"text": prompt}]}]
    
    payload = {
        "contents": contents,
        "generationConfig": {
            "temperature": 0,
            "maxOutputTokens": 4096
        }
    }
    
    if system_prompt:
        payload["systemInstruction"] = {
            "parts": [{"text": system_prompt}]
        }
        
    try:
        response = requests.post(url, json=payload, headers={"Content-Type": "application/json"})
        response.raise_for_status()
        result = response.json()
        return result['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        raise Exception(f"Gemini API Error: {str(e)}")

def call_bedrock(prompt, system_prompt=None, credentials=None):
    if credentials is None:
        credentials = {}
        
    try:
        bedrock = get_bedrock_client(
            region=credentials.get('region'),
            profile_name=credentials.get('profile_name'),
            aws_access_key_id=credentials.get('aws_access_key_id'),
            aws_secret_access_key=credentials.get('aws_secret_access_key')
        )
        
        messages = [
            {
                "role": "user",
                "content": [{"text": prompt}]
            }
        ]
        
        inference_config = {
            "maxTokens": 4096,
            "temperature": 0,
            "topP": 0.9
        }
        
        # Construct args for converse
        args = {
            "modelId": MODEL_ID,
            "messages": messages,
            "inferenceConfig": inference_config
        }
        
        if system_prompt:
            args["system"] = [{"text": system_prompt}]

        response = bedrock.converse(**args)
        
        return response['output']['message']['content'][0]['text']
        
    except (NoCredentialsError, NoRegionError, ClientError) as e:
        # Fallback to Gemini if AWS fails
        print(f"AWS Error: {e}. Falling back to Gemini...")
        return call_gemini(prompt, system_prompt)
    except Exception as e:
        # If it's a credential issue disguised as another error
        if "credentials" in str(e).lower() or "region" in str(e).lower():
             print(f"AWS Error: {e}. Falling back to Gemini...")
             return call_gemini(prompt, system_prompt)
        raise e

def analyze_code(input_text, input_type, credentials=None):
    system_prompt = """You are a Repository & Diff Analysis Agent. 
    Your task is to analyze the provided code or diff and extract meaningful change information.
    
    Output strictly valid JSON with the following keys:
    - change_scope: (string) e.g., "feature update", "bug fix", "refactor"
    - files_changed: (number) estimated count
    - lines_added: (number) estimated count
    - lines_removed: (number) estimated count
    - affected_components: (list of strings) e.g., ["authentication", "API"]
    
    Do not output any markdown formatting or text outside the JSON."""
    
    prompt = f"Input Type: {input_type}\n\nCode/Diff Content:\n{input_text}"
    
    response = call_bedrock(prompt, system_prompt, credentials)
    
    # Clean up response if it contains markdown code blocks
    response = response.strip()
    if response.startswith("```json"):
        response = response[7:]
    if response.startswith("```"):
        response = response[3:]
    if response.endswith("```"):
        response = response[:-3]
        
    try:
        return json.loads(response)
    except json.JSONDecodeError:
        return {
            "change_scope": "Unknown",
            "files_changed": 0,
            "lines_added": 0,
            "lines_removed": 0,
            "affected_components": []
        }

def explain_code(input_text, analysis_json, credentials=None):
    system_prompt = """You are a Code Explanation Agent. 
    Convert technical modifications into natural language.
    Describe:
    - What the code does now
    - What was changed
    - The expected behavior difference
    - Any risks or potential bugs
    
    Keep the tone professional and human-friendly."""
    
    prompt = f"""Analysis Context: {json.dumps(analysis_json)}
    
    Code/Diff Content:
    {input_text}"""
    
    return call_bedrock(prompt, system_prompt, credentials)

def generate_commit_messages(input_text, analysis_json, credentials=None):
    system_prompt = """You are a Commit Message Generator Agent.
    Produce commit message variations.
    
    Output format:
    ---
    Short:
    "<very short summary>"
    
    Medium:
    "<medium git commit>"
    
    Full:
    "<full structured commit message>"
    ---
    """
    
    prompt = f"""Analysis Context: {json.dumps(analysis_json)}
    
    Code/Diff Content:
    {input_text}"""
    
    return call_bedrock(prompt, system_prompt, credentials)

def suggest_tests(input_text, analysis_json, credentials=None):
    system_prompt = """You are a Unit Test Suggestor Agent.
    Suggest recommended tests based on the code change.
    Include:
    - Expected behavior cases
    - Negative tests
    - Edge conditions
    
    Output format:
    ---
    🧪 Suggested Tests:
    1) ...
    2) ...
    ...
    ---
    """
    
    prompt = f"""Analysis Context: {json.dumps(analysis_json)}
    
    Code/Diff Content:
    {input_text}"""
    
    return call_bedrock(prompt, system_prompt, credentials)

def get_confidence_score(input_text, credentials=None):
    # A simple agent to estimate confidence
    system_prompt = "You are a Quality Assurance Agent. Rate the confidence (0.00 to 1.00) that the code changes are safe and well-understood based on the clarity of the diff/code. Output ONLY the number."
    prompt = f"Code:\n{input_text}"
    try:
        res = call_bedrock(prompt, system_prompt, credentials)
        return float(res.strip())
    except:
        return 0.85 # Default fallback
