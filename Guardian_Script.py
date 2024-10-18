import cv2
import numpy as np
import pyautogui
import time

def resource_path(relative_path):
    """ Get the absolute path to the resource, works for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

# Function to find template on screen
def find_template(template_path, threshold=0.8):
    screenshot = pyautogui.screenshot()
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_BGR2GRAY)
    template = cv2.imread(template_path, 0)
    res = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)
    if len(loc[0]) > 0:
        return loc[::-1][0][0], loc[::-1][1][0], template.shape
    return None

# Function to click on coordinates
def click_coords(coords):
    pyautogui.moveTo(coords[0], coords[1])
    pyautogui.click()

# Main loop function
def main_loop():
    counter = 0

    while True:
        # Step 1: Click Start Button
        result = find_template(templates["start_button"])
        print("Step 1")
        if result:
            x, y, template_size = result
            # Adjust coordinates to click at the center
            click_coords((x + template_size[1] // 2, y + template_size[0] // 2))
            time.sleep(2)  # Wait for screen transition

        # Step 2: Click To Battle Button
        print("Step 2")
        result = find_template(templates["to_battle_button"])
        if result:
            x, y, template_size = result
            # Adjust coordinates to click at the center
            click_coords((x + template_size[1] // 2, y + template_size[0] // 2))
            time.sleep(8)  # Wait for screen transition

        # Step 3: Click Auto and X5 Buttons
        print("Step 3")
        result = find_template(templates["auto_button"])
        print(result)
        if result:
            print("found auto button")
            x, y, template_size = result
            # Adjust coordinates to click at the center
            click_coords((x + template_size[1] // 2, y + template_size[0] // 2))
            time.sleep(0.5)  # Short delay between clicks

        result = find_template(templates["x5_button"])
        if result:
            x, y, template_size = result
            # Adjust coordinates to click at the center
            click_coords((x + template_size[1] // 2, y + template_size[0] // 2))
            time.sleep(0.5)  # Short delay between clicks

        # Step 4: Monitor for Defeat Screen
        print("Step 4")
        defeat_detected = False
        while not defeat_detected:
            result = find_template(templates["defeat_ss"], threshold=0.9)
            if result:
                print("Defeat screen detected")
                # Step 5: Click OK Button
                result = find_template(templates["ok_button"], threshold=0.8)
                if result:
                    x, y, template_size = result
                    # Adjust coordinates to click at the center
                    click_coords((x + template_size[1] // 2, y + template_size[0] // 2))
                    counter += 1
                    print(f"Loop count: {counter}")
                    time.sleep(2)  # Wait for screen transition
                    defeat_detected = True
                else:
                    print("OK button not found")
            else:
                print("Waiting for defeat screen...")
                time.sleep(5)  # Check every 5 seconds

if __name__ == "__main__":
    # Use resource_path to locate the template files within the bundled executable
    templates = {
        "start_button": resource_path("templates/start_button_template.JPG"),
        "to_battle_button": resource_path("templates/to_battle_button_template.JPG"),
        "auto_button": resource_path("templates/auto_buttonMoC.JPG"),
        "x5_button": resource_path("templates/x5_button_template.JPG"),
        "ok_button": resource_path("templates/ok_button_template.JPG"),
        "defeat_ss": resource_path("templates/defeat_ss_template.png")
    }
    main_loop()
