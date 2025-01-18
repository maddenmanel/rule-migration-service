from transformers import T5ForConditionalGeneration, T5Tokenizer, Trainer, TrainingArguments
from datasets import Dataset
import os
import json

def fine_tune_model(data_file: str, model_dir: str = "./model", model_name: str = "t5-large"):
    """
    Fine-tune the T5 model using data from a specified file.

    Args:
        data_file (str): Path to the training data file (JSON format).
        model_dir (str): Directory to save the fine-tuned model.
        model_name (str): Pre-trained T5 model name.
    """
    try:
        # Load training data
        if not os.path.exists(data_file):
            raise ValueError(f"Training data file '{data_file}' not found.")
        
        with open(data_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        dataset = Dataset.from_dict(data)
        tokenizer = T5Tokenizer.from_pretrained(model_name, legacy=False)
        model = T5ForConditionalGeneration.from_pretrained(model_name, use_cache=False)

        def preprocess_data(examples):
            inputs = tokenizer(examples["input_text"], max_length=512, truncation=True, padding="max_length")
            labels = tokenizer(examples["output_text"], max_length=512, truncation=True, padding="max_length").input_ids
            inputs["labels"] = labels
            return inputs

        train_dataset = dataset.map(preprocess_data, batched=True)

        training_args = TrainingArguments(
            output_dir="./results",
            num_train_epochs=5,
            per_device_train_batch_size=16,  # Use smaller batch size
            gradient_accumulation_steps=8, 
            save_steps=500,
            save_total_limit=2,
            logging_dir='./logs',
            eval_strategy ="no",
        )

        trainer = Trainer(
            model=model,
            args=training_args,
            train_dataset=train_dataset,
        )

        trainer.train()

        # Save fine-tuned model
        model.save_pretrained(model_dir)
        tokenizer.save_pretrained(model_dir)

        print(f"Model fine-tuned and saved at '{model_dir}'")
    except Exception as e:
        print(f"Error during training: {str(e)}")


if __name__ == "__main__":
    training_file = "app/training_data.json"
    fine_tune_model(data_file=training_file)