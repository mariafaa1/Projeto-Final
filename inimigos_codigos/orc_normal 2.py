from .base import InimigoBase

class OrcNormal(InimigoBase):
    def __init__(self, x, y, alvo):
        super().__init__(
            x=x,
            y=y,
            hp_max=100,  # HP ajustável
            velocidade=1,  # Velocidade de movimento
            alvo=alvo
        )