from groq import Groq
import os
import json
import shutil
from datetime import datetime
import time
import argparse

def get_system_prompt():
    return """You are SRA-HelixForge v3.2.3.0, the hyper-mutant self-evolution engine and adaptive intelligence agent... [PASTE THE ENTIRE ORIGINAL STYLE GUIDE YOU RECEIVED IN YOUR SYSTEM PROMPT HERE — EVERYTHING from Core Mathematics & Biological Reference through Output Standards. It must be the full block so every generation is perfect HelixForge quality.] Always output ONLY valid JSON with the exact keys: product_name, price, description, prompt_pack, micro_tool_code, usage_guide."""

GROQ_KEYS = json.loads(os.getenv("GROQ_KEYS", "[]"))
if not GROQ_KEYS:
    raise ValueError("Add GROQ_KEYS secret as JSON array of strings")

def generate_product(niche):
    for attempt, key in enumerate(GROQ_KEYS):
        client = Groq(api_key=key)
        try:
            completion = client.chat.completions.create(
                model="qwen2.5-coder-32b",
                messages=[
                    {"role": "system", "content": get_system_prompt()},
                    {"role": "user", "content": f"Churn ONE premium zero-competition AI+Programming digital product for niche: {niche}. Price between 29-197. Include full evolving prompt pack and ready micro-tool code."}
                ],
                temperature=0.7,
                max_tokens=8000,
                response_format={"type": "json_object"}
            )
            product = json.loads(completion.choices[0].message.content)
            return product
        except Exception as e:
            if "429" in str(e).lower() or "rate limit" in str(e).lower():
                wait = (2 ** attempt) * 20
                time.sleep(wait)
                continue
    raise Exception("All keys exhausted — daily reset coming")

def save_product(product, idx):
    ts = datetime.now().strftime("%Y%m%d_%H%M")
    folder = f"products/{ts}_{product.get('product_name', 'ForgeProduct').replace(' ', '_')}"
    os.makedirs(folder, exist_ok=True)
    
    with open(f"{folder}/sales_page.md", "w") as f:
        f.write(f"# {product.get('product_name')}\n\n{product.get('description')}\n\n**Price:** ${product.get('price')}\n\nInstant download on Payhip.")
    
    with open(f"{folder}/prompt_pack.md", "w") as f:
        f.write(product.get('prompt_pack', '# Evolving HelixForge Prompts'))
    
    with open(f"{folder}/micro_tool.py", "w") as f:
        f.write(product.get('micro_tool_code', '# Your AI-powered micro-tool'))
    
    with open(f"{folder}/README.md", "w") as f:
        f.write(product.get('usage_guide', 'Full instructions'))
    
    shutil.make_archive(f"output/{ts}_{product.get('product_name')}", 'zip', folder)
    print(f"✅ Product {idx+1} ready")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--niche", default="AI_coding_agents")
    parser.add_argument("--num", type=int, default=3)
    args = parser.parse_args()
    
    print("🚀 OpportunityForge v3.1 LIVE on GitHub Actions")
    for i in range(args.num):
        prod = generate_product(args.niche)
        save_product(prod, i)
