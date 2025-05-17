from natsort import natsorted
from timecode import Timecode
from PIL import Image
import numpy as np
import srt
import glob


def process_video(f, sf, x: int, y: int, s: int, fps: int):
    size: tuple[int, int] = x, y
    
    # Write file metadata
    _ = f.write("{x} {y} {s}\n".format(x=x, y=y, s=s))

    files = glob.glob("./frames/*.jpg")
    files = natsorted(files)

    total_files = len(files)

    subs = list(srt.parse(sf))

    for (i, frame) in enumerate(files):
        with Image.open(frame) as im:
            resized = im.resize(size)
            resized = resized.convert("L")

            pixels = np.array(resized) / 255
            pixels = np.where(pixels > 0.6, 1, 0)

            for row in pixels:
                _ = f.write("".join(map(str, row)))
                _ = f.write("\n")
                
        process_subs(f, subs, s, fps, i)
        
        print(f"\rFrame {i} of {total_files}", end="", flush=True)


def process_subs(f, subs, s: int, fps: int, i: int):
    for sub in subs:
        start_tc = ''.join(('0', str(sub.start)[:11]))
        end_tc = ''.join(('0', str(sub.end)[:11]))

        if len(end_tc) < 11:
            end_tc = ''.join((end_tc, '.000'))

        # print(start_tc, " -> ", end_tc)

        start_frame = Timecode(fps, start_tc).frame_number
        end_frame = Timecode(fps, end_tc).frame_number

        if (i >= start_frame and i < end_frame):
            _ = f.write(sub.content)
            _ = f.write("\n\n")
            return

    _ = f.write("\n"*s)

def main():
    fps: int = 30
    R_X: int = 480 // 15
    R_Y: int = 360 // 15
    S_H: int = 4 # lines of subs to add (metadata reasons)


    out_file = "bad_apple_" + str(R_X) + "x" + str(R_Y) + ".txt"
    sub_file = "./assets/subs/bad_apple_en+ja-hyb.srt"

    print("Starting conversion...")

    with open(out_file, "w+") as f:
        with open(sub_file, "r") as sf:
            process_video(f, sf, R_X, R_Y, S_H, fps)
    
    print("\nDone!")


if __name__ == "__main__":
    main()
