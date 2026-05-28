from pathlib import Path

class PromptLoader:
    def __init__(self, prompt_dir: str = "app/prompts/text"):
        self.prompt_dir = Path(prompt_dir)

    def load_instructions(self, prompt_type: str) -> str:
        path = self.prompt_dir / f"{prompt_type}.txt"

        if not path.exists():
            raise FileExistsError(f"Prompt file not found: {path}")
        
        return path.read_text(encoding="utf-8")
        