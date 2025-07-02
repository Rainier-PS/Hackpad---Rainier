# Xiao 3x3 Pad

A compact 3x3 macropad with an encoder, OLED screen, RGB backlight, and multiple keymap layers. Built using KMK firmware and Seeed XIAO RP2040. Designed for shortcuts, media control, number input, and visual layer feedback.

## Features

- 3×3 key matrix (9 physical keys)
- EC11 rotary encoder with push switch
- Layer switching via encoder press or key combo
- OLED screen for layer/mode display
- WS2812B LED backlight with multiple brightness modes
- KMK firmware (Python-based, flexible and beginner-friendly)
- Custom PCB (2-layer) and 3D-printed case

## Visual Overview

### Assembled Hackpad
(*Insert a screenshot or photo of the final build here*)

### Schematic
(*Insert schematic screenshot here*)

### PCB Layout
(*Insert PCB layout screenshot from KiCad*)

### Exploded CAD View
(*Insert CAD render showing how the case fits together*)

## Layer Configuration

### Layer 0 – Shortcuts and Media
| Top Row       | Middle Row     | Bottom Row    |
|---------------|----------------|----------------|
| Media Prev    | Play/Pause     | Media Next     |
| Undo          | Redo           | Save           |
| Copy          | Paste          | Cut            |

Encoder: Volume control (default)  
Encoder button: Toggle between volume, zoom, brightness, and timeline scrubbing

### Layer 1 – Numpad
| Top Row       | Middle Row     | Bottom Row    |
|---------------|----------------|----------------|
| 7             | 8              | 9              |
| 4             | 5              | 6              |
| 1             | 2              | 3              |

Encoder and screen modes remain active.

## Firmware

- Written in Python using KMK firmware
- Supports multiple layers and encoder modes
- Keymap stored in `keymap.py`
- OLED uses SSD1306 I²C (SDA = GP6, SCL = GP7)
- LEDs controlled on GP1
- Fully customizable layout

## BOM: Bill of Materials

| Quantity | Component                  | Notes                                                                 |
|----------|----------------------------|-----------------------------------------------------------------------|
| 9        | Cherry MX-compatible switches | Any MX-style switch (linear/tactile/clicky)                          |
| 9        | DSA profile keycaps        | Or any compatible keycaps (1U)                                       |
| 12       | 1N4148 DO-35 diodes        | For switch matrix (only 9 needed, extras for spares)                 |
| 1        | EC11 rotary encoder        | With built-in push button                                            |
| 1        | 0.91" 128x32 OLED (I²C)    | SSD1306-compatible (GND/VCC/SCL/SDA)                                 |
| 16       | WS2812B addressable LEDs   | For underglow or key backlighting                                    |
| 1        | Seeed XIAO RP2040          | Through-hole version (required for compatibility)                    |
| 1        | Custom PCB                 | 2-layer, ≤100×100mm                                                  |
| 1        | 3D Printed Case            | Two parts: top and bottom                                            |
| 7        | M3×5×4 heat-set inserts    | Used for assembly                                                    |
| 7        | M3×4 screws                | For screwing into inserts                                            |
