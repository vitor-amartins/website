def get_color(value):
    COLORS = ["laranja", "verde", "rosa", "azul"]
    if value >= 0 and value < len(COLORS):
        return COLORS[value]
    return None
