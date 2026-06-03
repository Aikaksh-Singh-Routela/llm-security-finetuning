# finetune_security.py - Fine-tune Llama on security data
import json
import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TrainingArguments,
    Trainer,
    BitsAndBytesConfig
)
from datasets import Dataset
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
import os

print("🚀 Starting Security LLM Fine-tuning...")

# Check if GPU is available
print(f"CUDA available: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"GPU: {torch.cuda.get_device_name(0)}")

# Load dataset
print("\n📚 Loading security dataset...")
with open('security_dataset.json', 'r') as f:
    data = json.load(f)

# Format data for training
formatted_data = []
for item in data:
    text = f"""### Instruction: {item['instruction']}

### Input: {item['input']}

### Output: {item['output']}"""
    formatted_data.append({"text": text})

dataset = Dataset.from_list(formatted_data)
print(f"✅ Loaded {len(dataset)} examples")

# Split into train/eval
dataset = dataset.train_test_split(test_size=0.2)
train_dataset = dataset["train"]
eval_dataset = dataset["test"]

print(f"Train: {len(train_dataset)}, Eval: {len(eval_dataset)}")

# Model configuration (using smaller model for local training)
MODEL_NAME = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"  # 1.1B parameters - runs on CPU

print(f"\n📥 Loading model: {MODEL_NAME}")

# Load tokenizer
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
tokenizer.pad_token = tokenizer.eos_token

# Load model (quantized for efficiency)
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

# Prepare model for training
model = prepare_model_for_kbit_training(model)

# LoRA configuration
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

# Tokenization function
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

# Training arguments
training_args = TrainingArguments(
    output_dir="./security-llm-model",
    num_train_epochs=10,
    per_device_train_batch_size=1,
    per_device_eval_batch_size=1,
    warmup_steps=5,
    logging_steps=5,
    eval_steps=10,
    save_steps=50,
    evaluation_strategy="steps",
    save_strategy="steps",
    learning_rate=2e-4,
    fp16=True,
    report_to="none",
)

# Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_train,
    eval_dataset=tokenized_eval,
    tokenizer=tokenizer,
)

# Train
print("\n🚀 Starting training...")
trainer.train()

# Save model
print("\n💾 Saving model...")
trainer.save_model("./security-llm-final")
tokenizer.save_pretrained("./security-llm-final")

print("\n✅ Fine-tuning complete!")