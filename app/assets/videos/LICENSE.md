# Video Licence Manifest

Looping video backdrops for the Streamlit app's hero bands. **Only CC0 / Pexels-licence / Pixabay-licence / public-domain sources are permitted.** Getty, AP, Reuters, stock-house, and other rights-managed sources are not allowed.

When a video file is missing, [`app/styles.py::visual_anchor()`](../../styles.py) gracefully falls back to the corresponding still image in [`../images/`](../images/), and from there to a CSS-only illustration. Nothing breaks if this whole directory is empty.

## Expected Files

| Slot | Filename | Role in narrative | Poster still (fallback) |
|---|---|---|---|
| H1 | `hook_hero.mp4` | Opening hero — scale of tariff regime | `../images/hook_hero.jpg` |

Act II (`act2_hands.mp4`) and Act IV (`oval_office.mp4`) are intentionally image-only — the stills are treated with a Ken Burns slow-push animation in CSS. Adding a video there is optional; if added, Ken Burns auto-disables and the video motion takes over.

## Manifest

| Filename | Source | Licence | Author | Encoding |
|---|---|---|---|---|
| `hook_hero.mp4` | https://www.pexels.com/video/a-drone-footage-of-a-cargo-ship-with-containers-14807919/ | [Pexels Licence](https://www.pexels.com/license/) — free for commercial use, attribution not required | Luke Nomad (Pexels) | 1280×720, 6s, H.264 CRF 28, no audio, ~758 KB |

## Video Requirements

- Format: **MP4 / H.264** (preferred) or **WebM / VP9**. Must be browser-native so `<video autoplay muted loop playsinline>` works without a player.
- Target size: **<2 MB each** — the whole file is base64-inlined into the rendered HTML. Anything larger hurts Streamlit Cloud first paint.
- Duration: **5–8 seconds**. Longer clips bloat the payload; shorter clips loop too obviously.
- Resolution: **1280 wide** maximum. Hero bands are capped around 1100px by `.main .block-container { max-width: 1100px }`, so 1280 gives a small retina buffer without overshooting.
- Audio: **must be stripped** (`-an`). Autoplay with sound is blocked by every modern browser.
- Colour tone: dark / desaturated preferred — overlay gradients and headline text sit on top.

## How to Prepare a New Clip

Using the ffmpeg bundled with the `imageio-ffmpeg` package (already in `dvn-at3`):

```bash
# 1. Grab the source from Pexels — copy the "Free Download" HD 720p URL,
#    usually under videos.pexels.com/video-files/<id>/<id>-hd_1280_720_30fps.mp4
curl -L -o source.mp4 "<pexels_cdn_url>"

# 2. Trim to the best 6s window, re-encode to H.264 CRF 28, drop audio,
#    move moov atom to the front for streaming playback.
FFMPEG=$(python -c "import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())")
"$FFMPEG" -y -ss 3 -t 6 -i source.mp4 \
  -vf "scale=1280:-2" \
  -c:v libx264 -crf 28 -preset slow \
  -pix_fmt yuv420p -an -movflags +faststart \
  app/assets/videos/<slot>.mp4

# 3. Delete the source.
rm source.mp4
```

Adjust `-ss` (start offset) and `-t` (duration) to select the most narrative-relevant window.

## Acceptable Sources

- **Pexels** — Pexels Licence, free for commercial use, no attribution required. https://pexels.com/videos/
- **Pixabay** — Pixabay Content Licence, free for commercial use, no attribution required. https://pixabay.com/videos/
- **Coverr** — CC0 looping video. https://coverr.co
- **Mixkit** — Mixkit licence (free commercial). https://mixkit.co
- **Wikimedia Commons** — public domain or CC BY / CC BY-SA. https://commons.wikimedia.org
