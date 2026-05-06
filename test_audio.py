import pyaudio

def test_mic():
    p = pyaudio.PyAudio()
    print("--- Audio Devices Found ---")
    for i in range(p.get_device_count()):
        dev = p.get_device_info_by_index(i)
        print(f"Device {i}: {dev['name']} (Inputs: {dev['maxInputChannels']})")
    
    print("\nAttempting to open default input stream...")
    try:
        stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)
        print("Success: Default input stream opened.")
        stream.close()
    except Exception as e:
        print(f"Error opening stream: {e}")
    finally:
        p.terminate()

if __name__ == "__main__":
    test_mic()
