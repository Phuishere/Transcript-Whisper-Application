if __name__ != "__main__":
    from .queries import *
    from .time_utils import *
    from .transcript_handling import *

# For testing script
else:
    import sqlite3
    from transcript_handling import select_all
    from queries import *
    from time_utils import get_time, time_delta

    conn = sqlite3.connect("test.db") # or use :memory: to put it in RAM
    cursor = conn.cursor()

    # Create table
    cursor.execute(create_full_trans)
    conn.commit()

    data = [(0, "vi", get_time(), get_time() + time_delta(30), "Hello there. Chúng ta đang nói về cái gì ấy nhỉ?", "Google Meet")]
    cursor.executemany(insert_many_full_trans, data)
    conn.commit()

    select_all(cursor, "full_trans")