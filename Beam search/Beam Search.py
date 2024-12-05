import re
import random
import subprocess
import json
import datetime
import time
import copy

runCount = 7

metadata = {}
courses = []
rooms = {}
curricula = {}
constraints = []
hard_violations_list = []
soft_violations_list = []
beam_width = 3
branching_factor = 5
print(datetime.datetime.now())

file_path = f"datasets\\dataset{runCount}.rtf"

metadata_pattern = r"(Name|Courses|Rooms|Days|Periods_per_day|Curricula|Constraints): (\S+)"
course_pattern = r"([\w-]+)\s+(\w+)\s+(\d+)\s+(\d+)\s+(\d+)"
room_pattern = r"([\w-]+)\s+(\d+)"
curriculum_pattern = r"(q\d+)\s+(\d+)\s+((?:[\w-]+\s+)+)"
constraint_pattern = r"([\w-]+)\s+(\d+)\s+(\d+)"

with open(file_path, "r") as file:
    current_section = None
    for line in file:
        line = line.strip().replace("\\", "")
        if line.startswith("COURSES:"):
            current_section = "courses"
            continue
        elif line.startswith("ROOMS:"):
            current_section = "rooms"
            continue
        elif line.startswith("CURRICULA:"):
            current_section = "curricula"
            continue
        elif line.startswith("UNAVAILABILITY_CONSTRAINTS:"):
            current_section = "constraints"
            continue
        if current_section is None and line:
            match = re.match(metadata_pattern, line)
            if match:
                key, value = match.groups()
                metadata[key] = value
        elif current_section == "courses" and line:
            match = re.match(course_pattern, line)
            if match:
                course_id, teacher_id, lectures, minWorkDays, students = match.groups()
                course = {
                    "course_id": course_id,
                    "teacher_id": teacher_id,
                    "lectures": int(lectures),
                    "minWorkDays": int(minWorkDays),
                    "students": int(students)
                }
                courses.append(course)
        elif current_section == "rooms" and line:
            match = re.match(room_pattern, line)
            if match:
                room_id, capacity = match.groups()
                rooms[room_id] = int(capacity)
        elif current_section == "curricula" and line:
            match = re.match(curriculum_pattern, line)
            if match:
                curriculum_id, course_count, courses_in_curriculum = match.groups()
                courses_list = courses_in_curriculum.split()
                curricula[curriculum_id] = {
                    "course_count": int(course_count),
                    "courses": courses_list
                }
        elif current_section == "constraints" and line:
            match = re.match(constraint_pattern, line)
            if match:
                course_id, day, period = match.groups()
                constraint = {
                    "course_id": course_id,
                    "day": int(day),
                    "period": int(period)
                }
                constraints.append(constraint)

allLectures = [course["course_id"] for course in courses for _ in range(course["lectures"])]
periods_per_day = int(metadata.get("Periods_per_day"))
days = int(metadata.get("Days"))
roomAmount = len(rooms)


def timetable_creator():
    timetable = [[[0 for _ in range(roomAmount)] for _ in range(periods_per_day)] for _ in range(days)]
    for x in range(len(allLectures)):
        randomDay = random.randint(0, days - 1)
        randomPeriod = random.randint(0, periods_per_day - 1)
        randomRoom = random.randint(0, roomAmount - 1)
        currentLecture = allLectures[x]
        randomPos = timetable[randomDay][randomPeriod][randomRoom]
        if randomPos != 0:
            if isinstance(randomPos, list):
                randomPos.append(currentLecture)
            else:
                timetable[randomDay][randomPeriod][randomRoom] = [randomPos, currentLecture]
        else:
            timetable[randomDay][randomPeriod][randomRoom] = currentLecture
    return timetable


def evaluate_timetable(timetable):
    output_path = f"output_Timetables\output_timetable{runCount}.sol"
    write_timetable_to_file(timetable, output_path)
    return run_validator(output_path)


def write_timetable_to_file(timetable, output_path):
    content = ""
    for day in range(days):
        for period in range(periods_per_day):
            for room_index, room_id in enumerate(rooms.keys()):
                lecture = timetable[day][period][room_index]
                if lecture != 0:
                    if isinstance(lecture, list):
                        for item in lecture:
                            content += f"{item} {room_id} {day} {period} \n"
                    else:
                        content += f"{lecture} {room_id} {day} {period} \n"

    write_to_file_with_retry(output_path, content)


