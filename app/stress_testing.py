<<<<<<< HEAD
import whisper
import warnings


warnings.filterwarnings("ignore", category=FutureWarning)
model = whisper.load_model("turbo")
result = model.transcribe("audio.mp3")

=======
import whisper
import warnings


warnings.filterwarnings("ignore", category=FutureWarning)
model = whisper.load_model("turbo")
result = model.transcribe("audio.mp3")

>>>>>>> b95adf403473764fe4b0ce05d832b9fd992770b3
print(result["text"])