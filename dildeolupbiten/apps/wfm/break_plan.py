# -*- coding: utf-8 -*-

import asyncio
import pandas as pd

from datetime import datetime as dt, timedelta as td


def minutely_needs(needs):
    date = dt.strptime("2000-01-01 00:00", "%Y-%m-%d %H:%M")
    data = {(date + td(hours=i) + td(minutes=15 * j)).strftime("%H:%M"): needs[i] for i in range(len(needs)) for j in range(4)}
    return pd.DataFrame(data=[[i] for i in data.values()], index=list(data.keys()))


async def create_break_plans(shift_plan, needs, activities, work_hour):
    shift_plan = pd.DataFrame(shift_plan)
    date = dt.strptime("2000-01-01 00:00", "%Y-%m-%d %H:%M")
    leak_hour = work_hour - int(work_hour)
    needs = minutely_needs(needs)
    if leak_hour:
        work_hour += (1 - leak_hour)
        work_hour = int(work_hour)
    intervals = {}
    for col in shift_plan.columns[1:]:
        for shift in shift_plan[col][shift_plan[col] != "OFF"]:
            for hour in range(work_hour):
                for quarter in range(4):
                    key = date + td(days=col - 1) + td(hours=shift + hour) + td(minutes=15 * quarter)
                    if key in intervals:
                        intervals[key] += 1
                    else:
                        intervals[key] = 1
    intervals = pd.DataFrame(data=[[i] for i in intervals.values()], index=list(intervals.keys()))
    data = []
    for interval, value in zip(intervals.index, intervals.values[:, 0]):
        data += [[interval, value, (x := needs.iloc[needs.index == interval.strftime("%H:%M")].values[0][0]), value / x]]
    data = pd.DataFrame(data)
    break_plan = {}
    for col in shift_plan.columns[1:]:
        new = []
        for shift in shift_plan[col][shift_plan[col] != "OFF"]:
            row_data = [shift]
            for activity in activities:
                start = date + td(days=col - 1) + td(hours=shift + activity[0])
                end = date + td(days=col - 1) + td(hours=shift + activity[1])
                alternatives = data[(data[0] >= start) & (data[0] < end)]
                alternatives = alternatives[alternatives[3] == alternatives[3].max()].values
                if len(alternatives):
                    row_data += [alternatives[0][0].strftime("%H:%M")]
                    for quarter in range(activity[2] // 15):
                        t = alternatives[0][0] + td(minutes=15 * quarter)
                        row = data[data[0] == t].index
                        data.iloc[row, 1] -= 1
                        data.iloc[row, 3] = data.iloc[row, 1] / data.iloc[row, 2]
            new.append(row_data)
        df = pd.DataFrame(new)
        df.columns = [0 if not i else f"Break-{i}" for i in range(len(df.columns))]
        break_plan[col] = df.values.tolist()
    await asyncio.sleep(0)
    return break_plan, intervals.values.tolist()
