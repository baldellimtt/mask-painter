# Mask Painter

**Mask Painter** is an interactive tool to easily draw and edit binary masks for images.

<p align="center">
  <img src="https://www.sentireascoltare.com/wp-content/uploads/2017/05/twin-peaks-e1494510660493.jpg" alt="Logo TensorFlow" width="500"/>
</p>

## Features

- Freehand brush with adjustable size
- Eraser to remove parts of the mask
- Zoom in/out and pan to navigate large images
- Visible brush cursor with live size preview
- Draw filled circles with a single click
- Save masks to a separate folder with the same filenames as the input images

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `e` | Toggle eraser mode |
| `+` / `-` | Increase / decrease brush size |
| `z` | Zoom in |
| `x` | Zoom out |
| `r` | Reset pan and zoom |
| Right mouse button + drag | Pan the image |
| `c` | Draw or erase a filled circle at cursor position |
| `s` | Save the mask |
| `q` | Move to the next image |
| `w` | Move to the previous image |
| `Esc` | Confirm exit |

## Requirements

Install dependencies with:

```bash
pip install -r requirements.txt
