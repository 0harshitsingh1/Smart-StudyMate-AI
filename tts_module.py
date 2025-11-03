from gtts import gTTS

def summary_to_speech(summary):
    tts = gTTS(summary)
    output_path = "summary_audio.mp3"
    tts.save(output_path)
    # Return the path to the generated audio file
    return output_path