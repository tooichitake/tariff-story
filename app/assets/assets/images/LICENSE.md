# Image Licence Manifest

All imagery referenced by the Streamlit app lives in this directory. **Only PD / CC0 / CC BY-compatible sources are permitted.** Getty, AP, Reuters, and other rights-managed sources are not allowed.

If the expected file is not present, [`app/styles.py::visual_anchor()`](../../styles.py) gracefully falls back to a CSS-only anchor (gradient + illustrative SVG + overlay text), so the app still renders.

## Expected Files

| Slot | Filename | Role in narrative | Recommended subject |
|---|---|---|---|
| H1 | `hook_hero.jpg` | Opening hero | Supermarket checkout, shipping port, or macro $100 bills |
| H2 | `act2_hands.jpg` | Act II empathy anchor | Hands at checkout / counting change / holding receipt (no faces) |
| H3a | `inauguration.jpg` | Event: Trump inaugurated 2025-01-20 | Capitol steps swearing-in or Trump at podium |
| H3b | `liberation_day.jpg` | Event: Liberation Day 2025-04-02 | Rose Garden chart presentation, 2025-04-02 |
| H3c | `us_china_peak.jpg` | Event: US-China 125% peak 2025-04-10 | Cargo ships, trade imbalance imagery |
| H3d | `geneva_talks.jpg` | Event: Geneva talks 2025-05-14 | Negotiators / UN Geneva / handshake |
| H3e | `scotus_ruling.jpg` | Event: SCOTUS strikes down IEEPA 2026-02-20 | SCOTUS building exterior |
| H3f | `section_122.jpg` | Event: Section 122 effective 2026-02-24 | US Capitol / legislative document |
| H5 | `oval_office.jpg` | Act IV closing | Resolute Desk / empty Oval Office interior |

H4 (product-category icons in Act II viz4) is satisfied by inline Lucide SVG in the component code — no asset file needed.

## Manifest

Retrieved 2026-04-17. All from Wikimedia Commons (public domain or CC licences — see each image's "File:" page for licensing details). Downloaded as JPG at 1280px wide thumbnails.

| Filename | Source | Licence | Author |
|---|---|---|---|
| `inauguration.jpg` | https://commons.wikimedia.org/wiki/File:Donald_Trump_takes_the_oath_of_office_(2025)_(alternate).jpg | Public Domain (US Government work) | The White House |
| `us_china_peak.jpg` | https://commons.wikimedia.org/wiki/File:MAERSK_MC_KINNEY_M%C3%96LLER_%26_MARSEILLE_MAERSK_(48694054418).jpg | CC BY-SA 2.0 | Kees Torn (Flickr) |
| `scotus_ruling.jpg` | https://commons.wikimedia.org/wiki/File:Panorama_of_United_States_Supreme_Court_Building_at_Dusk.jpg | Public Domain | Joe Ravi (photographer) |
| `section_122.jpg` | https://commons.wikimedia.org/wiki/File:Capitol_Building_Full_View.jpg | Public Domain | US Government / Architect of the Capitol |
| `oval_office.jpg` | https://commons.wikimedia.org/wiki/File:View_of_Oval_Office_in_2017.jpg | Public Domain (US Government work) | Official White House Photo |
| `hook_hero.jpg` | https://commons.wikimedia.org/wiki/File:MAERSK_MC_KINNEY_M%C3%96LLER_%26_MARSEILLE_MAERSK_(48694054418).jpg | CC BY-SA 2.0 | Kees Torn (Flickr) — duplicate of `us_china_peak.jpg` |
| `act2_hands.jpg` | https://commons.wikimedia.org/wiki/File:Supermarket_check_out.JPG | Public Domain / CC0 | Wikimedia Commons contributor (Sainsbury's supermarket checkout, UK) |
| `liberation_day.jpg` | https://commons.wikimedia.org/wiki/File:P20250415JB-0003.jpg | Public Domain (US Government work) | The White House — Oval Office April 2025 (stand-in for Liberation Day narrative) |
| `geneva_talks.jpg` | https://commons.wikimedia.org/wiki/File:Conference_Room_in_Palace_of_Nations.jpg | CC BY-SA (Wikimedia Commons) | Palace of Nations, Geneva conference chamber |

**When replacing a fallback with a real photo**: drop the file in this directory with the exact expected filename (case-sensitive), append a row above, and commit. No code changes required.

## Acceptable Sources

- **White House Flickr** — public domain (US government work). https://www.flickr.com/photos/whitehouse
- **Wikimedia Commons** — public domain or CC BY / CC BY-SA. https://commons.wikimedia.org
- **Unsplash** — Unsplash Licence (commercial-friendly, attribution appreciated). https://unsplash.com
- **Pexels** — Pexels Licence (commercial-friendly, no attribution required). https://pexels.com
- **Library of Congress** — public domain for US government works. https://loc.gov

## Image Requirements

- Format: **WebP** (preferred) or **JPG** (fallback). Not PNG — too heavy for hero use.
- Target size: **100–250 KB** each, **<3 MB** total across all 9 files.
- Resolution: hero/anchor images 1600×900 or 1200×675; event thumbnails 400×300 or 600×450.
- Colour tone: dark/desaturated preferred — the app applies a half-transparent gradient overlay on hero/anchor images, so very bright or saturated photos clash with the dark theme.

## How to Compress

```python
from PIL import Image
img = Image.open("source.jpg")
img.save("hook_hero.jpg", "webp", quality=80)
```
