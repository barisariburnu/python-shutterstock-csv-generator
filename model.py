class ShutterStock:
    def __init__(self, data):
        self.data = data

    def to_array(self):
        return [
            ",".join(
                [
                    f'"{self.data["filename"]}.eps"',
                    f'"{self.data["title"].strip()}"',
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
                    f'"{self.data["title"].strip()}"',
                    f'"{self.data["keywords"]}"',
                    f'"{self.data["category"]}"',
                    'no',
                    'no',
                    'yes'
                ]
            )
        ]


class AdobeStock:
    def __init__(self, data):
        self.data = data

    def to_array(self):
        return [
            ",".join(
                [
                    f'"{self.data["filename"]}.eps"',
                    f'"{self.data["title"].strip()}"',
                    f'"{self.data["keywords"]}"',
                    f'{self.data["category_id"]}',
                    '""'
                ]
            ),
            ",".join(
                [
                    f'"{self.data["filename"]}.jpg"',
                    f'"{self.data["title"].strip()}"',
                    f'"{self.data["keywords"]}"',
                    f'{self.data["category_id"]}',
                    '""'
                ]
            )
        ]


class Freepik:
    def __init__(self, data):
        self.data = data

    def to_array(self):
        return [
            ";".join(
                [
                    f'"{self.data["filename"]}.eps"',
                    f'"{self.data["title"].strip()}"',
                    f'"{self.data["keywords"]}"'
                ]
            ),
            ";".join(
                [
                    f'"{self.data["filename"]}.jpg"',
                    f'"{self.data["title"].strip()}"',
                    f'"{self.data["keywords"]}"'
                ]
            )
        ]


class Vecteezy:
    def __init__(self, data):
        self.data = data

    def to_array(self):
        return [
            ",".join(
                [
                    f'"{self.data["filename"]}.eps"',
                    f'"{self.data["title"].strip()}"',
                    f'"{self.data["keywords"]}"'
                ]
            ),
            ",".join(
                [
                    f'"{self.data["filename"]}.jpg"',
                    f'"{self.data["title"].strip()}"',
                    f'"{self.data["keywords"]}"',
                ]
            )
        ]
