import os
import torch
import json
from transformers import AutoModelForCausalLM, AutoTokenizer, Trainer, TrainingArguments
from datasets import Dataset
from huggingface_hub import login

LOCAL_MODEL_DIR = "./fine_tuned_model"
print(torch.cuda.memory_allocated())
def main():
    token = "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"
    login(token)
    dataset_path = "vhdl_dataset.json"
    raw_dataset = Dataset.from_json(dataset_path)
    model_name = "EleutherAI/gpt-neo-125m"
    tokenizer = AutoTokenizer.from_pretrained(model_name, token = True)
    tokenizer.pad_token = tokenizer.eos_token
    def tokenize_function(examples):
        tokenized = tokenizer(
            examples['code'],
            padding="max_length",  
            truncation=True,       
            max_length=1024         
        )
        tokenized["labels"] = tokenized["input_ids"].copy()
        return tokenized
    tokenized_dataset = raw_dataset.map(tokenize_function, batched=True)

    train_test_split = tokenized_dataset.train_test_split(test_size=0.1)
    train_dataset = train_test_split['train']
    val_dataset = train_test_split['test']
    print(torch.cuda.memory_allocated())
    model = AutoModelForCausalLM.from_pretrained().cuda()
    training_args = TrainingArguments(
        output_dir="./results",               # Directory for saving model checkpoints
        evaluation_strategy="steps",          # Validate every few steps
        eval_steps=1000,                      # Validation step interval
        save_strategy="steps",                # Save model every few steps
        save_steps=1000,                      # Save interval
        learning_rate=5e-5,                   # Initial learning rate
        per_device_train_batch_size=4,        # Batch size per GPU
        gradient_accumulation_steps=4,        # Simulate larger batch size
        num_train_epochs=3,                   # Total number of epochs
        weight_decay=0.01,                    # Regularization to avoid overfitting
        fp16=True,                            # Enable mixed precision
        logging_dir="./logs",                 # Directory for logs
        logging_steps=100,                    # Log training metrics every 100 steps
        save_total_limit=2,                   # Max number of saved checkpoints
        load_best_model_at_end=True,          # Reload best model after training
        metric_for_best_model="loss",         # Use loss for model comparison
        greater_is_better=False,              # Lower loss is better
    )

    trainer = Trainer(
		model=model,
		args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
		tokenizer=tokenizer,
		)
		
    torch.cuda.empty_cache()
    trainer.train()
    trainer.save_model(LOCAL_MODEL_DIR)
    print(f"Model saved locally at {LOCAL_MODEL_DIR}")

if __name__ == "__main__":
	main()
