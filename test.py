import os
from ecflow import (
    Defs,Suite,Family,Task,Edit,Trigger,
    Complete,Event,Meter,Time,Day,Date,
    Edit,Cron,Label,RepeatString,RepeatInteger,
    RepeatDate,Limit,InLimit)

def create_family_f1():
    return Family("f1",
                Edit(SLEEP=3),
                Task("t1", Meter("progress", 1, 100, 90)),
                Task("t2", Trigger("t1 == complete"), Event("a"), Event("b")),
                Task("t3", Trigger("t2:a")),
                Task("t4", Trigger("t2 == complete"), Complete("t2:b")),
                Task("t5", Trigger("t1:progress ge 30")),
                Task("t6", Trigger("t1:progress ge 60")),
                Task("t7", Trigger("t1:progress ge 90")),
                Task("query", Label("query", "")))


def create_family_f2():
    return Family("f2",
            Edit(SLEEP=3),
            Task("t1", Trigger(":ECF_DATE == 20200720 and :TIME >= 1000")),
            Task("t2", Trigger(":DOW == 4 and :TIME >= 1300")),
            Task("t3", Trigger(":DD == 1 and :TIME >= 1200")),
            Task("t4", Trigger("(:DOW == 1 and :TIME >= 1300) or (:DOW == 5 and :TIME >= 1000)")),
            Task("t5", Trigger(":TIME == 0002")))


def create_family_house_keeping():
    return Family("house_keeping",
                  Task("clear_log", Cron("22:30", days_of_week=[0])))


def create_family_label():
    return Family("label",
                  Task("t1", Label("info", "")))


def create_family_f4():
    return Family("f4",
                  Edit(SLEEP=3),
                  RepeatString("NAME", ["a", "b", "c", "d", "e", "f"]),
                  Family("f5",
                         RepeatInteger("VALUE", 1, 10),
                         Task("t1", RepeatDate("DATE", 20101230, 20110105), Label("info", ""), Label("date", ""))))


def create_family_f5():
    return Family("f5",
                  Edit(SLEEP=3),
                  # limit_name(l1),limit_path(""),no_of_tokens_to_consume(1),limit node(False), limit submission(True)
                  InLimit("l1", "", 1, False, True),
                  [Task(f"t{i}") for i in range(1, 10)])


print("Creating suite definition")
home = os.path.join(os.getenv("HOME"),"ecflow/suite1")
defs = Defs(
        Suite('test',
            Edit(ECF_HOME=home, ECF_INCLUDE=home),
            Limit("l1", 2),  # How many tasks of a family will run at the same time
            create_family_f1(),
            create_family_f2(),
            create_family_house_keeping(),
            create_family_label(),
            create_family_f4(),
            create_family_f5()))
print(defs)

print("Checking job creation: .ecf -> .job0") 
print(defs.check_job_creation())

print("Saving definition to file 'test.def'")
defs.save_as_defs("test.def")
