import pandas as pd
import time

class NetworkAnalysis:
    def __init__(self, file_path="team10stats.csv"):
        self.data = pd.DataFrame(columns=["Event", "File Name", "File Size(Bytes)", "Transfer Time(s)", "Transfer Rate(MB/s)", "Timestamp"])
        self.file_path = file_path

    def log_event(self, event, file_name, file_size, transfer_time, transfer_rate):
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        entry = {
            "Event": event,
            "File Name": file_name,
            "File Size(Bytes)": file_size,
            "Transfer Time(s)": transfer_time,
            "Transfer Rate(MB/s)": transfer_rate,
            "Timestamp": timestamp,
        }
        self.data = pd.concat([self.data, pd.DataFrame([entry])], ignore_index=True)
        self.save_to_csv()

    def save_to_csv(self):
        self.data.to_csv(self.file_path, index=False)

    def display_summary(self):
        print("\nServer Stat Summary")
        print(self.data)
        print(f"\nData saved to {self.file_path}")