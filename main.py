import argparse
import os
import subprocess
from time import sleep
from shutil import which

def main(Popen_args):
    args = parser.parse_args()
    if not args.live:
        if not os.path.isdir(args.directory):
            raise argparse.ArgumentError(argument=None, message=f"{args.directory} is not a valid directory")
    try:
        subprocess.Popen("./mediamtx", env={"MTX_RTSPADDRESS": f"{args.ip}:{args.port}"}, **Popen_args)
    except:
        try:
            subprocess.Popen(which("mediamtx"), env={"MTX_RTSPADDRESS": f"{args.ip}:{args.port}"}, **Popen_args)
        except:
            print("Could not find mediamtx program in same directory as script or as user program")
            exit(1)
    
    sleep(3)

    if args.output:
        if os.path.isfile(args.output):
            os.remove(args.output)
        output_file = open(args.output, "a")
    if args.live:
        url = ffmpeg_command(args.directory, args, 100, Popen_args=Popen_args)
        if args.output:
            output_file.write(f"{url}\n")
    else:
        for i, file in enumerate(os.scandir(args.directory)):
            if file.is_file():
                url = ffmpeg_command(file.path, args, i, Popen_args=Popen_args)
                if args.output:
                    output_file.write(f"{url}\n")
    
    if args.output:
        output_file.close()

    sleep(5)

    input("Press ENTER to end execution...") #Doesn't seem to work, must fix...
    print("Triggered")
    exit(0)


def ffmpeg_command(file_path:str, args, iteration:int, Popen_args) -> str:
    command = list(filter(lambda s: not not s, [
            "ffmpeg", 
            "" if args.noloop else "-stream_loop",
            "" if args.noloop else "-1",
            "-hide_banner",
            "-loglevel",
            "error",
            "-i",
            file_path,
            "-f",
            "rtsp",
            f"rtsp://{args.ip}:{args.port}/{iteration}.sdp"
        ]))
    try:
        subprocess.Popen(command, **Popen_args)
    except:
        command[0] = "./ffmpeg"
        try:
            subprocess.Popen(command, **Popen_args)
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
    parser.add_argument("-l", "--live", action="store_true", default=False)
    parser.add_argument("-n", "--noloop", action="store_true", default=False)
    parser.add_argument("-i", "--ip", default="localhost")
    parser.add_argument("-p", "--port", default="8554")
    parser.add_argument("-o", "--output")

    if os.name == "nt":
        Popen_args = {
            "creationflags":subprocess.CREATE_NEW_PROCESS_GROUP
        }
    else:
        Popen_args = {
            "process_group":os.getpgid(os.getpid())
        }

    main(Popen_args)
