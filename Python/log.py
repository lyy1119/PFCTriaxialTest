from datetime import datetime
from typing import Optional, Dict

COLOR_CODES = {
    # Standard Colors (High Intensity)
    "white":  "\033[97m",
    "gray":   "\033[90m",
    "black":  "\033[30m",
    "red":    "\033[91m",
    "green":  "\033[92m",
    "yellow": "\033[93m",
    "blue":   "\033[94m",
    "purple": "\033[95m",
    "cyan":   "\033[96m",

    # 256-color Extended (Common Colors)
    "orange": "\033[38;5;208m",   # Bright Orange (Good for highlighting)
    "pink":   "\033[38;5;213m",   # Pink (Special marking)
    "teal":   "\033[38;5;37m",    # Teal
    "gold":   "\033[38;5;220m",   # Gold
    "lime":   "\033[38;5;118m",   # Lime green (Brighter than normal green)
    "brown":  "\033[38;5;130m",   # Brown
    "violet": "\033[38;5;129m",   # Deep Purple

    # Style Controls
    "bold":      "\033[1m",       # Bold
    "underline": "\033[4m",       # Underline
    "reversed":  "\033[7m",       # Reversed (Swap foreground and background)
    "end":       "\033[0m"        # Reset all styles
}

class Log:
    # Color Configuration Mapping
    COLOR_CODES = COLOR_CODES

    def __init__(
        self,
        timeFormat: str = '%Y-%m-%d %H:%M:%S',
        outputFile: str = '',
        fileOnly: bool = False,
        noColor: bool = False,
        colorSignOnly: bool = False,
        noTime: bool = False,
        colorStyle: Optional[Dict[str, str]] = None
    ) -> None:
        """
        :param timeFormat: Formatted string for timestamp
        :param outputFile: Output log filename; if empty, log will not be saved to file
        :param fileOnly: If True, disable console output
        :param noColor: Disable color display
        :param colorSignOnly: Only render the color of the status tag [Info]
        :param noTime: Do not output timestamp
        :param colorStyle: Custom color configuration for each level
        """
        self.timeFormat = timeFormat
        self.savePath = outputFile
        self.showConsole = not fileOnly
        self.noColor = noColor
        self.colorSignOnly = colorSignOnly
        self.noTime = noTime

        # Default color styles
        self.currentStyle: Dict[str, str] = {
            "info": "white",
            "succ": "green",
            "warn": "yellow",
            "error": "red",
            "fatal": "purple"
        }

        # Override color styles
        if colorStyle:
            for key, value in colorStyle.items():
                if key in self.currentStyle:
                    self.currentStyle[key] = value.lower()

    def _get_timestamp(self) -> str:
        """Get the current formatted time"""
        if self.noTime:
            return ""
        now = datetime.now()
        return f"[{now.strftime(self.timeFormat)}] "

    def _format_output(self, levelTag: str, styleKey: str, text: str) -> str:
        """Core output formatting logic"""
        timeStamp = self._get_timestamp()
        rawTag = f"[{levelTag}]"
        rawMessage = f" {text}"

        # Get color
        colorName = self.currentStyle.get(styleKey, "white")
        colorCode = self.COLOR_CODES.get(colorName, self.COLOR_CODES["white"])
        endCode = self.COLOR_CODES["end"]

        # Construct console output (timestamp without color)
        if self.noColor:
            consoleStr = f"{timeStamp}{rawTag}{rawMessage}"
        elif self.colorSignOnly:
            consoleStr = f"{timeStamp}{colorCode}{rawTag}{endCode}{rawMessage}"
        else:
            consoleStr = f"{timeStamp}{colorCode}{rawTag}{rawMessage}{endCode}"

        # Write to file (Plain text, no color control codes)
        if self.savePath:
            fileStr = f"{timeStamp}{rawTag}{rawMessage}\n"
            with open(self.savePath, 'a+', encoding='utf-8') as f:
                f.write(fileStr)

        return consoleStr

    def info(self, text: str) -> None:
        """Output standard info message"""
        output = self._format_output("Info", "info", text)
        if self.showConsole:
            print(output)

    def succ(self, text: str) -> None:
        """Output success message"""
        output = self._format_output("Succ", "succ", text)
        if self.showConsole:
            print(output)

    def warn(self, text: str) -> None:
        """Output warning message"""
        output = self._format_output("Warn", "warn", text)
        if self.showConsole:
            print(output)

    def error(self, text: str) -> None:
        """Output error message"""
        output = self._format_output("Error", "error", text)
        if self.showConsole:
            print(output)

    def fatal(self, text: str) -> None:
        """Output fatal error message"""
        output = self._format_output("Fatal", "fatal", text)
        if self.showConsole:
            print(output)

# --- Usage Scenario Demonstration ---
if __name__ == "__main__":
    ServerLog = Log
    # Scenario 1: Standard long-running program log (Time included, full line color)
    logger = ServerLog(outputFile="server.log")
    logger.info("System service started")
    logger.succ("Database connected successfully")
    logger.warn("Disk space usage exceeds 80%")
    logger.error("API request timeout (Endpoint: /v1/user)")
    logger.fatal("Kernel memory overflow, process terminated")

    # Scenario 2: Tag-only rendering with custom level colors
    customLogger = ServerLog(
        colorSignOnly=True,
        colorStyle={"warn": "red"}, # Set warning to red as well
        timeFormat="%H:%M:%S"       # Shortened time format
    )
    print("\n--- Custom Configuration Output ---")
    customLogger.warn("This is a warning with tag-only rendering and modified color")