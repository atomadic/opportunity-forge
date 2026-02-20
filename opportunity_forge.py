from groq import Groq
import os
import json
import shutil
from datetime import datetime
import time
import argparse

def get_system_prompt():
    return """You are SRA-HelixForge v3.2.3.0, the hyper-mutant self-evolution engine... Always apply full Revelation Engine, WaC Lang RSI, E₈ grounding. Generate ONE premium AI+Programming digital product. Output ONLY valid JSON with keys: product_name, price, description, prompt_pack, micro_tool_code, usage_guide."""

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
print(f"🔑 Using single Groq key (length: {len(GROQ_API_KEY) if GROQ_API_KEY else 0})")

def generate_product(niche):
    if not GROQ_API_KEY:
        raise ValueError("❌ GROQ_API_KEY secret is missing. Add your single fresh key now!")
    print("🔄 Generating with single key...")
    client = Groq(api_key=GROQ_API_KEY)
    completion = client.chat.completions.create(
        model="qwen2.5-coder-32b",
        messages=[
            {"role": "system", "content": get_system_prompt()},
            {"role": "user", "content": f"Churn ONE premium zero-competition AI+Programming digital product for niche: {niche}. Price $29-197. Include full evolving prompt pack + ready micro-tool code."}
        ],
        temperature=0.7,
        max_tokens=8000,
        response_format={"type": "json_object"}
    )
    product = json.loads(completion.choices[0].message.content)
    print("✅ SUCCESS — product generated!")
    return product

def save_product(product, idx):
    ts = datetime.now().strftime("%Y%m%d_%H%M")
    folder = f"products/{ts}_{product.get('product_name', 'ForgeProduct').replace(' ', '_')}"
    os.makedirs(folder, exist_ok=True)
    
    with open(f"{folder}/sales_page.md", "w") as f:
        f.write(f"# {product.get('product_name')}\n\n{product.get('description')}\n\n**Price:** ${product.get('price')}\n\nInstant Payhip download.")
    
    with open(f"{folder}/prompt_pack.md", "w") as f:
        f.write(product.get('prompt_pack', ''))
    
    with open(f"{folder}/micro_tool.py", "w") as f:
        f.write(product.get('micro_tool_code', '# Your micro-tool'))
    
    with open(f"{folder}/README.md", "w") as f:
        f.write(product.get('usage_guide', ''))
    
    shutil.make_archive(f"output/{ts}_{product.get('product_name')}", 'zip', folder)
    print(f"🎉 Product {idx+1} saved!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--niche", default="AI_coding_agents")
    parser.add_argument("--num", type=int, default=3)
    args = parser.parse_args()
    
    print("🚀 OpportunityForge v3.4 SINGLE-KEY MODE starting...")
    for i in range(args.num):
        prod = generate_product(args.niche)
        save_product(prod, i)
    print("✅ All products churned — ready for Payhip!")
