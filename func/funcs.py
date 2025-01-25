from datetime import datetime, timedelta

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
def find_consecutive_slots(available_times, busy_start_times, busy_end_times):
    busy_blocks = list(zip(
        [datetime.fromisoformat(start) for start in busy_start_times],
        [datetime.fromisoformat(end) for end in busy_end_times]
    ))

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