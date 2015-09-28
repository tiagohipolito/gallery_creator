#!/usr/bin/python

import sys, getopt
import os, os.path, re,shutil
import progressbar, subprocess


def main(argv):
    directory = parse_parameters(argv)

    # sort files
    sorted_files = os.listdir(directory)
    sorted_files.sort(key=alphanum_key)

    file_count = len(sorted_files)

    #define backup directory
    backup_directory = os.path.join(directory, 'original')
    if not os._exists(backup_directory):
        os.mkdir(backup_directory)

    counter = 0

    # define progress bar
    bar = progressbar.ProgressBar(maxval=file_count, widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
    bar.start()

    for item in sorted_files:
        full_file_name = os.path.join(directory, item)
        if os.path.isfile(full_file_name):
            path, file_name = os.path.split(full_file_name)
            extension = os.path.splitext(file_name)[1].lower()
            counter += 1
            bar.update(counter)

            #backup
            shutil.copy(full_file_name, backup_directory)

            #rename file
            new_file_name = str(counter).zfill(3) + extension
            new_full_file_name = os.path.join(path, new_file_name)

            os.rename(full_file_name, new_full_file_name)

            #resize file
            subprocess.call('convert {:s} -resize 500x500 "{:s}";'.format(new_full_file_name, new_full_file_name), shell=True)

            #create thumbnail
            command='convert {:s} -resize 75x75 -background white -gravity center -extent 75x75 -quality 75' \
                    ' "{:s}/s{:s}";'.format(new_full_file_name, path, new_file_name)
            subprocess.call(command, shell=True)

    bar.finish()


def parse_parameters(argv):
    usage = 'usage: create_gallery -d <directory>'
    selected_directory = ''
    try:
        opts, args = getopt.getopt(argv, "d:",["directory="])
    except getopt.GetoptError:
        print usage
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print usage
            sys.exit()
        elif opt in ("-d", "--directory"):
            selected_directory = arg

    return selected_directory


def alphanum_key(s):
    # Turn a string into a list of string and number chunks. "z23a" -> ["z", 23, "a"]
    return [try_int(c) for c in re.split('([0-9]+)', s)]


def try_int(s):
    try:
        return int(s)
    except:
        return s

if __name__ == "__main__":
    main(sys.argv[1:])