import serial
import time

# ------------------------------
# Configuration
# ------------------------------
BT_PORT = "COM11"       # Change this to your Bluetooth COM port
BAUD_RATE = 38400        # Must match Arduino's Serial baud rate
READ_INTERVAL = 0.05     # seconds between reads

# ------------------------------
# Helper functions
# ------------------------------
def parse_data(line):
    """
    Convert a comma-separated string from Arduino into numeric values.
    Expected format: x,y,joyBtn,jumpBtn,waveBtn,danceBtn
    """
    try:
        parts = list(map(int, line.split(',')))
        if len(parts) != 6:
            return None
        return {
            "x": parts[0],
            "y": parts[1],
            "joy": parts[2],
            "jump": parts[3],
            "wave": parts[4],
            "dance": parts[5]
        }
    except ValueError:
        return None


def handle_input(data):
    """Interpret joystick and button actions."""
    x = data["x"]
    y = data["y"]

    # Movement thresholds (adjust to your joystick sensitivity)
    deadzone = 100
    center = 512

    # Joystick movement
    if x < center - deadzone:
        print("← Moving Left")
    elif x > center + deadzone:
        print("→ Moving Right")
    if y < center - deadzone:
        print("↑ Moving Up")
    elif y > center + deadzone:
        print("↓ Moving Down")

    # Button actions
    if data["joy"]:
        print("🔵 Joystick button pressed")
    if data["jump"]:
        print("🟢 Jump!")
    if data["wave"]:
        print("🟣 Wave!")
    if data["dance"]:
        print("🟠 Dance!")

    print("-" * 40)


# ------------------------------
# Main Program
# ------------------------------
def main():
    print("🔗 Connecting to Bluetooth on", BT_PORT, "...")
    try:
        bt = serial.Serial(BT_PORT, BAUD_RATE, timeout=1)
        time.sleep(2)
        print("✅ Connected successfully! Listening for data...\n")

        while True:
            if bt.in_waiting > 0:
                line = bt.readline().decode("utf-8").strip()
                if line:
                    data = parse_data(line)
                    if data:
                        print(f"X:{data['x']:4d}  Y:{data['y']:4d} | "
                              f"Joy:{data['joy']} Jump:{data['jump']} "
                              f"Wave:{data['wave']} Dance:{data['dance']}")
                        handle_input(data)
                    else:
                        print("⚠️ Invalid data:", line)
            time.sleep(READ_INTERVAL)

    except serial.SerialException:
        print("❌ Could not open Bluetooth port. Check COM port and pairing.")
    except KeyboardInterrupt:
        print("\n👋 Exiting program...")
    finally:
        if 'bt' in locals() and bt.is_open:
            bt.close()
            print("🔌 Bluetooth connection closed.")


# ------------------------------
# Entry point
# ------------------------------
if __name__ == "__main__":
    main()
