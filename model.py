class ShutterStock:
    def __init__(self, data):
        self.data = data

    def to_array(self):
        return [
            ",".join(
                [
                    f'"{self.data["filename"]}.eps"',
                    f'"{self.data["eps_title"].strip()}"',
                    f'"{self.data["keywords"]}"',
                    f'"{self.data["category"]}"',
                    'no',
                    'no',
                    'yes'
                ]
            ),
            ",".join(
                [
                    f'"{self.data["filename"]}.jpg"',
                    f'"{self.data["jpg_title"].strip()}"',
                    f'"{self.data["keywords"]}"',
                    f'"{self.data["category"]}"',
                    'no',
                    'no',
                    'yes'
                ]
            )
        ]
