#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
import numpy as np
import pandas as pd


class ShiftPlan(pd.DataFrame):
    def __init__(self, hc, shifts, days, off):
        super().__init__(
            data=sorted(
                [s := int(i / (hc / len(shifts)))] + [shifts[(s + day // 7) % len(shifts)] for day in range(days)]
                for i in range(hc)
            ),
            columns=range(days + 1)
        )
        self.hc = hc
        self.shifts = shifts
        self.days = days
        self.off = off
        self.error = False

    async def build(self):
        await self.__add_offs(self.hc, self.shifts, self.off)
        await self.__add_next_offs(self.hc, self.shifts, self.off, self.days)
        await self.__modify_shift_plan(self.hc, self.shifts, self.off, opts={"col": 1, "var": -1, "index": 0, "start": 1})
        await self.__modify_shift_plan(self.hc, self.shifts, self.off, opts={"col": 7, "var": 1, "index": len(self.shifts) - 1, "start": 1})
        await self.__modify_all_df(self.days, self.shifts, self.hc, self.off)
        await self.__fix_shift_conflicts(self.shifts)
        await self.__fix_work_day_conflict(self.shifts)

    async def __modify_all_df(self, days, shifts, hc, off):
        start, end = 8, 15
        for day in range((days // 7) - 1):
            await self.__modify_df(start, end, day=day, shifts=shifts, hc=hc, off=off)
            start += 7
            end += 7

    async def __fix_shift_conflicts(self, shifts):
        for row, data in enumerate(self.values):
            for col in range(len(data) - 1):
                if data[col] in shifts and data[col + 1] in shifts and list(data).index(data[col]) > list(data).index(data[col + 1]):
                    self.iloc[row, col] = data[col + 1]
                    rows = [*self[(self[0] == data[0]) & (self[col] == data[col + 1]) & (self[col + 1] == data[col])].index]
                    if len(rows):
                        self.iloc[rows[0], col] = data[col]
        await asyncio.sleep(0)

    async def __fix_work_day_conflict(self, shifts):
        for row in self.index:
            data = self.iloc[row, :].values
            offs = list(np.where(data == "OFF")[0])
            for i in range(len(offs) - 1):
                if offs[i + 1] - offs[i] >= 8:
                    first = offs[i]
                    last = offs[i + 1]
                    need = last - first - 7
                    last -= need
                    ind = int(offs[i + 1] / 7)
                    self.iloc[row, last + need] = shifts[(data[0] + ind) % len(shifts)]
                    self.iloc[row, last] = "OFF"
        await asyncio.sleep(0)

    async def __modify_df(self, start, end, day, shifts, hc, off):
        df = self[[0] + list(range(start, end))]
        df.columns = range(8)
        df = df.assign(**{"new": (df[0] + day + 1) % len(shifts)})
        df = df.sort_values(by=["new"])
        new_df = df[["new"] + list(range(1, 8))]
        new_df.columns = range(8)
        new_df.index = range(len(new_df.values))
        await self.__modify_shift_plan(hc, shifts, off, opts={"col": 1, "var": -1, "index": 0, "start": 1}, df=new_df)
        await self.__modify_shift_plan(hc, shifts, off, opts={"col": 7, "var": 1, "index": len(shifts) - 1, "start": 1}, df=new_df)
        for __, _ in enumerate(df.index):
            self.iloc[_, start: end] = new_df.iloc[__, 1:]

    async def __modify_shift_plan(self, hc, shifts, off, opts, df=None):
        if df is None:
            df = self
        need = (1 - off / 7) * hc / len(shifts)
        var = len(shifts) - opts["index"] - 1
        shift = shifts[var]
        while df[opts["col"]].value_counts()[shifts[opts["index"]]] <= int(need):
            results = [df[j].value_counts()[shift] for j in range(opts["start"], opts["start"] + 7)]
            col = results.index(max(results)) + 1
            try:
                row = df[
                    (df[0] == shifts.index(shift)) & (df[opts["col"]] == "OFF") & (df[col] != "OFF")
                ].index[0]
            except IndexError:
                var += opts["var"]
                shift = shifts[var]
                continue
            try:
                df.iloc[row, opts["col"]] = shifts[(shifts.index(shift) + opts["var"])]
            except IndexError:
                self.error = True
                return
            df.iloc[row, col] = "OFF"
            start = shifts.index(shift) + opts["var"]
            end = 0 if opts["var"] == -1 else len(shifts) - 1
            for i in range(start, end, opts["var"]):
                row = df[
                    (df[0] == i) & (df[opts["col"]] != "OFF") & (df[opts["col"]] != shifts[i + opts["var"]])
                ].index
                df.iloc[row[0], opts["col"]] = shifts[i + opts["var"]]
        await asyncio.sleep(0)

    async def dist(self, start, end):
        await asyncio.sleep(0)
        return pd.DataFrame(
            data=[
                [self[col].value_counts()[unique] for col in self.columns[start:end]]
                for unique in self[start].unique()
            ],
            columns=self.columns[start:end],
            index=self[start].unique()
        )

    async def __add_offs(self, hc, shifts, off):
        for row, data in enumerate(self.values):
            for i in range(off):
                if (
                    data[0] == 0 and
                    self[1].value_counts()[shifts[data[0]]] >= hc / (2 * len(shifts)) and
                    self.iloc[row, 1] != "OFF"
                ):
                    self.iloc[row, 1] = "OFF"
                elif (
                    data[0] == len(shifts) - 1 and
                    self[7].value_counts()[shifts[data[0]]] >= hc / (2 * len(shifts)) and
                    self.iloc[row, 7] != "OFF"
                ):
                    self.iloc[row, 7] = "OFF"
                else:
                    results = [self[j].value_counts()[shifts[data[0]]] for j in range(1, 8)]
                    self.iloc[row, results.index(max(results)) + 1] = "OFF"
        await asyncio.sleep(0)

    async def __add_next_first(self, shifts, index_of_current_shift, end, i, row):
        results = [self[j].value_counts()[shifts[index_of_current_shift]] for j in range(end + 1, end + 7)]
        col = results.index(max(results)) + end + 1
        while True:
            if not i:
                if self.iloc[row, end - 1] != "OFF":
                    self.iloc[row, end] = "OFF"
                    break
                elif self.iloc[row, col] != "OFF":
                    self.iloc[row, col] = "OFF"
                    break
            else:
                if self.iloc[row, col] != "OFF":
                    self.iloc[row, col] = "OFF"
                    break
            results[col - end - 1] = 0
            col = results.index(max(results)) + end + 1
        await asyncio.sleep(0)

    async def __add_next_last(self, shifts, index_of_current_shift, end, i, row, hc, off):
        results = [self[j].value_counts()[shifts[index_of_current_shift]] for j in range(end, end + 7)]
        col = results.index(max(results)) + end
        need = (1 - off / 7) * hc / len(shifts)
        while True:
            if not i:
                if self[end + 6].value_counts()[shifts[index_of_current_shift]] >= hc / (2 * len(shifts)):
                    self.iloc[row, end + 6] = "OFF"
                    break
                else:
                    if self.iloc[row, col] != "OFF" and self[col].value_counts()[shifts[index_of_current_shift]] >= need:
                        self.iloc[row, col] = "OFF"
                        break
            else:
                if self.iloc[row, col] != "OFF" and self[col].value_counts()[shifts[index_of_current_shift]] >= need:
                    self.iloc[row, col] = "OFF"
                    break
            results[col - end] = 0
            col = results.index(max(results)) + end
        await asyncio.sleep(0)

    async def __add_next_others(self, shifts, index_of_current_shift, end, i, row):
        results = [self[j].value_counts()[shifts[index_of_current_shift]] for j in range(end, end + 7)]
        col = results.index(max(results)) + end
        while True:
            if not i:
                if self.iloc[row, col] != "OFF":
                    self.iloc[row, col] = "OFF"
                    break
            else:
                if self.iloc[row, col] != "OFF":
                    self.iloc[row, col] = "OFF"
                    break
            results[col - end] = 0
            col = results.index(max(results)) + end
        await asyncio.sleep(0)

    async def __add_new_offs(self, start, end, day, shifts):
        df = self[[0] + list(range(start, end))]
        df.columns = range(8)
        df = df.assign(**{"new": (df[0] + day + 1) % len(shifts)})
        new_df = pd.DataFrame(data=df[["new"] + list(range(1, 8))].values, columns=range(8))
        new_df = new_df.sort_values(by=[0])
        index = new_df.index
        new_df.index = range(len(new_df.values))
        for __, _ in enumerate(index):
            self.iloc[_, start:end] = new_df.iloc[__, 1:]
        await asyncio.sleep(0)

    async def __add_next_offs(self, hc, shifts, off, days):
        start = 1
        end = 8
        for day in range(int((days / 7)) - 1):
            for row, data in enumerate(self.values):
                for i in range(off):
                    index_of_current_shift = (data[0] + day + 1) % len(shifts)
                    if shifts[index_of_current_shift] == shifts[0]:
                        await self.__add_next_first(shifts, index_of_current_shift, end, i, row)
                    elif shifts[index_of_current_shift] == shifts[-1]:
                        await self.__add_next_last(shifts, index_of_current_shift, end, i, row, hc, off)
                    else:
                        await self.__add_next_others(shifts, index_of_current_shift, end, i, row)
            start += 7
            end += 7
            await self.__add_new_offs(start, end, day, shifts)
