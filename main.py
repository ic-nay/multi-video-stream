import argparse
import os
import subprocess
from time import sleep
from shutil import which

def main():
    pgid = os.getpgid(os.getpid())
    args = parser.parse_args()
    if not os.path.isdir(args.directory):
        raise argparse.ArgumentError(f"{args.directory} is not a valid directory")
    try:
        subprocess.Popen("./mediamtx", env={"MTX_RTSPADDRESS": f"localhost:{args.port}"}, process_group=pgid)
    except:
        try:
            subprocess.Popen(which("mediamtx"), env={"MTX_RTSPADDRESS": f"localhost:{args.port}"}, process_group=pgid)
        except:
            print("Could not find mediamtx program in same directory as script or as user program")
            exit(1)
    
    sleep(3)

    if (args.output):
        if os.path.isfile(args.output):
            os.remove(args.output)
        output_file = open(args.output, "a")
    for i, file in enumerate(os.scandir(args.directory)):
        if file.is_file():            
            command = ffmpeg_command(file.path, i, noloop=args.noloop, port=args.port, pgid=pgid)
            if (args.output):
                output_file.write(f"{command}\n")

    sleep(5)

    input("Press ENTER to end execution...")
    exit(0)


def ffmpeg_command(file_path:str, iteration:int, noloop:bool=False, port="8554", pgid:int=0) -> str:
    command = [
            "ffmpeg", 
            "" if noloop else "-stream_loop",
            "" if noloop else "-1",
            "-hide_banner",
            "-loglevel",
            "error",
            "-i",
            file_path,
            "-f",
            "rtsp",
            f"rtsp://localhost:{port}/{iteration}.sdp"
        ]
    try:
        subprocess.Popen(command, process_group=pgid)
    except:
        command[0] = "./ffmpeg"
        try:
            subprocess.Popen(command, process_group=pgid)
        except:
            print("Could not find ffmpeg program in same directory as script or as user program")
            exit(1)
    return command[-1]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Multivideo Streamer",
        description="Employs FFmpeg and MTX to stream a given directory of videos."
    )
    parser.add_argument("directory")
    parser.add_argument("-v", "--verbose", action="store_true", default=False)
    parser.add_argument("-n", "--noloop", action="store_true", default=False)
    parser.add_argument("-p", "--port", default="8554")
    parser.add_argument("-o", "--output")

    main()
