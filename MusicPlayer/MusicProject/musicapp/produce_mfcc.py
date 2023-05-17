import librosa
import math

def process_input(audio_files, track_duration):
    SAMPLE_RATE = 22050
    NUM_MFCC = 13
    N_FTT = 2048
    HOP_LENGTH = 512
    TRACK_DURATION = track_duration  # measured in seconds
    SAMPLES_PER_TRACK = SAMPLE_RATE * TRACK_DURATION
    NUM_SEGMENTS = 10

    samples_per_segment = int(SAMPLES_PER_TRACK / NUM_SEGMENTS)
    num_mfcc_vectors_per_segment = math.ceil(samples_per_segment / HOP_LENGTH)

    mfccs = []

    for audio_file in audio_files:
        signal, sample_rate = librosa.load(audio_file, sr=SAMPLE_RATE)

        for d in range(NUM_SEGMENTS):
            # calculate start and finish sample for current segment
            start = samples_per_segment * d
            finish = start + samples_per_segment

            # extract mfcc
            mfcc = librosa.feature.mfcc(
                y=signal[start:finish],
                sr=sample_rate,
                n_mfcc=NUM_MFCC,
                n_fft=N_FTT,
                hop_length=HOP_LENGTH
            )
            mfcc = mfcc.T
            mfccs.append(mfcc)

    return mfccs
