# multi-video-stream
Just a small tool that works with MediaMTX to stream multiple videos at once.

## Required software and set-up
Beyond Python (versions 3.11+), you will also need the following software:

[MediaMTX](https://mediamtx.org/docs/kickoff/install) is the video server we are using to host the RTSP streams

[FFmpeg](https://ffmpeg.org/download.html) is the client we are using to dispatch RTSP streams to the server.

You'll want to either install both of these tools and add them to your path (as `mediamtx` and `ffmpeg`) or download their executables and place them in the same folder as this script. Either way, it will have to be possible for you to execute them from the command line, as that is what this script automates.

NOTE: Ensure that the mediamtx.yml configuration file is present in the same directory as this script. If it is not, you will run into an issue where FFmpeg will not be able to find a path for the RTSP stream.

## Using the program
To use the program, simply run
`python3 main.py \[PATH_TO_DIRECTORY_WITH_VIDEO_FILES]`
### optional parameters
- `-v, --v`: verbosity (not yet implemented)
- `-n, --noloop`: Prevents the default behaviour of looping videos over and over again
- `-p, --port`: Specifies the port number for RTSP as something other than the default (8554)