from unittest import TestCase


def hash_algorithm(text: str) -> int:
    value = 0
    for char in text:
        value += ord(char)
        value *= 17
        value %= 256

    return value


def get_initialization_sequence(line: str) -> int:
    return sum(hash_algorithm(text) for text in line.split(","))


def boxes_with_lenses(line: str) -> dict:
    boxes = {key: list() for key in range(256)}
    for text in line.split(","):
        if "-" in text:
            key, value = text.split("-")
            box_number = hash_algorithm(key)

            box_update = boxes[box_number]

            for element in box_update:
                if key in element:
                    box_update.remove(element)

        if "=" in text:
            key, value = text.split("=")
            box_number = hash_algorithm(key)
            box_update = boxes[box_number]

            new_box = []
            exists = False
            for element in box_update:
                if key in element:
                    new_box.append(f"{key} {value}")
                    exists = True
                else:
                    new_box.append(element)

            if not exists:
                new_box.append(f"{key} {value}")

            boxes[box_number] = new_box

    return {key: value for key, value in boxes.items() if value}


def get_focusing_power(input: str) -> int:
    boxes = boxes_with_lenses(input)

    return sum(
        (box_number + 1) * slot * int(lens.split()[1])
        for box_number, lenses in boxes.items()
        for slot, lens in enumerate(lenses, 1)
    )


class AdventTest(TestCase):
    def test_hash(self):
        example = "HASH"

        hashed_example = hash_algorithm(example)

        self.assertEqual(hashed_example, 52)

        self.assertEqual(hash_algorithm("rn"), 0)
        self.assertEqual(hash_algorithm("pc"), 3)

    def test_initialization_sequence(self):
        example = "rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"

        self.assertEqual(get_initialization_sequence(example), 1320)

        self.assertDictEqual(
            boxes_with_lenses(example),
            {0: ["rn 1", "cm 2"], 3: ["ot 7", "ab 5", "pc 6"]},
        )

        self.assertEqual(get_focusing_power(example), 145)


if __name__ == "__main__":
    with open("advent/2023/input_2023_15.txt", "r") as f:
        text = f.read()
        result = get_initialization_sequence(text)

        print(f"2023 Day 15: Part 1: {result=}")
    with open("advent/2023/input_2023_15.txt", "r") as f:
        text = f.read()
        result = get_focusing_power(text)

        print(f"2023 Day 15: Part 2: {result=}")
