from dataclasses import dataclass


@dataclass
class Champion:
    name: str
    available: bool
    image_url: str
    tags: list[str]

    def __repr__(self) -> str:
        return self.name
