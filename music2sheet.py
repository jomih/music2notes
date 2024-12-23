import librosa
import numpy as np
from music21 import environment, stream, note, metadata
from music21 import converter, layout, graph, expressions
#from itertools import groupby

# Configure MuseScore or LilyPond path for rendering
#environment.set('musicxmlPath', '/Applications/MuseScore.app')  

# Instrument frequency ranges (in Hz)
INSTRUMENT_RANGES = {
    "contrabass": (41, 220),  # E1 to A3
    "piano": (27.5, 4186),   # A0 to C8
    "violin": (196, 3136),   # G3 to E7
    "flute": (262, 2093),    # C4 to C7
}

def transcribe_to_sheet(file_path, instrument="contrabass"):
    # Load the audio file
    y, sr = librosa.load(file_path, sr=None)
    
    # Perform pitch detection using librosa
    pitches, magnitudes = librosa.piptrack(y=y, sr=sr, fmin=INSTRUMENT_RANGES[instrument][0], fmax=INSTRUMENT_RANGES[instrument][1])
    
    # Convert frequencies to musical notes
    notes_list = []
    for t in range(pitches.shape[1]):
        index = magnitudes[:, t].argmax()
        pitch = pitches[index, t]
        if pitch > 0:  # Only consider non-zero pitches
            note_name = librosa.hz_to_note(pitch)
            note_name = note_name.replace('♯', '#').replace('♭', 'b')  # Convert to ASCII
            notes_list.append(note_name)

            # Calculate the musical duration
            quarter_note_duration = 60 / 120  # Assume 120 BPM
            note_duration_quarters = duration_sec / quarter_note_duration
            notes_list.append((note_name, note_duration_quarters))

            '''
            try:
                # Validate and append the note
                music21_pitch = pitch.Pitch(note_name)
                notes_list.append(note_name)
            except music21.pitch.AccidentalException:
                print(f"Invalid note: {note_name}")
            '''
    
    # Create a music21 Stream
    score = stream.Score()
    score.metadata = metadata.Metadata()
    score.metadata.title = "Transcription"
    score.metadata.composer = "AI Transcriber"
    
    # Add notes to the stream
    part = stream.Part()
    for note_name, note_duration in notes_list:
        music_note = note.Note(note_name)
        music_note.lyric = music_note.name  # Attach the note name as a lyric        
        music_note.duration = duration.Duration(note_duration) # Set the duration (round to the nearest common duration)
        #text_expr = expressions.TextExpression(note_name) # Another way to attach the note name
        #music_note.expressions.append(text_expr)
        #part.append(note.Note(note_name))
        part.append(music_note)

    score.append(part)
    
    # Save the sheet music as MusicXML
    output_file = f"transcription_{instrument}.musicxml"
    score.write("musicxml", output_file)
    print(f"Sheet music saved to {output_file}")

    '''
    # Save the sheet music as a PDF
    output_file = f"transcription_{instrument}.pdf"
    try:
        score.write("musicxml.pdf", output_file)
        print(f"PDF sheet music saved to {output_file}")
    except Exception as e:
        print(f"Error generating PDF: {e}")
    '''

    # Load MusicXML file
    #score = converter.parse(output_file)

    # Generate PNG
    #score.plot('png', filename='output.png', layout=layout.Layout())
    #print("PNG file saved as output.png")

    # Group consecutive identical notes and calculate durations
    #grouped_notes = [(note, len(list(group))) for note, group in groupby(notes_list)]
    #for note_name, duration in grouped_notes:
    #    part.append(note.Note(note_name, quarterLength=duration * 0.25))  # Adjust quarterLength as needed


# Example usage
file_path = "audio.wav"  # Path to your WAV file
transcribe_to_sheet(file_path, instrument="contrabass")


