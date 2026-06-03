# finetune_security_fixed_v2.py - Working fine-tuning script
import json
import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TrainingArguments,
    Trainer,
    BitsAndBytesConfig,
    DataCollatorForLanguageModeling
)
from datasets import Dataset
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
import os

print("🚀 Starting Security LLM Fine-tuning...")
print(f"CUDA available: {torch.cuda.is_available()}")

# Load dataset
print("\n📚 Loading security dataset...")
with open('security_dataset.json', 'r') as f:
    data = json.load(f)

# Format data
formatted_data = []
for item in data:
    text = f"""### Instruction: {item['instruction']}

### Input: {item['input']}

### Output: {item['output']}"""
    formatted_data.append({"text": text})

dataset = Dataset.from_list(formatted_data)
print(f"✅ Loaded {len(dataset)} examples")

# Split
dataset = dataset.train_test_split(test_size=0.2)
train_dataset = dataset["train"]
eval_dataset = dataset["test"]

print(f"Train: {len(train_dataset)}, Eval: {len(eval_dataset)}")

# Model
MODEL_NAME = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
print(f"\n📥 Loading model: {MODEL_NAME}")

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
tokenizer.pad_token = tokenizer.eos_token

# 4-bit quantization
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16,
)

model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    quantization_config=bnb_config,
    device_map="auto",
    trust_remote_code=True,
)

model = prepare_model_for_kbit_training(model)

# LoRA config
lora_config = LoraConfig(
    r=8,
    lora_alpha=16,
    target_modules=["q_proj", "v_proj", "k_proj", "o_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM",
)

model = get_peft_model(model, lora_config)
model.print_trainable_parameters()

# Tokenize function
def tokenize_function(examples):
    return tokenizer(
        examples["text"],
        truncation=True,
        padding="max_length",
        max_length=256,
    )

print("\n🔄 Tokenizing dataset...")
tokenized_train = train_dataset.map(tokenize_function, batched=True)
tokenized_eval = eval_dataset.map(tokenize_function, batched=True)

# Data collator (replaces passing tokenizer directly)
data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

# Training arguments
training_args = TrainingArguments(
    output_dir="./security-llm-model",
    num_train_epochs=10,
    per_device_train_batch_size=1,
    per_device_eval_batch_size=1,
    warmup_steps=5,
    logging_steps=5,
    eval_strategy="steps",
    eval_steps=10,
    save_steps=50,
    learning_rate=2e-4,
    fp16=False,  # Set to False for CPU training
    report_to="none",
)

# Trainer (without tokenizer argument)
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_train,
    eval_dataset=tokenized_eval,
    data_collator=data_collator,
)

# Train
print("\n🚀 Starting training...")
trainer.train()

# Save
print("\n💾 Saving model...")
trainer.save_model("./security-llm-final")
tokenizer.save_pretrained("./security-llm-final")

print("\n✅ Fine-tuning complete!")