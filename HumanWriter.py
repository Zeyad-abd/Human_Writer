import tkinter as tk
from tkinter import font
import time
import random
import threading  # Import the threading module for handling typing in a separate thread
import keyboard

# Global variable for typing speed
typing_speed_factor = 1.0

def simulate_typing(text, stop_event):
    time.sleep(5)
    wordCount = 0
    randomNumber = 0
    listOfNums = [6, 7, 8, 9, 10]
    
    for word in text.split():
        if stop_event.is_set():
            break  # Stop typing if the stop_event is set

        if randomNumber == 0:
            randomNumber = random.choice(listOfNums)
        wordCount += 1

        for char in word:
            if stop_event.is_set():
                break  # Stop typing if the stop_event is set
            keyboard.write(char)
            time.sleep(random.uniform(0.04, 0.07) / typing_speed_factor)

        keyboard.press(' ')
        keyboard.release(' ')

        typing_speed = random.uniform(60, 70) * typing_speed_factor
        time.sleep(60 / typing_speed)

        if wordCount == randomNumber:
            break_duration = random.uniform(3, 6) / typing_speed_factor
            time.sleep(break_duration)
            wordCount = 0
            randomNumber = 0

    time.sleep(random.uniform(4, 9) / typing_speed_factor)

def write_text():
    text_to_write = result_text.get("1.0", tk.END).strip()
    
    global typing_thread
    global stop_typing_event

    if typing_thread is None or not typing_thread.is_alive():
        # Start typing in a separate thread
        stop_typing_event = threading.Event()
        typing_thread = threading.Thread(target=simulate_typing, args=(text_to_write, stop_typing_event))
        typing_thread.start()

        # Change button image to "Stop"
        button10.config(image=image_7)
    else:
        # Stop typing by setting the stop_event
        stop_typing_event.set()
        
        # Change button image back to "Write"
        button10.config(image=image_6)
        label1.config(image=image_3)  # Reset to original image or clear the label
        label1.config(text="")  # Clear the text if any

def format_time(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return f"{int(hours)}H {int(minutes)}M {int(seconds)}S"

def estimate_typing_time(word_count):
    avg_typing_speed = 65  # average typing speed in words per minute
    avg_char_time = (0.04 + 0.07) / 2  # average time per character
    avg_pause_time = (60 / 70 + 60 / 60) / 2  # average time per word
    avg_break_duration = (3 + 6) / 2  # average break duration in seconds
    avg_final_pause = (4 + 9) / 2  # average final pause duration in seconds

    # Estimate the time for typing the characters
    avg_word_length = 5  # average word length (can be adjusted)
    typing_time = word_count * avg_word_length * avg_char_time

    # Estimate the time for pauses between words
    pause_time = word_count * avg_pause_time

    # Estimate the number of breaks
    avg_words_per_break = sum([6, 7, 8, 9, 10]) / len([6, 7, 8, 9, 10])
    num_breaks = word_count / avg_words_per_break
    break_time = num_breaks * avg_break_duration

    # Total estimated time
    total_time = 5 + typing_time + pause_time + break_time + avg_final_pause
    return total_time / typing_speed_factor if typing_speed_factor > 0 else total_time  # Ensure no division by zero

def get_word_count(text_widget):
    # Get the text from the Text widget
    text_content = text_widget.get("1.0", tk.END).strip()
    # Split the text into words
    words = text_content.split()
    # Return the number of words
    return len(words)

def add_speed():
    global typing_speed_factor
    if get_word_count(result_text) > 0:
        speed = int(label4.cget("text"))
        if speed < 500:
            speed += 10
            label4.config(text=speed)
            typing_speed_factor = max(speed / 100, 0.1)  # Ensure minimum speed factor of 0.1
            time_estimate = format_time(estimate_typing_time(get_word_count(result_text)))
            label5.config(text=f'Estimated Time: {time_estimate}')

def less_speed():
    global typing_speed_factor
    if get_word_count(result_text) > 0:
        speed = int(label4.cget("text"))
        if speed >= 10:
            speed -= 10
            label4.config(text=speed)
            typing_speed_factor = max(speed / 100, 0.1)  # Ensure minimum speed factor of 0.1
            time_estimate = format_time(estimate_typing_time(get_word_count(result_text)))
            label5.config(text=f'Estimated Time: {time_estimate}')

# Create the main window
root = tk.Tk()
root.title("Human Writer")
root.geometry("600x700")
root.configure(bg='#0B1A3E')

# Load images
image_1 = tk.PhotoImage(file="1.png")
image_2 = tk.PhotoImage(file="2.png")
image_3 = tk.PhotoImage(file="3.png")
image_4 = tk.PhotoImage(file="4.png")
image_5 = tk.PhotoImage(file="5.png")
image_6 = tk.PhotoImage(file="6.png")
image_7 = tk.PhotoImage(file="7.png")
image_8 = tk.PhotoImage(file="8.png")

# Create and place widgets
label = tk.Label(root, image=image_1, bg="#0B1A3E")
label.place(x=200, y=24)

label = tk.Label(root, image=image_2, bg="#0B1A3E")
label.place(x=208, y=85)

label1 = tk.Label(root, image=image_3, bg="#0B1A3E")
label1.place(x=10, y=130)

result_text = tk.Text(root, width=62, height=16, bg="#152A59", bd=0, highlightthickness=0, fg="white", font=("Helvetica"))
result_text.place(x=23, y=140)

label2 = tk.Label(root, image=image_4, bg="#0B1A3E")
label2.place(x=275, y=460)

label3 = tk.Label(root, image=image_5, bg="#0B1A3E")
label3.place(x=10, y=490)

button_add_speed = tk.Button(root, text="+", command=add_speed, cursor="hand2", font=("Helvetica", 16), bg="#27468A", fg="white", borderwidth=0, highlightthickness=0, relief="flat", activebackground="#27468A", activeforeground="white")
button_add_speed.place(x=556, y=504)

button_less_speed = tk.Button(root, text="-", command=less_speed, cursor="hand2", font=("Helvetica", 16), bg="#27468A", fg="white", borderwidth=0, highlightthickness=0, relief="flat", activebackground="#27468A", activeforeground="white")
button_less_speed.place(x=25, y=504)

label4 = tk.Label(root, text="100", bg="#152A59", fg="#4FC27D", font=("Helvetica", 16))
label4.place(x=65, y=508)

label5 = tk.Label(root, text="Estimated Time: 0H 00M 00S", bg="#0B1A3E", fg="#e8e8e8", font=("Helvetica", 16))
label5.place(x=189, y=570)

button10 = tk.Button(root, image=image_6, cursor="hand2", bg="#0B1A3E", borderwidth=0, highlightthickness=0, relief="flat", activebackground="#0B1A3E", activeforeground="#0B1A3E", command=write_text)
button10.place(x=189, y=610)

# Global variables for threading
typing_thread = None
stop_typing_event = None

# Start the main event loop
root.mainloop()