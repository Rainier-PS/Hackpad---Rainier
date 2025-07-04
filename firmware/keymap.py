import board
from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.matrix import DiodeOrientation
from kmk.modules.encoder import EncoderHandler
from kmk.modules.layers import Layers
from kmk.modules.combos import Combos, Chord
from kmk.modules.rgb import RGB
from kmk.extensions.OLED import OLED, OLEDExtension
from display.draw import draw_oled

keyboard = KMKKeyboard()
keyboard.diode_orientation = DiodeOrientation.COL2ROW

# --- Pin Mapping based on your schematic ---
keyboard.col_pins = (board.GP3, board.GP4, board.GP2)
keyboard.row_pins = (board.GP26, board.GP27, board.GP28)

# --- Modules ---
layers = Layers()
keyboard.modules.append(layers)

# --- Keymap (Layer 0 and Layer 1) ---
keyboard.keymap = [
    [  # Layer 0 – Shortcuts and Media
        KC.MPRV, KC.MPLY, KC.MNXT,
        KC.UNDO, KC.REDO, KC.SAVE,
        KC.COPY, KC.PASTE, KC.CUT,
    ],
    [  # Layer 1 – Numpad
        KC.N7, KC.N8, KC.N9,
        KC.N4, KC.N5, KC.N6,
        KC.N1, KC.N2, KC.N3,
    ],
]

# --- Encoder Setup ---
encoder_handler = EncoderHandler()
encoder_handler.pins = ((board.GP29, board.GP0),)  # A, B
keyboard.modules.append(encoder_handler)

# --- Encoder Modes ---
encoder_modes = [
    [KC.VOLD, KC.VOLU],         # 0: Volume
    [KC.ZOOM_OUT, KC.ZOOM_IN],  # 1: Zoom
    [KC.BRIGHTNESS_DOWN, KC.BRIGHTNESS_UP],  # 2: Brightness
    [KC.LEFT, KC.RIGHT],        # 3: Scrubbing
]
encoder_mode = 0
encoder_handler.map = [encoder_modes[encoder_mode]]

def cycle_encoder_mode():
    global encoder_mode
    encoder_mode = (encoder_mode + 1) % len(encoder_modes)
    encoder_handler.map = [encoder_modes[encoder_mode]]
    update_oled()

# --- RGB LED Setup (SK6812/WS2812 on GP1) ---
rgb = RGB(pixel_pin=board.GP1, num_pixels=16, hue_default=0, sat_default=255, val_default=32, val_limit=100)
keyboard.extensions.append(rgb)

led_mode = 0
def cycle_led_mode():
    global led_mode
    led_mode = (led_mode + 1) % 4
    modes = ['off', 'solid', 'breathing', 'rainbow']
    mode = modes[led_mode]

    if mode == 'off':
        rgb.disable()
    elif mode == 'solid':
        rgb.mode = rgb.MODE_STATIC
        rgb.enable()
    elif mode == 'breathing':
        rgb.mode = rgb.MODE_BREATHING
        rgb.enable()
    elif mode == 'rainbow':
        rgb.mode = rgb.MODE_RAINBOW
        rgb.enable()
    update_oled()

# --- OLED Setup ---
oled = OLED(driver=OLEDExtension(), position=(0, 0), draw_function=draw_oled)
keyboard.extensions.append(oled)

def update_oled():
    oled.display_text = f'Layer: {keyboard.active_layers[0]}\n' \
                        f'Encoder: {["Volume", "Zoom", "Bright", "Scrub"][encoder_mode]}\n' \
                        f'LED Mode: {["Off", "Solid", "Breath", "Rainbow"][led_mode]}'

update_oled()

# --- Combos ---
combos = Combos(combos=[
    # Key Layer toggle: K1 + K7 (MPLY + PASTE)
    Chord((KC.MPLY, KC.PASTE), KC.TO((keyboard.active_layers[0] + 1) % 2)),

    # Encoder Mode toggle: K2 + K6 (MNXT + REDO)
    Chord((KC.MNXT, KC.REDO), KC.NO),  # Trigger manually

    # LED Mode toggle: K3 + K5 (SAVE + COPY)
    Chord((KC.SAVE, KC.COPY), KC.NO),
])
keyboard.modules.append(combos)

# --- Encoder Button Override via Matrix (we detect it manually) ---
last_encoder_switch_state = False

@keyboard.on_matrix_scan
def encoder_switch_handler(kbd):
    global last_encoder_switch_state

    # Get matrix state for encoder switch location
    encoder_switch_pos = (2, 0)  # Example: ROW2, COL0 — adjust if different!
    row, col = encoder_switch_pos
    is_pressed = kbd.matrix[row][col]

    if is_pressed and not last_encoder_switch_state:
        cycle_encoder_mode()
    last_encoder_switch_state = is_pressed

# --- Combo triggers in runtime loop ---
@keyboard.on_runtime_update
def runtime_update(kbd):
    if kbd.combos.pressed((KC.MNXT, KC.REDO)):
        cycle_encoder_mode()
        kbd.combos.clear_combo_keys()

    if kbd.combos.pressed((KC.SAVE, KC.COPY)):
        cycle_led_mode()
        kbd.combos.clear_combo_keys()

if __name__ == '__main__':
    keyboard.go()
