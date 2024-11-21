 # GUI initialization
        self.root = root
        self.root.title("Directory of GUI")
        self.root.geometry("200x150")

        # Button for playing the file
        self.play_button = tk.Button(root, text="Play File", command=self.play)
        self.play_button.pack()

        # Button for loading the file
        self.load_button = tk.Button(root, text="Load File", command=self.load_file)
        self.load_button.pack()

        # Button for displaying low frequency plot
        self.display_low_button = tk.Button(root, text="Graph Low Frequency Plots", command=low_freq)
        self.display_low_button.pack()

        # Button for displaying med frequency plot
        self.display_med_button = tk.Button(root, text="Graph Medium Frequency Plots", command=med_freq)
        self.display_med_button.pack()

        # Button for displaying high frequency plot
        self.display_high_button = tk.Button(root, text="Graph High Frequency Plots", command=high_freq)
        self.display_high_button.pack()

        # Button for displaying combined plot
        self.combine_button = tk.Button(root, text="Combine Plots", command=self.combine_plots)
        self.combine_button.pack()

        # Button for displaying statistics
        self.statistics_button = tk.Button(root, text="Display Statistics", command=self.display_statistics)
        self.statistics_button.pack()

    def play(self):  # This function, when called by a button, plays the song given to it
        global start
        if self.file_name is None:
            return

        def get_duration():
            # Grabs the duration of the file for display
            audio_file = AS.from_file(self.file_path)
            self.duration = audio_file.duration_seconds

        # Displaying the name in new window
        self.play_window = tk.Toplevel(self.root)  # New window is called to start a new window to show songs playing
        self.play_window.title("Now Playing...")  # Title display
        header = tk.Label(self.play_window, font=("Times New Roman", 40), text="Now Playing....")  # Header display
        now_playing = tk.Label(self.play_window, font=("Impact", 80), text=self.file_name)  # Name of File Display
        get_duration()  # Grabs the duration of the file, for later ( in update_time() )

        def update_time():
            # Calculate the time elapsed
            time_elapsed = int(time.time())

            # Updates the label with the elapsed time
            wav_duration.config(text=str(int(time_elapsed - start + 1)) + "/" + str(int(self.duration)) + " seconds")

            self.play_window.after(1000, update_time)  # Updates the window after a second
            if int(time_elapsed - start) == int(self.duration):  # if the elapsed time is equal to the file time,
                # delete window
                time.sleep(3)
                self.play_window.destroy()

        header.pack()
        now_playing.pack()

        try:  # displays the time, errors can occur here occasionally which is why a try block is here
            wav_duration = tk.Label(self.play_window, font=("Times New Roman", 40), text="")
            wav_duration.pack()
        except:
            print("Error getting time")

        pygame.mixer.init()  # initialize pygame mixer so we can play the files

        try:  # Attempts to play wav file
            pygame.mixer.music.load(self.file_path)
            start = time.time()
            pygame.mixer.music.play(loops=0)

        except:  # Prints error message and prevents fatal error
            print("Could not load, either no file selected or wrong file type")

        # Loop to update the time passed from when the file is loaded and playing
        update_time()
        self.play_window.mainloop()

    def load_file(self):
        # erases any relevant data to make sure it's starting from scratch
        self.spectrum_display = 0
        self.file_path = None
        self.file_name = None
        self.duration = None
        self.low_data = None
        self.med_data = None
        self.high_data = None

        def name_getter():  # grabs the name of the file for GUI purposes, only needs to be called the once in practice
            i = len(self.file_path)
            counter = 0
            for x in self.file_path:  # Finds the name of the file and gets rid of the directory parts to display
                if self.file_path[(i - counter - 4)] == '/':
                    self.file_name = self.file_path[(i - 3 - counter):i - 4]
                    break
                counter = counter + 1

        def file_finder():
            #
            self.file_path = askopenfilename(initialdir="/", title="Select File", filetypes=(
                ("wav File", ".wav"), ("mp3 file", ".mp3"), ("All Files", "*.*")))
            if self.file_path is None:
                return
