import os
import torch
import gc
import pandas as pd
from datasets import Dataset
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig, TrainingArguments, pipeline
from peft import LoraConfig, PeftModel
from trl import SFTTrainer

# Step 1: Load and Format WhatsApp Dataset
df = pd.read_csv('whatsapp_dataset.csv')  # Ensure the dataset is in CSV format
dataset = Dataset.from_pandas(df)
dataset = dataset.map(lambda x: {"text": f"### Question: {x['question']}\n### Answer: {x['answer']}"})

# Step 2: Initialize Dolphin 3 Model & Tokenizer
model_name = "cognitivecomputations/dolphin-2.6-mistral"  # Replace with Dolphin-3 when available
tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)

# LoRA Configuration for Efficient Fine-Tuning
peft_config = LoraConfig(
    lora_alpha=16,
    lora_dropout=0.1,
    r=64,
    task_type="CAUSAL_LM"
)

# Load Base Model with Quantization (for lower VRAM usage)
base_model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.float16,
    device_map="auto",
    quantization_config=BitsAndBytesConfig(load_in_4bit=True)
)

# Step 3: Define Training Arguments
training_args = TrainingArguments(
    output_dir="./dolphin3_finetuned",
    per_device_train_batch_size=2,
    gradient_accumulation_steps=4,
    num_train_epochs=3,
    learning_rate=2e-4,
    fp16=True,
    save_strategy="epoch",
    save_total_limit=2,
    logging_dir="./logs",
    logging_steps=10,
    report_to="none"  # Change to "wandb" if using Weights & Biases
)

# Step 4: Fine-Tune the Model
trainer = SFTTrainer(
    model=base_model,
    train_dataset=dataset,
    peft_config=peft_config,
    tokenizer=tokenizer,
    args=training_args
)

trainer.train()

# Step 5: Save Fine-Tuned Model Locally
trainer.model.save_pretrained('finetuned_dolphin3')

# Step 6: Evaluate & Inference
pipe = pipeline('text-generation', model=trainer.model, tokenizer=tokenizer)
output = pipe("### Question: What is your name?")[0]['generated_text']
print(output)

# Step 7: Free Up Memory
del base_model, trainer, pipe
gc.collect()

# Step 8: Merge LoRA with Base Model & Upload to Hugging Face Hub
base_model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=torch.float16)
model = PeftModel.from_pretrained(base_model, 'finetuned_dolphin3')
model = model.merge_and_unload()

# Step 9: Push Fine-Tuned Model to Hugging Face Hub
# model.push_to_hub("your_huggingface_username/finetuned_dolphin3")
# tokenizer.push_to_hub("your_huggingface_username/finetuned_dolphin3")

print("✅ Fine-tuned Dolphin 3 model saved & uploaded!")
