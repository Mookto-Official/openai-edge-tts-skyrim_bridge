from flask import Flask, request, Response
import asyncio
import edge_tts

app = Flask(__name__)

# যেকোনো মেয়ে/ছেলে Skyrim ভয়েসকে সরাসরি বাংলা Edge TTS ভয়েসে ম্যাপ করা
def pick_bangla_voice(voice_name: str) -> str:
    v = (voice_name or "").lower()
    if any(k in v for k in ["female", "woman", "girl", "nabanita", "tanishaa", "nova", "shimmer", "aria", "jenny"]):
        return "bn-BD-NabanitaNeural"
    return "bn-BD-PradeepNeural"

# ১. SkyrimNet-এর ভয়েস এনরোলমেন্ট চেক (/v1/audio/voices) পাস করানো
@app.route("/v1/audio/voices", methods=["GET", "POST"])
@app.route("/audio/voices", methods=["GET", "POST"])
def mock_voices():
    voice_name = request.form.get("name") or (request.json.get("name") if request.is_json else None) or "bn-BD-NabanitaNeural"
    return {
        "id": voice_name,
        "voice_id": voice_name,
        "name": voice_name,
        "object": "voice"
    }, 200

# ২. আসল বাংলা অডিও জেনারেট করা (/v1/audio/speech)
@app.route("/v1/audio/speech", methods=["POST"])
@app.route("/audio/speech", methods=["POST"])
def generate_speech():
    data = request.get_json(force=True, silent=True) or {}
    text = data.get("input", "")
    requested_voice = data.get("voice", "bn-BD-NabanitaNeural")
    target_voice = pick_bangla_voice(requested_voice)

    async def _synth():
        communicate = edge_tts.Communicate(text, target_voice)
        audio_bytes = bytearray()
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_bytes.extend(chunk["data"])
        return bytes(audio_bytes)

    audio_data = asyncio.run(_synth())
    return Response(audio_data, mimetype="audio/mpeg")

if __name__ == "__main__":
    print("SkyrimNet Bangla Edge-TTS Bridge running on http://localhost:5055")
    app.run(host="127.0.0.1", port=5055)
