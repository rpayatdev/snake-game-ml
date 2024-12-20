class Direction:
    def convert2number(direction_char):
        match direction_char:
            case 'left':
                return 0
            case 'up':
                return 1
            case 'right':
                return 2
            case 'down':
                return 3
            case _:
                return -1

    def convert2char(direction_num):
        match direction_num:
            case 0:
                return 'left'
            case 1:
                return 'up'
            case 2:
                return 'right'
            case 3:
                return 'down'
            case _:
                return "none"
            