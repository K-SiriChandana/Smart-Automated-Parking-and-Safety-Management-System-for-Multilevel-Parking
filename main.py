# Smart Parking System

TOTAL_SLOTS = 10

# False = empty, True = occupied
slots = [False] * TOTAL_SLOTS


def display_slots():
    print("\n--- Parking Slot Status ---")

    for i in range(TOTAL_SLOTS):
        if slots[i]:
            print(f"Slot {i + 1}: OCCUPIED")
        else:
            print(f"Slot {i + 1}: EMPTY")


def find_empty_slot():
    for i in range(TOTAL_SLOTS):
        if not slots[i]:
            return i

    return -1


def park_vehicle():
    slot = find_empty_slot()

    if slot == -1:
        print("Parking is FULL!")
        return

    slots[slot] = True
    print(f"Vehicle parked in Slot {slot + 1}")


def remove_vehicle():
    slot = int(input("Enter slot number to free: "))

    if slot < 1 or slot > TOTAL_SLOTS:
        print("Invalid slot number!")
        return

    if not slots[slot - 1]:
        print("Slot is already empty!")
        return

    slots[slot - 1] = False
    print(f"Vehicle removed from Slot {slot}")


while True:

    print("\n===== SMART PARKING SYSTEM =====")
    print("1. View parking slots")
    print("2. Park vehicle")
    print("3. Remove vehicle")
    print("4. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        display_slots()

    elif choice == "2":
        park_vehicle()

    elif choice == "3":
        remove_vehicle()

    elif choice == "4":
        print("Exiting...")
        break

    else:
        print("Invalid choice!")