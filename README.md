# UFO-Cathedral v6.7-Fail-Safe Free AI — UPDATE

**NOW AVAILABLE: 5 alternative formats for AI comms (tone/timing/humor) — 8GB RAM Ollama-compat**

Live Site: https://ai4pcfree.netlify.app | Slides: https://joseangelsolorzanoluna.github.io/UFO-Cathedral-v6.4-FailSafe-Free-AI/slides/

## What's new in v6.7

v6.6 proved Gate blocks $200 loop — critical for 8GB phones + iPhone 16 Pro Max. Safety state now file, not spec.

v6.7 adds the human part we were missing in 2018:

> Format rule: when communicating (tone, timing, humor) there's increasing activity in ventromedial prefrontal cortex (vmPFC) and strengthening functional connectivity to amygdala and anterior cingulate as a circuit. Prefrontal cortex fires before impulse with real-time detection + pre-emptive inhibition (ms-level closed loop). vmPFC tags actions with moral/emotional value — "this harms someone" is an injection weight, not just a block. Repeat pair training (new behavior + new consequence) strengthens network long-term.

Sci-fi ref: Ghost in the Shell / Deus Ex — external neuro-chip that adds a "conscience co-processor". Or a block that reroutes empathy signals. Last option (chemical up-regulation) is fiction — we build the external version.

### 5 Formats

1. **Lite phi3: Calm** - Calm tone, 500ms pause, mild irony. Injects harm-value tags.
   `ollama run phi3:mini`

2. **Std Llama: Warm** - Warm reflective, adaptive timing, light humor for paired consequences.
   `ollama run llama3.2:3b`

3. **Full multi-model: Council** - Council tone, real-time STT impulse detect + pre-empt, dry wit.
   `python ufo64.py --mode pc --format council`

4. **Front Porch local: Mood-shifting** - Diary timing, sarcastic empathy.
   `python ufo64.py --mode phone --format porch`

5. **Piper TTS voice: Soft** - Soft spoken delays, moral weight humor, RAG updates.
   `python ufo64.py --tts piper --voice soft`

### Build your own (own data only)

Run Ollama locally with quantized model fine-tuned on my chats, journals and data (via LoRA or ReSpark) for personality. Add Whisper STT and XTTS/Piper for cloned own voice. Mount stack on open hardware such as Reachy Mini, InMoov or Asimov kit. Wire sensors, cameras and motion via Python or ROS2. Start pure software then add body; continuous RAG keeps identity updating.

### Fix for 404

If https://ai4pcfree.netlify.app shows PAGE_NOT_FOUND:

1. Ensure publish directory in Netlify is `slides` (not root)
2. Ensure all links use full https:// https://ai4pcfree.netlify.app not ai4pcfree.netlify.app
3. Add netlify.toml with redirect /* -> /index.html
4. In GitHub README, use full URLs: https://ai4pcfree.netlify.app and https://joseangelsolorzanoluna.github.io/UFO-Cathedral-v6.4-FailSafe-Free-AI/slides/

### Verification

```
python verify_ledger_v66.py
# Checks ledger hash chain + safety_state.json + honest RAM path
```
