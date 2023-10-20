import os
import json

def scan(input_folder, output_folder):
    tags = ["drums", "piano", "full"]
    for i in range(2):
        chords_data = {}
        for j in range(5):
            for k in range(5):
                src_path = os.path.join(input_folder, "{0:03d}".format(i + 1), 
                        "{0:03d}".format(j + 1), "{0:03d}".format(k) + ".wav.chord.lab")
                obj_path = os.path.join("{0:03d}".format(j + 1), "{0:03d}".format(k))
                with open(src_path, "r") as f:
                    lines = f.readlines()
                lines = [line.rstrip().split("\t") for line in lines]
                st = 0
                json_data = []
                for line in lines:
                    print(line)
                    ed = round(float(line[1])*50)
                    s = line[-1].split(":")
                    if len(s) == 1:
                        s = ["N", "N"]
                    json_data.append([st, ed] + s)
                    st = ed
                chords_data[obj_path] = json_data

        json_object = json.dumps([chords_data], indent=2)
        obj_path = os.path.join(output_folder, f"{tags[i]}_chords.json")
        with open(obj_path, "w") as f:
            f.write(json_object)


if __name__=="__main__":
    input_folder = "public/audios"
    output_folder = "src/assets/"
    scan(input_folder, output_folder)
