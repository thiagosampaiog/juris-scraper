from pydantic import BaseModel, field_validator

class CollectInput(BaseModel):
    cnjs: list[str]

    @field_validator("cnjs")
    @classmethod
    def validate_cnjs(cls, value: list[str]) -> list[str]:
        for cnj in value:
            digits_only = cnj.replace(".", "").replace("-", "")
            if not digits_only.isdigit() or len(digits_only) != 20:
                raise ValueError(f"{cnj}: CNJ deve ter 20 dígitos numéricos")
        return value