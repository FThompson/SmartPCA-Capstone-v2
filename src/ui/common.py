import ui.fonts as fonts
from ui.colors import Color

def render_question(screen, lines, y_start=68):
    font = fonts.get_font(fonts.FontType.ROBOTO_MEDIUM.value, 36)
    relative_y = 0
    for line in lines:
        text = font.render(line, True, Color.RIIT_DARKER_GRAY.value, Color.WHITE.value)
        centered_rect = center(text, 0, y_start + relative_y, screen.get_width())
        screen.blit(text, centered_rect)
        relative_y += 48

# returns rectangle to be passed to screen.blit with surface
# pass 0 to width for only-vertical centering, 0 to height for only-horizontal centering
def center(surface, x, y, w=0, h=0):
    return surface.get_rect(center=(x + w / 2, y + h / 2))
