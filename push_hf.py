from huggingface_hub import HfApi

print("Starting upload to Hugging Face...")
api = HfApi()

api.create_repo(
    repo_id="Friday425/resume-matching-system",
    repo_type="space",
    space_sdk="docker",
    exist_ok=True
)

api.upload_folder(
    folder_path=".",
    repo_id="Friday425/resume-matching-system",
    repo_type="space",
    ignore_patterns=[".git/*", "__pycache__/*", "candidates.db", "uploads/*", ".env", "push_hf.py"]
)
print("Upload complete!")
