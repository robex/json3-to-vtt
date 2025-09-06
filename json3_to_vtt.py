import json
import argparse
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser(description = "YouTube json3 to VTT subtitle converter")
    parser.add_argument("file", help = "Input file in json3 format")
    parser.add_argument("-l", "--lang_code", help = "ISO language code to use, default: en")

    args = parser.parse_args()

    if args.lang_code is None:
        args.lang_code = "en"

    return args

def write_vtt(vtt_data, outfile, lang_code):
    vtt_header = f"""WEBVTT
Kind: captions
Language: {lang_code}

"""

    with open(outfile, "w", encoding='utf-8') as f:
        f.write(vtt_header)

        for d in vtt_data:
            f.write(d["ts"] + "\n")
            f.write(d["text"] + "\n\n")

def read_json3(filename):
    with open(filename, "r", encoding="utf-8") as f:
        j = json.load(f)

        if "wireMagic" in j and j["wireMagic"] == "pb3":
            return j
        else:
            return None

def ms_to_vtt(ms):
    sec, ms = divmod(ms, 1000)
    hh, rem = divmod(sec, 3600)
    mm, ss = divmod(rem, 60)

    return f"{hh:02d}:{mm:02d}:{ss:02d}.{ms:03d}"

def json3_to_vtt(in_data):
    vtt_data = []

    l = len(in_data["events"])
    for i, evt in enumerate(in_data["events"]):
        if "dDurationMs" not in evt:
            continue

        start = evt["tStartMs"]
        end = start + evt["dDurationMs"]

        # trim overlapping parts
        if i != l - 1:
            next_start = in_data["events"][i + 1]["tStartMs"]
            end = min(end, next_start)

        if "segs" in evt:
            msg = ""
            for seg in evt["segs"]:
                msg += seg["utf8"]

            if msg.strip() != "":
                vtt_data.append({
                    "ts": f"{ms_to_vtt(start)} --> {ms_to_vtt(end)}",
                    "text": msg
                })

    return vtt_data

def main():
    args = parse_args()

    json_data = read_json3(args.file)
    if json_data is None:
        print("error: invalid input file")
        return

    vtt_data = json3_to_vtt(json_data)

    outfile = f"{Path(args.file).stem}.{args.lang_code}.vtt"
    write_vtt(vtt_data, outfile, args.lang_code)

main()