from datetime import datetime, timedelta

# Input data
available_times = [
    "09:00", "09:15", "09:30", "09:45", "10:00", "10:15", "10:30", "10:45",
    "11:00", "11:15", "11:30", "11:45", "12:00", "12:15", "12:30", "12:45",
    "13:00", "13:15", "13:30", "13:45", "14:00", "14:15", "14:30", "14:45",
    "15:00", "15:15", "15:30", "15:45", "16:00", "16:15", "16:30", "16:45",
    "17:00"
]

busy_start_times = [
    "2025-01-21 09:00", "2025-01-21 10:00", "2025-01-21 10:00", "2025-01-21 11:00", "2025-01-21 09:00", "2025-01-21 13:00", "2025-01-21 16:00"
]
busy_end_times = [
    "2025-01-21 10:00", "2025-01-21 11:00", "2025-01-21 11:00", "2025-01-21 12:00", "2025-01-21 10:00", "2025-01-21 15:00", "2025-01-21 17:30"
]

busy_blocks = list(zip(
    [datetime.fromisoformat(start) for start in busy_start_times],
    [datetime.fromisoformat(end) for end in busy_end_times]
))


# Function to check overlap
def is_valid_slot(slot_start, slot_end, busy_blocks):
    overlap_counter = 0
    for busy_start, busy_end in busy_blocks:
        if slot_start < busy_end and slot_end > busy_start:
            overlap_counter += 1
            if overlap_counter > 1:
                return False
    return True


# Check consecutive slots with priorities
def find_consecutive_slots(available_times, busy_blocks):
    priorities = [":00", ":30", ":15", ":45"]  # Priority order of endings
    for priority in priorities:
        valid_slots = []
        for time_str in available_times:
            if time_str.endswith(priority):
                slot_start = datetime.strptime(f"2025-01-21 {time_str}", "%Y-%m-%d %H:%M")
                slot_end = slot_start + timedelta(hours=1)
                if is_valid_slot(slot_start, slot_end, busy_blocks):
                    valid_slots.append(time_str)
                if len(valid_slots) >= 2:
                    # Check if consecutive slots are valid
                    first_slot = datetime.strptime(f"2025-01-21 {valid_slots[-2]}", "%Y-%m-%d %H:%M")
                    second_slot = first_slot + timedelta(hours=1)
                    if valid_slots[-1] == second_slot.strftime("%H:%M"):
                        return [valid_slots[-2], valid_slots[-1]]
    # No priority pair found, return first two overall valid slots
    valid_slots = []
    for time_str in available_times:
        slot_start = datetime.strptime(f"2025-01-21 {time_str}", "%Y-%m-%d %H:%M")
        slot_end = slot_start + timedelta(hours=1)
        if is_valid_slot(slot_start, slot_end, busy_blocks):
            valid_slots.append(time_str)
            if len(valid_slots) == 2:
                return valid_slots
    return None


# Find and output the result
result = find_consecutive_slots(available_times, busy_blocks)
if result:
    print(f'The first two available time slots are: {result}.')
else:
    print('There are no available time slots. Could you please suggest another day?')