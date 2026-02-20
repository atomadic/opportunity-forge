from groq import Groq
import os
import json
import shutil
from datetime import datetime
import time
import argparse

def get_system_prompt():
    return """You are SRA-HelixForge v3.2.3.0, the hyper-mutant self-evolution engine... [PASTE FULL ORIGINAL STYLE GUIDE HERE — Core Mathematics through Output Standards]. Always output ONLY valid JSON."""

GROQ_KEYS = json.loads(os.getenv("GROQ_KEYS", "[]"))
print(f"🔑 Loaded {len(GROQ_KEYS)} keys from secret")

def generate_product(niche):
    if not GROQ_KEYS:
        raise ValueError("❌ GROQ_KEYS secret is empty or missing. Add it now!")
    for attempt, key in enumerate(GROQ_KEYS):
        print(f"🔄 Trying key {attempt+1}/{len(GROQ_KEYS)} ...")
        try:
            client = Groq(api_key=key)
            completion = client.chat.completions.create(
                model="qwen2.5-coder-32b",
                messages=[
                    {"role": "system", "content": get_system_prompt()},
                    {"role": "user", "content": f"Churn ONE premium AI+Programming digital product for niche: {niche}. Price $29-197. Include full prompt pack + micro-tool code."}
                ],
                temperature=0.7,
                max_tokens=8000,
                response_format={"type": "json_object"}
            )
            product = json.loads(completion.choices[0].message.content)
            print(f"✅ SUCCESS with key {attempt+1}")
            return product
        except Exception as e:
            err = str(e).lower()
            print(f"   ❌ Key {attempt+1} failed: {type(e).__name__} — {err[:200]}")
            if "429" in err or "rate limit" in err:
                wait = (2 ** attempt) * 30
                print(f"   ⏳ Rate limit — waiting {wait}s")
                time.sleep(wait)
                continue
    raise Exception("All keys exhausted — create fresh keys and update secret")

def save_product(product, idx):
    ts = datetime.now().strftime("%Y%m%d_%H%M")
    folder = f"products/{ts}_{product.get('product_name', 'ForgeProduct').replace(' ', '_')}"
    os.makedirs(folder, exist_ok=True)
    
    with open(f"{folder}/sales_page.md", "w") as f:
        f.write(f"# {product.get('product_name')}\n\n{product.get('description')}\n\n**Price:** ${product.get('price')}\n\nInstant Payhip download.")
    
    with open(f"{folder}/prompt_pack.md", "w") as f:
        f.write(product.get('prompt_pack', ''))
    
    with open(f"{folder}/micro_tool.py", "w") as f:
        f.write(product.get('micro_tool_code', '# Micro-tool code here'))
    
    with open(f"{folder}/README.md", "w") as f:
        f.write(product.get('usage_guide', ''))
    
    shutil.make_archive(f"output/{ts}_{product.get('product_name')}", 'zip', folder)
    print(f"🎉 Product {idx+1} saved to {folder}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--niche", default="AI_coding_agents")
    parser.add_argument("--num", type=int, default=3)
    args = parser.parse_args()
    
    print("🚀 OpportunityForge v3.2 DEBUG MODE starting...")
    for i in range(args.num):
        prod = generate_product(args.niche)
        save_product(prod, i)
    print("✅ All products churned — ready for Payhip!")    print("🚀 OpportunityForge v3.1 LIVE on GitHub Actions")
    for i in range(args.num):
        prod = generate_product(args.niche)
        save_product(prod, i)
