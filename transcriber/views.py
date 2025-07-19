import tempfile
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from faster_whisper import WhisperModel

# ----------------Load model once at startup--------------------------

model = WhisperModel("base", device="cpu", compute_type="int8")  
def live_transcribe_view(request):
    return render(request, "transcriber/live.html")

@csrf_exempt
def transcribe_chunk(request):
    if request.method == "POST" and request.FILES.get("audio"):
        audio_file = request.FILES["audio"]

# --------------------Save uploaded audio to temp file----------------

        with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as temp_audio:
            for chunk in audio_file.chunks():
                temp_audio.write(chunk)
            temp_audio_path = temp_audio.name

        try:

 # --------------------Transcribe using faster-whisper----------------

            segments, _ = model.transcribe(temp_audio_path)
            text = " ".join([segment.text for segment in segments])
            return JsonResponse({"text": text})
        except Exception as e:
            return JsonResponse({"error": str(e)})

    return JsonResponse({"error": "Invalid request"})
