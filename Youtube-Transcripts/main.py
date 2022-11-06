# importing modules
from youtube_transcript_api import YouTubeTranscriptApi

# using the srt variable with the list of dictonaries
# obtained by the the .get_transcript() function
srt = YouTubeTranscriptApi.get_transcript("K8UgjzJTdHw")

# creating or overwriting a file "subtitles.txt" with
# the info inside the context manager
with open("subtitles.txt", "w") as f:
    # iterating through each element of list srt
    for i in srt:
        # writing each element of srt on a new line
        f.write("{}\n".format(i))
