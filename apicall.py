from google import genai
import test

API_KEY = ""

client = genai.Client(api_key=API_KEY)

with open("router_config192.168.8.151.txt", "r", encoding="utf-8") as f:
    config = f.read()

prompt = f"""
Analyze this Cisco router configuration from a cybersecurity perspective.

Identify:
1. Security weaknesses
2. Missing security controls
3. Misconfigurations
4. Potential vulnerabilities
5. Recommended fixes
6. Tell me in a list what I have configured

Cisco configuration:

{config}
"""

response = client.models.generate_content(
    model="gemini-3.6-flash",
    contents=prompt
)

print(response.text)

with open(f"analysis_{test.HOST}.txt", "w", encoding="utf-8") as f:
    f.write(response.text)