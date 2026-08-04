from dataclasses import dataclass, field


@dataclass
class Result:
    success: bool
    errors: list[str] = field(default_factory=list)