def run_validator(output_path):
    hardViolations = []
    softViolations = []
    cpp_file = r"C:\Users\paolo\CLionProjects\Validator\validator.cc"
    executable = r"C:\Users\paolo\CLionProjects\Validator\cmake-build-debug\Validator.exe"

    try:
        compile_process = subprocess.run(
            ["g++", cpp_file, "-o", executable],
            check=True,
            capture_output=True,
            text=True
        )
    except subprocess.CalledProcessError as e:
        print("Compilation failed:")
        print(e.stderr)
        exit(1)

    arg1 = f"cttDatasets\comp{runCount:02}.ctt"
    args = [arg1, output_path]
    retries = 3

    try:
        run_process = subprocess.run(
            [executable] + args,
            check=True,
            capture_output=True,
            text=True
        )
        output = run_process.stdout

        hard_violations_pattern = r"Violations of (\w+) \(hard\) : (\d+)"
        soft_costs_pattern = r"Cost of (\w+) \(soft\) : (\d+)"

        hard_violations = {match[0]: int(match[1]) for match in re.findall(hard_violations_pattern, output)}

        soft_costs = {match[0]: int(match[1]) for match in re.findall(soft_costs_pattern, output)}

        summary_pattern = r"Summary: Violations = (\d+)?, Total Cost = (\d+)"
        second_pattern = r"Summary: Total Cost = (\d+)"

        summary_match = re.search(summary_pattern, output)
        second_match = re.search(second_pattern, output)
        if summary_match:
            total_violations = int(summary_match.group(1)) if summary_match.group(1) else 0
            total_cost = int(summary_match.group(2))
        elif second_match:
            total_violations = 0
            total_cost = int(second_match.group(1))

        hardViolations.append(hard_violations)
        softViolations.append(soft_costs)
    except subprocess.CalledProcessError as e:
        print(output_path)
        run_process = subprocess.run(
            [executable] + args,
            check=True,
            capture_output=True,
            text=True
        )
        output = run_process.stdout
        print(output)

        summary_pattern = r"Summary: Violations = (\d+)?, Total Cost = (\d+)"
        second_pattern = r"Summary: Total Cost = (\d+)"

        summary_match = re.search(summary_pattern, output)
        second_match = re.search(second_pattern, output)
        if summary_match:
            total_violations = int(summary_match.group(1)) if summary_match.group(1) else 0
            total_cost = int(summary_match.group(2))
        elif second_match:
            total_violations = 0
            total_cost = int(second_match.group(1))


        print("Execution failed:")
        print(e.stderr)

    return total_violations, total_cost


def write_to_file_with_retry(path, content, retries=3, delay=0.1):
    for attempt in range(retries):
        try:
            with open(path, "w") as output_file:
                output_file.write(content)
            return
        except PermissionError:
            if attempt < retries - 1:
                print("entered permission error")
                time.sleep(delay)
            else:
                raise


def swap_random_lecture(timetable):
    new_timetable = copy.deepcopy(timetable)

    while True:
        day = random.randint(0, days - 1)
        period = random.randint(0, periods_per_day - 1)
        room = random.randint(0, roomAmount - 1)
        lecture = new_timetable[day][period][room]

        if lecture != 0:
            if isinstance(lecture, list):
                selected_lecture = lecture.pop(random.randint(0, len(lecture) - 1))
                if not lecture:
                    new_timetable[day][period][room] = 0
            else:
                selected_lecture = lecture
                new_timetable[day][period][room] = 0
            break

    while True:
        new_day = random.randint(0, days - 1)
        new_period = random.randint(0, periods_per_day - 1)
        new_room = random.randint(0, roomAmount - 1)
        destination = new_timetable[new_day][new_period][new_room]

        if destination == 0:
            new_timetable[new_day][new_period][new_room] = selected_lecture
            break
        elif isinstance(destination, list):
            destination.append(selected_lecture)
            break
        else:
            new_timetable[new_day][new_period][new_room] = [destination, selected_lecture]
            break
    return new_timetable


def local_beam_search(beam_width, branching_factor, neighbours_list):

    hard_score_list = []
    soft_score_list = []

    for j in neighbours_list:
        hard_violations, soft_violations = evaluate_timetable(j)
        if soft_violations == 0 and hard_violations == 0:
            return True, j
        hard_score_list.append(hard_violations)
        soft_score_list.append(soft_violations)

    scored_current = list(zip(neighbours_list, hard_score_list, soft_score_list))

    scored_current.sort(key=lambda item: (item[1], item[2]))

    top_x_current = scored_current[:beam_width]

    top_current = [item[0] for item in top_x_current]
    top_x_hard_violations = [item[1] for item in top_x_current]
    top_x_soft_violations = [item[2] for item in top_x_current]

    hard_violations_list.extend(top_x_hard_violations)
    soft_violations_list.extend(top_x_soft_violations)

    neighbours_list = []
    for i in top_current:
        for y in range(branching_factor):
            neighbour = swap_random_lecture(i)
            if neighbour not in neighbours_list:
                neighbours_list.append(neighbour)
    return False, neighbours_list


finalTimetable = []
neighbours_list = []
final_hard = 0
final_soft = 0
count = 0

for _ in range(branching_factor):
    starting_timetable = timetable_creator()
    neighbours_list.append(starting_timetable)

for _ in range(10000):
    count += 1
    found_perfect, result = local_beam_search(beam_width, branching_factor, neighbours_list)
    if found_perfect:
        finalTimetable = result
        hard_violations_list.append(0)
        soft_violations_list.append(0)
        break
    else:
        neighbours_list = result

results = {
    "hard_violations": hard_violations_list,
    "soft_violations": soft_violations_list
}

with open(f"Jsons\data{runCount}.json", "w") as json_file:
    json.dump(results, json_file, indent=4)

print(datetime.datetime.now())

