def get_color(value):
    COLORS = ["laranja", "verde", "rosa", "azul"]
    if value >= 0 and value < len(COLORS):
        return COLORS[value]
    return None

COLOR_CHOICES = (
    (0, get_color(0)),
    (1, get_color(1)),
    (2, get_color(2)),
    (3, get_color(3))
)
