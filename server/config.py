import json
import os


class Config:
    fallback = "500 Error"

    def __init__(self, config_dir: str) -> None:
        self.config_dir = config_dir
        self.whoami = {
            "text1": self.fallback,
            "text2": self.fallback,
        }
        self.projects = [
            {
                "name": self.fallback,
                "desc": self.fallback,
                "url": self.fallback,
                "img": "https://placehold.co/600x400",
            },
        ]
        self.hobbies = [{"name": self.fallback, "percent": 100}]
        self.knowledge = [{"name": self.fallback, "percent": 100}]
        self.timeline = [
            {"year": "2023", "event": self.fallback},
        ]
        self.general_footer = {
            "name": self.fallback,
            "git_url": self.fallback,
            "contact": [
                {
                    "href": "mailto:" + self.fallback,
                    "text": self.fallback,
                },
            ],
            "footer_text": self.fallback,
            # Copyright is hardcoded on the website. Because it won't change, no need to put it in the config
            # The "easter egg" is also hardcoded on the website, because it has CSS.
        }

        self.load_config()

    def load_config(self) -> None:
        os.makedirs(self.config_dir, exist_ok=True)
        self.whoami = self.load_single_config("whoami.json", self.whoami)
        self.projects = self.load_single_config("projects.json", self.projects)
        self.hobbies = self.load_single_config("hobbies.json", self.hobbies)
        self.knowledge = self.load_single_config("knowledge.json", self.knowledge)
        self.timeline = self.load_single_config("timeline.json", self.timeline)
        self.general_footer = self.load_single_config(
            "general_footer.json", self.general_footer
        )

    def set_config(self, config_name: str, config_data: dict | list) -> None:
        if config_name not in [
            "whoami",
            "projects",
            "hobbies",
            "knowledge",
            "timeline",
            "general_footer",
        ]:
            return
        with open(f"{self.config_dir}/{config_name}.json", "w") as f:
            json.dump(config_data, f, indent=4)
        self.load_config()  # Reload the config

    def load_single_config(self, filename: str, if_not_found_default) -> dict:
        try:
            with open(f"{self.config_dir}/{filename}", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            with open(f"{self.config_dir}/{filename}", "w") as f:
                json.dump(if_not_found_default, f, indent=4)
            return if_not_found_default
