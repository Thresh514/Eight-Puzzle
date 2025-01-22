import time

class Timer:
    """
    A class to measure and report the time taken for code execution.
    Instances store the start and end times, and calculate the elapsed duration.
    """

    def __init__(self, name='Timer'):
        """
        Initializes a new Timer instance.

        Args:
            name (str): The name of the timer, used for reporting. Default is 'Timer'.
        """
        self.name = name
        self.start_time = None
        self.end_time = None

    def start(self):
        """
        Starts the timer.
        """
        self.start_time = time.time()
        self.end_time = None
        print(f"{self.name} started.")

    def end(self):
        """
        Stops the timer and calculates the end time.
        """
        if self.start_time is None:
            raise ValueError("Timer has not been started. Use the `start()` method first.")
        self.end_time = time.time()
        print(f"{self.name} ended. Duration: {self.get_diff():.5f} seconds.")

    def get_diff(self):
        """
        Calculates the elapsed time between the start and end times.

        Returns:
            float: The elapsed time in seconds.
        """
        if self.start_time is None:
            raise ValueError("Timer has not been started. Use the `start()` method first.")
        if self.end_time is None:
            raise ValueError("Timer has not been stopped. Use the `end()` method first.")
        return self.end_time - self.start_time

    def reset(self):
        """
        Resets the timer, clearing the start and end times.
        """
        self.start_time = None
        self.end_time = None
        print(f"{self.name} has been reset.")

    def __repr__(self):
        """
        Returns a string representation of the Timer instance.

        Returns:
            str: A string reporting the timer name and elapsed time.
        """
        try:
            elapsed = self.get_diff()
            return f"{self.name}: {elapsed:.5f} seconds"
        except ValueError:
            return f"{self.name}: Timer not completed"

    def elapsed_time(self):
        """
        Returns the current elapsed time without stopping the timer.

        Returns:
            float: The elapsed time in seconds since the timer started.
        """
        if self.start_time is None:
            raise ValueError("Timer has not been started. Use the `start()` method first.")
        return time.time() - self.start_time
