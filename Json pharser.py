import json
import datetime


def format_time(seconds):
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    milliseconds = int((seconds - int(seconds)) * 1000)
    return "{:02}:{:02}:{:02},{:03}".format(int(hours), int(minutes), int(seconds), milliseconds)


def process_json(jsonfile):
    with open(jsonfile) as f:
        document = json.load(f)

    data = []
    for segment in document["segments"]:
        for word in segment["words"]:
            data.append(
                {"word": word["word"], "start": word["start"], "end": word["end"]})

    return data


def create_srt(data, outputfile):
    output = ""
    line_number = 1
    words = []
    start = 0
    end = 0
    punctuation = ".,?!"

    for word in data:
        if not words:
            start = word["start"]
        words.append(word["word"].strip())
        end = word["end"]
        if len(words) >= 2 and (word["word"][-1] in punctuation) or len(words) >= 12:
            start_formatted = format_time(start)
            end_formatted = format_time(end)
            line = ' '.join(words)
            output += f"{line_number}\n{start_formatted} --> {end_formatted}\n{line}\n\n"
            line_number += 1
            words = []

    with open(outputfile, "w") as outfile:
        outfile.write(output)


def main():
    data = process_json("input.json")
    create_srt(data, "output.srt")


if __name__ == "__main__":
    main()
